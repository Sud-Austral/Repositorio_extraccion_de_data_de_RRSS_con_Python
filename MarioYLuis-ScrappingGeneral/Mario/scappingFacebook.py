from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import pandas as pd
import numpy as np
import pandas as pd
from facebook_scraper import get_posts
from datetime import datetime
import cargaEnlaces as cE


def Final(pagina,n):
    data = getComentarios(pagina,n)
    saveCSV(data,pagina)
    return data

def comentarioPorLugar(lugar,top,posts):
    datos = []
    driver = getDriver()
    for i in getPaginaFacebook(lugar,top):
        datos.append(getComentarios(i,posts, driver))
    data = pd.concat(datos)
    saveCSV(data,lugar)
    return datos


def getPaginaFacebook(lugar,top):
    salida = []
    for i in cE.cargarEnlacesLugar(lugar):
        if len(i) > 0:
            salida.append(i.replace("https://www.facebook.com/","").replace("/",""))
    return salida[:top]


def getPostTopico(lista,text):
    resultado=0
    for palabra in lista:
        if palabra in text:
            resultado = 1
                
    return resultado


def getPost(pagina, n):
    salida = []
    lista = ["covid","pandemia","Coronavirus","COVID"]
    
    for post in get_posts(pagina, pages=n, credentials=("informaticasudaustral@gmail.com","Info.Sud91")):
        if type(post["post_url"]) == str:
                #print(type(post["post_url"]))
                #salida.append(post["post_url"].replace("m.facebook","www.facebook"))
                post["Nombre"] = pagina
                filtro = getPostTopico(lista,str(post["text"]))
                if  filtro == 1:
                    salida.append(post)
                
                        
    return salida[:n]



            
def cambiarWWW(url):
    return url.replace("m.facebook","www.facebook")

def agregarPostInfo(data,post):
    data["post_id"] = post["post_id"]
    data["Texto post"] = post["text"]
    data["Texto post 2"] = post["post_text"]
    data["Texto compartido"] = post["shared_text"]
    data["Hora de posteo"] = post["time"]
    data["Imagen"] = post["image"]
    data["Likes del post"] = post["likes"]
    data["Comentarios del Post"] = post["comments"]
    data["Compartido"] = post["shares"]
    data["URL"] = post["post_url"]
    data["Link"] = post["link"]
    data["Hora consulta"] = datetime.now()
    data["Nombre Facebook"] = post["Nombre"]
    return data

def getDriver():
    driver = webdriver.Firefox()
    driver.set_page_load_timeout("60")
    driver.get("https://www.facebook.com")

    driver.find_element_by_name("email").send_keys("informaticasudaustral@gmail.com")
    driver.find_element_by_name("pass").send_keys("Info.Sud91")

    driver.find_element_by_id("loginbutton").click()
    #driver.set_page_load_timeout("60")
    return driver

def getComentarios(pagina,n, driver):
    datos = []
    #driver = getDriver()
    
    for i in getPost(pagina,n):
        datos.append(comentarioPost2(driver,i))
    return pd.concat(datos)

def saveCSV(data,lugar):
    now = datetime.now()
    nombreArchivo = lugar + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
    print("Se guardaron los datos en " + nombreArchivo)
    data.to_csv(nombreArchivo, index=False)

