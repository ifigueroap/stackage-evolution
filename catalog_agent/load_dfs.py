import pandas as pd
import os 

def load_generated_df(dfs_name: str, lts: str):
    path = f"../data/dfs/lts-{lts}/lts-{lts}-{dfs_name}.df"
    if not os.path.exists(path):
        print("Error: file path not found " + path)
        return None
    return pd.read_pickle(path)


writer_df=load_generated_df("writer","24-37")

print("columns:", writer_df.columns.tolist())
print(f"Total Writer files classified: {len(writer_df)}")
print(writer_df.head())
