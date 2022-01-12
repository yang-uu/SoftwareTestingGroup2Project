# -*- coding: utf-8 -*-
# This class is intended to test 5 following functionalities:
# insert()
# append()
# expend()
# insert_before()
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
        
    # This function adds content to a tag, just like Python's .append() method for lists.
    def test_append(self):
        Soup = self.soup()
        # 1.add "test_append_1" after the content of the <p> tag;
        Soup.p.append(" test_append_1")
        # Expected outputs: "<p>Hello World test_append_1</p>"
        self.assertEqual("<p>Hello World test_append_1</p>", str(Soup.p))
        # 2.add "test_append_2" after the content of the <p> tag;
        Soup.p.append(" test_append_2")
        # Expected outputs: "<p>Hello World test_append_1 test_append_2</p>"
        self.assertEqual("<p>Hello World test_append_1 test_append_2</p>", str(Soup.p))
        # 3.add "test_append_3" after the content of the <p> tag;
        Soup.p.append(" test_append_3")
        # Expected outputs: "<p>Hello World test_append_1 test_append_2 test_append_3</p>"
        self.assertEqual("<p>Hello World test_append_1 test_append_2 test_append_3</p>", str(Soup.p))

    # This function is similar to the .append() function, except that it does not add a new element to the end of the parent node's .contents property, but inserts the element at the specified position.
    def test_insert(self):
        Soup = self.soup()
        tag = Soup.find("p")
        # 1.Insert "test_insert_1" after the <p> tag;
        tag.insert(0,"test_insert_1 ")
        # Expected outputs: "<p>test_insert_1 Hello World</p>"
        self.assertEqual("<p>test_insert_1 Hello World</p>", str(Soup.p))
        # 2.Insert "test_insert_2" after the first string of the <p> tag;
        tag.insert(1,"test_insert_2 ")
        # Expected outputs: "<p>Hello World test_insert_1 test_insert_2</p>"
        self.assertEqual("<p>test_insert_1 test_insert_2 Hello World</p>", str(Soup.p))
        # 3.Insert "test_insert_3" after the third string of the <p> tag;
        tag.insert(3," test_insert_3")
        # Expected outputs: "<p>Hello World test_insert_1 test_insert_2 test_insert_3</p>"
        self.assertEqual("<p>test_insert_1 test_insert_2 Hello World test_insert_3</p>", str(Soup.p))

    # This function is similar to the .append() function, except that it can add multiple new elements at the end of the parent node's .contents property.
    def test_expend(self): 
        Soup = self.soup()
        # 1.Insert array [" ", "test_expend_1", "?"] after the content of the <p> tag;
        extend_text_1 = [" ", "test_expend_1", "?"]
        Soup.p.extend(extend_text_1)
        # Expected outputs: "<p>Hello World test_expend_1?</p>"
        self.assertEqual("<p>Hello World test_expend_1?</p>", str(Soup.p))
        # 2.Insert array [" ", "test_expend_2", "!"] after the content of the <p> tag;
        extend_text_2 = [" ", "test_expend_2", "!"]
        Soup.p.extend(extend_text_2)
        # Expected outputs: "<p>Hello World test_expend_1? test_expend_2!</p>"
        self.assertEqual("<p>Hello World test_expend_1? test_expend_2!</p>", str(Soup.p))
        # 3.Insert array [" ", "test_expend_3", "..."] after the content of the <p> tag;
        extend_text_3 = [" ", "test_expend_3", "..."]
        Soup.p.extend(extend_text_3)
        # Expected outputs: "<p>Hello World test_expend_1? test_expend_2! test_expend_3...</p>"
        self.assertEqual("<p>Hello World test_expend_1? test_expend_2! test_expend_3...</p>", str(Soup.p))
        
    # This function inserts tags or strings immediately before something else in the parse tree
    def test_insert_before(self):
        Soup = self.soup()
        alex_tag = Soup.find("p")
        # 1.Insert "test_insert_before_1" before the <p> tag;
        alex_tag.insert_before("test_insert_before_1 ")
        # Expected outputs: "test_insert_before_1 <p>Hello World</p>"
        self.assertEqual("<div>test_insert_before_1 <p>Hello World</p></div>", str(Soup.div))
        # 2.Insert "test_insert_before_2" before the <p> tag;
        alex_tag.insert_before("test_insert_before_2 ")
        # Expected outputs: "test_insert_before_1 test_insert_before_2 <p>Hello World</p>"
        self.assertEqual("<div>test_insert_before_1 test_insert_before_2 <p>Hello World</p></div>", str(Soup.div))
        # 3.Insert "test_insert_before_2" before the <p> tag;
        alex_tag.insert_before("test_insert_before_3 ")
        # Expected outputs: "test_insert_before_1 test_insert_before_2 test_insert_before_3 <p>Hello World</p>"
        self.assertEqual("<div>test_insert_before_1 test_insert_before_2 test_insert_before_3 <p>Hello World</p></div>", str(Soup.div))

    # This function inserts tags or strings immediately following something else in the parse tree
    def test_insert_after(self):
        Soup = self.soup()
        alex_tag = Soup.find("p")
        # 1.Insert "test_insert_before_1" after the <p> tag;
        alex_tag.insert_after(" test_insert_after_1")
        # Expected outputs: "<p>Hello World</p> test_insert_after_1"
        self.assertEqual("<div><p>Hello World</p> test_insert_after_1</div>", str(Soup.div))
        # 2.Insert "test_insert_after_2" after the <p> tag;
        alex_tag.insert_after(" test_insert_after_2")
        # Expected outputs: "<p>Hello World</p> test_insert_after_2 test_insert_after_1"
        self.assertEqual("<div><p>Hello World</p> test_insert_after_2 test_insert_after_1</div>", str(Soup.div))
        # 3.Insert "test_insert_after_3" after the <p> tag;
        alex_tag.insert_after(" test_insert_after_3")
        # Expected outputs: "<p>Hello World</p> test_insert_after_3 test_insert_after_2 test_insert_after_1"
        self.assertEqual("<div><p>Hello World</p> test_insert_after_3 test_insert_after_2 test_insert_after_1</div>", str(Soup.div))


    # Whitebox Testing
    def test_insert(self):
        Soup = BeautifulSoup("<div><a></a>text</div>", "html.parser")
        tag = Soup.find("p")
        # 1.Insert "test_insert_1" after the <p> tag;
        tag.insert(0,"test_insert_1 ")
        # Expected outputs: "<p>test_insert_1 Hello World</p>"
        self.assertEqual("<p>test_insert_1 Hello World</p>", str(Soup.p))
        
        # 2.Insert "test_insert_2" after the first string of the <p> tag;
        tag.insert(1," test_insert_2")
        # Expected outputs: "<p>Hello World test_insert_1 test_insert_2</p>"
        self.assertEqual("<p>test_insert_1 Hello World test_insert_2</p>", str(Soup.p))
        
        # 3.Insert "test_insert_3" after the third string of the <p> tag;
        tag.insert(3," test_insert_3")
        # Expected outputs: "<p>Hello World test_insert_1 test_insert_2 test_insert_3</p>"
        self.assertEqual("<p>test_insert_1 Hello World test_insert_2 test_insert_3</p>", str(Soup.p))
        
        
if __name__ == '__main__':
    unittest.main()