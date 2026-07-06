import os
from pathlib import Path
#from tqdm import tqdm
import pandas as pd
import os
import fnmatch
import subprocess
import re

#function that gets the directory of a file.
def get_cabal_file_directory(cabal_file):
    if not cabal_file or cabal_file == "":
        return ""
    return os.path.dirname(cabal_file)


def get_haskell_files(package_root):
    """
    Find all .hs files in the package directory.

    args:
        a directory, where .hs files will be searched
    return: 
        list of relative directories to said files
    
    """
    package_path = Path(package_root)
    if not package_path.exists():
        return []
    
    skip_dirs = {
        '.stack-work',
        'dist',
        'dist-newstyle',
        '.git',
        'vendor',
        'node_modules',
        '.cabal-sandbox',
    }
    skip_patterns = ['Setup.hs', 
                     'Paths_*.hs']
    
    hs_files = []

    for file_path in package_path.rglob('*.hs'):
        rel_path = file_path.relative_to(package_path)
        rel_str = str(rel_path)
        #check if in skipped directory
        path_parts = set(rel_path.parts)
        if skip_dirs.intersection(path_parts):
            continue
        #check if matches skipped file pattern
        should_skip = False
        for pattern in skip_patterns:
            if fnmatch.fnmatch(rel_str, pattern):
                should_skip = True
                break
        if should_skip:
            continue
        
        hs_files.append(rel_str)
    
    return hs_files

def get_file_stats(file_path, package_root):
    """
    get statistics for a haskellfile: line count, word count and char count
    returns a dictionary with the file stats
    args:
        file_path: relative path to the .hs file (for example, "Data/Concurrent/Deque/Class.hs")
        package_root: absolute path to the package root directory
    """
    full_path = Path(package_root) / file_path
    
    if not full_path.exists():
        return {
            'line_count':0,
            'word_count':0,
            'char_count':0,
            # 'function_count': 0
        }
    
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.split('\n')
        line_count =len(lines)
        word_count =len(content.split())
        char_count =len(content)
        return {
            'line_count':line_count,
            'word_count':word_count,
            'char_count':char_count,
            # 'function_count': function_count
        }
    except Exception as e:
        print(f"Error reading {full_path}: {e}")
        return {
            'line_count': 0,
            'word_count': 0,
            'char_count': 0,
            # 'function_count': 0
        }

def path_to_module_name(file_path):
    """
    convert relative file path to module name.
    
    examples:
    "src/Network/Warp/Server.hs" ->"Network.Warp.Server"
    "Data/Concurrent/Deque/Class.hs" ->"Data.Concurrent.Deque.Class"
    "Setup.hs" -> "Setup"
    """
    module_path = file_path.replace('.hs', '') #remove .hs extension
    parts = module_path.split('/') #split by / path separator
    
    #remove common source directory prefixes if they're first
    if parts and parts[0] in ['src', 'source', 'app', 
                              'lib', 'bench', 
                              'test', 'test-suite', 'src-exe',
                              'library', 'examples']:
        parts = parts[1:]
    
    return '.'.join(parts) #joined with .

