import pandas as pd
import os 
from utils import *

writer_df=load_generated_df("writer","24-37")

print("columns:", writer_df.columns.tolist())
print(f"Total Writer files classified: {len(writer_df)}")
print(writer_df.head())
