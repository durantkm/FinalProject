## Your name: Kyle Durant
## The option you've chosen: Option 1

# Put import statements you expect to need here!
import requests
import json
import unittest
import itertools
import collections
import sqlite3
import random
from bs4 import BeautifulSoup

 #Name: Kyle Durant
#Set up code to create/open a cache:

CACHE_FNAME = "206_final_project_cache.txt" #Cache file's name
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


State_urllst = [] # Creates variable for all the state urls
Homepage_links = Homepage_Soup.find_all("li") #Makes a list of all 'li' tag related html

# Creates variable for all the article urls
Article_urllst = []
Homepage_article_links = Homepage_Soup.find_all("a") #Makes a list of all 'a tag related html


#List Comp which creates a list of url for each state's page	
[State_urllst.append(("https://www.nps.gov" + link.contents[0].attrs["href"], link.text)) for link in Homepage_links[4:60] ]

#List Comp which creates a list of url for each article's page	
[Article_urllst.append("https://www.nps.gov" + link.attrs["href"]) for link in Homepage_article_links[64:72] ]


#Create the constructor portion of the Articles class
class Article:
	def __init__(self,url):
		#Article classes instance variables
		self.article_webdata = GetWebPage_Data(url)
		self.articles_titles = []
		self.article_contents_list = []
		#Creates the html soup for the inst
		article_html_soup = BeautifulSoup(self.article_webdata,"html.parser")

		#Searches and returns title related text to be stored in the titles inst variables
		article_title_search_resp = article_html_soup.find_all("title")
		for item in article_title_search_resp:
			self.articles_titles.append(item.text)

		#Searches and returns article body text related text to be stored in the titles inst variables
		article_contents = article_html_soup.find_all("p")
		for item in article_contents:
			self.article_contents_list.append(item.text)
	#Returns main_title(the first associated title to the article) for the article
	def get_main_title(self):
		return self.articles_titles[0]
		#Returns all available titles associated with the articles
	def get_all_titles(self):
		return self.articles_titles
	#Returns  article body text snippets based on the specified amount default:all or optional
	#Numeric up to the available snippets of text
	def get_snippets(self, n=None):
		snippets = []
		if n==None:
			return self.article_contents_list
		else:
			if(n > (len(self.article_contents_list))):
				print("Error Requested More Snippets Than Available")
			else:
				while (i <= n):
					snippets.append(self.article_contents_list[i])
					i =+ 1

#Create the constructor portion of the NationalPark class
class NationalPark:
	def __init__(self, url):
		self.state_webdata = GetWebPage_Data(url[0])
		self.Location = url[1]
		self.NationalPark_names =[]
		self.NationalPark_description = []
		#Gets the names of Park associated with the given state
		state_webdata_soup = BeautifulSoup(self.state_webdata,"html.parser")
		MonumentorPark_h3data = state_webdata_soup.find_all("h3")
		for h3 in MonumentorPark_h3data:
			if "a href" in str(h3.contents):
				self.NationalPark_names.append(h3.text)

		# Gets the Parks' descriptions
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
			all_park_info.append((item,self.NationalPark_description[i]))
			i = i + 1
		return all_park_info

#Create code to set up database connection, cursor as well as the table
#(database will be called Final_Project.db) 
connection_FP = sqlite3.connect('Final_Project.db') #Sets up database and  its connection
FP_cur = connection_FP.cursor() #Sets up the cursor

try: #Drops the associated tables from the database if there (deletes it)
	FP_cur.execute("DROP TABLE IF EXISTS Parks") 
	connection_FP.commit()
except: #If Table don't exist nothing happens
	pass 

try:
	FP_cur.execute("DROP TABLE IF EXISTS States")
	connection_FP.commit()
except:
	pass

try:
	FP_cur.execute("DROP TABLE IF EXISTS Articles")
	connection_FP.commit()
except:
	pass

#Creates the tables Parks,States, and Articles
creation_statement = "CREATE TABLE IF NOT EXISTS " 
creation_statement += "Parks (Park_id DEFAULT INTEGER PRIMARY KEY, Park_Name TEXT, State TEXT, Description TEXT)"
FP_cur.execute(creation_statement)
connection_FP.commit()

creation_statement2 = "CREATE TABLE IF NOT EXISTS " 
creation_statement2 += "States (State_id INTEGER PRIMARY KEY, State TEXT, Avg_Temp_Fahrenheit INTEGER, Avg_Temp_Celsius INTEGER, Temp_Rank INTEGER)"
FP_cur.execute(creation_statement2)
connection_FP.commit()

creation_statement3 = "CREATE TABLE IF NOT EXISTS " 
creation_statement3 += "Articles (Article_id INTEGER PRIMARY KEY, Article_Main_Title TEXT, Article_All_Associated__Titles TEXT, Article_Text TEXT)"
FP_cur.execute(creation_statement3)
connection_FP.commit()



#Write code to insert values into the table	

def save_park_info(National_Park_inst):
	#Calls a method of the National Park that assigns the list of tuples with the park info to Alabama_Park_Info
	The_Park_Info = National_Park_inst.Get_Available_National_Parks()
	#The sequence that will be used for inserting values
	insert_sql = 'INSERT INTO Parks VALUES (?, ?, ?, ?)'
	outcomes = []
	#the code that actually inserts the value
	#test_f.write(str(The_Park_Info))
	for item in The_Park_Info:
		#Creates random number to be used as park id
		Park_id = random.randrange(1,1000000)
		#Holds state that the park is located in
		Loc = National_Park_inst.Get_Location()
		#holds park description
		Nam = item[0].replace(" ", "_")   #Issuehappens here
		# holds park description
		Descip = item[1]

		FP_cur.execute(insert_sql, (Park_id, Nam, Loc, Descip))
		connection_FP.commit()
		outcomes.append((Park_id, Nam, Loc, Descip))
	return outcomes

def save_state_tempinfos(func_input='https://www.currentresults.com/Weather/US/average-annual-state-temperatures.php'):
	state_tempdata_htmldoc = GetWebPage_Data(func_input)
	state_tempdata_soup = BeautifulSoup(state_tempdata_htmldoc,"html.parser")
	state_tempdata = state_tempdata_soup.find_all('td')
	i=0
	x=0
	#The sequence that will be used for inserting values
	insert_sql = 'INSERT INTO States VALUES (?, ?, ?, ?, ?)'
	select_search_response = []
	# The sequence for selecting the Park if present in table
	select_sql = "SELECT State FROM States"
	state = []
	temp_f = []
	temp_c = []
	rank = []
	for item in state_tempdata:
		if(i == 0):# Grabs state name
			state.append(item.text)
			i = i + 1
		elif(i == 1):#Grabs fahrenheit tem
			temp_f.append(item.text)
			i = i + 1
		elif(i == 2):#Grabs Celsius Temp
			temp_c.append(item.text)
			i = i + 1
		elif(i == 3):#Grabs Temp Rank
			rank.append(item.text)
			i = i + 1

		if(i == 4):
			i=0
	for item in state:
		FP_cur.execute(select_sql)
		#Executes a select statement
		for row in FP_cur:
			select_search_response.append(row)
		if item not in select_search_response:# IF there isn't even one when it tries to select Then do the insert statement.

			#Inserts the info into the database
			FP_cur.execute(insert_sql, (x, item, temp_f[x], temp_c[x], rank[x]))
			connection_FP.commit()
			x = x + 1
		else:
			x = x + 1
	return((state,temp_f,temp_c,rank))

