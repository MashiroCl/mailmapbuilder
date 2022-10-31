import subprocess

class Repository:
    def __init__(self, path):
        self.path = path

    def get_useremails(self):
        '''
        using local commit history to obtain a dict {user1:{email1, email2}, user2:{email1, email2}}
        :return:
        '''
        data = subprocess.check_output(["git","-C", self.path, "shortlog", "HEAD", "-s","-e"], encoding = "utf-8",errors ="ignore")
        d = self._split_shortlog(data.split("\n"))
        return d

    def _split_shortlog(self, shortlog):
        # shortlog example:     48	Benjamin Diedrichsen <b.diedrichsen@gmail.com>
        d = dict()
        for log in shortlog:
            if len(log)>0:
                name = log.split(" <")[0].split("\t")[1]
                email = log.split(" <")[1].split(">")[0]
                d.setdefault(name, set()).add(email)
        return d
