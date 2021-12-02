# coding: utf-8

import unittest
from bs4 import BeautifulSoup


class BS4Test(unittest.TestCase):

    soup1 = BeautifulSoup("""
        <html>
          <body>
            <div>
              <div>
              </div>
            </div>
          </body>
        </html>
    """, "html.parser")

    def test_parents(self):
        tag_no_parents = self.soup1.html
        tag_parents = self.soup1.div
        not_a_tag = self.soup1
        self.assertEqual(list(tag_no_parents.parents), [self.soup1])
        self.assertEqual(list(tag_parents.parents), [self.soup1.body, self.soup1.html, self.soup1])
        self.assertEqual(list(not_a_tag.parents), [])
