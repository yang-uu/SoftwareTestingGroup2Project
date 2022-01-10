# coding: utf-8

import unittest
from bs4 import BeautifulSoup


class BS4Test(unittest.TestCase):
    @staticmethod
    def soup1(*args, **kwargs):
        # Common document used by all black box testing.
        return BeautifulSoup("""
            <html>
              <body>
                <nochild></nochild>
                <onechild><child></child></onechild>
                <twochildren><child1></child1><child2></child2></twochildren>
                <grandchildren><withchild>a</withchild><withchild2>b</withchild2></grandchildren>
                <a id="34df9e" class="class-a class-b" rel="nofollow"></a>
              </body>
            </html>
        """, "html.parser", *args, **kwargs)

    # get all parents of a tag
    def test_parents(self):
        soup = self.soup1()
        # when the tag is the root of the document
        self.assertEqual(list(soup.html.parents), [soup])
        # when the tag has parents
        self.assertEqual(list(soup.nochild.parents), [soup.body, soup.html, soup])
        # when the tag is the document itself
        self.assertEqual(list(soup.parents), [])

    # get the index of a tag in its parent
    def test_index(self):
        soup = self.soup1()
        # when the parameter tag is a child of the tag
        self.assertEqual(soup.body.index(soup.nochild), 1)
        # when it is not
        with self.assertRaises(ValueError):
            soup.body.index(soup.withchild)

    # get all descendants of a tag
    def test_descendants(self):
        soup = self.soup1()
        # when the tag has no children
        self.assertEqual(list(soup.nochild.descendants), [])
        # when the tag has one child and no grandchildren
        onechild = soup.onechild
        self.assertEqual(list(onechild.descendants), [onechild.child])
        # when the tag has two children and no grandchildren
        twochildren = soup.twochildren
        self.assertEqual(list(twochildren.descendants), [twochildren.child1, twochildren.child2])
        # when the tag has grandchildren
        grandchildren = soup.grandchildren
        self.assertEqual(list(grandchildren.descendants), [grandchildren.withchild, grandchildren.withchild.string, grandchildren.withchild2, grandchildren.withchild2.string])

    # check if a tag has an attribute
    def test_has_attr(self):
        tag = self.soup1().a
        # the tag has the attribute
        self.assertTrue(tag.has_attr("class"))
        # the tag does not have the attribute
        self.assertFalse(tag.has_attr("no-attr"))

    # get an attribute of a tag
    def test_get(self):
        tag = self.soup1().a
        # the tag does not have the attribute
        self.assertEqual(tag.get("no-attr", None), None)
        # the tag does not have the attribute, but there is a default value
        self.assertEqual(tag.get("no-attr", []), [])
        # single-valued attribute
        self.assertEqual(tag.get("id"), "34df9e")
        # multi-valued attribute, but the tag only has one of the attribute
        self.assertEqual(tag.get("rel"), ["nofollow"])
        # mnulti-valued attribute, the tag has two of the attribute
        self.assertEqual(tag.get("class"), ["class-a", "class-b"])
        tag = self.soup1(multi_valued_attributes=None).a
        # similar to 4, but `multi_valued_attributes` set to `None`
        self.assertEqual(tag.get("rel"), "nofollow")
        # similar to 5, but `multi_valued_attributes` set to `None`
        self.assertEqual(tag.get("class"), " ".join(["class-a", "class-b"]))

    # white box testing
    def test_clear(self):
        none_tag = BeautifulSoup("<a></a>", "html.parser")
        none_tag.name = none_tag.attrs = None
        none_tag.contents = []

        # two test cases for node and branch coverage
        # decompose=True, `tag` has two children, the first is a `Tag` object and the second is not
        soup = BeautifulSoup("<div><a></a>text</div>", "html.parser")
        tag = soup.div
        tag_children = [tag.a]
        tag.clear(True)
        self.assertEqual(list(tag.children), [])
        for c in tag_children:
            self.assertEqual(c, none_tag)

        # decompose=False, `tag` has two children
        soup = BeautifulSoup("<div><a></a>text</div>", "html.parser")
        tag = soup.div
        tag.clear(False)
        self.assertEqual(list(tag.children), [])

        # test cases for prime paths
        # decompose=True, `tag` has one child, which is a `Tag` object
        soup = BeautifulSoup("<div><a></a></div>", "html.parser")
        tag = soup.div
        tag_children = [tag.a]
        tag.clear(True)
        self.assertEqual(list(tag.children), [])
        for c in tag_children:
            self.assertEqual(c, none_tag)

        # decompose=True, `tag` has one child, which is not a `Tag` object
        soup = BeautifulSoup("<div>text</div>", "html.parser")
        tag = soup.div
        tag.clear(True)
        self.assertEqual(list(tag.children), [])

        # decompose=False, `tag` has one child
        soup = BeautifulSoup("<div>text</div>", "html.parser")
        tag = soup.div
        tag.clear(False)
        self.assertEqual(list(tag.children), [])

        # decompose=True, `tag` has five children, the first, the second and the fifth are a `Tag` object and the others are not
        soup = BeautifulSoup("<div><a></a><b></b>c<e></e></div>", "html.parser")
        tag = soup.div
        tag.insert(3, "d")
        tag_children = [tag.a, tag.b, tag.e]
        tag.clear(True)
        self.assertEqual(list(tag.children), [])
        for c in tag_children:
            self.assertEqual(c, none_tag)