def comentarioPost2(driver, post):
    #driver.get("https://www.facebook.com/story.php?story_fbid=10157425418460895&id=313191260894")
    url = cambiarWWW(post["post_url"])
    driver.get(url)
    driver.set_page_load_timeout("60")
    time.sleep(3)
    flag  = 1
    while flag < 8:
    #while exit == "Message: Unable to locate element: ._4sxc":
        try:
            #driver.find_element_by_class_name("_4sxc _42ft").click()
            driver.find_element_by_class_name("_4sxc").click()
            #print("Hola")
        except Exception as e:
            #print(e)
            #print("Oops! ",sys.exc_info()[0]," occured.")
            flag = flag + 1        
    hola = "ola"  
    Xpath = "/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[2]/form/div/div[3]/ul/li"
    comentario = []
    likes = []
    hora = []
    for i in driver.find_elements_by_xpath(Xpath):
        try:
            maduro = i.find_element_by_class_name("_72vr")
            #print(i.find_element_by_class_name("livetimestamp").text)
            #print("Comentario:" + maduro.text)
            comentario.append(maduro.text)
            try:
                like = i.find_element_by_class_name("_1lld")
                likes.append(like.text)
                #print("Likes: " + like.text)
            except:
                likes.append("0")
                #print("Likes: " +"0")
            #print("Hora: " + i.find_element_by_class_name("livetimestamp").text)
            hora.append(i.find_element_by_class_name("livetimestamp").text)
            #print("_________________________________________________________________________________")
            #parent_ID = numeroId
            #numeroId = numeroId + 1
            try:
                subcomentarios = i.find_element_by_class_name("_2h2j")

                for j in range(len(subcomentarios.find_elements_by_class_name("_6c7i"))):
                    #print(str(j))
                    aux = subcomentarios.find_elements_by_class_name("_6c7i")[j]
                    maduro = aux.find_element_by_class_name("_72vr")
                    #print("Comentario:" + maduro.text)
                    comentario.append(maduro.text)
                    try:
                        like = aux.find_element_by_class_name("_1lld")
                        likes.append(like.text)
                        #print("Likes: " + like.text)
                    except:
                        likes.append("0")
                        #print("Likes: " +"0")
                    
                    aux = subcomentarios.find_elements_by_class_name("livetimestamp")[j]
                    #print("Hora: " + aux.text)
                    hora.append(aux.text)
                    #print("////////////////////////////////////////////////////////////////////////////////")
                    #numeroId = numeroId + 1
                    #numeroId = numeroId + 1
                        #print("0")
                    #print("///////////////////////////////////////////////////////////////////////////////////")
                #print(subcomentarios.text)
            except:
                print("sin subtextos")
        except:
            print("error")
            
    data = pd.DataFrame({
        "comentario":comentario,
        "likes":likes,
        "hora": hora
    })
    return agregarPostInfo(data,post)



#*************************************************TEST*********************************************************************************************************
def comentario(url):
    driver = webdriver.Firefox()
    driver.set_page_load_timeout("60")
    driver.get("https://www.facebook.com")

    driver.find_element_by_name("email").send_keys("informaticasudaustral@gmail.com")
    driver.find_element_by_name("pass").send_keys("Info.Sud91")

    driver.find_element_by_id("loginbutton").click()
    driver.set_page_load_timeout("60")

    #driver.get("https://www.facebook.com/story.php?story_fbid=10157425418460895&id=313191260894")
    driver.get(url)
    driver.set_page_load_timeout("60")
    time.sleep(5)
    flag  = 1
    exit = ""
    while flag < 8:
    #while exit == "Message: Unable to locate element: ._4sxc":
        try:
            #driver.find_element_by_class_name("_4sxc _42ft").click()
            driver.find_element_by_class_name("_4sxc").click()
            #print("Hola")
        except Exception as e:
            exit = e
            #print(e)
            #print("Oops! ",sys.exc_info()[0]," occured.")
            flag = flag + 1        
    hola = "ola"  
    Xpath = "/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[2]/form/div/div[3]/ul/li"
    comentario = []
    likes = []
    lista_id = []
    lista_parent_id = []
    hora = []

    numeroId = 1
    for i in driver.find_elements_by_xpath(Xpath):
        #lista_id.append(numeroId)
        #numeroId = numeroId + 1
        try:
            #print("ID " + str(numeroId))
            lista_id.append(numeroId)
            #print("Parent_ID " + str(0))
            lista_parent_id.append(0)
            maduro = i.find_element_by_class_name("_72vr")
            #print(i.find_element_by_class_name("livetimestamp").text)
            #print("Comentario:" + maduro.text)
            comentario.append(maduro.text)
            try:
                like = i.find_element_by_class_name("_1lld")
                likes.append(like.text)
                #print("Likes: " + like.text)
            except:
                likes.append("0")
                #print("Likes: " +"0")
            #print("Hora: " + i.find_element_by_class_name("livetimestamp").text)
            hora.append(i.find_element_by_class_name("livetimestamp").text)
            #print("_________________________________________________________________________________")
            parent_ID = numeroId
            numeroId = numeroId + 1
            try:
                subcomentarios = i.find_element_by_class_name("_2h2j")
                
                #print(str(len(subcomentarios.find_elements_by_class_name("_6c7i"))))
                #print(str(len(subcomentarios.find_elements_by_class_name("livetimestamp"))))
                    
                #for j in subcomentarios.find_elements_by_class_name("livetimestamp"):
                    #print(j.text)
                for j in range(len(subcomentarios.find_elements_by_class_name("_6c7i"))):
                    #print(str(j))
                    aux = subcomentarios.find_elements_by_class_name("_6c7i")[j]
                    maduro = aux.find_element_by_class_name("_72vr")
                    #print("ID " + str(numeroIderoId))
                    #print("ID " + str(numeroId))
                    lista_id.append(numeroId)
                    #print("Parent_ID " + str(parent_ID))
                    lista_parent_id.append(parent_ID)
                    #print("Comentario:" + maduro.text)
                    comentario.append(maduro.text)
                    try:
                        like = aux.find_element_by_class_name("_1lld")
                        likes.append(like.text)
                        #print("Likes: " + like.text)
                    except:
                        likes.append("0")
                        #print("Likes: " +"0")
                    
                    aux = subcomentarios.find_elements_by_class_name("livetimestamp")[j]
                    #print("Hora: " + aux.text)
                    hora.append(aux.text)
                    #print("////////////////////////////////////////////////////////////////////////////////")
                    numeroId = numeroId + 1
                    #numeroId = numeroId + 1
                        #print("0")
                    #print("///////////////////////////////////////////////////////////////////////////////////")
                #print(subcomentarios.text)
                #for j in subcomentarios.text.split("\n"):
                    #print(j)
                    #print("///////////////////////////////////////////////////////////////////////////////////")
            except:
                print("sin subtextos")
        except:
            print("error")
            
    data = pd.DataFrame({
        "comentario":comentario,
        "likes":likes,
        "id": lista_id,
        "id_padre":lista_parent_id,
        "hora": hora
    })
    driver.close()
    return data


