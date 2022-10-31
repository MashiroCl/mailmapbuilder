import glob
import os
from core.repository import Repository
from core.main import MailMap
import datetime


def run(dataset_path, record):
    candidates = glob.glob(dataset_path)
    for each in candidates:
        repo_name = each.split("/")[-1]
        with open(record,"a") as f:
            f.write(f"{datetime.datetime.now()} {repo_name} running \n")
        MailMap(Repository(each)).build_mailmap(os.path.join(each, ".mailmap"))
        with open(record,"a") as f:
            f.write(f"{datetime.datetime.now()} {repo_name} finished \n")
