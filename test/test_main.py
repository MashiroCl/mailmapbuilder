import unittest
import os
from github import Github
from core.main import search, MailMap
from core.repository import Repository

github = Github(user_agent="mashirocl", password=os.getenv("MAILMAPBUILDER"))

class MyTestCase(unittest.TestCase):


    def test_search(self):
        githuber = search("Benjamin Diedrichsen", github)
        self.assertEqual(githuber.login, "bennidi")

    def test_search_2(self):
        githuber = search("Andreas Perhab", github)
        print(githuber.login)
        print(githuber.names)
        print(githuber.emails)

    def test_build_githubers(self):
        githuber = search("Andreas Perhab", github)

    def test_mailmap_building(self):
        path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        repo = Repository(path)
        mailmap = MailMap(repo)
        mailmap.build_mailmap(".mailmap")


if __name__ == '__main__':
    unittest.main()
