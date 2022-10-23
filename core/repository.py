import os

class Repository:
    def __init__(self, path):
        self.path = path

    def get_useremails(self):
        '''
        using local commit history to obtain a dict {user1:{email1, email2}, user2:{email1, email2}}
        :return:
        '''
        readObj = os.popen(f"git -C {self.path} shortlog HEAD -s -e")
        d = self._split_shortlog(readObj.readlines())
        readObj.close()
        return d

    def _split_shortlog(self, shortlog):
        # shortlog example:     48	Benjamin Diedrichsen <b.diedrichsen@gmail.com>
        d = dict()
        for log in shortlog:
            name = log.split(" <")[0].split("\t")[1]
            email = log.split(" <")[1].split(">")[0]
            d.setdefault(name, set()).add(email)
        return d
