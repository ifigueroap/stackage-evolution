import sys
from pathlib import Path
# Get the absolute path of the directory 1 level up
parent_dir = str(Path(__file__).resolve().parents[1])
# Add it to the front of the search path
sys.path.insert(0, parent_dir)

from utils.utils  import *


d0=""
d2= "/home/giacamole/projects/memoria-haskell/stackage-evolution"
d1="/home/giacamole/projects/memoria-haskell/stackage-evolution/lts_downloaded/tar_package/lts-21-7/AC-Angle/AC-Angle-1.0/AC-Angle.cabal"
d3="/home/giacamole/projects/memoria-haskell/stackage-evolution/lts_downloaded/tar_package/lts-21-7/aeson/aeson-2.1.2.1/aeson.cabal"
d4='/home/giacamole/projects/memoria-haskell/stackage-evolution/lts_downloaded/tar_package/lts-13-19/active/active-0.2.0.13/active.cabal'
#   get_cabal_file_directory
assert get_cabal_file_directory(d1) == "/home/giacamole/projects/memoria-haskell/stackage-evolution/lts_downloaded/tar_package/lts-21-7/AC-Angle/AC-Angle-1.0"
assert get_cabal_file_directory(d2) == "/home/giacamole/projects/memoria-haskell"
assert get_cabal_file_directory(d0) ==""

#   get_haskell_files
hs_list1= get_haskell_files(get_cabal_file_directory(d1))
hs_list4= get_haskell_files(get_cabal_file_directory(d4))
hs_list3= get_haskell_files(get_cabal_file_directory(d3))
assert hs_list1 == ['Data/Angle.hs']
assert hs_list4 == ['test/active-tests.hs', 'src/Data/Active.hs']


def print_list(lis):
  for element in lis:
    print(element)

# print_list(hs_list1)
# print_list(hs_list4)
assert get_file_stats(hs_list1[0],get_cabal_file_directory(d1)) == {'line_count': 52, 'word_count': 250, 'char_count': 1412}

d5="/home/giacamole/projects/memoria-haskell/stackage-evolution/lts_downloaded/tar_package/lts-21-7/AC-Angle/AC-Angle-1.0"
d6="src/Data/AC-Angle.hs"
d7="test/Data/Warp/AC-Angle.hs"
#print(path_to_module_name(d6))
assert path_to_module_name(d6)=='Data.AC-Angle'
assert path_to_module_name(d7)=='Data.Warp.AC-Angle'

# import pandas as pd
# from pathlib import Path

# # Use absolute path (adjust if needed)
# base_path = "/home/giacamole/projects/memoria-haskell/stackage-evolution/data/dfs"
# lts_to_test = '21-7'

# # Check if the file exists
# df_path = Path(base_path) / f"lts-{lts_to_test}" / f"lts-{lts_to_test}.df"
# print(f"Looking for: {df_path}")
# print(f"File exists: {df_path.exists()}")

# # List what LTS directories you have
# dfs_dir = Path(base_path)
# if dfs_dir.exists():
#     print(f"\nAvailable LTS folders:")
#     for folder in sorted(dfs_dir.glob("lts-*")):
#         print(f"  {folder.name}")
# else:
#     print(f"\nBase path not found: {base_path}")

# # If the file exists, load it
# if df_path.exists():
#     df = pd.read_pickle(df_path)
#     print(f"\nLoaded {len(df)} packages from {lts_to_test}")
# else:
#     print(f"\nFile not found. Please check the path.")

# test1.py - place this in /explorer directory
# import pandas as pd
# import os

# # Check where we are
# print("Current directory:", os.getcwd())

# # Try relative path from /explorer
# # From /explorer, ../../data/dfs goes up two levels to stackage-evolution/data/dfs
# df_path = '../../data/dfs/lts-21-7/lts-21-7.df'
# print(f"Looking for: {df_path}")
# print(f"File exists: {os.path.exists(df_path)}")

# # List what's in the path to debug
# if not os.path.exists(df_path):
#     print("\nDebug: Checking path components")
#     print("data/dfs exists?", os.path.exists('../../data/dfs'))
#     print("data/dfs/lts-21-7 exists?", os.path.exists('../../data/dfs/lts-21-7'))
    
#     # List contents of data/dfs
#     if os.path.exists('../../data/dfs'):
#         print("\nContents of ../../data/dfs:")
#         print(os.listdir('../../data/dfs'))

import pandas as pd

# Load a unified DataFrame
df = pd.read_pickle('../data/dfs/lts-21-7/lts-21-7-unified.df')

# Check columns
print(f"Total columns: {len(df.columns)}")
print(f"\nSample columns:")
for col in df.columns[:20]:
    print(f"  {col}")

# Check monad columns
monad_cols = [col for col in df.columns if 'Control.Monad' in col]
print(f"\nMonad columns: {len(monad_cols)}")
print(f"First 5: {monad_cols[:5]}")

# Check a specific package
pkg = df[df['package'] == 'text']
if len(pkg) > 0:
    print(f"\nPackage 'text' monad usage:")
    for monad in monad_cols[:10]:
        print(f"  {monad}: {pkg.iloc[0][monad]}")