import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



class data_gather:

    def __init__(self,driver,data_empty_array,atb_path):

        self.data = data_empty_array # Empty array of data of concrete length
        self.path = atb_path # Path to atributes
        self.driver = driver

        # Data gathering in a non-legible format
        for i in range(len(self.path)):
            self.data[i] = self.driver.find_elements(By.XPATH, f'{self.path[i]}')



    # Translation of non-legible format
    # Save all data in list of lists with following format---> 
    # ---> [[destinations], [dates], [prices], [scales], [duration]]
    def save_data(self, atb_data):

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j].text != '':
                    atb_data[i].append(self.data[i][j].text)

        return atb_data



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