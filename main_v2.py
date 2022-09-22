import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from src import flight
from src import flights_data
from src import search



# We gather destinations data and put it in a list
destinations_file = open('destinations.txt', 'r')
destinations_string = destinations_file.read()
destinations = destinations_string.split(',') 
destinations_file.close()


# We gather departures data and put it in a list
departures_file = open('departures.txt', 'r')
departures_string = departures_file.read()
departures = departures_string.split(',')
departures_file.close()








###########################################################
##################### Google Flights ######################
###########################################################

# Initialize driver
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver) # Define actions in driver


url_google = 'https://www.google.com/'
url_flights = f'https://www.google.com/travel/explore?q=Flights+to+Europe+from+{departures[0]}+in+the+next+6+months+round+trip&hl=en-GB'


# First search google, just to reject all cookies, since we cant reject them when searching google flights directly
driver.get(url_google)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()

# Load google flights web
driver.get(url_flights)



###########################################################
####################### Departure #########################
###########################################################

# Initialize class
s = search(driver, action)

# Add departures
s.add_departure(departures)


###########################################################
##################### Airport search ######################
###########################################################

# s.search_destinations(destinations)



###################################
######### Data gathering ##########
###################################

# Initialize lists of atributes
destination=[]; date=[]; price=[]; scales=[]; duration=[]
atributes = [destination, date, price, scales, duration]

# We need an empty list and the atributes XPath to define the data_gather class 
atributes_empty = ['','','','','']
atributes_path = ['//h3[@class="W6bZuc YMlIz"]','//div[@class="CQYfx"]','//span[@class="QB2Jof xLPuCe"]', '//span[@class="nx0jzf"]','//span[@class="Xq1DAb"]']

# Initialize flights_data class and data saving
fd = flights_data(driver, action,atributes_empty, atributes_path)
fd.data_gather(destinations)
fd.show_flights()





input()