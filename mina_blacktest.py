import re
import unittest

from bs4 import BeautifulSoup


# This class is intended to test 5 following functionalities:
# replace_with
# wrap
# unwrap
# extract
# find_all

class MyTestCase(unittest.TestCase):

    @staticmethod
    def MockSoup(*args, **kwargs):
        return BeautifulSoup("""
                <html><body><p>This paragraph has a section which is<b class="boldest">Extremely bold</b></p></body></html>
            """, "html.parser", *args, **kwargs)

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
        self.assertNotEquals(soup.find_all("i"), [])

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


if __name__ == '__main__':
    unittest.main()
