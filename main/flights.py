import time
import pickle
import os
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

    def erase_file(self, file_location):
        with open(file_location, 'wb') as f:
            pass

    def save_string(self, file_location, string,*args):
        '''
        Saves string to a file. 

        Additional arguments are used for concatenation E.g. --> 'TIA98€'
        So it's easy to compare old and new flights to find duplicates
        '''
        with open(file_location, 'a') as f:
                f.write(f"{string+''.join(args)},")


############# We should put this  below in flights_data class or in other class


    def get_olddata(self, old_data_file = './docs/show/old_flights.txt'):
        with open('./docs/show/old_flights.txt', 'rb') as f:
            return pickle.load(f)

    

    def compare_files(self, fold = './docs/IATA-codes/old.txt', fnew = './docs/IATA-codes/new.txt', fdeleted = './docs/IATA-codes/new_non-avalaible.txt', favalaible = './docs/IATA-codes/new_avalaible.txt'):
        lold = self.read_file(fold)
        lnew = self.read_file(fnew)

        self.erase_file(fdeleted)
        self.erase_file(favalaible)

        for i in lold:
            if i not in lnew:
                self.save_string(fdeleted,i)
        for i in lnew:
            if i not in lold:
                self.save_string(favalaible, i)





    def read_iata(self, iata_file):
        ''' Read iata+price file and convert it to iata list '''
        
        l_iata = self.read_file(iata_file)
        l = []
        for i in l_iata:
            i = i.split('€')
            l.append(i[0])
        
        return l[:-1] # Last element is [''], so we dont want to return it

    def iata_to_flights(self, iata_file, flights_list):
        ''' Converts iata list to full flight list ''' 

        l  = self.read_iata(iata_file)
        print(f'l -----> {l}')

        # Read element of l and compare its IATA code to the one in flights_list ---> saving complete flight in a list
        lf = []
        for i in l:
            for j in range(len(flights_list)):
                if i in flights_list[j].IATA:
                    lf.append(flights_list[j])
        return lf

    def save_flights(self, new, new_avalaible, new_nonavalaible, file_old = './docs/show/old_flights.txt', file_new = './docs/show/new_flights.txt', file_new_avalaible = './docs/show/new_flights_avalaible.txt', file_new_nonavalaible = './docs/show/new_flights_nonavalaible.txt'):
        ''' Save flight objects in files & replace old flights with new flights'''
        
        l = [new, new_avalaible, new_nonavalaible]
        lf = [file_new, file_new_avalaible, file_new_nonavalaible]

        for i in lf:
            with open(i, 'wb') as f:
                for j in l:
                    pickle.dump(j, f)


        # Replace old flights with new flights (delete old_flights.txt and rename new to old)
        os.remove(file_old)
        os.rename(file_new, file_old)
        
            
        




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
        fm.erase_file('./docs/IATA-codes/new.txt')
        
        
        # Searching new destination
        for j in range(10):
            time.sleep(1)
            self.driver.find_element(By.XPATH, self.search_box).click()     
            self.action.send_keys(destinations[j]).perform() 
            self.action.key_down(Keys.ENTER).perform()
            self.action.key_up(Keys.ENTER).perform() 



            # Gathering data and creating flight 
            try:
                price = int(WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="EDKFBb QB2Jof SgNiff"]'))).text.strip('€'))

                if price < 200:
                    for i in range(len(self.path)):
                        self.data[i] = self.driver.find_element(By.XPATH, f'{self.path[i]}')
                    f = flight(self.data[0].text, destinations[j] ,f'{self.data[1].text} ({self.data[2].text})', self.data[3].text, self.data[4].text, self.data[5].text.split('\n')[0], self.data[5].text.split('\n')[1])
                    self.flights_list.append(f)
                    print(f'{f.departure} --> {f.IATA}: \t {f.destination} \t - \t {f.date} \t - \t {f.price} \t - \t {f.scales} \t - \t {f.duration}')
                    
                    # Saving flights as 'destination+price' into new flights data 
                    fm.save_string('./docs/IATA-codes/new.txt', f.IATA, f.price)

            except:
                pass

            try:
                WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH,'/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[2]/div[1]/button/div[1]'))).click()
            except:
                pass

        return self.flights_list

    def show_flights(self, flights):
        ''' Prints flights '''
        for i in flights:
            print(f'--> {i.destination} \t - \t {i.date} \t - \t {i.price} \t - \t {i.scales} \t - \t {i.duration}')




