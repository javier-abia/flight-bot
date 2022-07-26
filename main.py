import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.google.com/travel/explore?q=Flights+to+Europe+from+OPO+in+the+next+6+months+one+way&hl=en-GB'
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-RLmnJb"))).click()

# filter_button = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/button/span').click()

# action = ActionChains(driver)
# filter_drag = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div/div[1]/section[4]/div/div[1]/div/div/div/div[2]/div/div/div/div[2]/div[2]')
# action.drag_and_drop_by_offset(source1, 100, 0).perform()
time.sleep(30)










'''

REMOVE

# explore = driver.find_element(By.XPATH,'/html/body/c-wiz[1]/div[3]/div/div/div/nav/div[2]/a/button/div[1]').click()

# departure = driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input')

# time.sleep(2)
# departure.click()
# time.sleep(2)
# departure.clear()
# departure.send_keys("oporto")

# # add_button =driver.find_element('xpath', '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input')
# # add_button.click()
# # departure.send_keys(Keys.RETURN)


# search_button = driver.find_element('xpath', '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button/span[2]')
# search_button.click()
# time.sleep(2)
'''