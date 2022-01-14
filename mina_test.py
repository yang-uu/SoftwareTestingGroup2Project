import re
import unittest

from bs4 import BeautifulSoup


# This class is intended to test 5 following functionalities:
# smooth
# wrap
# unwrap
# extract
# find_all
# replace_with

class MyTestCase(unittest.TestCase):

    @staticmethod
    def MockSoup(*args, **kwargs):
        return BeautifulSoup("""
                <html><body><p>This paragraph has a section which is<b class="boldest">Extremely bold</b></p></body></html>
            """, "html.parser", *args, **kwargs)

    # This function cleans up the parse tree by consolidating adjacent strings:
    # e.g.:
    # <b class="boldest">
    #  Extremely bold
    #  , an added part
    # </b>
    # To
    # <b class="boldest">
    #  Extremely bold, an added part
    # </b>
    def test_smooth(self):
        soup = self.MockSoup()
        soup.b.append(", an added part")

        self.assertNotEqual(soup.b.string, "Extremely bold, an added part")
        soup.smooth()
        self.assertEqual(soup.b.string, "Extremely bold, an added part")

    # this function would wrap an element in the desired tag and also returns a wrapper
    def test_wrap(self):
        soup = self.MockSoup()
        soup.p.wrap(soup.new_tag("div"))
        # check if there is an added <div> tag in the soup
        self.assertNotEqual(soup.find_all("div"), [])

    # this function would replace a tag with its content
    def test_unwrap(self):
        soup = self.MockSoup()
        soup.b.unwrap()
        # check if the unwrapped tag is removed from the soup
        self.assertEqual(soup.find_all("b"), [])

    # this function would extract a tag or string from the original tree and also return that removed part
    def test_extract(self):
        soup = self.MockSoup()
        tag_b = soup.b.extract()
        # check the extracted tag doesn't exist in the original soup anymore
        self.assertEqual(soup.find_all("b"), [])
        # check if the removed part is the one we've extracted
        self.assertEqual(tag_b.string, "Extremely bold")

    # this function will be used for searching the tree
    # there are some options that can be fed to this function as a filter:
    # String
    # regular expression
    # list
    # True
    def test_find_all(self):
        soup = self.MockSoup()
        # String filter
        result = soup.find_all('b')
        self.assertEqual(result.__str__(), '[<b class="boldest">Extremely bold</b>]')
        # regular expression
        result = soup.find_all(re.compile("^p"))
        self.assertEqual(result.__str__(), '[<p>This paragraph has a section which is<b class="boldest">Extremely '
                                           'bold</b></p>]')
        # list filter
        result = soup.find_all(["b", "p"])
        self.assertEqual(result.__str__(), '[<p>This paragraph has a section which is<b class="boldest">Extremely '
                                           'bold</b></p>, '
                                           '<b class="boldest">Extremely bold</b>]')
        # True filter (which outputs all the tags)
        result = soup.find_all(True)
        self.assertEqual(result.__str__(), '[<html><body><p>This paragraph has a section which is<b '
                                           'class="boldest">Extremely bold</b></p></body></html>, <body><p>This '
                                           'paragraph has a section which is<b class="boldest">Extremely '
                                           'bold</b></p></body>, <p>This paragraph has a section which is<b '
                                           'class="boldest">Extremely bold</b></p>, <b class="boldest">Extremely '
                                           'bold</b>]')

    # White Box Testing
    # this function would change the string/tag of a page element
    def test_replace_with(self):
        # test the functionality of changing the string
        soup = self.MockSoup()
        tag = soup.p
        tag.b.string.replace_with("still bold")
        self.assertEqual(tag.b.string, 'still bold')

        # test the functionality of changing the tag
        new_tag = soup.new_tag("i")
        new_tag.string = "No longer bold"
        tag.b.replace_with(new_tag)
        self.assertNotEqual(soup.find_all("i"), [])

        # test the functionality of replacing a tag with a list of new tags
        soup = self.MockSoup()
        tag = soup.p
        new_tag = soup.new_tag("i")
        new_tag2 = soup.new_tag("u")
        new_tag3 = soup.new_tag("p")
        new_tag4 = soup.new_tag("random")
        new_tag.string = "italic and underline!"
        tag.b.replace_with(new_tag, new_tag2, new_tag3, new_tag4)
        self.assertNotEqual(soup.find_all("i"), [])
        self.assertNotEqual(soup.find_all("u"), [])
        self.assertNotEqual(soup.find_all("p"), [])
        self.assertNotEqual(soup.find_all("random"), [])

        # test the functionality of replacing a tag with a list of new tags consisting 2 new tags
        soup = self.MockSoup()
        tag = soup.p
        new_tag = soup.new_tag("i")
        new_tag2 = soup.new_tag("u")
        new_tag.string = "italic and underline!"
        tag.b.replace_with(new_tag, new_tag2)
        self.assertNotEqual(soup.find_all("i"), [])
        self.assertNotEqual(soup.find_all("u"), [])

        # test the functionality of replacing a tag
        # with a list of new page elements including tags and strings
        soup = self.MockSoup()
        tag = soup.p
        new_tag = soup.new_tag("i")
        new_tag.string = "italic and underline!"
        tag.b.replace_with(new_tag, "Mina")
        self.assertNotEqual(soup.find_all("i"), [])

        # test the error handling, replace a tag which doesn't exist
        with self.assertRaises(Exception):
            tag.div.string.replace_with("error")

        # test the error handling, replace a tag which no args
        with self.assertRaises(Exception):
            tag.b.string.replace_with()

        # test the error handling, replace a tag with the same tag
        new_tag = soup.new_tag("b")
        new_tag.string = "the boldest!"
        with self.assertRaises(Exception):
            tag.b.replace_with(new_tag)

        # test the error handling, replace a tag with its parent
        soup = self.MockSoup()
        tag = soup.p
        new_tag.string = "italic and underline!"
        with self.assertRaises(Exception):
            tag.b.replace_with(tag)

        # test the error handling, replace a tag with the list of tags which one of them is its parent
        soup = self.MockSoup()
        tag = soup.p
        new_tag = soup.new_tag("i")
        new_tag.string = "italic!"
        with self.assertRaises(Exception):
            tag.b.replace_with(tag, new_tag)


if __name__ == '__main__':
    unittest.main()
