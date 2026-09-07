#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
import os
import subprocess

console = Console()

############## modules #################

mtl_modules = [
    "Control.Monad.Cont", "Control.Monad.Cont.Class",
    "Control.Monad.Error", "Control.Monad.Error.Class",
    "Control.Monad.Except", "Control.Monad.Identity",
    "Control.Monad.List", "Control.Monad.RWS",
    "Control.Monad.RWS.Class", "Control.Monad.RWS.Lazy",
    "Control.Monad.RWS.Strict", "Control.Monad.Reader",
    "Control.Monad.Reader.Class", "Control.Monad.State",
    "Control.Monad.State.Class", "Control.Monad.State.Lazy",
    "Control.Monad.State.Strict", "Control.Monad.Trans",
    "Control.Monad.Writer", "Control.Monad.Writer.Class",
    "Control.Monad.Writer.Lazy", "Control.Monad.Writer.Strict",
    "Control.Monad.Trans.Class",
]

transfromers_modules = [
    "Control.Monad.Trans.Accum", "Control.Monad.Trans.Class",
    "Control.Monad.Trans.Cont", "Control.Monad.Trans.Except",
    "Control.Monad.Trans.Identity", "Control.Monad.Trans.Maybe",
    "Control.Monad.Trans.RWS", "Control.Monad.Trans.RWS.CPS",
    "Control.Monad.Trans.RWS.Lazy", "Control.Monad.Trans.RWS.Strict",
    "Control.Monad.Trans.Reader", "Control.Monad.Trans.Select",
    "Control.Monad.Trans.State", "Control.Monad.Trans.State.Lazy",
    "Control.Monad.Trans.State.Strict", "Control.Monad.Trans.Writer",
    "Control.Monad.Trans.Writer.CPS", "Control.Monad.Trans.Writer.Lazy",
    "Control.Monad.Trans.Writer.Strict"
]

other_modules = [
    "Control.Monad", "System.IO", "Control.Monad.Trans.Control",
    "Control.Monad.Free", "Control.Monad.Free.Ap",
    "Control.Monad.Free.Church", "Control.Monad.Free.Class",
    "Control.Monad.Free.TH"
]

ALL_MONAD_MODULES = mtl_modules + transfromers_modules + other_modules

################## load dataframes ####################
def load_files_df(lts):
    """load the files dataframe for a given lts
    lts: string label for lts version, for example, '12-13' """

    files_path = f'../data/dfs/lts-{lts}/lts-{lts}-files.df'
    if not os.path.exists(files_path):
        console.print("[red]Error:[/red] "+files_path+" not found")
        return None
    return pd.read_pickle(files_path)
    

def load_packages_df(lts):
    """load the packages dataframe for a given lts
    lts: string label for lts version, for example, '12-13' """

    pkg_path = f'../data/dfs/lts-{lts}/lts-{lts}.df'
    if not os.path.exists(pkg_path):
        console.print("[red]Error:[/red] "+pkg_path+" not found")
        return None
    return pd.read_pickle(pkg_path)

def get_available_lts_list():
    """get list of available lts versions, from the data/dfs folder"""
    data_path = Path('../data/dfs')
    lts_list=[]
    for df in data_path.glob('lts-*'):
        if df.is_dir():
            lts_list.append(df.name.replace("lts-", ""))
    return sorted(lts_list, key=lambda x: [int(i) for i in x.split('-')])

def get_monad_files(files_df, monad_name):
    """get files that import a specific monad"""
    if monad_name not in files_df.columns:
        return pd.DataFrame()
    return files_df[files_df[monad_name] == 1]

############ display functrions##########

def find_package_root(cabal_path):
    """returns the directory in which the input file is in"""
    if pd.isna(cabal_path) or not cabal_path:
        return None
    return os.path.dirname(cabal_path)

def get_absolute_file_path(row, packages_df):
    pkg_info = packages_df[packages_df['package'] == row['package_name']]
    if len(pkg_info) == 0:
        return None
    
    cabal_file = pkg_info.iloc[0].get('cabal-file', '')
    package_root = find_package_root(cabal_file)
    if not package_root:
        return None
    
    return os.path.join(package_root, row['file_path'])

def display_file(file_path):
    if not file_path or not os.path.exists(file_path):
        console.print(f"[red]File not found: {file_path}[/red]")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        syntax = Syntax(content, "haskell", theme="monokai", line_numbers=True)
        console.print(syntax)
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")

