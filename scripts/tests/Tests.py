"""
    Unit tests for scripts portion of app

    Author: Jake Poirier
    Date: 11/4/16
"""

import unittest
import os
from scripts.set_ip_adds import parse_nmap, run_nmap


class TestSetIPs(unittest.TestCase):

    def test_nmap(self):
        if os.name == "nt":
            self.assertEqual(1, 1)
        if os.name == "posix":
            self.assertEqual(run_nmap(), 1)

    def test_parse_nmap(self):
        self.assertEqual(parse_nmap(list='tests/iplist_test.txt'), ['192.168.42.15'])

    def test_parse_nmap_blank(self):
        self.assertEqual(parse_nmap(list='tests/iplist_testblank.txt'), [])