def comentario2(url, driver):
    #driver.get("https://www.facebook.com/story.php?story_fbid=10157425418460895&id=313191260894")
    driver.get(url)
    driver.set_page_load_timeout("60")
    time.sleep(3)
    flag  = 1
    while flag < 8:
    #while exit == "Message: Unable to locate element: ._4sxc":
        try:
            #driver.find_element_by_class_name("_4sxc _42ft").click()
            driver.find_element_by_class_name("_4sxc").click()
            #print("Hola")
        except Exception as e:
            #print(e)
            #print("Oops! ",sys.exc_info()[0]," occured.")
            flag = flag + 1        
    hola = "ola"  
    Xpath = "/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[2]/form/div/div[3]/ul/li"
    comentario = []
    likes = []
    lista_id = []
    lista_parent_id = []
    hora = []

    numeroId = 1
    for i in driver.find_elements_by_xpath(Xpath):
        try:
            #print("ID " + str(numeroId))
            lista_id.append(numeroId)
            #print("Parent_ID " + str(0))
            lista_parent_id.append(0)
            maduro = i.find_element_by_class_name("_72vr")
            #print(i.find_element_by_class_name("livetimestamp").text)
            #print("Comentario:" + maduro.text)
            comentario.append(maduro.text)
            try:
                like = i.find_element_by_class_name("_1lld")
                likes.append(like.text)
                #print("Likes: " + like.text)
            except:
                likes.append("0")
                #print("Likes: " +"0")
            #print("Hora: " + i.find_element_by_class_name("livetimestamp").text)
            hora.append(i.find_element_by_class_name("livetimestamp").text)
            #print("_________________________________________________________________________________")
            parent_ID = numeroId
            numeroId = numeroId + 1
            try:
                subcomentarios = i.find_element_by_class_name("_2h2j")

                for j in range(len(subcomentarios.find_elements_by_class_name("_6c7i"))):
                    #print(str(j))
                    aux = subcomentarios.find_elements_by_class_name("_6c7i")[j]
                    maduro = aux.find_element_by_class_name("_72vr")
                    #print("ID " + str(numeroIderoId))
                    #print("ID " + str(numeroId))
                    lista_id.append(numeroId)
                    #print("Parent_ID " + str(parent_ID))
                    lista_parent_id.append(parent_ID)
                    #print("Comentario:" + maduro.text)
                    comentario.append(maduro.text)
                    try:
                        like = aux.find_element_by_class_name("_1lld")
                        likes.append(like.text)
                        #print("Likes: " + like.text)
                    except:
                        likes.append("0")
                        #print("Likes: " +"0")
                    
                    aux = subcomentarios.find_elements_by_class_name("livetimestamp")[j]
                    #print("Hora: " + aux.text)
                    hora.append(aux.text)
                    #print("////////////////////////////////////////////////////////////////////////////////")
                    numeroId = numeroId + 1
                    #numeroId = numeroId + 1
                        #print("0")
                    #print("///////////////////////////////////////////////////////////////////////////////////")
                #print(subcomentarios.text)
            except:
                print("sin subtextos")
        except:
            print("error")
            
    data = pd.DataFrame({
        "comentario":comentario,
        "likes":likes,
        "id": lista_id,
        "id_padre":lista_parent_id,
        "hora": hora
    })
    #driver.close()
    return data


