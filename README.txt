Final_Project.py README
Name: Kyle Durant

Background:

	*I chose option one because I felt it would be best for showing my level of understanding. 

What Does it Do?

	*This program can be used to store in a database weather information related to states, as well as gather data from the National Park Service website.

	*The program can then use the database's information to provide insight on parks like average temperature of a park based on the state it resides in, and writes that info to its output file "Info_Regarding_NPG.txt"

How To Use:
	*Depending on your setup you may need to pip install modules for:
		- requests
	 	- json
	 	- unittest
	 	- itertools
	 	- collections
	 	- sqlite3
	 	- random
	 	- Beautiful Soup

	*This program requires the 206_final_project_cache to run without accessing the internet, otherwise no input 

	*So in order to use it all you need to do is to point or terminal to the file that has the program in it and run the program by typing into the terminal "python  $ python -u Final_Project.py" and pressing enter to run it

The following files are included:
	*Final_Project.py: Contains the programming code/will allow you to run the program
	
	*206_final_project_cache: Contains the pre cached html information from the necessary websites so accessing the internet isn't needed.
	
	*README: The instructional material regarding the Final_Project program(To guide you on your way)
	
	*Final_Project Database: Contains the chosen stored(if deleted program will make a new one unless you have pinged the targeted website)
	
	*Info_Regarding_NPG.txt: Contains the output from the code(If deleted program will make another)


Functions:

	-GetWebPage_Data:
		*Input(required): A given url
		*Return Value: Returns the html data for that page
		*Behaviour: Returns html data for the given url as well as cacheing that data for later use

	-save_park_info:
		*Input(required): National Park Instance
		*Return Value: A list of the the Monument/Park information related to the given National Park Instance
		*Behavior: Takes information from a National Park Instance and Inserts it into the appropriate database.
		*Return Value is only for testing

	-save_state_tempinfos:
		*Input(required): State Weather url
		*Return Value: A tuple made up of four lists representing state, two temps, and rank based on average temps 
		*Behavior: Takes information from a weather site url and Inserts it into the appropriate database.
		*Return Value is more for testing

	-save_article_info:
		*Input(required): Article Url
		*Return Value: A tuple relating to that instances article info. 
		*Behavior: Takes information from a Article Instance and Inserts it into the appropriate database.
		*Return Value is only for testing

Classes:

	Article
		*One instance represents one article
		*Required Constructor Input: Article url
		*Methods:
			-get_main_title:
				+No additional  INput aside from self
				+Grabs first title associated with that article
				+Returns that first title
			get_all_titles:
				+No additional  INput aside from self
				+Grabs all titles associated with that article
				+Returns all available titles
			-get_snippets:
				+One optional Input: n(an Integer or None)
				+Grabs all text associated with that article or number of pieces of that code based on input if invalid will print to screen invalid
				+Returns Requested number of snippets

	NationalPark:
		*One instance represents the available Parks/Monuments for the given state's url
		*Required Constructor Input: NationalPark
		*Methods:
			get_Location:
				+No additional  INput aside from self
				+Grabs the name of the State which will act as the location for that Instance's Parks/Monuments
				+Returns Instance's related state
			get_available_national_parks:
				+No additional  INput aside from self
				+Grabs the info for that Instance's Parks/Monuments and appends that info to a list
				+Returns Instance's list of Park Info

Database:

*Parks:
	-Each Row Represents Park/Monument
	-The attributes in each row from left to right(up down are):
		*Park_id--DEFAULT INTEGER PRIMARY KEY
		*Park_Name--TEXT
		*State--TEXT
		*Description--TEXT

States:
	-Each Row Represents a state
	-The attributes in each row from left to right(up down are):
		*State_id--DEFAULT INTEGER PRIMARY KEY
		*State--TEXT
		*Avg_Temp_Fahrenheit INTEGER
		*Avg_Temp_Celsius INTEGER 
		*Temp_Rank INTEGER

Articles:
	-Each Row Represents an Article
	-The attributes in each row from left to right(up down are):
		*Article_id--DEEFAULT INTEGER PRIMARY KEY
		*Article_Main_Title--TEXT 
		*Article_All_Associated__Titles--TEXT 
		*Article_Text--TEXT

Data Manipulation:

	*The code can be used to compare information within the database
	*This information can be handy when trying to make decisions regarding what parks to visit
	*The Output file as of now will show the top five ranked states as far as temperature.
	*The user should expect The information in the output file a complete cache, a complete database, and a helpful program!

Extra Info:
	*Line(s) on which each of your data gathering functions begin(s): 30, 191, 214, 260

	*Line(s) on which your class definition(s) begin(s): 79, 118

	*Line(s) where your database is created in the program:150-185

	*Line(s) of code that load data into your database: 209-210, 253-254, 277-278

	*Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used? 325, 336-337,

	*Line(s) of code that generate the output: 315-317, 342-344

