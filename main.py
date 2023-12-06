import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from time import sleep
import tkinter as tk
from tkinter import ttk

# Configuración global
TWITTER_URL = 'https://www.twitter.com'
USERNAME = 'roberwianitxas'  
PASSWORD = 'Nuncameacuerdo123'
PERFIL_ANALIZAR = 'FlagsMashupBot'

# Configuración de XPaths
cookies_button_xpath = "//span[contains(text(),'Aceptar todas las cookies')]"
login_button_xpath = '//*[text()="Iniciar sesión"]'
user_field_xpath = "//input[@name='text' and @autocomplete='username']"
password_field_xpath = "//input[@name='password' and @autocomplete='current-password']"
analized_user_xpath = "//div[@data-testid='UserProfileHeader_Items']"
followers_xpath = "//a[contains(@href,'/verified_followers')]//span[1]"
following_xpath = "//a[contains(@href,'/following')]//span[1]"
tweets_xpath =  "//div[contains(text(),'posts')]"
tweet_xpath = "//a[.//time]"
reply_xpath = "//article[@data-testid='tweet']"
load_more_button_xpath = "//button[text()='Show more replies']"
xpath_cuenta_verificada = "//div[@aria-label='Provides details about verified accounts.']"
xpath_descripcion = "//div[@data-testid='UserDescription']"
creation_date_xpath = "//span[@data-testid='UserJoinDate']"


# Funciones auxiliares
def random_sleep():
    sleep(random.randint(1, 5))

def convert_to_absolute_number(text):
    if 'K' in text.upper():
        return int(float(text.replace('K', '').replace(',', '.')) * 1000)
    elif 'M' in text.upper():
        return int(float(text.replace('M', '').replace(',', '.')) * 1000000)
    else:
        return int(text.replace(',', ''))

def es_posible_bot(usuario, followers, following, tweets, cuenta_verificada, description, year, month):
    umbral = 1
    puntaje = 0

    if cuenta_verificada: #Si la cuenta está verificada, no es un bot
        return False
    
    elif 'bot' in usuario.lower(): # Si el nombre de usuario contiene la palabra "bot", es un bot
        return True
    
    else:
        # Criterio 1: Proporción de seguidores a seguidos
        if following > 0 and followers / following < 0.1:
            puntaje += 0.5

        # Criterio 2: Número muy bajo de seguidores y muy alto de seguidos
        if followers < 50 and following > 100:
            puntaje += 0.25

        # Criterio 3: Número muy alto de tweets (esto podría indicar actividad automatizada)
        if followers < 200 and tweets > 10000:
            puntaje += 0.5
            if year == datetime.datetime.now().year:
                return True
        
        if year == datetime.datetime.now().year:
            puntaje += 0.5
            if month == datetime.datetime.now().month:
                puntaje += 0.25

        if description == False:
            puntaje += 0.5

        # Comprueba si el puntaje supera el umbral
        return puntaje >= umbral

# Inicio del script Selenium
driver = webdriver.Chrome()

try:
    # Abre Twitter y acepta cookies
    driver.get(TWITTER_URL)
    random_sleep()
    cookies_accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cookies_button_xpath)))
    cookies_accept_button.click()
    random_sleep()

    # Iniciar sesión
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_button_xpath))).click()
    random_sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, user_field_xpath))).send_keys(USERNAME + Keys.RETURN)
    random_sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, password_field_xpath))).send_keys(PASSWORD + Keys.RETURN)
    random_sleep()

    # Navegar al perfil y analizar seguidores
    driver.get(f'{TWITTER_URL}/{PERFIL_ANALIZAR}')
    random_sleep()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, analized_user_xpath)))
    random_sleep()

    try:
        cuenta_verificada = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_cuenta_verificada)))
        if cuenta_verificada:
            print("La cuenta está verificada.")
    except:
        cuenta_verificada = False
        print("La cuenta no está verificada o no se pudo verificar.")

    try:
        descripcion = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_descripcion)))
        if descripcion:
            print("La cuenta tiene descripción.")
    except:
        descripcion = False

    elemento_creation_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, creation_date_xpath))).text.split('Joined ')[1]
    cretation_date = time.strptime(elemento_creation_date, '%B %Y')
    year = cretation_date.tm_year
    month = cretation_date.tm_mon
    print("Fecha de creación de la cuenta:", cretation_date)

    followers = convert_to_absolute_number(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, followers_xpath))).text)
    following = convert_to_absolute_number(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, following_xpath))).text)
    elemento_tweets = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tweets_xpath)))
    texto_tweets = elemento_tweets.text.split(" posts")[0]
    tweets = convert_to_absolute_number(texto_tweets)
    if es_posible_bot(PERFIL_ANALIZAR, followers, following, tweets, cuenta_verificada, descripcion, year, month):
        print(f'El perfil {PERFIL_ANALIZAR} podría ser un bot.')
    else:
        print(f'El perfil {PERFIL_ANALIZAR} parece ser un usuario real.')


    # Navegar al tweet más reciente y recoger usuarios que comentaron
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tweet_xpath))).click()
    random_sleep()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, reply_xpath)))

    # Desplazarse hacia abajo en la página para cargar más comentarios
    SCROLL_PAUSE_TIME = 4  # Pausa en segundos
    # Obtener altura inicial de la página
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Desplazarse hacia abajo de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Esperar a que cargue la página
        time.sleep(SCROLL_PAUSE_TIME)
        # Calcular nueva altura de scroll y comparar con la altura anterior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Si la altura no cambió, se alcanzó el final de la página
        last_height = new_height

    # Cargar más comentarios si los hubiera
    try:
        load_more_button = driver.find_element(By.XPATH, load_more_button_xpath)
        load_more_button.click()
        time.sleep(SCROLL_PAUSE_TIME)
    except Exception as e:
        pass  # No hay más botones para cargar contenido

    usuarios_comentarios = set()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, reply_xpath)))
    comentarios = driver.find_elements(By.XPATH, reply_xpath)
    for comentario in comentarios:
        usuario = comentario.find_element(By.XPATH, ".//span[contains(text(), '@')]").text.lstrip('@') # Elimina el símbolo '@'
        if usuario not in usuarios_comentarios:
                usuarios_comentarios.add(usuario)
    print("Usuarios que comentaron el tweet:", usuarios_comentarios)

    # Analizar cada perfil de usuario
    bots_sospechosos = []
    for usuario in usuarios_comentarios:
        driver.get(f'{TWITTER_URL}/{usuario}')
        random_sleep()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='UserProfileHeader_Items']")))
        random_sleep()
        followers = convert_to_absolute_number(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, followers_xpath))).text)
        following = convert_to_absolute_number(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, following_xpath))).text)
        elemento_tweets = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tweets_xpath)))
        texto_tweets = elemento_tweets.text.split(" posts")[0]
        tweets = convert_to_absolute_number(texto_tweets)
        try:
            cuenta_verificada = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_cuenta_verificada)))
        except:
            cuenta_verificada = False
        try:
            descripcion = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_descripcion)))
        except:
            descripcion = False
        if es_posible_bot(usuario, followers, following, tweets, cuenta_verificada, descripcion):
            bots_sospechosos.append(usuario)
    print("Usuarios sospechosos de ser bots:", bots_sospechosos) #TODO - Mostrar en una ventana de Tkinter

except Exception as e:
    print(f"Se produjo un error: {e}")

finally:
    driver.quit()
