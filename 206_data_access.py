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


#Set up code to create/open a cache:

CACHE_FNAME = "206_data_access_cache.txt" #Cache file's name
try: # Tries to open and read the cache file if it exists
	cache_file = open(CACHE_FNAME,'r', encoding = "utf-8")
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except: #If cache doesn't already exist will create a dictionary which will be the basis for the cache
	CACHE_DICTION = {}



#Create code for pulling webdata from the site/cache

def GetWebPage_Data(url):
	#Makes a connection from within the function to the variable CACHE_DICTION
	#and CACHE_FNAME outside the function.
	global CACHE_DICTION
	global CACHE_FNAME

	#If the passed url's info is already in the cache pull it and
	#save it to the variable webdata.
	if(str(url) in CACHE_DICTION):
		webdata = CACHE_DICTION[str(url)]

	#Else retrieve the data from the site, cache it, and save it to
	#the variable webdata	
	else:
		response = requests.get(str(url))
		htmldoc = response.text
		webdata = htmldoc
		CACHE_DICTION[str(url)] = webdata
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	#Return the data related to the url
	return webdata

# Make a list containing urls for each available state webpage
Homepage_htmldoc = GetWebPage_Data("https://www.nps.gov/index.htm") 
Homepage_Soup = BeautifulSoup(Homepage_htmldoc,"html.parser")
print(type(Homepage_Soup))

State_urllst = []
Homepage_links = Homepage_Soup.find_all("li")
test_f = open("Homepage_links3.txt",'w', encoding = "utf-8")
# for link in Homepage_links[4:60]:
	# test_f.write(str(link.contents[0].attrs["href"])+"\n")#test_f.write(str(Homepage_links)+"\n")
[State_urllst.append(link.contents[0].attrs["href"]) for link in Homepage_links[4:60] ]

test_f.write(str(State_urllst))
test_f.close






# Write your test cases here.
class Test_DictComprehension(unittest.TestCase):
	def check_is_dict(self):
		self.assertEqual(type(State_parkandmonument_dict), type({}))
	def check_num_keys(self):
		self.assertEqual(len(State_parkandmonument_dict.keys), 56)


class Test_lstcomprehension(unittest.TestCase):
	def check_is_lst(self):
		self.assertEqual(type(State_urllst), type([]))
	def check_num_list_items(self):
		self.assertEqual(len(State_urllist), 56)

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