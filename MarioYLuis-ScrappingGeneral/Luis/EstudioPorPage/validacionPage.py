from facebook_scraper import get_posts
from datetime import datetime
import pandas as pd


def getPostX(pagina, pages = 200):
    salida =  get_posts(pagina, pages=pages)       
    return salida


def getDataFromPage(pagina, pages = 200):
    return pd.DataFrame.from_dict(getPostX(pagina, pages))


def saveParaAnalisis(pagina, pages = 200):
    data = getDataFromPage(pagina, pages)
    now = datetime.now()
    nombreArchivo = pagina + now.strftime("%d-%m-%Y_%H-%M-%S") + ".csv"
    nombreArchivo = nombreArchivo.replace(" ","_")
    data.to_csv(nombreArchivo, index=False)
    return data