def open_in_vscode(file_path, line_num=0, open_file=None):
    """
    Open a file in vscode using the 'code' command
    file_path: absolute path to the file
    line_num: optional line number to jump to
    """
    if not file_path or not os.path.exists(file_path):
        console.print("[red]File not found: [/red]"+file_path)
        return
    
    #build the command
    cmd = ['code']
    if line_num: # here is for the O command, opening a new tab in an already opened vscode tab
        cmd.append('--goto')
        cmd.append(file_path+':'+str(line_num))
    else: # here is for the o command, opening the directory
        cmd.append(file_path)
        if open_file:
            cmd.append(open_file)
    try:
        subprocess.run(cmd, check=True)
        console.print("[green]opened in vscode: [/green]"+file_path)
    except FileNotFoundError:
        console.print("[red]Error:[/red] 'code' command not found. make sure vscode is installed and in path...")

##########################################################
################# search functions #######################

def search_packages(files_df, packages_df, search_term):
    """search for packages by name"""
    matching_packages = packages_df[packages_df['package'].str.contains(search_term, case=False)]
    number_matching = len(matching_packages)
    if len(matching_packages) == 0:
        console.print("[red]No packages found[/red]")
        return None, None
    
    console.print("\n[green]Found [/green]" +str(number_matching) + "[green]packages:[/green]")
    for i, (_, row) in enumerate(matching_packages.head(20).iterrows(), 1):
        file_count = len(files_df[files_df['package_name'] == row['package']])
        console.print(f"  {i}. {row['package']} ({row['version']}) - {file_count} files")
    
    if len(matching_packages) > 20:
        console.print("  ... and" +str(number_matching - 20)+" more")
    
    if len(matching_packages) == 1:
        selected = matching_packages.iloc[0]
    else:
        choice = Prompt.ask("Select package number (or q to cancel)", default="0")
        if choice == "q":
            return None, None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(matching_packages):
                selected = matching_packages.iloc[idx]
            else:
                console.print("[red]Invalid selection[/red]")
                return None, None
        except ValueError:
            console.print("[red]Invalid input[/red]")
            return None, None
    
    package_files = files_df[files_df['package_name'] == selected['package']].to_dict('records')
    return package_files, 0

def list_monad_usage(files_df):
    """Show monad usage statistics"""
    monad_cols = [c for c in files_df.columns if c in ALL_MONAD_MODULES]
    
    console.print("\n[bold cyan]Monad Usage Statistics[/bold cyan]")
    console.print("-" * 50)
    
    stats = []
    for monad in monad_cols:
        count = files_df[files_df[monad] == 1].shape[0]
        if count > 0:
            stats.append((monad, count))
    
    stats.sort(key=lambda x: -x[1])
    #show in columns 
    for i, (monad, count) in enumerate(stats[:20], 1):
        pct = (count / len(files_df)) * 100
        console.print(f"{i:2}. {monad:45} {count:6} files ({pct:4.1f}%)")
    
    return stats

def select_monad(files_df):
    """Let user select a monad to browse"""
    stats = list_monad_usage(files_df)
    
    if not stats:
        console.print("[red]No monad imports found![/red]")
        return None
    
    console.print("\n[bold]Enter monad number or name to browse[/bold]")
    choice = Prompt.ask("Monad selection", default="")
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(stats):
            return stats[idx][0]
    else:
        #match by name
        matches = [m for m in stats if choice.lower() in m[0].lower()]
        if matches:
            return matches[0][0]
    
    return None