def save_article_info(Article_inst):
	Article_id = random.randrange(1,1000000)
	The_article_main_title = Article_inst.get_main_title()
	The_article_all_titles = ""
	#Creates one long string with the articles related titles
	for item in Article_inst.get_all_titles():
		item = item + "\n"
		The_article_all_titles += item

	##Creates one long string with the articles related content
	The_articles_contents = ""
	for item in Article_inst.get_snippets():
		The_articles_contents += item
	#Article_id INTEGER PRIMARY KEY, Article_Main_Title TEXT, Article_All_Associated__Titles TEXT, Article_Text TEXT
	insert_sql = 'INSERT INTO Articles VALUES (?, ?, ?, ?)'

	#Inserts info into database
	FP_cur.execute(insert_sql, (Article_id, The_article_main_title, The_article_all_titles, The_articles_contents))
	connection_FP.commit()
	return((Article_id, The_article_main_title, The_article_all_titles, The_articles_contents))


#Create an instance of national class and get a list of available parks

# #Passes state urls to the NationalPark class to be used to create inst of National_Park and initiate load into database
for states_page in State_urllst:
 	That_states_Parks = NationalPark(states_page)
 	save_park_info(That_states_Parks)

save_state_tempinfos()
# #Passes article urls to the Articles class to be used to create inst of Article and initiate load into database
for article_url in Article_urllst:
	That_Article_Inst = Article(article_url)
	save_article_info(That_Article_Inst)
# test_f.write(str(article_contents_list)




# #Beginning of Query Section
#Creates the programs output file
Output_File = open("Info_Regarding_NPG",'w', encoding = "utf-8")

#Creates the necessary variables for the queries below
Park_and_temps = []

#Query segment that will get and print to file the top 5 ranking states
State_Temp_Top_Query = "SELECT * FROM States WHERE Temp_Rank <= 1"


FP_cur.execute(State_Temp_Top_Query)
Output_File.write("According to collected data here's the top rated state temp wise:\n")
for row in FP_cur:
	Output_File.write(str(row[1]) +"\n")
###########################################################################################################################
#Query Segment to get Parks that would have a avg_temp of 70 or above in farhrenheit
Best_Park_Temp_Query = "SELECT Parks.Park_Name, States.Avg_Temp_Fahrenheit FROM Parks INNER JOIN States on Parks.State = States.State WHERE Avg_Temp_Fahrenheit >= 70"


FP_cur.execute(Best_Park_Temp_Query)

[ Park_and_temps.append(row) for row in FP_cur ]
#######################################################################################################################
#Query Segment to get Parks that would have a avg_temp of 32 or below in farhrenheit
Best_Snow_Park_Chance_Temp_Query = "SELECT Parks.Park_Name, States.Avg_Temp_Fahrenheit FROM Parks INNER JOIN States on Parks.State = States.State WHERE Avg_Temp_Fahrenheit <= 32"

FP_cur.execute(Best_Snow_Park_Chance_Temp_Query)

[ Park_and_temps.append(row) for row in FP_cur ]

Park_and_Temps_dict = collections.defaultdict(list)

for k,v in Park_and_temps:
	Park_and_Temps_dict[k].append(v)
################################################################################################################ 

#Writes to the output file the information for the previous two join requests
#(I noticed that the list icon appears with th numbers representing temps but left them be because I felt they looked nice)
Output_File.write("Howdy, according to collected data here's a list of Parks \nwith an Awesome temperature range(70-Above Best For Warm Weather while 32-Below Best For Snowy Weather):\n")
for a,b in Park_and_Temps_dict.items():
	Output_File.write("Park: "+ str(a) + "\n"+ "Avg_Temp: "+ str(b) + "\n\n")




# # Write your test cases here.

