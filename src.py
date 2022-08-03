import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import collections



class data_gather:

    def __init__(self,driver,data_empty_array,atb_path):

        self.data = data_empty_array # Empty array of data of concrete length
        self.path = atb_path # Path to atributes
        self.driver = driver

        # Data gathering in a non-legible format
        for i in range(len(self.path)):
            self.data[i] = self.driver.find_elements(By.XPATH, f'{self.path[i]}')



    # Translation of non-legible format to text
    # Save all data in list of lists with following format---> 
    # ---> [[destinations], [dates], [prices], [scales], [duration]]
    def save_dataa(self, atb_data):

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j].text == '' or self.data[0][j] in atb_data[0]:
                    pass
                else:
                    atb_data[i].append(self.data[i][j].text)

        return atb_data


    def save_data(self, atb_data):

        # Save data just for first atributes (data[0][:])
        for i in range(len(self.data[0])):
            if self.data[0][i].text != '':
                atb_data[0].append(self.data[0][i].text)

        # Remove duplicates from translated atributes (atb_data[0])
        # This way, we limit the length of new elements to append

        '''
        Creo que esto solo sirve para el caso en el que los elementos repetidos se 
        añadan al final o en un determinado orden. No estoy seguro, pero convendría comprobar 
        algunas cosas antes de continuar.

        Pista: Ver cuanto es el len() de cada uno de los atributos. Ahí es donde está el mayor problema, 
        ya que anteriormente lo que hacía era detectar la posición de los duplicados en el atributo:destino,
        ya que en este atributo es en el únicoo que podemos comprobar duplicados, y más tarde hacía que 
        los índices en los que estuvieran esos duplicados en el array de destinos, no se agregaran a los
        demás arrays de los otros atributos.
        El problema de esto residía en que no todos los arrays tenían el mismo len(), por lo que 
        no servía de nada pasar de un índice a otro. Esto dificulta el trabajo con arrays paralelos, 
        ya que no te puedes basar en los índices.
        '''
        atb_data[0] = list(collections.OrderedDict.fromkeys(atb_data[0]))
        # data[0] without duplicates

        for i in range(1,len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j].text == '' or len(atb_data[i]) >= len(atb_data[0]):
                    pass
                else:
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