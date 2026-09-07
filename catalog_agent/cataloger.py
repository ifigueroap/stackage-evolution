import pandas as pd
import os 
import subprocess
from utils import *
LTS="24-37"
MONAD="Control.Monad.Writer"
#MONAD="Control.Monad.Writer.Lazy"
#MONAD="Control.Monad.Writer.Strict"
MONADS=["Control.Monad.Writer",
        "Control.Monad.Writer.Lazy",
        "Control.Monad.Writer.Strict"]
MODEL_MINI="gpt-4.1-mini"
MODEL_DEFAULT="gpt-5.6"
out_jsonl = "results_writer.jsonl"
package_df=load_package_df(LTS)
files_df=load_files_df(LTS)
repo_root = os.path.abspath("..")#get project root dir

#checkpoint
if os.path.exists("checkpoint.txt"): #if it exists, we open it
    with open("checkpoint.txt", "r") as f:
        checkpoint = int(f.read().strip())
else:
    checkpoint = 0
    with open("checkpoint.txt", "w") as f: #if it doesnt exist, we create it
        f.write("0")
#results file
if not os.path.exists(out_jsonl):
    with open(out_jsonl, "w") as f: #if it doesnt exist, we create it
            f.write("")

#combine import variations into one df
df_files = pd.DataFrame()
for monad in MONADS:
    df = get_monad_files(files_df, monad)
    df_files = pd.concat([df_files, df])
df_files = df_files.drop_duplicates(
    subset=["package_id", "file_path"]
).reset_index(drop=True)

#add a column with the absolute_file_path
# so that it can easily be given to the codex
df_files['absolute_file_path'] = df_files.apply(
    get_absolute_file_path,
    axis=1,
    packages_df=package_df
)


#load instructions
instructions_path = "instructions_writer.md"
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
    path = os.path.relpath(abs_path, repo_root)
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
        ["codex", "exec", "--json", "-C", repo_root, prompt],
        capture_output=True,
        text=True
    )
    parsed = extract_item_completed(result.stdout)

    record = {
        "index": index,
        "package_id": package_id,
        "package": package_name,
        "module": module,
        "path": path,
        **parsed
    }

    with open(out_jsonl, "a") as f:
        f.write(json.dumps(record) + "\n")

    with open("checkpoint.txt", "w") as f:
        f.write(str(index+1))
    
    
    print("saved")
    print(result.stdout)
        

