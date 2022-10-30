import time
import pickle
import os
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import collections

class files_manage:
    def __init__(self):
        pass

    def erase_file(self, file_location):
        with open(file_location, 'wb') as f:
            pass

    def read_json(self, file_location):
        # Read JSON file with json.load
        with open(file_location, 'r') as f:
            return json.load(f)

    def save_json(self, file_location, lst):
        # Save JSON as dictionary with json.dump
        with open(file_location, 'w') as f:
            json.dump([i.__dict__ for i in lst], f, indent=2)


    def compare_files(self, fold = './docs/json/old.json', fnew = './docs/json/new.json', fdeleted = './docs/json/new_non-avalaible.json', favalaible = './docs/json/new_avalaible.json'):
        
        lold = self.read_json(fold)
        lnew = self.read_json(fnew)
        print(f'F OLF\n{lold}')

        avalaible = []
        non_avalaible = []

        self.erase_file(fdeleted)
        self.erase_file(favalaible)

        for i in lold:
            if i not in lnew:
                non_avalaible.append(i)

        for i in lnew:
            if i not in lold:
                avalaible.append(i)
        
        # Save in json file
        with open('./docs/json/new_non-avalaible.json', 'w') as f: json.dump(non_avalaible, f, indent=2)
        with open('./docs/json/new_avalaible.json', 'w') as f: json.dump(avalaible, f, indent=2)



class flight:
    def __init__(self, departure, IATA,destination, date, price, scales, duration):
        self.departure = departure
        self.IATA = IATA
        self.destination = destination
        self.date = date
        self.price = price
        self.scales = scales
        self.duration = duration


class flights_data:

    def __init__(self, driver, action):
        self.driver = driver
        self.action = action
        self.flights_set = set()
        self.path = ['//span[@class="mrLYAe"]', '//span[@class="HVJNrc CIydMe"]', '//div[@class="CQYfx Wb6ww"]','//div[@class="CQYfx c2y3C"]','//div[@class="EDKFBb QB2Jof SgNiff"]', '//span[@class="yApPxd"]'] # Path to atributes
        self.data = [''] * len(self.path) # Array of empty data of concrete length
        self.search_box = '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/input'
        self.ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)



    def add_departure(self, departures):

        # Click departure airport textbox
        self.driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/input').click()

        # Click add airport button
        path = '//button[@class="VfPpkd-Bz112c-LgbsSe yHy1rc eT1oJ mN1ivc evEd9e"]'
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, path))).click()

        # Add departure airport
        for i in range(1,len(departures)):
            self.action.send_keys(departures[i]).perform()
            time.sleep(0.5)
            self.action.key_down(Keys.ENTER).perform()
            self.action.key_up(Keys.ENTER).perform()

        map_body = self.driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/section/div/div[1]/div[1]/span/div/div/div[2]/div[2]')
        map_body.click()
            




    def destination_gather(self, destinations):

        '''
        Gathers the data from google flights in a non-legible format.
        ---------------------------------------------------------------
        Translation non-legible format to text.
        Saves all data in list of lists with following format---> 
        ---> [[destinations], [dates], [prices], [scales], [duration]]
        ---------------------------------------------------------------
        Saves translated data to a set. Each element of the set is a flight
        with all of its atributes.
        '''


        fm = files_manage()
        
        # Searching new destination
        for j in range(5):
            time.sleep(1)
            self.driver.find_element(By.XPATH, self.search_box).click()     
            self.action.send_keys(destinations[j]).perform() 
            self.action.key_down(Keys.ENTER).perform()
            self.action.key_up(Keys.ENTER).perform() 



            # Gathering data and creating flight 
            try:
                price = int(WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="EDKFBb QB2Jof SgNiff"]'))).text.strip('€'))

                if price < 200: # Filter flights by price
                    for i in range(len(self.path)):
                        self.data[i] = self.driver.find_element(By.XPATH, f'{self.path[i]}')
                    
                    # Add elements to flights object
                    f = flight(self.data[0].text, destinations[j] ,f'{self.data[1].text} ({self.data[2].text})', self.data[3].text, self.data[4].text, self.data[5].text.split('\n')[0], self.data[5].text.split('\n')[1])
                    
                    # Add flight objbect to set
                    self.flights_set.add(f)

                    print(f'{f.departure} --> {f.IATA}: \t {f.destination} \t - \t {f.date} \t - \t {f.price} \t - \t {f.scales} \t - \t {f.duration}')
                    
            except:
                pass

            try:
                WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH,'/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[2]/div[1]/button/div[1]'))).click()
            except:
                pass
        
        # Save flights set in json file as dictionary
        fm.save_json('./docs//json/new.json', self.flights_set)
        
        return self.flights_set

    def show_flights(self, flights):
        ''' Prints flights '''
        for i in range(len(flights)):
            print(f'--> {flights[i].get("destination")} \t - \t {flights[i].get("date")} \t - \t {flights[i].get("price")} \t - \t {flights[i].get("scales")} \t - \t {flights[i].get("duration")}')
        