def comentarioPost(driver, post):
    #driver.get("https://www.facebook.com/story.php?story_fbid=10157425418460895&id=313191260894")
    url = cambiarWWW(post["post_url"])
    driver.get(url)
    driver.set_page_load_timeout("60")
    time.sleep(3)
    flag  = 1
    while flag < 8:
    #while exit == "Message: Unable to locate element: ._4sxc":
        try:
            #driver.find_element_by_class_name("_4sxc _42ft").click()
            driver.find_element_by_class_name("_4sxc").click()
            #print("Hola")
        except Exception as e:
            #print(e)
            #print("Oops! ",sys.exc_info()[0]," occured.")
            flag = flag + 1        
    hola = "ola"  
    Xpath = "/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[2]/form/div/div[3]/ul/li"
    comentario = []
    likes = []
    lista_id = []
    lista_parent_id = []
    hora = []

    numeroId = 1
    for i in driver.find_elements_by_xpath(Xpath):
        try:
            #print("ID " + str(numeroId))
            lista_id.append(numeroId)
            #print("Parent_ID " + str(0))
            lista_parent_id.append(0)
            maduro = i.find_element_by_class_name("_72vr")
            #print(i.find_element_by_class_name("livetimestamp").text)
            #print("Comentario:" + maduro.text)
            comentario.append(maduro.text)
            try:
                like = i.find_element_by_class_name("_1lld")
                likes.append(like.text)
                #print("Likes: " + like.text)
            except:
                likes.append("0")
                #print("Likes: " +"0")
            #print("Hora: " + i.find_element_by_class_name("livetimestamp").text)
            hora.append(i.find_element_by_class_name("livetimestamp").text)
            #print("_________________________________________________________________________________")
            parent_ID = numeroId
            numeroId = numeroId + 1
            try:
                subcomentarios = i.find_element_by_class_name("_2h2j")

                for j in range(len(subcomentarios.find_elements_by_class_name("_6c7i"))):
                    #print(str(j))
                    aux = subcomentarios.find_elements_by_class_name("_6c7i")[j]
                    maduro = aux.find_element_by_class_name("_72vr")
                    #print("ID " + str(numeroIderoId))
                    #print("ID " + str(numeroId))
                    lista_id.append(numeroId)
                    #print("Parent_ID " + str(parent_ID))
                    lista_parent_id.append(parent_ID)
                    #print("Comentario:" + maduro.text)
                    comentario.append(maduro.text)
                    try:
                        like = aux.find_element_by_class_name("_1lld")
                        likes.append(like.text)
                        #print("Likes: " + like.text)
                    except:
                        likes.append("0")
                        #print("Likes: " +"0")
                    
                    aux = subcomentarios.find_elements_by_class_name("livetimestamp")[j]
                    #print("Hora: " + aux.text)
                    hora.append(aux.text)
                    #print("////////////////////////////////////////////////////////////////////////////////")
                    numeroId = numeroId + 1
                    #numeroId = numeroId + 1
                        #print("0")
                    #print("///////////////////////////////////////////////////////////////////////////////////")
                #print(subcomentarios.text)
            except:
                print("sin subtextos")
        except:
            print("error")
            
    data = pd.DataFrame({
        "comentario":comentario,
        "likes":likes,
        "id": lista_id,
        "id_padre":lista_parent_id,
        "hora": hora
    })
    #driver.close()    
    return agregarPostInfo(data,post)