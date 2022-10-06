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


from flights import flight
from flights import flights_data
from flights import files_manage



# We read both destinations and departures files and put their data in a variable
f=files_manage()

destinations = f.read_file('./data/destinations.txt')
departures = f.read_file('./data/departures.txt')




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

# Select weekends flights
driver.find_element(By.XPATH, '//div[@class="Kn4yub ZsBBeb"]').click()
WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[3]/span/div/div[2]/div[2]/span[1]/span/span/button/span/span'))).click()
WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[3]/div[1]/button/span'))).click()



###########################################################
####################### Departure #########################
###########################################################

# Initialize class
fd = flights_data(driver, action)

# Add departures
fd.add_departure(departures)


###########################################################
################### Data gathering ########################
###########################################################

# Initialize flights_data class and data saving
fd.destination_gather(destinations)


