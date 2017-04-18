## Your name: Kyle Durant
## The option you've chosen: Option 1

# Put import statements you expect to need here!
import requests
import json
import unittest
import itertools
import collections
import sqlite3
from bs4 import BeautifulSoup













# Write your test cases here.
class Test_DictComprehension(unittest.TestCase):
	def check_is_dict(self):
		self.assertEqual(type(State_parkandmonument_dict), type({}))
	def check_num_keys(self):
		self.assertEqual(len(State_parkandmonument_dict.keys), 56)


class Test_lstcomprehension(unittest.TestCase):
	def check_is_lst(self):
		self.assertEqual(type(State_parkandmonument_urllst), type([]))
	def check_num_list_items(self):
		self.assertEqual(len(State_parkandmonument_urllist), 56)

class Test_GetState_ParkandMonument_data(unittest.TestCase):
	def GetState_return_type(self):
		test_lst = []
		rooturl ='https://www.nps.gov/index.htm'
		returned_value = GetState_ParkandMonument_data(rooturl)
		self.assertEqual(type(returned_value), type(test_lst))
	def GetState_returnedvalues_contenttype(self):
		rooturl ='https://www.nps.gov/index.htm'
		returned_value = GetState_ParkandMonument_data(rooturl)
		self.assertEqual(type(returned_value[0]), type(" "))
	def GetState_returnedvalues_numcontent(self):
		rooturl ='https://www.nps.gov/index.htm'
		returned_value = GetState_ParkandMonument_data(rooturl)
		self.assertEqual(len(returned_value), 56)
	def GetState_returnedvalues_contentcheck(self):
		rooturl ='https://www.nps.gov/index.htm'
		returned_value = GetState_ParkandMonument_data(rooturl)
		correct_values =["https://www.nps.gov/state//al/index.htm","https://www.nps.gov/state//ak/index.htm,""https://www.nps.gov/state//as/index.htm","https://www.nps.gov/state//az/index.htm","https://www.nps.gov/state//ar/index.htm","https://www.nps.gov/state//ca/index.htm","https://www.nps.gov/state//co/index.htm","https://www.nps.gov/state//ct/index.htm","https://www.nps.gov/state//de/index.htm","https://www.nps.gov/state//dc/index.htm","https://www.nps.gov/state//fl/index.htm","https://www.nps.gov/state//ga/index.htm","https://www.nps.gov/state//gu/index.htm","https://www.nps.gov/state//hi/index.htm","https://www.nps.gov/state//id/index.htm","https://www.nps.gov/state//il/index.htm","https://www.nps.gov/state//in/index.htm","https://www.nps.gov/state//ia/index.htm","https://www.nps.gov/state//ks/index.htm","https://www.nps.gov/state//ky/index.htm","https://www.nps.gov/state//la/index.htm","https://www.nps.gov/state//me/index.htm","https://www.nps.gov/state//md/index.htm","https://www.nps.gov/state//ma/index.htm","https://www.nps.gov/state//mi/index.htm","https://www.nps.gov/state//mn/index.htm","https://www.nps.gov/state//ms/index.htm","https://www.nps.gov/state//mo/index.htm","https://www.nps.gov/state//mt/index.htm","https://www.nps.gov/state//ne/index.htm","https://www.nps.gov/state//nv/index.htm","https://www.nps.gov/state//nh/index.htm","https://www.nps.gov/state//nj/index.htm","https://www.nps.gov/state//nm/index.htm","https://www.nps.gov/state//ny/index.htm","https://www.nps.gov/state//nc/index.htm","https://www.nps.gov/state//nd/index.htm","https://www.nps.gov/state//mp/index.htm","https://www.nps.gov/state//oh/index.htm","https://www.nps.gov/state//ok/index.htm","https://www.nps.gov/state//or/index.htm","https://www.nps.gov/state//pa/index.htm","https://www.nps.gov/state//pr/index.htm","https://www.nps.gov/state//ri/index.htm","https://www.nps.gov/state//sc/index.htm","https://www.nps.gov/state//sd/index.htm","https://www.nps.gov/state//tn/index.htm","https://www.nps.gov/state//tx/index.htm","https://www.nps.gov/state//ut/index.htm","https://www.nps.gov/state//vt/index.htm","https://www.nps.gov/state//vi/index.htm","https://www.nps.gov/state//va/index.htm","https://www.nps.gov/state//wa/index.htm","https://www.nps.gov/state//wv/index.htm","https://www.nps.gov/state//wi/index.htm","https://www.nps.gov/state//wy/index.htm",]
		self.assertEqual(returned_value, correct_values)

class Test_DictComprehension(unittest.TestCase):
	def check_is_dict(self):
		self.assertEqual(type(State_parkandmonument_dict), type({}))
	def check_num_keys(self):
		self.assertEqual(len(State_parkandmonument_dict.keys), 56)


class Test_lstcomprehension(unittest.TestCase):
	def check_is_lst(self):
		self.assertEqual(type(State_parkandmonument_urllst), type([]))
	def check_num_list_items(self):
		self.assertEqual(len(State_parkandmonument_urllist), 56)

## Remember to invoke all your tests...
unittest.main(verbosity=2)