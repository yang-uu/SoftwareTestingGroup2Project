# coding: utf-8

import unittest
from bs4 import BeautifulSoup


class BS4Test(unittest.TestCase):

    @staticmethod
    def soup1(*args, **kwargs):
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

    def test_parents(self):
        soup = self.soup1()
        self.assertEqual(list(soup.html.parents), [soup])
        self.assertEqual(list(soup.nochild.parents), [soup.body, soup.html, soup])
        self.assertEqual(list(soup.parents), [])

    def test_index(self):
        soup = self.soup1()
        self.assertEqual(soup.body.index(soup.nochild), 1)
        with self.assertRaises(ValueError):
            soup.body.index(soup.withchild)

    def test_descendants(self):
        soup = self.soup1()
        self.assertEqual(list(soup.nochild.descendants), [])
        onechild = soup.onechild
        self.assertEqual(list(onechild.descendants), [onechild.child])
        twochildren = soup.twochildren
        self.assertEqual(list(twochildren.descendants), [twochildren.child1, twochildren.child2])
        grandchildren = soup.grandchildren
        self.assertEqual(list(grandchildren.descendants), [grandchildren.withchild, grandchildren.withchild.string, grandchildren.withchild2, grandchildren.withchild2.string])

    def test_has_attr(self):
        tag = self.soup1().a
        self.assertTrue(tag.has_attr("class"))
        self.assertFalse(tag.has_attr("no-attr"))

    def test_get(self):
        tag = self.soup1().a
        self.assertEqual(tag.get("no-attr", None), None)
        self.assertEqual(tag.get("no-attr", []), [])
        self.assertEqual(tag.get("id"), "34df9e")
        self.assertEqual(tag.get("rel"), ["nofollow"])
        self.assertEqual(tag.get("class"), ["class-a", "class-b"])
        tag = self.soup1(multi_valued_attributes=None).a
        self.assertEqual(tag.get("rel"), "nofollow")
        self.assertEqual(tag.get("class"), " ".join(["class-a", "class-b"]))

    def test_clear(self):
        none_tag = BeautifulSoup("<a></a>", "html.parser")
        none_tag.name = none_tag.attrs = None
        none_tag.contents = []

        soup = BeautifulSoup("<div><a></a>text</div>", "html.parser")
        tag = soup.div
        tag_children = [tag.a]
        tag.clear(True)
        self.assertEqual(list(tag.children), [])
        for c in tag_children:
            self.assertEqual(c, none_tag)

        soup = BeautifulSoup("<div><a></a>text</div>", "html.parser")
        tag = soup.div
        tag.clear(False)
        self.assertEqual(list(tag.children), [])

        soup = BeautifulSoup("<div><a></a></div>", "html.parser")
        tag = soup.div
        tag_children = [tag.a]
        tag.clear(True)
        self.assertEqual(list(tag.children), [])
        for c in tag_children:
            self.assertEqual(c, none_tag)

        soup = BeautifulSoup("<div>text</div>", "html.parser")
        tag = soup.div
        tag.clear(True)
        self.assertEqual(list(tag.children), [])

        soup = BeautifulSoup("<div>text</div>", "html.parser")
        tag = soup.div
        tag.clear(False)
        self.assertEqual(list(tag.children), [])

        soup = BeautifulSoup("<div><a></a><b></b>c<e></e></div>", "html.parser")
        tag = soup.div
        tag.insert(3, "d")
        tag_children = [tag.a, tag.b, tag.e]
        tag.clear(True)
        self.assertEqual(list(tag.children), [])
        for c in tag_children:
            self.assertEqual(c, none_tag)
