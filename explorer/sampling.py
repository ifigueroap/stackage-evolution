from random import *
import pandas as pd
from math import *
from utils.utils import get_sample_from_lts
seed(24398576)
SAMPLE_PERCENT=0.2 #what percentage is going to be selected, in this case, its 20%
data = pd.read_csv("../src/lts_list.csv")
lts_list = data.columns

def create_sample_file(lts:str, monad_name:str, numbers:list[int]):
  file_name="sampling/lts-"+lts+"-"+monad_name+".txt"
  with open(file_name, "w") as file:
    for number in numbers:
      file.write(str(number)+"\n")
  

# writer
sample_writer=get_sample_from_lts("24-37","Control.Monad.Writer", SAMPLE_PERCENT)
create_sample_file("24-37", "writer",sample_writer)
# reader
sample_reader=get_sample_from_lts("24-37","Control.Monad.Reader", SAMPLE_PERCENT)
create_sample_file("24-37", "reader",sample_reader)
# state
sample_state=get_sample_from_lts("24-37","Control.Monad.State", SAMPLE_PERCENT)
create_sample_file("24-37", "state",sample_state)


  