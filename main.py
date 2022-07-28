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


def move_left(t):
    endtime = time.time() + t
    
    while True:
        action.key_down(Keys.ARROW_LEFT).perform()
    
        if time.time() > endtime:
            action.key_up(Keys.ARROW_LEFT).perform()
            break    

def move_right(t):
    endtime = time.time() + t
    
    while True:
        action.key_down(Keys.ARROW_RIGHT).perform()
    
        if time.time() > endtime:
            action.key_up(Keys.ARROW_RIGHT).perform()
            break    

def move_up(t):
    endtime = time.time() + t
    
    while True:
        action.key_down(Keys.ARROW_UP).perform()
    
        if time.time() > endtime:
            action.key_up(Keys.ARROW_UP).perform()
            break    

def move_down(t):
    endtime = time.time() + t
    
    while True:
        action.key_down(Keys.ARROW_DOWN).perform()
    
        if time.time() > endtime:
            action.key_up(Keys.ARROW_DOWN).perform()
            break    

def jump_left(n):
    for i in range(n):
        action.send_keys(Keys.HOME)
    time.sleep(0.1)

def jump_right(n):
    for i in range(n):
        action.send_keys(Keys.END)
    time.sleep(0.1)

def jump_down(n):
    for i in range(n):
        action.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)

def jump_up(n):
    for i in range(n):
        action.send_keys(Keys.PAGE_UP)
    time.sleep(0.1)

def reload_flights():
    action.drag_and_drop_by_offset(map_body, -277, 0).perform()

def list_save(data):
    data_list = []
    for i in range(len(data)):
        if data[i].text != '':
            data_list.append(data[i].text)
    return data_list

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

zoom = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/section/div/div[1]/div[1]/span/div/div/div[13]/div/div[2]/div/button[1]')
zoom.click()
zoom.click()
zoom.click()

# Focus on map to move with keys
map_body = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/section/div/div[1]/div[1]/span/div/div/div[2]/div[2]')
map_body.click()

# Time to let map fully load
time.sleep(1.5)

# Movement to Portuguese islands 
jump_left(4)
move_left(0.7)
time.sleep(0.1)
jump_down(3)

# We need to click and drag, so the web can reload flights in current location
reload_flights()




###################################
######### Data gathering ##########
###################################

time.sleep(2) # Load wait

######## Destination ###########
# Destination names gather
flights = driver.find_elements(By.XPATH, '//h3[@class="W6bZuc YMlIz"]') 

# Translate data to text and save in a list
flight_list = list_save(flights)
print(flight_list)


########## Date ################
date = driver.find_elements(By.XPATH, '//div[@class="CQYfx"]') 
date_list = list_save(date)
print(date_list)


########## Price ###############
price = driver.find_elements(By.XPATH, '//span[@class="QB2Jof xLPuCe"]') 
price_list = list_save(price)
print(price_list)


########## Scales ##############
scales = driver.find_elements(By.XPATH, '//span[@class="nx0jzf"]')
scales_list = list_save(scales)
print(scales_list)


########## Duration ############
duration = driver.find_elements(By.XPATH, '//span[@class="Xq1DAb"]')
duration_list = list_save(duration)
print(duration_list)


