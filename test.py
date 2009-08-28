#! /usr/bin/python

import anglosaxon
import unittest, doctest

class OptionsKnownValues(unittest.TestCase):
    knownValues = (
        ("", {}, {}),
        ("-s mynode -v attr", {'mynode': [('-v', 'attr')]}, {}),
        ("-s mynode -o node(id= -v id -o )", {'mynode': [('-o', 'node(id='), ('-v', 'id'), ('-o', ')')]}, {}),
        ("-s mynode -o node( -e mynode -o )node", {'mynode': [('-o', 'node(')]}, {'mynode': [('-o', ')node')]}),
        ("-s mynode -o node( -o id= -v id --nl -e mynode -o )node",
            {'mynode': [('-o', 'node('), ('-o', 'id='), ('-v', 'id'), ('-o', '\n')]}, 
            {'mynode': [('-o', ')node')]} ),
        ("-s mynode -o node( -o id= -v id --nl -e mynode -o )node --nl",
            {'mynode': [('-o', 'node('), ('-o', 'id='), ('-v', 'id'), ('-o', '\n')]}, 
            {'mynode': [('-o', ')node'), ('-o', '\n')]} ),

    )

    def testKnownValues(self):
        for input, expected_start_functions, expected_end_functions in self.knownValues:
            actual_start_functions, actual_end_functions = anglosaxon.parse_options(input.split(" "))
            self.assertEqual(expected_start_functions, actual_start_functions)
            self.assertEqual(expected_end_functions, actual_end_functions)

class InvalidOptions(unittest.TestCase):
    def test_o_needs_something_before(self):
        self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-o foo".split(" "))
        anglosaxon.parse_options("-s node -o foo".split(" "))

    def test_o_need_an_option(self):
        self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-s node -o".split(" "))
        anglosaxon.parse_options("-s node -o foo".split(" "))

    def test_s_or_e_needs_an_option(self):
        self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-s".split(" "))
        self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-e".split(" "))
        #self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-s -o foo".split(" "))
        #self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-e -o foo".split(" "))

    def test_V_needs_an_option(self):
        self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-s node -V".split(" "))
        self.assertRaises(anglosaxon.AngloSaxonExceptionInvalidOptions, anglosaxon.parse_options, "-s node -V id".split(" "))
        anglosaxon.parse_options("-s node -V id NULL".split(" "))
        
class DocTests(unittest.TestCase):
    def testdoctests(self):
        doctest.testfile("doctests.txt")




if __name__ == "__main__":
    unittest.main()   
