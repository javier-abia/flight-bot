import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import collections



class flight:
    def __init__(self, destination, date, price, scales, duration):
        self.destination = destination
        self.date = date
        self.price = price
        self.scales = scales
        self.duration = duration


class flights_data:

    def __init__(self, driver, action, data_empty_array, atb_path):
        self.st = set()
        self.driver = driver
        self.action = action
        self.data = data_empty_array # Empty array of data of concrete length
        self.path = atb_path # Path to atributes
        self.ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        self.search_box = '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/input'



    def data_gather(self, destinations):
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
        atb_data = [[],[],[],[],[]]

        for i in range(len(self.path)):
            time.sleep(2)
            self.data[i] = self.driver.find_elements(By.XPATH, f'{self.path[i]}')
            # self.data[i] = WebDriverWait(self.driver,5,ignored_exceptions=self.ignored_exceptions).until(EC.presence_of_all_elements_located((By.XPATH, f'{self.path[i]}')))
            
            print('len data', len(self.data))
            print('len data[0]', len(self.data[0]))
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j].text != '':
                    atb_data[i].append(self.data[i][j].text)
        for  i in range(len(atb_data[0])): # data[0] = number of flights
            f = flight(atb_data[0][i], atb_data[1][i], atb_data[2][i], atb_data[3][i], atb_data[4][i])
            self.st.add(f)
                            















    def show_flights(self):
        ''' Prints flights '''
        print('Destination \t - \t Date \t - \t Price \t - \t Scales \t - \t Duration')
        for i in self.st:
            print(f'--> {i.destination} \t - \t {i.date} \t - \t {i.price} \t - \t {i.scales} \t - \t {i.duration}')





class movement:
    def __init__(self,driver,action):
        self.driver = driver
        self.action = action
        

    def zoom(self,button,n):
        for i in range(n):
            button.click()


    def move_left(self,t):
        endtime = time.time() + t
        
        while True:
            self.action.key_down(Keys.ARROW_LEFT).perform()
        
            if time.time() > endtime:
                self.action.key_up(Keys.ARROW_LEFT).perform()
                time.sleep(0.1)
                break    

    def move_right(self,t):
        endtime = time.time() + t
        
        while True:
            self.action.key_down(Keys.ARROW_RIGHT).perform()
        
            if time.time() > endtime:
                self.action.key_up(Keys.ARROW_RIGHT).perform()
                time.sleep(0.1)
                break    

    def move_up(self,t):
        endtime = time.time() + t
        
        while True:
            self.action.key_down(Keys.ARROW_UP).perform()
        
            if time.time() > endtime:
                self.action.key_up(Keys.ARROW_UP).perform()
                time.sleep(0.1)
                break    

    def move_down(self,t):
        endtime = time.time() + t
        
        while True:
            self.action.key_down(Keys.ARROW_DOWN).perform()
        
            if time.time() > endtime:
                self.action.key_up(Keys.ARROW_DOWN).perform()
                time.sleep(0.1)
                break    

    def jump_left(self,n):
        for i in range(n):
            self.action.send_keys(Keys.HOME)
        time.sleep(0.1)

    def jump_right(self,n):
        for i in range(n):
            self.action.send_keys(Keys.END)
        time.sleep(0.1)

    def jump_down(self,n):
        for i in range(n):
            self.action.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)

    def jump_up(self,n):
        for i in range(n):
            self.action.send_keys(Keys.PAGE_UP)
        time.sleep(0.1)


    def reload_flights(self,map_body):
        self.action.drag_and_drop_by_offset(map_body, -277, 0).perform()



class search:
    def __init__(self, driver, action):
        self.driver = driver
        self.action = action
        self.search_box = '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[1]/div[1]/section/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/input'



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
            

    def search_destinations(self, destinations):

        for i in range(2):
            time.sleep(1)
            self.driver.find_element(By.XPATH, self.search_box).click()     
            self.action.send_keys(destinations[i]).perform() 
            self.action.key_down(Keys.ENTER).perform()
            self.action.key_up(Keys.ENTER).perform() 
    

            # flight = int(WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH, fpath))).text.strip('€'))
            time.sleep(3)
            
            try:
                price = int(self.driver.find_element(By.XPATH, '//div[@class="EDKFBb QB2Jof SgNiff"]').text.strip('€'))
                    
            except:
                pass


            self.driver.find_element(By.XPATH, '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div/div/div[2]/div/div[2]/div[1]/button/div[1]').click()