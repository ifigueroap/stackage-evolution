import pandas as pd
import os 
import subprocess
from utils import *
# LTS="24-37"
# MONADS=["Control.Monad.Writer",
#         "Control.Monad.Writer.Lazy",
#         "Control.Monad.Writer.Strict"]

# #out_jsonl = "results_writer.jsonl"
# package_df=load_package_df(LTS)
# files_df=load_files_df(LTS)
# #repo_root = os.path.abspath("..")#get project root dir
# #print(repo_root)


# #combine import variations into one df
# DF_FILES = pd.DataFrame()
# for monad in MONADS:
#     df = get_monad_files(files_df, monad)
#     DF_FILES = pd.concat([DF_FILES, df])
# DF_FILES = DF_FILES.drop_duplicates(
#     subset=["package_id", "file_path"]
# ).reset_index(drop=True)


#  #add a column with the absolute_file_path
# # so that it can easily be given to the codex
# DF_FILES['absolute_file_path'] = DF_FILES.apply(
#     get_absolute_file_path,
#     axis=1,
#     packages_df=package_df
# )


def run_cataloger(lts:str, out_jsonl_filename:str, repo_root_dir:str,instructions_path:str, df_files):
    #checkpoint
    if os.path.exists("checkpoint.txt"): #if it exists, we open it
        with open("checkpoint.txt", "r") as f:
            checkpoint = int(f.read().strip())
    else:
        checkpoint = 0
        with open("checkpoint.txt", "w") as f: #if it doesnt exist, we create it
            f.write("0")
    #results file
    if not os.path.exists(out_jsonl_filename):
        with open(out_jsonl_filename, "w") as f: #if it doesnt exist, we create it
                f.write("")

    # #combine import variations into one df
    # df_files = pd.DataFrame()
    # for monad in monads:
    #     df = get_monad_files(files_df, monad)
    #     df_files = pd.concat([df_files, df])
    # df_files = df_files.drop_duplicates(
    #     subset=["package_id", "file_path"]
    # ).reset_index(drop=True)

    # #add a column with the absolute_file_path
    # # so that it can easily be given to the codex
    # df_files['absolute_file_path'] = df_files.apply(
    #     get_absolute_file_path,
    #     axis=1,
    #     packages_df=package_df
    # )

    #load instructions
    with open(instructions_path, "r") as f:
        instructions = f.read()

    print("Starting cataloger at row", checkpoint)

    #go through the files
    total_files = len(df_files)
    for index in range(checkpoint, total_files):
        print("-----------------------------")
        row = df_files.iloc[index]
        package_id=row["package_id"]
        package_name=row["package_name"]
        module=row["module_name"]
        abs_path=row["absolute_file_path"]
        path = os.path.relpath(abs_path, repo_root_dir)
        print("index =", index,"/", total_files)
        print(package_id)
        print(package_name)
        print(module)
        print(path)

        #promt
        prompt = f"""{instructions}

        Review this Haskell file according to the instructions above:
        package_id: {package_id}
        package: {package_name}
        module: {module}
        file_path: {path}
        """

        #codex
        result = subprocess.run(
            #["codex", "exec", "--json", "--model", MODEL_DEFAULT, "-C", repo_root, prompt],
            ["codex", "exec", "--json", "-C", repo_root_dir, prompt],
            capture_output=True,
            text=True
        )
        parsed = extract_item_completed(result.stdout)
        sample_number = int(row["sample_number"])
        record = {
            # "index": index,
            "index": sample_number,
            "package_id": package_id,
            "package": package_name,
            "module": module,
            "file_path": path,
            **parsed
        }

        with open(out_jsonl_filename, "a") as f:
            f.write(json.dumps(record) + "\n")

        with open("checkpoint.txt", "w") as f:
            f.write(str(index+1))
        
        
        print("saved")
        print(result.stdout)
        

