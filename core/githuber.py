from typing import List

class GitHuber(object):
    def __init__(self, login):
        self.login = login
        self.names = set()
        self.emails = set()

    def __key(self):
        return self.login

    def __hash__(self):
        return self.__key()

    def add_names(self, name:str):
        if name not in self.names:
            self.names.add(name)

    def add_emails(self, email:str):
        if email not in self.emails:
            self.emails.add(email)

    def mailmap_format(self)->List[str]:
        res = []
        l = list(self.emails)
        proper_email = "<" + l[0] + ">"
        for i in range(len(l)):
            actual_email = "<" + l[i] + ">"
            res.append(self.login + " " + proper_email + " " + actual_email + "\n")
        return res