print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class Test_GetWebPage_Data(unittest.TestCase):
	def GetWebPage_Data_returns_response(self):
		returned_webdata = GetWebPage_Data('https://www.nps.gov/index.htm')
		self.assertEqual(returned_webdata, """<!doctype html> <html lang=\"en\"  class=\"no-js\"> <!-- Content Copyright National Park Service -->\n<!-- JavaScript & DHTML Code Copyright © 1998-2016, PaperThin, Inc. All Rights Reserved. --> <head> <meta content=\"IE=edge\" http-equiv=\"X-UA-Compatible\"> <title>Mississippi (U.S. National Park Service)</title> <script>\nvar jsDlgLoader = '/state/ms/loader.cfm';\nvar jsSiteResourceLoader = '/cs-resources.cfm?r=';\nvar jsSiteResourceSettings = {canCombine: false, canMinify: false};\n</script>\n<!-- beg (1) PrimaryResources -->\n<script type=\"text/javascript\" src=\"/ADF/thirdParty/jquery/jquery-1.12.js\"></script><script type=\"text/javascript\" src=\"/commonspot/javascript/browser-all.js\"></script>\n<!-- end (1) PrimaryResources -->\n<!-- beg (2) SecondaryResources -->\n<!-- end (2) SecondaryResources -->\n<!-- beg (3) StyleTags -->\n<!-- end (3) StyleTags -->\n<!-- beg (4) JavaScript -->\n<script type=\"text/javascript\">\n<!--\nvar gMenuControlID = 0;\nvar menus_included = 0;\nvar jsSiteID = 1;\nvar jsSubSiteID = 30169;\nvar js_gvPageID = 4085673;\nvar jsPageID = 4085673;\nvar jsPageSetID = 0;\nvar jsPageType = 0; var jsSiteSecurityCreateControls = 0;\nvar jsShowRejectForApprover = 1;\n// -->\n</script><script>\nvar jsDlgLoader = '/state/ms/loader.cfm';\nvar jsSiteResourceLoader = '/cs-resources.cfm?r=';\nvar jsSiteResourceSettings = {canCombine: false, canMinify: false};\n</script>\n<!-- end (4) JavaScript -->\n<!-- beg (5) CustomHead -->\n<meta charset=\"utf-8\">\n<link href=\"/common/commonspot/templates/images/icons/favicon.ico\" rel=\"shortcut icon\">\n<meta name=\"description\" content=\"Mississippi\">\n<meta http-equiv=\"Pragma\" content=\"no-cache\" />\n<meta http-equiv=\"Expires\" content=\"0\" />\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<!--[if gt IE 8]>\n<script src=\"/common/commonspot/templates/assetsCT/javascripts/app.early.min.js?v=3hto-103g2dv\"></script>\n<link href=\"/common/commonspot/templates/assetsCT/stylesheets/css/split-css/main.min.css?v=2rpz-n03cpj\" media=\"screen, print\" rel=\"stylesheet\">\n<link href=\"/common/commonspot/templates/assetsCT/stylesheets/css/split-css/main-min-blessed1.css\" media=\"screen, print\" rel=\"stylesheet\">\n<![endif]-->\n<!--[if lt IE 9]>\n<script src=\"https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js\"></script>\n<script src=\"https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js\"></script>\n<script src=\"/common/commonspot/templates/assetsCT/javascripts/app.early.min.js?v=3hto-103g2dv\"></script>\n<link href=\"/common/commonspot/templates/assetsCT/stylesheets/css/split-css/main.min.css?v=2rpz-n03cpj\" media=\"screen, print\" rel=\"stylesheet\">\n<link href=\"/common/commonspot/templates/assetsCT/stylesheets/css/split-css/main-min-blessed1.css\" media=\"screen, print\" rel=\"stylesheet\">\n<![endif]-->\n<!--[if !IE]> -->\n<script src=\"/common/commonspot/templates/assetsCT/javascripts/app.early.min.js?v=3hto-103g2dv\"></script>\n<link href=\"/common/commonspot/templates/assetsCT/stylesheets/css/main.min.css?v=6sid-1hts5t9\" media=\"screen, print\" rel=\"stylesheet\">\n<!-- <![endif]-->\n<link href=\"/common/commonspot/templates/assets/css/statePage.css\" rel=\"stylesheet\">\n<link href=\"/common/commonspot/templates/assetsCT/ctExtraStyles.css\" media=\"screen, print\" rel=\"stylesheet\">\n<link href='//fonts.googleapis.com/css?family=Open+Sans:700,600,400|Open+Sans+Condensed:300,700' rel='stylesheet' type='text/css'>\n<link href=\"/common/commonspot/templates/assets/css/redesign.css\" media=\"screen, print\" rel=\"stylesheet\">\n<style>\ntable#cs_idLayout2,\ntable#cs_idLayout2 > tbody,\ntable#cs_idLayout2 > tbody > tr,\ntable#cs_idLayout2 > tbody > tr >  td\n{\ndisplay: block;\nborder-collapse:separate;\n}\n</style>\n<script src='/common/commonspot/templates/js/federated-analytics-uav1.js?ver=true&agency=DOI&subagency=NPS&exts=rtf,odt,ods,odp&dclink=true&enhlink=true' id='_fed_an_ua_tag'></script>\n<!-- end (5) CustomHead -->\n<!-- beg (6) TertiaryResources -->\n<!-- end (6) TertiaryResources -->\n<!-- beg (7) authormode_inlinestyles -->\n<link rel=\"stylesheet\" type=\"text/css\" href=\"/commonspot/commonspot.css\">\n<!-- end (7) authormode_inlinestyles -->\n\n                    <script>var w=window;if(w.performance||w.mozPerformance||w.msPerformance||w.webkitPerformance){var d=document;AKSB=w.AKSB||{},AKSB.q=AKSB.q||[],AKSB.mark=AKSB.mark||function(e,_){AKSB.q.push([\"mark\",e,_||(new Date).getTime()])},AKSB.measure=AKSB.measure||function(e,_,t){AKSB.q.push([\"measure\",e,_,t||(new Date).getTime()])},AKSB.done=AKSB.done||function(e){AKSB.q.push([\"done\",e])},AKSB.mark(\"firstbyte\",(new Date).getTime()),AKSB.prof={custid:\"328362\",ustr:\"\",originlat:\"0\",clientrtt:\"40\",ghostip:\"23.77.238.20\",ipv6:true,pct:\"10\",clientip:\"2602:306:cfce:9e00:cc7a:61cf:9d30:8380\",requestid:\"35b3d4f\",region:\"20257\",protocol:\"\",blver:13,akM:\"dscg\",akN:\"ae\",akTT:\"O\",akTX:\"1\",akTI:\"35b3d4f\",ai:\"201862\",ra:\"false\",pmgn:\"\",pmgi:\"\",pmp:\"\",qc:\"\"},function(e){var _=d.createElement(\"script\");_.async=\"async\",_.src=e;var t=d.getElementsByTagName(\"script\"),t=t[t.length-1];t.parentNode.insertBefore(_,t)}((\"https:\"===d.location.protocol?\"https:\":\"http:\")+\"//ds-aksb-a.akamaihd.net/aksb.min.js\")}</script>\n                    </head><body lang=\"en\" class=\"ParkSite\"><a name=\"__topdoc__\"></a><script type=\"text/javascript\">\n<!--\n// always-include-ie.js  Copyright 1998-2005 PaperThin, Inc. All rights reserved.\nbName = navigator.appName;\nbVer = parseInt(navigator.appVersion);\nvar bCanRollover=0\nif (bName == \"Netscape\")\n{\nif(bVer >= 3)\nbCanRollover=1;\n}\nelse if (bName == \"Microsoft Internet Explorer\")\n{\nif(bVer >= 4)\nbCanRollover=1;\n}\nfunction ImageSet(imgID,newTarget)\n{\nif (bCanRollover)\ndocument[imgID].src=newTarget;\n}\nfunction clearStatus()\n{\nwindow.status = \"\";\n}\nfunction setStatbar(statbar)\n{\n// #22793 - no-op because browsers don't honor the assignment\n//\tvar strStatbar=unescape(statbar);\n//\twindow.status=strStatbar;\n}\nfunction onLoadComplete()\n{\nif( menus_included == 1 )\ndocument.onmouseover = document_mouseover;\t// defined in menu_ie.js\n}\nfunction HandleLink(parentID,link,displaylink)\n{\n// links are in one of the following formats:\n// \t\tcpe_60_0,CP___PAGEID=100\n// \t\tCPNEWWIN:WindowName^params@CP___\n// \t\t\tCPNEWWIN:child^top=110:left=130:ww=140:hh=150:tb=1:loc=1:dir=0:stat=1:mb=1:sb=1:rs=1@CP___PAGEID=3811,Adv-Search-2,1\n// displaylink is the server relative URL or fully qualified URL\nwindowname = \"\";\nwindowparams = \"\";\n// \"CPNEWWIN:\" & NewWindowName & \"^\" & params & \"@\" & linkStruct.LinkURL;\npos = link.indexOf(\"CPNEWWIN:\");\nif (pos != -1)\n{\npos1 = link.indexOf (\"^\");\nwindowname = link.substring (pos+9, pos1);\npos2 = link.indexOf (\"@\");\nwindowparams = link.substring (pos1 + 1, pos2);\nlink = link.substring (pos2 + 1, link.length);\n}\nif( displaylink && displaylink != \"\" )\n{\nif (windowname == \"\")\nwindow.location = displaylink;\nelse\n{\nwindowparams = FormatWindowParams(windowparams);\nwindow.open (displaylink, windowname, windowparams);\n}\n}\nelse\n{\ntargetLink = link;\nif (link.indexOf (\"CP___\") != -1)\n{\nhttpPos = -1;\ncommaPos = link.indexOf(\",\");\nif (commaPos != -1)\n{\ntargetUrl = link.substr(commaPos + 1);\nif (targetUrl.indexOf(\"://\") != -1 || targetUrl.indexOf(\"/\") == 0)\n{\nhttpPos = commaPos + 1;\n}\n}\nif (httpPos != -1)\n{\ntargetLink = link.substr(httpPos);\ncommaPos = targetLink.indexOf(\",\");\nif (commaPos != -1)\ntargetLink = targetLink.substr(0, commaPos);\n}\nelse\ntargetLink = jsDlgLoader + \"?csModule=utilities/handle-link&thelink=\" + link;\nif (windowname == \"\")\nwindow.location = targetLink;\nelse\n{\nwindowparams = FormatWindowParams(windowparams);\nwindow.open (targetLink, windowname, windowparams);\n}\n}\nelse\n{\n//commaPos = link.indexOf(\",\");\n//if (commaPos != -1)\n//\tlink = link.substr(0, commaPos);\nif (windowname == \"\")\nwindow.location = link;\nelse\n{\nwindowparams = FormatWindowParams(windowparams);\nwindow.open (link, windowname, windowparams);\n}\n}\n}\n}\nfunction doWindowOpen(href,name,params)\n{\nif (params != '')\nwindow.open (href, name, params);\nelse\nwindow.open (href, name);\n}\n// \tCPNEWWIN:child^top=110:left=130:ww=140:hh=150:tb=1:loc=1:dir=0:stat=1:mb=1:sb=1:rs=1@CP___PAGEID=3811,Adv-Search-2,1\nfunction FormatWindowParams(windowparams)\n{\nif( windowparams.indexOf(\":loc=\") != -1 || windowparams.indexOf(\":ww=\") != -1 || windowparams.indexOf(\":hh=\") != -1 ||\nwindowparams.indexOf(\":left=\") != -1 || windowparams.indexOf(\":top=\") != -1 )\n{\nwindowparams = substringReplace(windowparams,':left=',',left=');\nwindowparams = substringReplace(windowparams,'left=','left=');\nwindowparams = substringReplace(windowparams,':ww=',',width=');\nwindowparams = substringReplace(windowparams,'ww=','width=');\nwindowparams = substringReplace(windowparams,':hh=',',height=');\nwindowparams = substringReplace(windowparams,'hh=','height=');\nwindowparams = substringReplace(windowparams,':loc=',',location=');\nwindowparams = substringReplace(windowparams,'loc=','location=');\nwindowparams = substringReplace(windowparams,':dir=',',directories=');\nwindowparams = substringReplace(windowparams,'dir=','directories=');\nwindowparams = substringReplace(windowparams,':tb=',',toolbar=');\nwindowparams = substringReplace(windowparams,'tb=','toolbar=');\nwindowparams = substringReplace(windowparams,':stat=',',status=');\nwindowparams = substringReplace(windowparams,':mb=',',menubar=');\nwindowparams = substringReplace(windowparams,':sb=',',scrollbars=');\nwindowparams = substringReplace(windowparams,':rs=',',resizable=');\n}\nreturn windowparams;\n}\n// -->\n</script>\n<div class=\"skip-links\">\n<ul>\n<li><a href=\"#GlobalNav-toggle\">Skip to global NPS navigation</a></li>\n<li><a href=\"#ParkNavigation\">Skip to park navigation</a></li>\n<li><a href=\"#main\">Skip to main content</a></li>\n<li><a href=\"#ParkFooter\">Skip to park information</a></li>\n<li><a href=\"#GlobalFooter\">Skip to footer</a></li>\n</ul>\n</div>\n<!--googleoff: index-->\n<div class=\"GlobalHeader\">\n<div class=\"container relative\">\n<a class=\"GlobalHeader-homelink\"  href=\"/\" >\n<span class=\"GlobalHeader-logo hide-text\">National Park Service Logo</span>\n<span class=\"GlobalHeader-text\">National Park Service</span>\n</a>\n<div class=\"GlobalHeader-buttonRow row\">\n<div class=\"GlobalHeader-buttonContainer\">\n<div id=\"SearchHeader\" class=\"GlobalSearch\">\n<a id=\"footerSearchLink\" href=\"#site_search_footer\" class=\"GlobalSearch-footerLink js-scrollTo\">\n<i class=\"fa fa-search\"></i> <span class=\"visuallyhidden\">Search</span>\n</a>\n<form class=\"GlobalSearch-form\" id=\"globalSearchForm\" action=\"/search/index.htm\" method=\"GET\">\n<div class=\"GlobalSearch-inputGroup\">\n<input class=\"GlobalSearch-input\" type=\"text\" autocomplete=\"off\" id=\"site_search\" name=\"query\" placeholder=\"Keyword Search\">\n<button class=\"GlobalSearch-button GlobalSearch-submitButton btn-form btn-form-primary js-use-site-limit\" type=\"submit\">This Site</button>\n<button class=\"GlobalSearch-button GlobalSearch-secondaryButton btn-form btn-form-primary\" type=\"submit\">All NPS</button>\n<div id=\"search-suggestions\"></div>\n</div>\n<script type=\"text/template\" id=\"suggestionsTemplate\">\n<div class=\"GlobalSearch-suggestions\">\n<ul>\n{{ _.each(suggestions, function(suggestion) { }}\n<li><a href=\"{{{ url }}}{{{ suggestion }}}\">{{{ suggestion }}}</a></li>\n{{ }) }}\n</ul>\n</div>\n</script>\n</form>\n<label class=\"GlobalSearch-label js-toggle GlobalHeader-button\" for=\"site_search\">\n<button type=\"button\" class=\"js-toggle\" title=\"Global Search\">\n<i class=\"fa fa-search\"></i> Search\n</button>\n</label>\n</div>\n<h3 class=\"GlobalHeader-menuHeader js-collapser GlobalHeader-button\" style=\"display: block;\"\ndata-aria-controls=\"GlobalNav\"\ndata-class=\"GlobalHeader-menuButton\"\ndata-id=\"GlobalNav-toggle\"\ndata-text-active=\"<i class='fa fa-times'></i> Close<span class='visuallyhidden'> Menu</span>\"\ndata-text-inactive=\"<i class='fa fa-bars'></i> <span class='visuallyhidden'>Open </span>Menu\"\ndata-slide-speed=\"500\"\ndata-remove-header=\"true\"\n>\n<button class=\"js-collapser-button GlobalHeader-menuButton\" id=\"GlobalNav-toggle\" aria-expanded=\"false\">\n<i class=\"fa fa-bars\"></i>\n<span class=\"visuallyhidden\">Open </span>\nMenu\n</button>\n</h3>\n</div>\n</div>\n<nav id=\"GlobalNav-container\" class=\"row\" role=\"navigation\" aria-label=\"NPS Primary Navigation\" aria-labelledby=\"GlobalNav-toggle\" tabindex=\"-1\">\n<ul id=\"GlobalNav\" class=\"GlobalNav GlobalNav-lvl-1\">\n</ul> <!-- <ul id=\"GlobalNav\" class=\"GlobalNav GlobalNav-lvl-1\"> -->\n</nav>\n</div>\n</div>\n<!--googleon: index-->\n<script type=\"text/javascript\">\njQuery(document).ready(function() {\nsetTimeout( function() {\nNPS.display.showAdminTools( 0 );\n} ,10);\n});\n</script>\n<div id=\"main\" role=\"main\" class=\"MainContent\">\n<style>\n#modal-contact-us .modal-body { padding-top:0px; }\n.modal-header {border:none;}\n</style>\n<div aria-labeledby=\"modal-contact-us-label\" class=\"modal\" id=\"modal-contact-us\" role=\"dialog\">\n<div class=\"modal-dialog\">\n<div class=\"modal-content\">\n<div class=\"modal-header\">\n<button aria-hidden=\"true\" class=\"close\" data-dismiss=\"modal\" type=\"button\">×</button>\n<h4 class=\"sr-only\" id=\"modal-contact-us-label\">Contact Us</h4>\n</div>\n<div class=\"modal-body\">\n<iframe frameborder=\"0\" id=\"modal-contact-us-iframe\" width=\"100%\" height=\"100%\" title=\"Contact Us\"></iframe>\n</div>\n</div>\n</div>\n</div>\n<div id=\"adminTools\"></div>\n<iframe id=\"iframe\" src=\"/maps/embed.html?mapId=f0cc55f0-99a6-4be4-a4d8-b9cbdb5931db&state=MS#MS/parks\" height=\"426\"></iframe>\n<div class=\"container\">\n<div class=\"ColumnGrid row\">\n<div class=\"ColumnMain col-sm-12\">\n<!--googleoff: index-->\n<div class=\"Breadcrumbs container\">\n<div class=\"row\">\n<div class=\"col-sm-12\">\n<ol id=\"breadcrumbs\" style=\"display:none;\" class=\"Breadcrumbs\"></ol>\n</div>\n</div>\n</div>\n<div class=\"breadcrumbSourceContainer\" style=\"display:none;\">\n<div id=\"cs_control_5255284\" class=\"cs_control  CS_Element_Custom\"> </div>\n</div>\n<!--googleon: index-->\n<script>\njQuery(document).ready(function() {\n//this is done manually because there isn't a nav on the state pages\njQuery(\"ol#breadcrumbs\").append('<li><a href=\"/\">NPS.gov</a></li><li><a href=\"/findapark/index.htm\">Find A Park</a></li><li>Mississippi</li>').show();\n});\n</script>\n<div class=\"ContentHeader\">\n<h1 class=\"page-title\">Mississippi</h1>\n</div>\n<div class=\"row\">\n<div class=\"col-sm-12\">\n<div id=\"state_wrapper\">\n<div class=\"col-md-9 col-sm-12 col-xs-12 stateCol\">\n<div class=\"stateParkList\"><h2 class=\"Tag -green\">Parks</h2></div>\n<div id=\"parkListResults\">\n<div id=\"parkListResultsArea\">\n<ul id=\"list_parks\">\n<li class=\"clearfix\" id=\"asset_brcr\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Battlefield Site</h2>\n<h3><a href=\"/brcr/\">Brices Cross Roads</a></h3>\n<h4>Baldwyn, MS</h4>\n<p>\nThe Confederate victory at Brices Cross Roads was a significant victory for Major General Nathan Bedford Forrest, but its long term effect on the war proved costly for the Confederates. Brices Cross Roads is an excellent example of winning the battle, but losing the war.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/7BC1D5AF-1DD8-B71C-0E3EFA8B51336174.jpg\" alt=\"the monument with a cannon on each side\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/brcr/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/brcr/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/brcr/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/brcr/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_guis\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Seashore</h2>\n<h3><a href=\"/guis/\">Gulf Islands</a></h3>\n<h4>Gulf Breeze, Florida  and Ocean Springs, Mississippi            , FL,MS</h4>\n<p>\nWhat is it that entices people to the sea?  Poet John Masefield wrote, “I must go down to the seas again, for the call of the running tide is a wild call and a clear call that may not be denied.”  Millions of visitors are drawn to the islands in the northern Gulf of Mexico for the white sandy beaches, the aquamarine waters, a boat ride, a camping spot, a tour of an old fort, or a place to fish.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/BC36CD87-1DD8-B71C-0EE70C81AED4F51A.jpg\" alt=\"Bottlenose dolpin jumping out of the water\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/guis/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/guis/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/guis/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/guis/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_mide\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Heritage Area</h2>\n<h3><a href=\"/mide/\">Mississippi Delta</a></h3>\n<h4></h4>\n<p>\nThe Blues, Welty, Wright, Williams, Civil War and Civil Rights, The Great Flood, Bogues and Bayous, Plantations, The Great Migration, Rock ‘n’ Roll, Soul Food, King Cotton, The River, Precision Agriculture, Catfish, Gospel, Immigrants' Stories, Highway 61, Segregation, Integration, Share Cropping, Freedom Songs, Freedom Summer, Folk Tales, Swamp Forests, Hunting Clubs, and surprisingly, hot tamale\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/792A247A-1DD8-B71C-07331EF4FB66195D.jpg\" alt=\"The River bore the alluvial plain that is the Mississippi Delta, and the Delta bore fruit.......\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/mide/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/mide/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/mide/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/mide/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_migu\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Heritage Area</h2>\n<h3><a href=\"/migu/\">Mississippi Gulf</a></h3>\n<h4></h4>\n<p>\nThe Mississippi Gulf Coast is a culturally, historically, and environmentally distinctive region where many chapters in the national story have been written. The bounties of the Mississippi Gulf Coast's natural resources have brought people to this area from all over the world. The modern culture of the Coast consists of a multi-ethnic gumbo of people and traditions.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/44E7A1E1-1DD8-B71C-0780DD96BCA4658E.jpg\" alt=\"Mississippi Gulf Coast National Heritage Area\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/migu/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/migu/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/migu/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/migu/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_mihi\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Heritage Area</h2>\n<h3><a href=\"/mihi/\">Mississippi Hills</a></h3>\n<h4></h4>\n<p>\nSee the birthplace where Elvis made his entrance to the world stage ... Walk among the nation’s most extensive remaining Civil War earthworks from one of the largest sieges in the Western Hemisphere, at the Crossroads of the Confederacy ... There’s so much to see and do in the Mississippi Hills. Faulkner once said he could spend a lifetime writing about it—you could spend a lifetime exploring it.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/E96B0B6D-1DD8-B71C-070200EF8A90BA5F.jpg\" alt=\"Discover our stories. Experience our culture. Celebrate our heritage.\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/mihi/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/mihi/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/mihi/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/mihi/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_natc\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Historical Park</h2>\n<h3><a href=\"/natc/\">Natchez</a></h3>\n<h4>Natchez, MS</h4>\n<p>\nDiscover the history of all the peoples of Natchez, Mississippi, from European settlement, African enslavement, the American cotton economy, to the Civil Rights struggle on the lower Mississippi River.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/4ED5D3DB-1DD8-B71C-0EDC3F0FFBA257F8.jpg\" alt=\"Mississippi River from the Bluffs of Natchez\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/natc/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natc/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natc/planyourvisit/conditions.htm\"> Current Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natc/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_natr\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>Parkway</h2>\n<h3><a href=\"/natr/\">Natchez Trace</a></h3>\n<h4>the states of, AL,MS,TN</h4>\n<p>\nThe Natchez Trace Parkway is a 444-mile recreational road and scenic drive through three states. It roughly follows the \"Old Natchez Trace\" a historic travel corridor used by American Indians, \"Kaintucks,\" European settlers, slave traders, soldiers, and future presidents. Today, people can enjoy not only a scenic drive but also hiking, biking, horseback riding, and camping along the parkway.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/B00B7136-1DD8-B71C-0E853FFA5C794F32.jpg\" alt=\"A curve along the Natchez Trace Parkway with fall colors\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/natr/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natr/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natr/planyourvisit/conditions.htm\"> Current Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natr/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_natt\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Scenic Trail</h2>\n<h3><a href=\"/natt/\">Natchez Trace</a></h3>\n<h4>Tupelo, MS</h4>\n<p>\nThe 450-mile foot trail that became known as the Natchez Trace was the lifeline through the Old Southwest.  You can experience portions of that journey the way earlier travelers did - on foot.  Today there are five separate trails totaling over 60 miles and they are administered by the Natchez Trace Parkway.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/8BA84223-1DD8-B71C-0E8FCBC218DE44A8.jpg\" alt=\"3 hikers and a dog walk next to a creek\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/natt/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natt/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natt/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/natt/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_shil\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Military Park</h2>\n<h3><a href=\"/shil/\">Shiloh</a></h3>\n<h4>Shiloh, TN,MS</h4>\n<p>\nVisit the sites of the most epic struggle in the Western Theater of the Civil War. Nearly 110,000 American troops clashed in a bloody contest that resulted in 23,746 casualties; more casualties than in all of America's previous wars combined. Explore both the Shiloh and Corinth battlefields to discover the impact of this struggle on the soldiers and on the nation.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/82EA3BCF-1DD8-B71C-0E600B9D1415B94E.jpg\" alt=\"The Tennessee Monument at Shiloh National Military Park\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/shil/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/shil/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/shil/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/shil/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_tupe\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Battlefield</h2>\n<h3><a href=\"/tupe/\">Tupelo</a></h3>\n<h4>Tupelo, MS</h4>\n<p>\nIn July, 1864, Union forces, including men from the United States Colored Troops, marched into Tupelo, Mississippi.  Disorganized Confederate soldiers fought fiercely but could not overpower the federal troops.  Neither side could claim a clear victory, but Union troops had succeeded in their main goal:  keeping the Confederates away from Union railroads in Tennessee.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/B2677D57-1DD8-B71C-0EB5C602E91B1618.jpg\" alt=\"monumnent to the batle of tupelo, with a canon in the foreground \" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/tupe/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/tupe/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/tupe/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/tupe/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n<li class=\"clearfix\" id=\"asset_vick\">\n<div class=\"col-md-9 col-sm-9 col-xs-12 table-cell list_left\">\n<h2>National Military Park</h2>\n<h3><a href=\"/vick/\">Vicksburg</a></h3>\n<h4>Vicksburg, MS,LA</h4>\n<p>\nTwo statements, two Presidents, both aware of the importance of the city on the Mississippi River. President Davis knew it was vital to hold the city for the Confederacy to survive. President Lincoln wanted the key to gain control of the river and divide the South. Vicksburg National Military Park commemorates this campaign and its significance as a critical turning point of the Civil War.\n</p>\n</div>\n<div class=\"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right\">\n<div class=\"col-md-12 col-sm-12 col-xs-6 noPadding stateThumbnail\">\n<img class=\"stateResultImage\" src=\"/customcf/apps/CMS_HandF/ParkSearchPics/B72E3D49-1DD8-B71C-0EFA195838DFF48F.jpg\" alt=\"View from Battery DeGolyer\" border=\"0\" />\n</div>\n<div class=\"col-md-12 col-sm-12  noPadding stateListLinks\" >\n<ul>\n<li><a href=\"http://www.nps.gov/vick/planyourvisit/conditions.htm\"> Alerts & Conditions<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/vick/planyourvisit/basicinfo.htm\"> Basic Information<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/vick/planyourvisit/calendar.htm\"> Calendar<span class=\"hidden-xs\"> »</span></a></li>\n<li><a href=\"http://www.nps.gov/vick/planyourvisit/maps.htm\"> Maps<span class=\"hidden-xs\"> »</span></a></li>\n</ul>\n</div>\n</div>\n</li>\n</ul>\n</div>\n</div>\n</div>\n<h2  class=\"Tag -black\">By The Numbers</h2>\n<div class=\"col-md-3 col-sm-12 col-xs-12 stateCol stateCol-right\">\n<div id=\"cs_control_4083830\" class=\"cs_control \">\n<div id=\"list_numbers\">\n<a name=\"numbers\"></a>\n<script>\njQuery(document).ready(function(){\nvar deviceAgent = navigator.userAgent.toLowerCase();\nvar iOSAgent = deviceAgent.match(/(iphone|ipod|ipad)/);\njQuery(\".disclaimer\").each(function(){\njQuery(this).attr(\"title\", \"This figure is based on the number of official National Park Service units in the state. The sites shown on this page may also include sites affiliated with or managed by the National Park Service.\");\njQuery(this).tooltip(); // Bootstrap tooltip, NOT jQueryUI tooltip\njQuery(this).on('show.bs.tooltip', function () {\njQuery(document).data(\"tooltipShowing\", true);\n});\njQuery(this).on('hide.bs.tooltip', function () {\njQuery(document).data(\"tooltipShowing\", false);\n});\n});\n// Check onClick event of \"container\" class to see if a tooltip is open.\n// If so, close it: iOS touch hack\nif (iOSAgent) {\n// mobile code here\njQuery(\".container\").bind('click',function() {\nif(jQuery(document).data(\"tooltipShowing\") == true){\njQuery(\".disclaimer\").tooltip(\"hide\");\n}\n});\n}\n});\n</script>\n<ul class=\"state_numbers\">\n<li><strong>8</strong> National Parks <a class=\"disclaimer\" href=\"javascript:void(0)\"><i class=\"fa fa-question-circle\"></i></a></li> <li><strong>6,542,704</strong> Visitors to National Parks</li> <li><a href=\"http://nature.nps.gov/socialscience/vse.cfm\"><strong>$206,900,000</strong> Economic Benefit from National Park Tourism »</a></li> <li><a href=\"/tps/tax-incentives.htm\"><strong>$326,533,714</strong> of Rehabilitation Projects Stimulated by Tax Incentives (since 1995) »</a></li> <li><a href=\"/lwcf/\"><strong>$50,450,229</strong> of Land & Water Conservation Fund Appropriated for Projects (since 1965) »</a></li> <li><a href=\"/clg/\"><strong>62</strong> Certified Local Governments »</a></li> <li><a href=\"/ncrc/programs/rtca/\"><strong>31</strong> Community Conservation & Recreation Projects (since 1987) »</a></li> <li><a href=\"/flp/\"><strong>805</strong> Acres Transferred by Federal Lands to Parks for Local Parks and Recreation (since 1948) »</a></li> <li><a href=\"/getinvolved/volunteer.htm\"><strong>19,839</strong> Hours Donated by Volunteers »</a></li> <li><a href=\"/subjects/heritageareas/discover-nhas.htm#ms\"><strong>3</strong> National Heritage Areas »</a></li> <li><a href=\"/nts/\"><strong>1</strong> National Trails Managed by NPS »</a></li> <li><a href=\"/nr/\"><strong>1,422</strong> National Register of Historic Places Listings »</a></li> <li><a href=\"/nhl/\"><strong>39</strong> National Historic Landmarks »</a></li> <li><a href=\"https://nature.nps.gov/nnl/\"><strong>5</strong> National Natural Landmarks »</a></li> <li><a href=\"/hdp/\"><strong>354</strong> Places Recorded by Heritage Documentation Programs »</a></li> <li><a href=\"/museum/\"><strong>1,472,404</strong> Objects in National Park Museum Collections »</a></li> <li><a href=\"/archeology/\"><strong>376</strong> Archeological Sites in National Parks »</a></li> <li><a href=\"/subjects/teachingwithhistoricplaces/index.htm\"><strong>1</strong> Teaching with Historic Places Lesson Plan »</a></li> <li><a href=\"/subjects/heritagetravel/discover-our-shared-heritage.htm\"><strong>6</strong> Discover Our Shared Heritage Travel Itineraries »</a></li>\n<li class=\"numbers_download clearfix\"><img src=\"/state/templates/images/buttons/download_numbers.png\" alt=\"Download numbers\" /><a href=\"/state/customcf/bythenumbers/ms.pdf\"> Download the summary »</a></li>\n</ul>\n</div>\n</div>\n<p id=\"list_disclaimer\">These numbers are just a sample of the National Park Service's work. Figures are for the fiscal year that ended 9/30/2016.</p>\n<div id=\"list_numbers\" class=\"more_info clearfix\">\n<h2 style=\"font-family:Open Sans Condensed; font-size:1.4em;\">MORE INFORMATION</h2>\n<ul class=\"state_numbers\">\n<li><a href=\"/findapark/event-search.htm?states_filter=MS\">Events</a></li>\n<li><a href=\"/planyourvisit/alerts.htm?s=MS\">Active Alerts in Parks</a></li>\n<li><a href=\"/media/multimedia-search.htm?q=Mississippi\">Photos & Multimedia</a></li>\n<li><a href=\"/media/article-search.htm?q=Mississippi\">Articles</a></li>\n<li><a href=\"/news/index.htm\">Nationwide News</a></li>\n<li><a href=\"/findapark/passes.htm\">Get Your America the Beautiful Pass!</a></li>\n<li><a href=\"/aboutus/workwithus.htm\">Work With Us</a></li>\n</ul>\n</div>\n</div>\n</div>\n</div><!-- col-sm-12 -->\n</div><!-- row -->\n</div><!-- ColumnMain col-sm-9 -->\n</div><!-- ColumnGrid row -->\n</div><!-- end container -->\n</div><!-- end of <div main> -->\n<!--googleoff: index-->\n<footer id=\"GlobalFooter\" class=\"GlobalFooter\">\n<div class=\"container\">\n<div id=\"SearchFooter\" class=\"GlobalSearch\">\n<form class=\"GlobalSearch-form\" action=\"/search/index.htm\"  method=\"GET\">\n<label class=\"GlobalSearch-label js-toggle\" for=\"site_search_footer\">Search <i class=\"fa fa-search\"></i></label>\n<div class=\"GlobalSearch-inputGroup\">\n<input class=\"GlobalSearch-input\" type=\"text\" autocomplete=\"off\" id=\"site_search_footer\" name=\"query\" placeholder=\"Keyword Search\">\n<button class=\"GlobalSearch-button GlobalSearch-submitButton btn-form btn-form-primary js-use-site-limit\" type=\"submit\">This Site</button>\n<button class=\"GlobalSearch-button GlobalSearch-secondaryButton btn-form btn-form-primary\" type=\"submit\">All NPS</button>\n</div>\n</form>\n</div>\n<div class=\"row\">\n<img class=\"GlobalFooter-printLogo print-only\" src=\"/common/commonspot/templates/assetsCT/images/branding/nps_logo-bw.gif\" alt=\"NPS print format logo\">\n<div class=\"col-sm-12\">\n<img class=\"GlobalFooter-slogan\" src=\"/common/commonspot/templates/assetsCT/images/branding/nps-footer-slogan.png\" srcset=\"/common/commonspot/templates/assetsCT/images/branding/nps-footer-slogan.png 1x, /common/commonspot/templates/assetsCT/images/branding/nps-footer-slogan.png 2x\" alt=\"Experience Your America\">\n</div>\n</div>\n<hr>\n<div class=\"row\">\n<div class=\"col-xs-12 col-sm-4 col-sm-push-8\">\n<div class=\"GlobalFooter-nps-logo\">\n<div class=\"GlobalFooter-nps-logo-text\" style=\"padding-right:30px;\">\n<a href=\"//www.nps.gov\">National Park Service</a>\n<a href=\"//www.doi.gov\">U.S. Department of the Interior</a>\n</div>\n<div class=\"GlobalFooter-nps-logo-image\">\n<a href=\"//www.nps.gov\">\n<svg role=\"img\" focusable=\"false\" id=\"nps-logo-footer\" aria-labelledby=\"nps-logo-title nps-logo-desc\">\n<title id=\"nps-logo-title\">National Park Service Logo</title>\n<desc id=\"nps-logo-desc\">National Park Service Logo</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#nps-logo\"></use>\n</svg>\n</a>\n</div>\n</div>\n</div>\n<div class=\"col-xs-12 col-sm-8 col-sm-pull-4\">\n<ul class=\"GlobalFooter-generalLinks\">\n<li><a href=\"//www.nps.gov/aboutus/accessibility.htm\">Accessibility</a></li>\n<li><a href=\"//www.nps.gov/aboutus/privacy.htm\">Privacy Policy</a></li>\n<li><a href=\"//www.nps.gov/aboutus/foia/index.htm \">FOIA</a></li>\n<li><a href=\"//www.nps.gov/aboutus/notices.htm\">Notices</a></li>\n<li><a href=\"//www.nps.gov/aboutus/disclaimer.htm\">Disclaimer</a></li>\n</ul>\n<ul class=\"GlobalFooter-generalLinks\">\n<li><a href=\"//www.nps.gov/aboutus/faqs.htm\">FAQ</a></li>\n<li><a href=\"//www.doi.gov/pmb/eeo/no-fear-act\">No Fear Act</a></li>\n<li><a href=\"//www.nps.gov/aboutus/contactus.htm\">Contact Us</a></li>\n<li><a href=\"//www.usa.gov\">USA.gov</a></li>\n</ul>\n<ul class=\"GlobalFooter-socialLinks\">\n<li>\n<a href=\"//www.facebook.com/nationalparkservice\">\n<svg role=\"img\" focusable=\"false\" id=\"facebook-footer-link\" aria-labelledby=\"facebookTitle facebookDesc\">\n<title id=\"facebookTitle\">Facebook</title>\n<desc id=\"facebookDesc\">Facebook</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#facebook\"></use>\n</svg>\n<span>Facebook</span>\n</a>\n</li>\n<li>\n<a href=\"//www.youtube.com/nationalparkservice\">\n<svg role=\"img\" focusable=\"false\" id=\"youtube-footer-link\" aria-labelledby=\"youtubeTitle youtubeDesc\">\n<title id=\"youtubeTitle\">Youtube</title>\n<desc id=\"youtubeDesc\">Youtube</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#youtube\"></use>\n</svg>\n<span>Youtube</span>\n</a>\n</li>\n<li>\n<a href=\"//www.twitter.com/natlparkservice\">\n<svg role=\"img\" focusable=\"false\" id=\"twitter-footer-link\" aria-labelledby=\"twitterTitle twitterDesc\">\n<title id=\"twitterTitle\">Twitter</title>\n<desc id=\"twitterDesc\">Twitter</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#twitter\"></use>\n</svg>\n<span>Twitter</span>\n</a>\n</li>\n<li>\n<a href=\"//www.instagram.com/nationalparkservice\">\n<svg role=\"img\" focusable=\"false\" id=\"instagram-footer-link\" aria-labelledby=\"instagramTitle instagramDesc\">\n<title id=\"instagramTitle\">Instagram</title>\n<desc id=\"instagramDesc\">Instagram</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#instagram\"></use>\n</svg>\n<span>Instagram</span>\n</a>\n</li>\n<li>\n<a href=\"//www.flickr.com/nationalparkservice\">\n<svg role=\"img\" focusable=\"false\" id=\"flickr-footer-link\" aria-labelledby=\"flickrTitle flickrDesc\">\n<title id=\"flickrTitle\">Flickr</title>\n<desc id=\"flickrDesc\">Flickr</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#flickr\"></use>\n</svg>\n<span>Flickr</span>\n</a>\n</li>\n<li>\n<a href=\"//itunes.apple.com/WebObjects/MZStore.woa/wa/viewArtistLegacy?cc=us&id=216751324\">\n<svg role=\"img\" focusable=\"false\" id=\"itunes-footer-link\" aria-labelledby=\"itunesTitle itunesDesc\">\n<title id=\"itunesTitle\">iTunes</title>\n<desc id=\"itunesDesc\">iTunes</desc>\n<use xlink:href=\"/common/commonspot/templates/assetsCT/sprite.symbol.svg#itunes\"></use>\n</svg>\n<span>iTunes</span>\n</a>\n</li>\n</ul>\n</div>\n</div>\n</div>\n</footer>\n<!--googleon: index-->\n<!-- the rest of the scripts are leftovers from before the centennial down and should be pared down where possible -->\n<script src=\"/common/commonspot/templates/jsCT/global.js\"></script>\n<script src=\"/common/commonspot/templates/assets/libs/jquery.magnific-popup/jquery.magnific-popup.js\"></script>\n<script src=\"/common/commonspot/templates/assets/js/redesign.js\"></script>\n<link href=\"/common/commonspot/templates/assets/libs/colorbox/colorbox.css\" rel=\"stylesheet\">\n<script type=\"text/javascript\" src=\"/common/commonspot/templates/js/libs/jquery.colorbox-min.js\"></script>\n<script src=\"/common/commonspot/templates/jsCT/intercept-include.js\"></script>\n<script src=\"/common/commonspot/templates/assets/libs/image-map-resizer/imageMapResizer.min.js\"></script>\n<script src=\"/common/commonspot/templates/assetsCT/javascripts/app.late.min.js\"></script>\n<div class=\"modal fade\" id=\"outdated-browser\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"myModalLabel\">\n</div>\n<script type=\"text/javascript\">\n// Instructions: please embed this snippet directly into every page in your website template.\n// For optimal performance, this must be embedded directly into the template, not referenced\n// as an external file.\n// Answers Cloud Services Embed Script v1.02\n// DO NOT MODIFY BELOW THIS LINE *****************************************\n;(function (g) {\nvar d = document, i, am = d.createElement('script'), h = d.head || d.getElementsByTagName(\"head\")[0],\naex = {\n\"src\": \"//gateway.answerscloud.com/nps-gov/production/gateway.min.js\",\n\"type\": \"text/javascript\",\n\"async\": \"true\",\n\"data-vendor\": \"acs\",\n\"data-role\": \"gateway\"\n};\nfor (var attr in aex) { am.setAttribute(attr,aex[attr]); }\nh.appendChild(am);\ng['acsReady'] = function () {var aT = '__acsReady__', args = Array.prototype.slice.call(arguments, 0),k = setInterval(function () {if (typeof g[aT] === 'function') {clearInterval(k);for (i = 0; i < args.length; i++) {g[aT].call(g, function(fn) { return function() { setTimeout(fn, 1) };}(args[i]));}}}, 50);};\n})(window);\n// DO NOT MODIFY ABOVE THIS LINE *****************************************\n</script>\n<script type=\"text/javascript\">\n//<![CDATA[\nif (window.location.href.indexOf(\"www\") > -1) {\nvar usasearch_config = { siteHandle:\"nps\" };\nvar script = document.createElement(\"script\");\nscript.type = \"text/javascript\";\nscript.src = \"//search.usa.gov/javascripts/remote.loader.js\";\ndocument.getElementsByTagName(\"head\")[0].appendChild(script);\n}\n//]]>\n</script>\n</body>\n</html>\n<!-- beg (1) PrimaryResources -->\n<script type=\"text/javascript\" src=\"/commonspot/javascript/lightbox/overrides.js\"></script><script type=\"text/javascript\" src=\"/commonspot/javascript/lightbox/window_ref.js\"></script><script type=\"text/javascript\" src=\"/commonspot/pagemode/always-include-common.js\"></script>\n<!-- end (1) PrimaryResources -->\n<!-- beg (2) SecondaryResources -->\n<script type=\"text/javascript\" src=\"/ADF/thirdParty/jquery/cookie/jquery.cookie.js\"></script>\n<!-- end (2) SecondaryResources -->\n<!-- beg (3) CustomFoot -->\n<!-- end (3) CustomFoot -->\n<!-- beg (4) TertiaryResources -->\n<!-- end (4) TertiaryResources -->\r\n<script type=\"text/javascript\">\r\n<!--\r\nvar jsPageContributeMode = 'read';\r\nvar jsPageSessionContributeMode = 'read';\r\n\r\nvar jsPageAuthorMode = 0;\r\nvar jsPageEditMode = 0;\r\n\r\n\r\nif(!commonspot)\r\n\tvar commonspot = {};\r\ncommonspot.csPage = {};\r\n\r\n\r\n\tcommonspot.csPage.url = '/state/ms/index.htm';\r\n\r\n\r\ncommonspot.csPage.id = 4085673;\r\n\r\ncommonspot.csPage.siteRoot = '/';\r\ncommonspot.csPage.subsiteRoot = '/state/ms/';\r\n\r\n\r\n// -->\r\n</script>\r\n<script type=\"text/javascript\">\r\n<!--\r\n\tif (typeof parent.commonspot == 'undefined' || typeof parent.commonspot.lview == 'undefined' || typeof parent.commonspot.lightbox == 'undefined')\r\n\t\tloadNonDashboardFiles();\r\n\telse if (parent.commonspot && typeof newWindow == 'undefined')\r\n\t{\r\n\t\tvar arrFiles = \r\n\t\t\t\t[\r\n\t\t\t\t\t{fileName: '/commonspot/javascript/lightbox/overrides.js', fileType: 'script', fileID: 'cs_overrides'},\r\n\t\t\t\t\t{fileName: '/commonspot/javascript/lightbox/window_ref.js', fileType: 'script', fileID: 'cs_windowref'}\r\n\t\t\t\t];\r\n\t\t\r\n\t\tloadDashboardFiles(arrFiles);\r\n\t}\r\n//-->\r\n</script>\r\n</body></html>""")

	def GetWebPage_Data_type(self):
		returned_webdata = GetWebPage_Data('https://www.nps.gov/index.htm')
		self.assertEqual(type(returned_webdata), type(" "))

