import unittest
import os
from github import Github
from core.githuber import GitHuber
from core.main import search, MailMap, add_name_email, search_top_user
from core.repository import Repository

github = Github(user_agent="mashirocl", password=os.getenv("MAILMAPBUILDER"))

class MyTestCase(unittest.TestCase):


    def test_search(self):
        githuber = search("Benjamin Diedrichsen", github)
        self.assertEqual(githuber.login, "bennidi")

    def test_search2(self):
        githuber = search("Andreas Perhab")
        self.assertEqual(githuber.login,"bigbear3001")

    def test_add_name_email(self):
        githuber = GitHuber("mashirocl")
        add_name_email(githuber)

    # def test_search_rate_limit(self):
    #     for i in range(60):
    #         search_top_user("Benjamin Diedrichsen")

    def test_search_top_user(self):
        url = search_top_user("Benjamin Diedrichsen")["url"]
        self.assertEqual("https://api.github.com/users/bennidi", url)

    def test_search(self):
        githuber = search("bennidi")
        self.assertTrue("b.diedrichsen@gmail.com" in githuber.emails)

    def test_mailmap_building(self):
        path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        repo = Repository(path)
        mailmap = MailMap(repo)
        mailmap.build_mailmap(".mailmap")

if __name__ == '__main__':
    unittest.main()
