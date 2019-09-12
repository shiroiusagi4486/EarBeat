#Librerias a utilizar
import requests
import re
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import pandas as pd
from pandas.io.json import json_normalize
import json
print('beatscrap importado')

# Modelo de Machine Learning
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from numpy import genfromtxt
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
print('librerias de clusterizacion y machine learning cargadas')

#lectura de pulso cardiaco
import serial
import time
print('Fingerbeat importado y sanito')

#presentacion de la recomendación de cluster
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print('Earbeat ensamblado')


# # Beatscrap

# # Web scraping
def paginas():
    urls=[]
    while True:
        entrada = input("Hola, introduce el link de tu enlace de perfil de spotify, puedes introducir cualquier otra cosa para salir")
        if 'https://open.spotify.com/user/' in entrada:
            urls.append(entrada)
        else:
            break
    html =[requests.get(url).content for url in urls]
    usrs =[re.findall(r'\w*(?=\?)', url) for url in urls]
    usuariosID = [elemento[0] for elemento in usrs]
    playlists = [re.findall(r'\/playlist\/\w*', str(pagina)) for pagina in html]
    soups = [BeautifulSoup(pagina, 'lxml') for pagina in html]
    az = [soup.find_all('span',{'dir':'auto'}) for soup in soups]
    PlstName=[]
    nombres = []
    for etiquetas in az:
        limpio =[]
        for contenido in etiquetas:
            limpio.append(str(contenido).replace('<span dir="auto">', '').replace('</span>', ''))
        nombres.append(limpio[0])
        PlstName.append(limpio[1:])
    print('Obteniendo datos, no desesperes')
    listota = []
    diccionario = {}
    comprimido = zip(usuariosID, nombres, PlstName,playlists)
    for rar in comprimido:
        for p in range(len(rar[2])):
            diccionario= {'Id_usr':rar[0], 'Nombre_perfil':rar[1], 'PlaylistName':rar[2][p] ,'Id_playlist':rar[3][p]}
            listota.append(diccionario.copy())
    scrapdf = pd.DataFrame(listota)
    scrapdf.to_csv("./UsrPlay.csv", index = False)
    print('Scrap de paginas terminado, gracias por tus datos')
    return scrapdf

# # API Parsing
def musical(scrapdf):
    print('Hola nos estamos conectando a la API de Spotify')
    print('Espero no tardar con la obtencion de canciones de la lista que me has mandado, asi que no desesperes')
    CLIENT_ID = "2b7f57a2e7d74e43b0a0771a99fbb470"
    CLIENT_SECRET = "219cfd4ed31349d5b3175e3526de4921"

    credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)

    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)

    apiDF = pd.DataFrame({'href':[], 'items':[], 'limit':[], 'next':[], 'offset':[], 'previous':[], 'total':[]})
    dataframes = []
    for row in scrapdf.itertuples():
        canciones = spotify.user_playlist_tracks(row.Id_usr, str(row.Id_playlist).replace('/playlist/', ''))
        dataframes.append(pd.DataFrame(canciones))
    print('He terminado con obtención de canciones')
    apiDF = pd.concat(dataframes)
    apiDF.reset_index(inplace = True)
    candionero2 = json_normalize(apiDF['items'])
    dfinal = candionero2[['track.name', 'track.external_urls.spotify', 'track.href', 'track.id'  ,'track.popularity']]
    dfinal.drop_duplicates(inplace = True)
    dfinal.dropna(inplace = True)
    dfinal.to_csv("./SpotifyApi.csv", index = False)
    return dfinal

#Caracteristicas de las canciones estraidas directo del API de spotify
def caracteristicas(dfinal):
    CLIENT_ID = "2b7f57a2e7d74e43b0a0771a99fbb470"
    CLIENT_SECRET = "219cfd4ed31349d5b3175e3526de4921"

    credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)

    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)
    
    print('Comenzando con la obtencion de caracteristicas de cada canción de tus listas')
    df = pd.DataFrame(columns=['danceability',
                               'energy',
                               'key',
                               'loudness',
                               'mode',
                               'speechiness',
                               'acousticness',
                               'instrumentalness',
                               'liveness',
                               'valence',
                               'tempo',
                               'type',
                               'id',
                               'uri',
                               'track_href',
                               'analysis_url',
                               'duration_ms',
                               'time_signature'])
    
    n=0
    for ide in dfinal['track.id']: 
        elemento = spotify.audio_features(ide)
        anexado = pd.DataFrame(elemento[0].values())
        anexado = anexado.T
        anexado.columns = elemento[0].keys()
        df =df.append(anexado)
        n+=1
        print('Elemento:', n, ' de ', len(dfinal['track.id']))
    print('Obtencion de características Terminada, muchas gracias por tu paciencia')

    df.to_csv("./caracteristicas.csv", index = False)
    print('Fin de BEATSCRAP')
    return df


# # Earlearning

#Construccion del modelo Para machine learning
def modeloreja(csv):
    modelo = csv.drop(columns = ['type', 'uri', 'track_href', 'analysis_url', 'duration_ms','time_signature'], axis = 1)
    modelo.reset_index(inplace = True)
    modelo.set_index('id', inplace = True)
    modelo = modelo.astype('float64')
    return modelo

