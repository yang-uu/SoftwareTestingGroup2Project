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
                        <div class="test_insert"><p> Hello World </p> Hello World </div>
                    </body>
                </html>
            """, "html.parser", *args, **kwargs)    
        
    # This function adds content to a tag, just like Python's .append() method for lists.
    def test_append(self):
        Soup = self.soup()
        # 1.add "test_append_1" after the content of the <p> tag;
        Soup.p.append(" test_append_1")
        # Expected: "<p>Hello World test_append_1</p>"
        self.assertEqual("<p>Hello World test_append_1</p>", str(Soup.p))
        # 2.add "test_append_2" after the content of the <p> tag;
        Soup.p.append(" test_append_2")
        # Expected: "<p>Hello World test_append_1 test_append_2</p>"
        self.assertEqual("<p>Hello World test_append_1 test_append_2</p>", str(Soup.p))
        # 3.add "<p>" after the content of the <p> tag;
        Soup.p.append("<p>")
        # Expected: "<p>Hello World test_append_1 test_append_2&lt; &gt;</p>"
        self.assertEqual("<p>Hello World test_append_1 test_append_2&lt;p&gt;</p>", str(Soup.p))
    
    # This function is similar to the .append() function, except that it does not add a new element to the end of the parent node's .contents property, but inserts the element at the specified position.
    def test_insert(self):
        Soup = self.soup()
        tag = Soup.find("p")
        # 1.Insert "test_insert_0" in the 0 position of the content <p> tag;
        tag.insert(0,"test_insert_0 ")
        # Expected outputs: "<p>test_insert_1 Hello World</p>"
        self.assertEqual("<p>test_insert_0 Hello World</p>", str(Soup.p))
        
        # 2.Insert "test_insert_2" in the 2 position of the content <p> tag;
        tag.insert(2,"test_insert_2 ")
        # Expected outputs: "<p>test_insert_0 test_insert_2 Hello World</p>"
        self.assertEqual("<p>test_insert_0 test_insert_2 Hello World</p>", str(Soup.p))
        
        # 3.Insert "<p>"  in the 3 position of the content <p> tag;
        tag.insert(3,"<p>")
        # Expected outputs: "<p>Hello World test_insert_1 test_insert_2&lt;p&gt;</p>"
        self.assertEqual("<p>test_insert_1 test_insert_2 Hello World&lt;p&gt;</p>", str(Soup.p))
        
    # This function is similar to the .append() function, except that it can add multiple new elements at the end of the parent node's .contents property.
    def test_expend(self): 
        Soup = self.soup()
        # 1.Insert array [" ", "test_expend_1", "?"] after the content of the <p> tag;
        extend_text_1 = [" ", "test_expend_1", "?"]
        Soup.p.extend(extend_text_1)
        # Expected: "<p>Hello World test_expend_1?</p>"
        self.assertEqual("<p>Hello World test_expend_1?</p>", str(Soup.p))
        # 2.Insert array [" ", "test_expend_2", "!"] after the content of the <p> tag;
        extend_text_2 = [" ", "test_expend_2", "!"]
        Soup.p.extend(extend_text_2)
        # Expected: "<p>Hello World test_expend_1? test_expend_2!</p>"
        self.assertEqual("<p>Hello World test_expend_1? test_expend_2!</p>", str(Soup.p))
        # 3.Insert array ["<", "test_expend_3", ">"] after the content of the <p> tag;
        extend_text_3 = ["<", "test_expend_3", ">"]
        Soup.p.extend(extend_text_3)
        # Expected: "<p>Hello World test_expend_1? test_expend_2!&lt;test_expend_3&gt;</p>"
        self.assertEqual("<p>Hello World test_expend_1? test_expend_2!&lt;test_expend_3&gt;</p>", str(Soup.p))
        
    # This function inserts tags or strings immediately before something else in the parse tree
    def test_insert_before(self):
        Soup = self.soup()
        alex_tag = Soup.find("p")
        # 1.Insert "test_insert_before_1" before the <p> tag;
        alex_tag.insert_before("test_insert_before_1 ")
        # Expected: "test_insert_before_1 <p>Hello World</p>"
        self.assertEqual("<div>test_insert_before_1 <p>Hello World</p></div>", str(Soup.div))
        # 2.Insert "test_insert_before_2" before the <p> tag;
        alex_tag.insert_before("test_insert_before_2 ")
        # Expected: "test_insert_before_1 test_insert_before_2 <p>Hello World</p>"
        self.assertEqual("<div>test_insert_before_1 test_insert_before_2 <p>Hello World</p></div>", str(Soup.div))
        # 3.Insert "< >" before the <p> tag;
        alex_tag.insert_before("< >")
        # Expected: "test_insert_before_1 test_insert_before_2 &lt; &gt;<p>Hello World</p>"
        self.assertEqual("<div>test_insert_before_1 test_insert_before_2 &lt; &gt;<p>Hello World</p></div>", str(Soup.div))

    # This function inserts tags or strings immediately following something else in the parse tree
    def test_insert_after(self):
        Soup = self.soup()
        alex_tag = Soup.find("p")
        # 1.Insert "test_insert_before_1" after the <p> tag;
        alex_tag.insert_after(" test_insert_after_1")
        # Expected: "<p>Hello World</p> test_insert_after_1"
        self.assertEqual("<div><p>Hello World</p> test_insert_after_1</div>", str(Soup.div))
        # 2.Insert "test_insert_after_2" after the <p> tag;
        alex_tag.insert_after(" test_insert_after_2")
        # Expected: "<p>Hello World</p> test_insert_after_2 test_insert_after_1"
        self.assertEqual("<div><p>Hello World</p> test_insert_after_2 test_insert_after_1</div>", str(Soup.div))
        # 3.Insert "< >" after the <p> tag;
        alex_tag.insert_after("< >")
        # Expected: "<p>Hello World</p>&lt; &gt; test_insert_after_2 test_insert_after_1"
        self.assertEqual("<div><p>Hello World</p>&lt; &gt; test_insert_after_2 test_insert_after_1</div>", str(Soup.div))


    # Whitebox Testing
    # # This function is similar to the .append() function, except that it does not add a new element to the end of the parent node's .contents property, but inserts the element at the specified position.
    def test_insert(self):
        Soup = self.soup()
        tag = Soup.find(class_="test_insert")
        
        # Test that the insertion position is in the middle of the string
        tag.insert(0,"test_insert_0 ")
        self.assertEqual('<div class="test_insert">test_insert_0 <p> Hello World </p> Hello World </div>', str(tag))
                
        Soup = self.soup()
        tag = Soup.find(class_="test_insert")
        # Test the case where the insertion position exceeds the length of the string, and there are escape characters in the inserted string
        tag.insert(10,' <p> test_insert_10  & "&" </p> &lt;p&gt;')
        self.assertEqual('<div class="test_insert"><p> Hello World </p> Hello World  &lt;p&gt; test_insert_10  &amp; "&amp;" &lt;/p&gt; &amp;lt;p&amp;gt;</div>', str(tag))
        self.assertEqual(' Hello World  Hello World  <p> test_insert_10  & "&" </p> &lt;p&gt;', tag.text)

        Soup = self.soup()
        tag = Soup.find(class_="test_insert")
        # If the insert position is negative, the function will throw an exception
        # tag.insert(-10,' test_insert_-10 ')
        try:
            tag.insert(-10,' test_insert_-10 ')
        except:
            # Throws an exception, this test passes
            self.assertEqual(1,1)
        else:
            # No exception was thrown, this test failed
            self.assertEqual(1,0)
                
        
        
if __name__ == '__main__':
    unittest.main()