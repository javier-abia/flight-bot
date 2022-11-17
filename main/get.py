import time
import os
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

def trip_duration(driver, d):
    if d == 'weekend':
        driver.find_element(By.XPATH, '//div[@class="Kn4yub ZsBBeb"]').click()
        WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[3]/span/div/div[2]/div[2]/span[1]/span/span/button/span/span'))).click()
        WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[3]/div[1]/button/span'))).click()

    if d == '2week':
        driver.find_element(By.XPATH, '//div[@class="Kn4yub ZsBBeb"]').click()
        WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[3]/span/div/div[2]/div[2]/span[3]/span/span/button/span/span'))).click()
        WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[3]/div[1]/button/span'))).click()

    if d == '1week':
        pass


def main(duration = '1week'):
    # We read both destinations and departures files and put their data in a variable
    fm = files_manage()

    # Define paths to files
    des = fm.des
    dep = fm.dep
    new_file = fm.new_file
    old_file = fm.old_file
    avalaible_file = fm.avalaible_file
    non_avalaible_file = fm.non_avalaible_file


    destinations = fm.read_json(des)
    departures = fm.read_json(dep)




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

    
    # Select duration flights (do nothing if it is 1 week trip)
    trip_duration(driver, duration)


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
    new_data = fd.destination_gather(destinations)
    fm.save_json(new_file, new_data)

    new_data = fm.read_json(new_file)
    old_data = fm.read_json(old_file)



    ###########################################################
    ################### Comparing flights #####################
    ###########################################################


    fm.compare_files()

    new_avalaible = fm.read_json(avalaible_file)
    non_avalaible = fm.read_json(non_avalaible_file)


    print('------------NEW-------------------')
    fd.show_flights(new_avalaible)
    print('----------NOT AVALAIBLE-----------')
    fd.show_flights(non_avalaible)


    os.remove(old_file)
    os.rename(new_file, old_file)