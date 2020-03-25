#Cargar librerias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from typing import List, Tuple, Dict, TextIO
import array


def cargarEnlacesLugar(lugar):
    driver = webdriver.Firefox()
    driver.set_page_load_timeout("60")
    driver.get("https://www.facebook.com")

    driver.find_element_by_name("email").send_keys("informaticasudaustral@gmail.com")
    driver.find_element_by_name("pass").send_keys("Info.Sud91")

    driver.find_element_by_id("loginbutton").click()
    driver.set_page_load_timeout("60")

    lugar.replace(" ","%20")
    driver.get("https://www.facebook.com/search/places/?q="+str(lugar)+"&epa=SERP_TAB")
    driver.set_page_load_timeout("60")
    #arr = array.array('i')
    listas = []
    #contador = 0
    #paginas = 2
    #while contador < paginas:
     #   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      #  time.sleep(5)
       # contador+=1

    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    for i in driver.find_elements_by_class_name("_1wu_"):
        tag = i.find_element_by_tag_name("a")
        salida = tag.get_attribute("href")
        listas.append(str(salida))
        
    
        for j in salida.split("\n"):
            j = j.replace("Responder","").replace(" ·  · ","")
            j = j.replace("Escribe una respuesta...","")
            j = j.replace('Está seleccionada la opción "Más relevantes", por lo que es posible que algunas respuestas se hayan filtrado.',"")
            j = j.replace('Presiona "Enter" para publicar.',"")
            if(len(j) > 0):
                print(str(len(j)))

                print(j)
                print("*********************************************************************************************")
        print("--------------------------------------------------------------------------------------------------")
   
    return listas



