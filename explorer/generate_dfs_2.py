from  utils.utils import *
from add_monad_columns import *
#process_all_lts()
#process_all_lts_with_monads()
# Run with checkpointing



# check_corrupted.py
import pandas as pd
import os

lts_list = get_lts_list_from_csv()
corrupted = []

for lts in lts_list:
    files_path = f'../data/dfs/lts-{lts}/lts-{lts}-files.df'
    if os.path.exists(files_path):
        try:
            df = pd.read_pickle(files_path)
            # Check if it has the required columns
            if 'file_path' not in df.columns:
                corrupted.append(lts)
        except Exception as e:
            print(f"❌ Corrupted LTS {lts}: {e}")
            corrupted.append(lts)

print(f"\nCorrupted files found: {corrupted}")
check_processed_lts()
process_all_lts_with_monads()
clean_all_lts() 