class Test_Article(unittest.TestCase):
	def Article_Test_get_Main_titles(self):
		Test_Art_inst = Article("https://www.nps.gov/kids/jrRangers.cfm")
		Test_Art_Main_Title = Test_Art_inst.get_main_title()
		self.assertEqual(str(Test_Art_Main_Title), "Junior Rangers | National Park Service")
	def Article_Test_get_snippets(self):
		Test_Art_inst = Article("https://www.nps.gov/kids/jrRangers.cfm")
		Test_Art_get_snippets = Test_Art_inst.get_snippets()
		self.assertEqual(type(Test_Art_get_snippets), type([]))

class Test_National_Park(unittest.TestCase):
	def National_Park_Test_get_Location(self):
		Test_NP_inst = National_Park(("https://www.nps.gov/state/al/index.htm", "Alabama"))
		Test_NP_Loc= Test_NP_inst.get_Location()
		self.assertEqual(str(Test_NP_Loc), "Alabama")
	def National_Park_Test_get_Available_National_Parks(self):
		Test_NP_inst = National_Park(("https://www.nps.gov/state/al/index.htm", "Alabama"))
		Test_NP_ANP= Test_NP_inst.Get_Available_National_Parks()
		self.assertEqual(type(Test_NP_ANP), type([]))

