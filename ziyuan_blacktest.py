# -*- coding: utf-8 -*-
# This class is intended to test 5 following functionalities:
# insert()
# append()
# expend()
# before()
# insert_after()

import unittest
from bs4 import BeautifulSoup


class TestCase(unittest.TestCase):
    @staticmethod
    def soup(*args, **kwargs):
        return BeautifulSoup(
            """
                <html>
                    <body>
                        <div><p>Hello World</p></div>
                    </body>
                </html>
            """, "html.parser", *args, **kwargs)

    def test_insert(self):
        Soup = self.soup()
        tag = Soup.find("p")
        tag.insert(1, " test_insert_1")
        print(str(Soup.p))
        self.assertEqual("<p>Hello World test_insert_1</p>", str(Soup.p))
        tag.insert(2, " test_insert_2")
        self.assertEqual("<p>Hello World test_insert_1 test_insert_2</p>", str(Soup.p))
        tag.insert(3, " test_insert_3")
        self.assertEqual("<p>Hello World test_insert_1 test_insert_2 test_insert_3</p>", str(Soup.p))

    def test_append(self):
        Soup = self.soup()
        Soup.p.append(" test_append_1")
        self.assertEqual("<p>Hello World test_append_1</p>", str(Soup.p))
        Soup.p.append(" test_append_2")
        self.assertEqual("<p>Hello World test_append_1 test_append_2</p>", str(Soup.p))
        Soup.p.append(" test_append_3")
        self.assertEqual("<p>Hello World test_append_1 test_append_2 test_append_3</p>", str(Soup.p))

    def test_expend(self):
        Soup = self.soup()
        extend_text_1 = [" ", "test_expend_1", "?"]
        Soup.p.extend(extend_text_1)
        self.assertEqual("<p>Hello World test_expend_1?</p>", str(Soup.p))
        extend_text_2 = [" ", "test_expend_2", "!"]
        Soup.p.extend(extend_text_2)
        self.assertEqual("<p>Hello World test_expend_1? test_expend_2!</p>", str(Soup.p))
        extend_text_3 = [" ", "test_expend_3", "..."]
        Soup.p.extend(extend_text_3)
        self.assertEqual("<p>Hello World test_expend_1? test_expend_2! test_expend_3...</p>", str(Soup.p))

    def test_insert_before(self):
        Soup = self.soup()
        alex_tag = Soup.find("p")
        alex_tag.insert_before("test_insert_before_1 ")
        self.assertEqual("<div>test_insert_before_1 <p>Hello World</p></div>", str(Soup.div))
        alex_tag.insert_before("test_insert_before_2 ")
        self.assertEqual("<div>test_insert_before_1 test_insert_before_2 <p>Hello World</p></div>", str(Soup.div))
        alex_tag.insert_before("test_insert_before_3 ")
        self.assertEqual("<div>test_insert_before_1 test_insert_before_2 test_insert_before_3 <p>Hello World</p></div>",
                         str(Soup.div))

    def test_insert_after(self):
        Soup = self.soup()
        alex_tag = Soup.find("p")
        alex_tag.insert_after(" test_insert_after_1")
        self.assertEqual("<div><p>Hello World</p> test_insert_after_1</div>", str(Soup.div))
        alex_tag.insert_after(" test_insert_after_2")
        self.assertEqual("<div><p>Hello World</p> test_insert_after_2 test_insert_after_1</div>", str(Soup.div))
        alex_tag.insert_after(" test_insert_after_3")
        self.assertEqual("<div><p>Hello World</p> test_insert_after_3 test_insert_after_2 test_insert_after_1</div>",
                         str(Soup.div))


if __name__ == '__main__':
    unittest.main()
