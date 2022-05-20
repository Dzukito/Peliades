import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import STOPWORDS, WordCloud, ImageColorGenerator

import datetime
from sys import argv #argumentos para pasarle al programa
import argparse
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
otx = OTXv2("48d217cf542e4b126274d68ce7ae06e78291ef68887540d032c6fe5c80c254c0")






def nube(textoANube,palab):
  # Generar nube
  stopwords = STOPWORDS
  mask = np.array(Image.open("./alien.png"))
  wordcloud1 = WordCloud(stopwords=stopwords, max_words=palab, mask=mask,min_font_size=5).generate(textoANube)

  # crear imagen
  image_colors = ImageColorGenerator(mask)
  plt.figure(figsize=[15,15])
  plt.imshow(wordcloud1.recolor(color_func=image_colors), interpolation="bilinear")
  plt.axis("off")

  # guardar
  plt.savefig("./alienTrends.png", format="png")



def obtenerTendencias(dia,mes,anio,palabras):
  noticias = otx.getall(modified_since=anio+"-"+mes+"-"+dia+" 00:00:00")
  
  todosLosTags=[]
  for noticia in noticias:
    tagsNoticia=noticia.get("tags")
    todosLosTags.extend(tagsNoticia)

  tagsEnTexto = ' '.join(todosLosTags)
  nube(tagsEnTexto,palabras)






def parseArguments():
    parser= argparse.ArgumentParser()
    parser.add_argument("-w", type=int, nargs=1, help="Cantidad de palabras")
    parser.add_argument("--today", action= 'store_true', help="Tendencias de hoy")
    parser.add_argument("--thismonth",action= 'store_true', help="Tendencias del mes")
    parser.add_argument("--thisyear", action= 'store_true', help="Tendencias del anio. WARNING: Esta funcion puede demorar dependiendo la cantidad de noticias")



    parser.print_help()
    return parser.parse_args()

def banner():
    textoBaner= '''      
    ____  __     _           __         
   / __ \/ /__  (_)___ _____/ /__  _____
  / /_/ / / _ \/ / __ `/ __  / _ \/ ___/
 / ____/ /  __/ / /_/ / /_/ /  __(__  ) 
/_/   /_/\___/_/\__,_/\__,_/\___/____/ 
      AlienVault Trends Visualization  
                                                                                                                                                                     
    '''


    print("{}".format(textoBaner))
    
#__________________________________________________________________________________________________________________________
banner()
args= parseArguments()

#Default values
anio=str(datetime.datetime.today().year)
palabras=20

if(args.w):
  print("[Pleiades]: Se modifico la cantidad de palabras.")
  palabras=args.w[0]

if(args.today):
    print("[Pleiades]: Buscando tendencias de hoy...")
    dia=str(datetime.datetime.today().day)
    mes=str(datetime.datetime.today().month)
    obtenerTendencias(dia,mes,anio,palabras)
    print("[Pleiades]: Visualización creada")

if(args.thismonth):
    print("[Pleiades]: Buscando tendencias del mes...")
    dia="01"
    mes=str(datetime.datetime.today().month-1)
    obtenerTendencias(dia,mes,anio,palabras)
    print("[Pleiades]: Visualización creada")
if(args.thisyear):
    print("[Pleiades]: Buscando tendencias del año...")
    dia="01"
    mes="01"
    obtenerTendencias(dia,mes,anio,palabras)
    print("[Pleiades]: Visualización creada")