class Test_save_park_info(unittest.TestCase):

	def Check_That_There_Is_Return(self):
		Test_NP_inst = National_Park(("https://www.nps.gov/state/al/index.htm", "Alabama"))
		test1 = save_park_info(Test_NP_inst)
		self.assertEqual(type(test1), type([]))
		
	def Check_Return_Type(self):
		Test_NP_inst = National_Park(("https://www.nps.gov/state/al/index.htm", "Alabama"))
		test2 = save_park_info(Test_NP_inst)
		self.assertEqual(type(test2[0]), type((0,0)))

class Test_save_article_info(unittest.TestCase):

	def Check_That_There_Is_Return(self):
		Test_Art_inst = Articles("https://www.nps.gov/getinvolved/volunteer.htm")
		test1 = save_article_info(Test_Art_inst)
		self.assertEqual(type(test1), type((0,0)))
		
	def Check_Return_Type(self):
		Test_Art_inst = Articles("https://www.nps.gov/getinvolved/volunteer.htm")
		test2 = save_article_info(Test_Art_inst)
		self.assertEqual(type(test2[2]), type(" "))

class Test_save_state_tempinfos(unittest.TestCase):

	def Check_That_There_Is_Return(self):
		Tested1 = save_state_tempinfos()
		self.assertEqual(type(Tested1), type((0,0)))
		
	def Check_Return_Type(self):
		Tested2 = save_state_tempinfos()
		self.assertEqual(type(Tested2[0]), type([]))


#Closes database so its not locked
FP_cur.close()
## Remember to invoke all your tests...
unittest.main(verbosity=2)