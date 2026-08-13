import json
import pandas as pd
import os
import utils

WRITER_JSONL_PATH = "results_writer.jsonl"

#this grabs the content of the jsonl files and creates pandas dataframes 
#dfs_name would be for example, "writer".
def generate_dfs_from_jsonl(jsonl_path:str, dfs_name:str, lts:str):
    df = pd.read_json(jsonl_path, lines=True)

    #flatten api_usage and categories
    api_df = pd.json_normalize(df["api_usage"]).add_prefix("api_")
    df = pd.concat([df.drop(columns=["api_usage"]), api_df], axis=1)
    cat_df = pd.json_normalize(df["categories"]).add_prefix("cat_")
    df = pd.concat([df.drop(columns=["categories"]), cat_df], axis=1)

    #save
    out_dir = f"../data/dfs/lts-{lts}"
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, f"lts-{lts}-{dfs_name}.df")
    df.to_pickle(out_path)


generate_dfs_from_jsonl(WRITER_JSONL_PATH, "writer", "24-37")
print("Writer dataframes saved at data/dfs/lts-24-37")

