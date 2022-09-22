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



# Initialize web driver
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
action = ActionChains(driver) # Define actions in driver


url_google = 'https://www.google.com/'
airports = 'https://es.wikipedia.org/wiki/Anexo:Aeropuertos_de_Europa'
table='//tr[@valign="top"]'
tables = '//tr//td'

# First search google, just to reject all cookies, since we cant reject them when searching google flights directly
driver.get(url_google)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()

driver.get(airports)

# Gather airports in a list (non-legible)
airports_list = driver.find_elements(By.XPATH, tables)


f=[]

# Convert to a legible list and add them only the elements that have 3 characters
# Elements that have 3 characters are airports in IATA code
for i in range(len(airports_list)):
    if len(airports_list[i].text) == 3:
        f.append(airports_list[i].text)


# Remove all elements that are not in uppercase, since other elements with 3 characters (such as numbers) could have been added
'''
NOTE: The reason not to do this process before is that the "3 character filter" reduces the size of the list a lot.
By applying the "upper case filter" now, we ensure that the list is smaller, so it will spend less time filtering data
'''
i=0
while i < len(f):
    if f[i].isupper() == False:
        f.remove(f[i])
    else:
        i+=1

# Change data format (by making it as a csv file) so it can be clean when open it later
f = f.replace('\'', '') # Remove ''
f = f.replace('[', '') # Remove [
f = f.replace(']','') # Remove ]
f = f.replace(' ','') # Remove blank spaces

# Finally, we write the data into a file
airports_file = open('destinations.txt', 'w')
airports_file.write(f)
airports_file.close()

print(f)