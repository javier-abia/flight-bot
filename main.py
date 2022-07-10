from selenium import webdriver
import time

DRIVER_PATH = './geckodriver'
driver = webdriver.Firefox(executable_path=DRIVER_PATH)
driver.get('https://www.google.com/travel/flights')

search_button = driver.find_element('xpath', '/html/body/c-wiz[2]/div/div[2]/c-wiz/div/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button/span[2]')
search_button.click()