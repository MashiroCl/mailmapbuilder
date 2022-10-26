from typing import List
import os
import requests
from time import sleep, time
from core.githuber import GitHuber
from core.repository import Repository

GITHUB_GET_USER_API = "https://api.github.com/users/"
GITHUB_SEARCH_USER_API = "https://api.github.com/search/users?q="
NULL = "null"

class MailMap:
    def __init__(self, repo: Repository):
        self.repo = repo

    def build_mailmap(self, mailmap_path: str) -> List[GitHuber]:
        '''
        use commit history to build mailmap
        :param mailmap_path:
        :param repo:
        :return: list of GithHbers
        '''
        d = self.repo.get_useremails()
        l = list(d)
        record = [0] * len(l)
        githubers = []

        def supplement_githuber(g: GitHuber, name, emails):
            g.names.add(name)
            for email in emails:
                if email:  # avoid None email
                    g.emails.add(email)

        for p1 in range(len(l)):
            if record[p1] == 0:
                githuber = search(l[p1])
                supplement_githuber(githuber, l[p1], d.get(l[p1]))
                first, changed = True, False
                while first or changed:
                    first, changed = False, False
                    for p2 in range(p1 + 1, len(l)):
                        if record[p2] == 0:
                            if l[p2] == githuber.login or l[p2] in githuber.names:
                                supplement_githuber(githuber, l[p2], d.get(l[p2]))
                                record[p2] = 1
                                changed = True
                            elif set_intersection(githuber.emails, d.get(l[p2])):
                                supplement_githuber(githuber, l[p2], d.get(l[p2]))
                                record[p2] = 1
                                changed = True
                githuber2mailmap(githuber, mailmap_path)
                githubers.append(githuber)
        return githubers


def githuber2mailmap(githuber: GitHuber, path: str):
    with open(path, "a", encoding="utf-8") as f:
        f.writelines(githuber.mailmap_format())


def wait_api_rate_limit(response:requests.Response):
    if int(response.headers["X-RateLimit-Remaining"]) <= 1:
        while int(time()) < int(response.headers["X-RateLimit-Reset"]):
            sleep(1)

def search(user_name: str) -> GitHuber:
    user = search_top_user(user_name)
    githuber = GitHuber(user["login"])
    add_name_email(githuber)
    return githuber


def search_top_user(user_name:str)->dict:
    # choose the top 1 search result
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + os.getenv("MAILMAPBUILDER"),
    }
    response = requests.get(GITHUB_SEARCH_USER_API + user_name, headers=headers)
    wait_api_rate_limit(response)
    candidates = response.json()["items"]

    # if "items" in response.json():
    #     candidates = response.json()["items"]
    # else:
    #     candidates = []
    if len(candidates)>0:
        return candidates[0]
    # if user not found, use the name as his/her login
    else:
        return {"login":user_name}

def add_name_email(githuber: GitHuber):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + os.getenv("MAILMAPBUILDER"),
    }
    response = requests.get(GITHUB_GET_USER_API + githuber.login, headers=headers)
    wait_api_rate_limit(response)
    response_json = response.json()
    name, email = response_json.get("name", None),  response_json.get("email", None)
    if name:
        githuber.add_names(name)
    if email:  # if the personal page doesn't contain a public eamil, the return value will be None
        githuber.add_emails(email)


def set_intersection(a, b) -> bool:
    for each in a:
        if each in b:
            return True
    return False


def write_file(data):
    with open("/Users/leichen/Desktop/header.json", "a") as f:
        f.write(data)
        f.write("\n")
