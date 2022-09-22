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

from src import movement
from src import flight
from src import flights_data



###############################
####### Google Flights ########
###############################

# Initialize web driver
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver) # Define actions in driver


url_google = 'https://www.google.com/'
url_flights = 'https://www.google.com/travel/explore?q=Flights+to+Europe+from+OPO+in+the+next+6+months+round+trip&hl=en-GB'


# First search google, just to reject all cookies, since we cant reject them when searching google flights directly
driver.get(url_google)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()

# Load google flights web
driver.get(url_flights)




############################
######### Filters ##########
############################

# Press filter button
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/button/span'))).click()
time.sleep(2) # Needed to work

# Filter price, to minimun
filter_drag = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div/div[1]/section[4]/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]')
action.drag_and_drop_by_offset(filter_drag, -277, 0).perform()

# Close filter dialogue
driver.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/span/button').click()
time.sleep(3)





#########################################
######### Movement accross map ##########
#########################################
mv = movement(driver,action)

zoom_button = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/section/div/div[1]/div[1]/span/div/div/div[13]/div/div[2]/div/button[1]')
mv.zoom(zoom_button, 3)

# Focus on map to move with keys
map_body = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/section/div/div[1]/div[1]/span/div/div/div[2]/div[2]')
map_body.click()

# Time to let map fully load
time.sleep(1.5)

# Movement to Azores islands
mv.jump_left(4)
mv.move_left(0.7)
mv.jump_down(3)

# We need to click and drag, so the web can reload flights in current location
mv.reload_flights(map_body)




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
fd = flights_data(driver, atributes_empty, atributes_path)
fd.data_gather()




# ####################################
# ######### Sweep whole map ##########
# ####################################

# Spain
time.sleep(1.5)
mv.jump_right(2)
mv.jump_up(1)
mv.move_left(1)
mv.move_down(1)
time.sleep(0.2)

mv.reload_flights(map_body)

fd.data_gather()


time.sleep(1.5)
mv.move_up(1)
mv.move_right(1)
mv.jump_down(1)
mv.jump_left(2)
time.sleep(0.2)


mv.reload_flights(map_body)
time.sleep(2)

fd.data_gather()

fd.show_flights()



input()