def get_file_imports(file_path, package_root, cabal_file):
    """
    Run PackageImports parser on a single file.
    Returns list of imported module names.
    """
    full_path = Path(package_root) / file_path
    
    if not full_path.exists():
        return []
    
    try: #the parser expects a cabal_file path and then a file path
        input_data = f"{cabal_file}\n{full_path}\n"
        result = subprocess.run(
            ['../src/parse/PackageImports'],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                #split into lines and take the last line
                lines = output.split('\n')
                last_line = lines[-1].strip()
                
                if last_line:
                    #split by comma and get module names
                    imports = [mod.strip() for mod in last_line.split(',') if mod.strip()]
                    #filter out file paths and debug info
                    imports = [mod for mod in imports if not mod.startswith('/') and not mod.startswith('[')]
                    return imports
        return []
    except subprocess.TimeoutExpired:
        return []
    except Exception as e:
        return []

def create_files_dataframe_single_lts(df, lts_version):
    """
    returns a DataFrame with file-level information for one lts
    args:
        df: The main package dataframe for the lts
        lts_version: LTS version string (for example: '21-7')
    """
    files_data = []
    
    #go through each package in the dataframe
    for idx, row in df.iterrows():
        package_name = row['package']
        version = row['version']
        package_id = f"{package_name}-{version}"
        
        #get package root directory from cabal file
        cabal_file = row.get('cabal-file', '')
        if not cabal_file or pd.isna(cabal_file):
            print('missing cabal_file path for: '+package_id)
            continue
        
        package_root = os.path.dirname(cabal_file)
        
        #get .hs files for this package
        hs_files = get_haskell_files(package_root)
        
        #get stats for the files
        for hs_file in hs_files:
            stats = get_file_stats(hs_file, package_root)
            module_name = path_to_module_name(hs_file)
            files_data.append({
                'package_id':package_id,
                'package_name':package_name,
                'version':version,
                'lts':lts_version,
                'file_path':hs_file,
                'module_name':module_name,
                'line_count':stats['line_count'],
                'word_count':stats['word_count'],
                'char_count':stats['char_count'],
            })
    
    #create the df
    files_df = pd.DataFrame(files_data)
    files_df.to_pickle(f'../data/dfs/lts-{lts_version}/lts-{lts_version}-files.df')
    return files_df

def get_lts_list_from_csv():
    """Read LTS versions from the CSV file"""
    csv_path = '../src/lts_list.csv'
    df = pd.read_csv(csv_path, header=None)
    lts_list = df.iloc[0].tolist()#first row contains all lts version
    return lts_list

def process_all_lts():
    """process all lts versions from .csv file"""
    lts_list = get_lts_list_from_csv()
    print("found"+ str(len(lts_list))+ "lts versions in csv:")
    results = []
    for i, lts in enumerate(lts_list, 1):
        print(f"\n[{i}/{len(lts_list)}] Processing LTS {lts}...")
        try:
            #if package df exists...
            pkg_df_path = f'../data/dfs/lts-{lts}/lts-{lts}.df'
            if not os.path.exists(pkg_df_path):
                print(f"WARNING: {pkg_df_path} not found, skipping")
                results.append({'lts': lts, 'status': 'skipped', 'reason': 'package_df_missing'})
                continue
            
            #if file df exists...
            files_df_path = f'../data/dfs/lts-{lts}/lts-{lts}-files.df'
            if os.path.exists(files_df_path):
                print(f"Files DataFrame already exists, skipping")
                results.append({'lts': lts, 'status': 'skipped', 'reason': 'already_exists'})
                continue
            
            #load package df
            df = pd.read_pickle(pkg_df_path)
            print(f"Loaded {len(df)} packages")
            #create files df
            files_df = create_files_dataframe_single_lts(df, lts)
            results.append({
                'lts': lts,
                'status': 'success',
                'packages': len(df),
                'files': len(files_df),
            })
            print(f"...created {len(files_df)} file rows")
            
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({'lts': lts, 'status': 'error', 'error': str(e)})
    
    #
    print("\n" +"--------------------------")
    print("sumary")
    print("--------------------------------")
    
    success = [r for r in results if r['status'] == 'success']
    skipped = [r for r in results if r['status'] == 'skipped']
    errors = [r for r in results if r['status'] == 'error']
    
    print(f"successful: {len(success)}")
    print(f"skipped: {len(skipped)}")
    print(f"errors: {len(errors)}")
    
    if success:
        print("\nsuccessful lts versions:")
        for r in success:
            print(f"lts {r['lts']}: {r['packages']} packages -> {r['files']} files")
    
    if errors:
        print("\nfailed lts versions:")
        for r in errors:
            print(f"lts {r['lts']}: {r['error']}")
    
    return results

