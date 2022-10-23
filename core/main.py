from github import Github
from typing import List
import os
import requests
from time import sleep
from core.githuber import GitHuber
from core.repository import Repository

GITHUB_GET_USER_API = "https://api.github.com/users/"
NULL = "null"

class LimitCount:
    """Class count the api limit"""
    _counter = 0

    def addcounter(self):
        self._counter += 1
        if self._counter == 30:
            sleep(60)
            self._counter = 0


limitcount = LimitCount()


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
        github = Github(user_agent="anonymous", password=os.getenv("MAILMAPBUILDER"))

        # print(github.get_rate_limit())

        def supplement_githuber(g: GitHuber, name, emails):
            g.names.add(name)
            for email in emails:
                if email:  # avoid None email
                    g.emails.add(email)

        for p1 in range(len(l)):
            if record[p1] == 0:
                githuber = search(l[p1], github)
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


def search(user_name: str, g: Github) -> GitHuber:
    print(f"user name: {user_name}")
    res = g.search_users(user_name)
    limitcount.addcounter()
    # choose the top 1 search result and obtain the 'login' and 'name'
    if res.totalCount > 0:
        githuber = GitHuber(res[0].login)
        if not res[0].name == NULL:
            githuber.add_names(res[0].name)
        add_email(githuber)
        # print(f"name: {githuber.names}, login: {githuber.login}, email: {githuber.emails}")
    else:  # user name not found in GitHub
        githuber = GitHuber(user_name)
    return githuber


def add_email(githuber: GitHuber):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + os.getenv("MAILMAPBUILDER"),
    }
    response = requests.get(GITHUB_GET_USER_API + githuber.login, headers=headers)
    limitcount.addcounter()
    email = response.json()["email"]
    if email: # if the personal page doesn't contain a public eamil, the return value will be None
        githuber.add_emails(email)


def set_intersection(a, b) -> bool:
    for each in a:
        if each in b:
            return True
    return False


