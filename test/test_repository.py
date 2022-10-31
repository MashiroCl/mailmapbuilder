import unittest
from core.repository import Repository


class MyTestCase(unittest.TestCase):

    def test_repository(self):
        path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        r = Repository(path)

    def test_get_useremails(self):
        path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jsoup"
        r = Repository(path)
        d = r.get_useremails()
        print("================")
        print(d)
        print("================")
        self.assertEqual({'benjamin.diedrichsen@okotta.com', 'b.diedrichsen@googlemail.com', 'b.diedrichsen@gmail.com'},
                         d.get("Benjamin Diedrichsen"))

    def test_split_shortlog(self):
        path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        r = Repository(path)
        res = r._split_shortlog(["\t48	Benjamin Diedrichsen <b.diedrichsen@gmail.com>"])
        print(res)

if __name__ == '__main__':
    unittest.main()
