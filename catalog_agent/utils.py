import os 
import pandas as pd
import json
def get_monad_files(files_df, monad_name):
    """get files that import a specific monad"""
    if monad_name not in files_df.columns:
        return pd.DataFrame()
    return files_df[files_df[monad_name] == 1]

def load_files_df(lts):
    """load the files dataframe for a given lts
    lts: string label for lts version, for example, '12-13' """
    files_path = f'../data/dfs/lts-{lts}/lts-{lts}-files.df'
    if not os.path.exists(files_path):
        print("Error: file path not found "+files_path)
        return None
    return pd.read_pickle(files_path)

def load_package_df(lts):
    """load the package dataframe for a given lts
    lts: string label for lts version, for example, '12-13' """
    files_path = f'../data/dfs/lts-{lts}/lts-{lts}.df'
    if not os.path.exists(files_path):
        print("Error: file path not found "+files_path)
        return None
    return pd.read_pickle(files_path)
def find_package_root(cabal_path):
    """returns the directory in which the input file is in"""
    if pd.isna(cabal_path) or not cabal_path:
        return None
    return os.path.dirname(cabal_path)

def get_absolute_file_path(row, packages_df):
    pkg_info = packages_df[
        (packages_df['package'] == row['package_name']) &
        (packages_df['version'] == row['version'])
    ]

    if pkg_info.empty:
        return None

    cabal_file = pkg_info.iloc[0]['cabal-file']

    if pd.isna(cabal_file) or not cabal_file:
        return None

    package_root = os.path.dirname(cabal_file)

    return os.path.normpath(
        os.path.join(package_root, row['file_path'])
    )

#extracts the item.completed
def extract_item_completed(codex_text):
    events = []
    for line in codex_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    for ev in reversed(events):
        if ev.get("type") == "item.completed":
            item = ev.get("item", {})
            if item.get("type") == "agent_message":
                text = item.get("text", "").strip()

                # 1) Try exact JSON
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass

                # 2) Try to extract the first JSON object from the text
                start = text.find("{")
                if start != -1:
                    decoder = json.JSONDecoder()
                    try:
                        obj, _ = decoder.raw_decode(text[start:])
                        return obj
                    except json.JSONDecodeError:
                        pass

                return {"parse_error": True, "raw_text": text}

    return {"parse_error": True, "raw_text": codex_text}