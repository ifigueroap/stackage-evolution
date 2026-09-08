import os 
import pandas as pd
import sys
sys.path.append("..")
from cataloger import *
from utils import load_sample

LTS="24-37"
MONADS=["Control.Monad.Reader",
        "Control.Monad.Reader.Lazy",
        "Control.Monad.Reader.Strict"]
OUTPUT_JSONL="reader_testing.jsonl"
INSTRUCTIONS_PATH = "../instructions/instructions_reader.md"
SAMPLE_PATH="lts-24-37-reader-sample.txt"
REPO_ROOT = os.path.abspath("../..")
print("root:",REPO_ROOT)

#out_jsonl = "results_writer.jsonl"
package_df=load_package_df(LTS)
files_df=load_files_df(LTS)
#repo_root = os.path.abspath("..")#get project root dir
#print(repo_root)


#combine import variations into one df
DF_FILES = pd.DataFrame()
for monad in MONADS:
    df = get_monad_files(files_df, monad)
    DF_FILES = pd.concat([DF_FILES, df])
DF_FILES = DF_FILES.drop_duplicates(
    subset=["package_id", "file_path"]
  #  ).copy()
).reset_index(drop=True)

sample = load_sample(SAMPLE_PATH)

DF_FILES = DF_FILES.iloc[
    [i - 1 for i in sample]
].copy()
# ].reset_index(drop=True)

DF_FILES["sample_number"] = sample
#DF_FILES = DF_FILES.reset_index(drop=True)
 #add a column with the absolute_file_path
# so that it can easily be given to the codex
DF_FILES['absolute_file_path'] = DF_FILES.apply(
    get_absolute_file_path,
    axis=1,
    packages_df=package_df
)

run_cataloger(LTS, OUTPUT_JSONL,REPO_ROOT, INSTRUCTIONS_PATH, DF_FILES)