import glob
import time
import os
from core.repository import Repository
from core.main import MailMap

path = "/home/chenlei/projects/master_thesis/dataset/candidates/*"
record = "/home/chenlei/projects/master_thesis/dataset/record.txt"
candidates = glob.glob(path)
for each in candidates:
    MailMap(Repository(each)).build_mailmap(os.path.join(each, ".mailmap"))
    with open(record,"a") as f:
        f.write(each.split("/")[-1] + "\n")
    time.sleep(60)
