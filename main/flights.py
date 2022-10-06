import time
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

    def read_file(self, file_location):
        # We gather file data and put it in a list
        with open(file_location, 'r') as f:
            f_string = f.read()
            return(f_string.split(','))
    



class flight:
    def __init__(self, departure, destination, date, price, scales, duration):
        self.departure = departure
        self.destination = destination
        self.date = date
        self.price = price
        self.scales = scales
        self.duration = duration


class flights_data:

    def __init__(self, driver, action):
        self.driver = driver
        self.action = action
        self.flights_list = []
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

        for i in range(len(destinations)):
            time.sleep(1)
            self.driver.find_element(By.XPATH, self.search_box).click()     
            self.action.send_keys(destinations[i]).perform() 
            self.action.key_down(Keys.ENTER).perform()
            self.action.key_up(Keys.ENTER).perform() 
                
            try:
                price = int(WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="EDKFBb QB2Jof SgNiff"]'))).text.strip('€'))

                if price < 100:
                    for i in range(len(self.path)):
                        self.data[i] = self.driver.find_element(By.XPATH, f'{self.path[i]}')
                    f = flight(self.data[0].text, f'{self.data[1].text} ({self.data[2].text})', self.data[3].text, self.data[4].text, self.data[5].text.split('\n')[0], self.data[5].text.split('\n')[1])
                    self.flights_list.append(f)
                    print(f'{f.departure} --> {f.destination} \t - \t {f.date} \t - \t {f.price} \t - \t {f.scales} \t - \t {f.duration}')
                    fm.append_to_file('./data/flight_obj.txt',f)
            except:
                pass

            try:
                WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH,'/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[2]/div[1]/button/div[1]'))).click()
            except:
                pass


    def show_flights(self):
        ''' Prints flights '''
        for i in self.flights_list:
            print(f'--> {i.destination} \t - \t {i.date} \t - \t {i.price} \t - \t {i.scales} \t - \t {i.duration}')