######################### main function ##########################
def browse_files(lts):
    """main browsing function with monad filtering, for 1 specific lts"""
    
    #load dfs
    files_df = load_files_df(lts)
    if files_df is None:
        return
    packages_df = load_packages_df(lts)
    if packages_df is None:
        return
    #grab unique files (dictionary)
    file_list = files_df.to_dict('records')
    total_files = len(file_list)
    
    console.print(f"\n[bold green]Haskell File Browser - LTS {lts}[/bold green]")
    console.print(f"[dim]Total files: {total_files}[/dim]")
    
    idx = 0
    search_mode = False
    searched_files = None
    monad_mode = False
    monad_name = None
    
    while True:
        #current file list
        if monad_mode and monad_name:
            current_files = searched_files
            mode_indicator = f" [MONAD: {monad_name}]"
            current_total = len(current_files)
        elif search_mode and searched_files:
            current_files = searched_files
            mode_indicator = " [SEARCH MODE]"
            current_total = len(current_files)
        else:
            current_files = file_list
            mode_indicator = ""
            current_total = total_files
        #is index valid
        if idx >= current_total:
            idx = current_total - 1
        if idx < 0:
            idx = 0
        current = current_files[idx]
        
        os.system('clear')
        
        #file info
        console.print(f"[bold cyan]File {idx+1}/{current_total}{mode_indicator}[/bold cyan]")
        #console.print(f"[yellow]Package:[/yellow] {current['package_name']} ({current['version']})")
        console.print(f"[yellow]Package ID:[/yellow] {current['package_id']}")
        console.print(f"[yellow]Module:[/yellow] {current['module_name']}")
        console.print(f"[yellow]Path:[/yellow] {current['file_path']}")
        #console.print(f"[yellow]Lines:[/yellow] {current['line_count']}")
        
        #monad imports for the file
        monad_cols = [c for c in files_df.columns if c in ALL_MONAD_MODULES]
        monads_used = [m for m in monad_cols if current.get(m, 0) == 1]
        if monads_used:
            console.print(f"[green]Monads:[/green] {', '.join(monads_used[:5])}")
        console.print("-" * 50)
        
        #display file content
        abs_path = get_absolute_file_path(current, packages_df)
        #display_file(abs_path)
        
        #navigation prompt
        #commands labels
        console.print("\n[dim]Commands:")
        console.print("[bold]n[/bold] next | [bold]p[/bold] previous | [bold]g[/bold] go to")
        console.print("[bold]s[/bold] search package | [bold]m[/bold] filter by monad | [bold]r[/bold] reset")
        console.print("[bold]o[/bold] open package directory | [bold]O[/bold] open in VSCode")
        console.print("[dim][bold]q[/bold] quit[/dim]")

        choice = Prompt.ask("", choices=["n", "p", "s", "m", "r", "o", "O", "g", "q"], default="n")
                
        if choice =='q':
            break
        elif choice =='r':
            search_mode = False
            monad_mode = False
            monad_name = None
            searched_files = None
            idx = 0
            console.print("[green]Reset to normal browsing mode[/green]")
            Prompt.ask("Press Enter to continue")
        elif choice =='s':
            result = search_packages(files_df, packages_df, 
                                     Prompt.ask("Enter package name (or part of it)"))
            if result[0] is not None:
                searched_files = result[0]
                search_mode = True
                monad_mode = False
                monad_name = None
                idx = 0
        elif choice =='m':
            #filter by monad
            selected_monad = select_monad(files_df)
            if selected_monad:
                monad_name = selected_monad
                monad_mode = True
                search_mode = False
                searched_files = get_monad_files(files_df, monad_name).to_dict('records')
                if searched_files:
                    idx = 0
                    console.print(f"[green]Showing {len(searched_files)} files that import {monad_name}[/green]")
                else:
                    console.print(f"[yellow]No files found importing {monad_name}[/yellow]")
                    monad_mode = False
                
        elif choice =='n':
            if idx<current_total-1:
                idx += 1
            else:
                console.print("[yellow]Already at last file[/yellow]")
                Prompt.ask("Press Enter to continue")
        elif choice =='p':
            if idx>0:
                idx -= 1
            else:
                console.print("[yellow]Already at first file[/yellow]")
                Prompt.ask("Press Enter to continue")
        elif choice =='g':
            try:
                num = int(Prompt.ask(f"Enter file number (1-{current_total})"))
                if 1 <= num <= current_total:
                    idx = num - 1
                else:
                    console.print(f"[red]Invalid number. Must be 1-{current_total}[/red]")
                    Prompt.ask("Press Enter to continue")
            except ValueError:
                console.print("[red]Invalid input[/red]")
                Prompt.ask("Press Enter to continue")
        elif choice =='O':
            #file in vsode
            abs_path = get_absolute_file_path(current, packages_df)
            if abs_path:
                # open_in_vscode(abs_path, current.get('line_count', None))
                open_in_vscode(abs_path, 0)
            else:
                console.print("[red]Could not find file path[/red]")
                Prompt.ask("Press Enter to continue")

        elif choice =='o':
            #open file directory in vscode
            abs_path = get_absolute_file_path(current, packages_df)
            pkg_info = packages_df[packages_df['package'] == current['package_name']]
            if len(pkg_info)>0:
                cabal_file = pkg_info.iloc[0].get('cabal-file', '')
                if cabal_file and not pd.isna(cabal_file):
                    package_root = os.path.dirname(cabal_file)
                    if os.path.exists(package_root):
                        open_in_vscode(package_root, 0, abs_path)
                    else:
                        console.print(f"[red]Package directory not found: {package_root}[/red]")
                        Prompt.ask("Press Enter to continue")
                else:
                    console.print("[red]No cabal file found for this package[/red]")
                    Prompt.ask("Press Enter to continue")
            else:
                console.print("[red]Package not found in packages DataFrame[/red]")
                Prompt.ask("Press Enter to continue")

def main():
    console.print("[bold]Haskell File Browser with Monad Filtering[/bold]")
    
    lts_list = get_available_lts_list()
    console.print("\n[bold]Available LTS versions:[/bold]")
    for i, lts in enumerate(lts_list[-10:], 1):
        console.print(f"  {i}. {lts}")
    
    lts = Prompt.ask("Enter LTS version", default=lts_list[-1])
    if lts not in lts_list:
        console.print(f"[red]LTS {lts} not found[/red]")
        return
    
    browse_files(lts)

if __name__ == "__main__":
    main()