#gráfico de dendograma y KElbow ilustrativos
def dendo(modelo):
    dendogram = modelo.copy()
    weighted = linkage(dendogram, method='weighted')

    print('weighted')
    fig = plt.figure(figsize=(25, 10))
    weightedplt = dendrogram(
        weighted,
        truncate_mode = 'lastp',
        p=12)
    plt.show()

    calinski_harabasz = KMeans()
    visualizer = KElbowVisualizer(calinski_harabasz, k=(2, 20), metric='calinski_harabasz')
    visualizer.fit(weighted)
    visualizer.poof();


#Clusterizacion y entrenamiento del modelo usando kmeans, tambien imprimimos metricas ilustrativas
def kmean(modelo):
    meansK12 = modelo.copy()
    kmeans12 = KMeans(n_clusters=25)
    spoty_clusters12 = kmeans12.fit(meansK12)
    print('Centros')
    print(spoty_clusters12.cluster_centers_)
    print()
    #predicciones para el modelo
    predictions12 = spoty_clusters12.fit_predict(meansK12)
    print('Predicciones')
    print(predictions12)
    print()
    #Distancias entre cada prediccion
    distances12 = spoty_clusters12.fit_transform(meansK12)
    print('Distancias')
    print(distances12)
    #creamos nueva columna con las predicciones 
    meansK12['Cluster12'] = predictions12
    meansK12.reset_index(inplace = True)
    meansK12.to_csv("./clusterizado.csv", index = False)
    #agrupamos el dataframe pormedio de la columna cluster12, y usamos el promedio del tempo, para crear una serie
    serie = meansK12.groupby(['Cluster12'])['tempo'].mean()
    return serie, meansK12


# # FingerBeat

#lectura e impresion de pulsos desde el dedo
def dedito():
    print('Comenzaremos a recolectar algunas lecturas de frecuencia cardiaca, si no se recolectan, es debido a que algo interfiere con nuestra lectura')
    arduino = serial.Serial('COM3', 9600)
    time.sleep(2)
    pulsos = np.array([], dtype = float)
    n=0

    while n <2500:
        try:
            a = float(arduino.readline())
            if a>= 60.0 and a<=200.0:
                print('pulso: ',n , 'leido: ' ,a)
                pulsos = np.append(pulsos, a)
                n+=1
        except:
            pass
    print('Lectura Finalizada, muchas gracias por esperar')
    return pulsos.mean()


# # Earbeat

#Generacion de recomendacion por primera vez
def recomendacion(dedopromedio, terminado, recomendacion, original):
    print('Generaremos las recomendaciones usando los resultados obtenidos de tus canciones y Frecuencia cardiaca')
    terminado.to_csv("./terminado.csv", index = False)
    recomendacion.to_csv("./recomendacion.csv", index = False)
    
    reformado = np.array([], dtype = float)
    for lectura in terminado:
        reformado = np.append(reformado, abs(lectura - dedopromedio))
    cercanocero = reformado.min()
    cluster = 0
    for indice in range(len(reformado)):
        if reformado[indice]== cercanocero:
            cluster= indice
    recomendacion = recomendacion[recomendacion['Cluster12'] == cluster]
    recomendacion = recomendacion.rename(columns = {'id':'track.id'})
    href = pd.merge(original, recomendacion, on='track.id', how='left')
    href.dropna(inplace = True)
    external = href['track.external_urls.spotify']
    return external


#Creamos nuevas recomendaciones usamos modelos ya creados
def nuevaRec(dedopromedio):
    print('Generaremos las recomendaciones usando los resultados obtenidos de tus canciones y Frecuencia cardiaca')
    terminado = genfromtxt("./terminado.csv", delimiter=',')
    recomendacion_csv = pd.read_csv("./recomendacion.csv")
    original_csv = pd.read_csv('./SpotifyApi.csv')
    
    recomendacion = pd.DataFrame(recomendacion_csv)
    original= pd.DataFrame(original_csv)
    
    reformado = np.array([], dtype = float)
    for lectura in terminado:
        reformado = np.append(reformado, abs(lectura - dedopromedio))

    cercanocero = reformado.min()
    cluster = 0
    for indice in range(len(reformado)):
        if reformado[indice]== cercanocero:
            cluster= indice
    recomendacion = recomendacion[recomendacion['Cluster12'] == cluster]
    recomendacion = recomendacion.rename(columns = {'id':'track.id'})

    href = pd.merge(original, recomendacion, on='track.id', how='left')
    href.dropna(inplace = True)

    external = href['track.external_urls.spotify']
    return external

def presentacion(external):
    driver = webdriver.Chrome()
    driver.get('https://open.spotify.com')
    driver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div[1]/nav/div[2]/div/p[2]/button").click()
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div/a").click()
    time.sleep(1)

    usr=''
    pwd=''

    username_box = driver.find_element_by_id('email') 
    username_box.send_keys(usr) 
    print ("Email Id entered") 
    time.sleep(1) 

    password_box = driver.find_element_by_id('pass') 
    password_box.send_keys(pwd) 
    print ("Password entered") 

    login_box = driver.find_element_by_id('loginbutton') 
    login_box.click()
    print ("Done") 

    aleatorio = random.sample(list(external), k=10)

    for url in aleatorio:
        driver.get(url)
        time.sleep(120)

    driver.quit()
