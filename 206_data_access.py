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

State_urllst = [] # Creates variable for all the url lists
Homepage_links = Homepage_Soup.find_all("li") #Makes a list of all link tag related html
test_f = open("Homepage_links4.txt",'w', encoding = "utf-8")
# for link in Homepage_links[4:60]:
	# test_f.write(str(link.contents[0].attrs["href"])+"\n")#test_f.write(str(Homepage_links)+"\n")

#List Comp which creates a list of url for each state's page	
[State_urllst.append(("https://www.nps.gov" + link.contents[0].attrs["href"], link.text)) for link in Homepage_links[4:60] ]


#Per code writing tests
# A_state = GetWebPage_Data(State_urllst[0][0])
# A_state_soup = BeautifulSoup(A_state,"html.parser")
# A_state_Search = A_state_soup.find_all("p")
# for item in A_state_Search:
# 	#if "a href" in str(item.contents):
# 	test_f.write(str(item.text)+"\n")#test_f.write(str(Homepage_links)+"\n")

# #test_f.write(str(A_state_Search))
# test_f.close()


	

#Create the constructor portion of the NationalPark class
class NationalPark:
	def __init__(self, url):
		self.state_webdata = GetWebPage_Data(url[0])
		self.Location = url[1]
		self.NationalPark_names =[]
		self.NationalPark_description = []
		
		state_webdata_soup = BeautifulSoup(self.state_webdata,"html.parser")
		MonumentorPark_h3data = state_webdata_soup.find_all("h3")
		for h3 in MonumentorPark_h3data:
			if "a href" in str(h3.contents):
				self.NationalPark_names.append(h3.text)

		MonumentorPark_desc = state_webdata_soup.find_all("p")
		for desc in MonumentorPark_desc:
			self.NationalPark_description.append(desc.text)#test_f.write(str(Homepage_links)+"\n")

#Create methods which will allow you to access the national parks data

	def Get_Location(self): # Method which returns person to get the location of related parks
		return self.Location

	def Get_Available_National_Parks(self):#Method returns a list of tuples with each available park name, state that its located in, and description
		all_park_info =[]
		i = 0
		for item in self.NationalPark_names:
			all_park_info.append((item,self.NationalPark_description[i],self.Location))
			i = i + 1
			return all_park_info
#Create an instance of national class and get a list of available parks

#A Created NationalPark class
That_states_Parks = NationalPark(State_urllst[0])

#Calls a method of the National Park that assigns the list of tuples with the park info to Alabama_Park_Info
The_Park_Info = That_states_Parks.Get_Available_National_Parks()
#Create code to set up database connection, cursor as well as the table
#(database will be called Final_Project.db) 
connection_FP = sqlite3.connect('Final_Project.db') #Sets up database and  its connection
FP_cur = connection_FP.cursor() #Sets up the cursor

try: #Drops the associated tables from the database if there (deletes it)
	FP_cur.execute("DROP TABLE IF EXISTS Parks") 
	connection_FP.commit()

	FP_cur.execute("DROP TABLE IF EXISTS States")
	connection_FP.commit()

	FP_cur.execute("DROP TABLE IF EXISTS Articles")
	connection_FP.commit()

except: #If Table don't exist nothing happens
	pass 

#Creates the tables Parks,States, and Article
creation_statement = "CREATE TABLE IF NOT EXISTS " 
creation_statement += "Parks (Park_id DEFAULT INTEGER PRIMARY KEY, Park_Name TEXT, State TEXT, Description TEXT)"
FP_cur.execute(creation_statement)
connection_FP.commit()

#creation_statement = "CREATE TABLE IF NOT EXISTS " 
#creation_statement += "Users (user_id INTEGER PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT )"
#p3DB_cur.execute(creation_statement)
#connection_p3DB.commit()

#test_f = open("Homepage_links5.txt",'w', encoding = "utf-8")


#Write code to insert values into the table

#The sequence that will be used for inserting values
insert_sql = 'INSERT INTO Tweets VALUES (?, ?, ?, ?)'

#the code that actually nserts the value
for item in The_Park_Info:
	Loc = item[2]
	Nam = item[0]
	Descip = item[1]
	FPcur.execute(insert_sql, (NONE, Nam, Loc, Descip))
	connection_FP.commit()

#Closes database so its not locked
FP_cur.close()




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