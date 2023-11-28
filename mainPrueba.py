from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from time import sleep

# Función para esperar un tiempo aleatorio entre 1 y 5 segundos
def random_sleep():
    sleep(random.randint(1, 5))

# Función para convertir números de Twitter a números absolutos
def convert_to_absolute_number(text):
    if 'K' in text:
        # Reemplaza la coma por un punto para manejar decimales, elimina la 'K' y multiplica por 1,000
        return int(float(text.replace('K', '')) * 1000)
    elif ',' in text:
        # Reemplaza la coma 
        return int(float(text.replace(',', '')))
    elif 'M' in text:
        # Reemplaza la coma por un punto para manejar decimales, elimina la 'M' y multiplica por 1,000,000
        return int(float(text.replace('M', '')) * 1000000)
    else:
        # Si no hay 'K' o 'M', simplemente convierte el número a un entero
        return int(text)

# Función para determinar si un perfil es un posible bot basandose en la proporción de seguidores a seguidos
def es_posible_bot(followers, following):
    # Calcula la proporción de seguidores a seguidos
    if following > 0:  # Evita la división por cero
        ratio = followers / following
        # Establece umbrales que consideras sospechosos
        if ratio < 0.1:  # Por ejemplo, una proporción muy baja de seguidores/seguidos
            return True
    return False

# Configura el driver de Selenium
driver = webdriver.Chrome()


# Abre Twitter
driver.get('https://www.twitter.com')
random_sleep()  # Espera aleatoria después de cargar la página

# Aceptar cookies
cookies_button_xpath = "//span[contains(text(),'Aceptar todas las cookies')]"
try:
    cookies_accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, cookies_button_xpath))
    )
    cookies_accept_button.click()
    random_sleep()  # Espera aleatoria después de aceptar las cookies
except Exception as e:
    print("El botón de aceptar cookies no se encontró o no se pudo hacer clic en él:", e)

# Espera a que el botón de iniciar sesión sea clickeable y haz click
login_button_xpath = '//*[text()="Iniciar sesión"]'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_button_xpath))).click()
random_sleep()  # Espera aleatoria después de hacer clic en el botón de iniciar sesión

# Ingresar nombre de usuario
user_field_xpath = "//input[@name='text' and @autocomplete='username']"
try:
    user_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, user_field_xpath))
    )
    user_field.send_keys('roberwianitxas')
    random_sleep()  # Espera aleatoria después de introducir el nombre de usuario
    user_field.send_keys(Keys.RETURN)
    random_sleep()  # Espera aleatoria después de presionar ENTER
except Exception as e:
    print("El campo de usuario no se encontró o no se pudo interactuar con él:", e)

# Ingresar contraseña de usuario
password_field_xpath = "//input[@name='password' and @autocomplete='current-password']"
try:
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, password_field_xpath))
    )
    password_field.send_keys('Nuncameacuerdo123')
    random_sleep()  # Espera aleatoria después de introducir el nombre de usuario
    password_field.send_keys(Keys.RETURN)
    random_sleep()  # Espera aleatoria después de presionar ENTER
except Exception as e:
    print("El campo de contraseña no se encontró o no se pudo interactuar con él:", e)


# Navega al perfil de Twitter que deseas analizar
perfil_usuario = 'jonbraylock'  # Reemplaza con el nombre de usuario del perfil a analizar
driver.get(f'https://twitter.com/{perfil_usuario}')
random_sleep()  # Espera aleatoria después de presionar ENTER

# Espera hasta que la página del perfil cargue
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='UserProfileHeader_Items']"))
)
random_sleep()  # Espera aleatoria después de presionar ENTER

# Recopila la información básica del perfil
try:
    # Número de Seguidores
    followers = convert_to_absolute_number(driver.find_element(By.XPATH, "//a[contains(@href,'/verified_followers')]//span[1]").text)
    # Número de Siguiendo
    following = convert_to_absolute_number(driver.find_element(By.XPATH, "//a[contains(@href,'/following')]//span[1]").text)
    random_sleep()  # Espera aleatoria después de presionar ENTER
    print(es_posible_bot(followers, following))
except Exception as e:
    print("Hubo un error extrayendo la información del perfil:", e)

#Continuación 

# Navegar a la página de comentarios

# Navegar al tweet más reciente
try:
    # Encuentra el enlace al tweet más reciente basado en el elemento 'time'
    enlace_tweet_reciente = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[.//time]"))
    )
    enlace_tweet_reciente.click()
    random_sleep()
except Exception as e:
    print("No se pudo acceder al tweet más reciente:", e)

# Recoger la lista de usuarios que han comentado en el tweet
usuarios_comentarios = []
try:
    # Espera hasta que los comentarios estén cargados
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
    )
    comentarios = driver.find_elements(By.XPATH, "//div[@data-testid='reply']")
    comentarios = driver.find_elements(By.XPATH, "//div[@data-testid='User-Name']")
    for comentario in comentarios:
        # Encuentra el nombre de usuario en cada comentario
        try:
            span_usuario = comentario.find_element(By.XPATH, ".//span[contains(text(), '@')]")
            nombre_usuario = span_usuario.text.lstrip('@')  # Elimina el símbolo '@'
            if nombre_usuario not in usuarios_comentarios:
                usuarios_comentarios.append(nombre_usuario)
        except Exception as e:
            print("No se pudo encontrar el nombre de usuario en un comentario:", e)
    random_sleep()
    usuarios_comentarios.remove(perfil_usuario)  # Elimina el nombre de usuario del perfil de la lista
except Exception as e:
    print("Error al recopilar usuarios que comentaron:", e)

# Imprime o procesa la lista de usuarios
print("Usuarios que comentaron:", usuarios_comentarios)
print()



# Analizar cada perfil de usuario
bots_sospechosos = []
for usuario in usuarios_comentarios:
    driver.get(f'https://twitter.com/{usuario}')
    random_sleep()
    # Espera hasta que la página del perfil cargue
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-testid='UserProfileHeader_Items']"))
    )
    random_sleep()  # Espera aleatoria después de presionar ENTER
    try:
        # Extraer seguidores y seguidos del perfil
        # Número de Seguidores
        followers = convert_to_absolute_number(driver.find_element(By.XPATH, "//a[contains(@href,'/verified_followers')]//span[1]").text)
        # Número de Siguiendo
        following = convert_to_absolute_number(driver.find_element(By.XPATH, "//a[contains(@href,'/following')]//span[1]").text)
        random_sleep()  # Espera aleatoria después de presionar ENTER
        # Determinar si el perfil es un posible bot
        if es_posible_bot(followers, following):
            print(f"El perfil de {usuario} parece ser un bot.")
            print("Seguidores del perfil:", followers)
            print("Siguiendo del perfil:", following)
            print("Proporción de seguidores a seguidos:", followers / following)
            print()
            bots_sospechosos.append(usuario)
    except Exception as e:
        print(f"Error al analizar el perfil de {usuario}:", e)

# Imprimir lista de bots sospechosos
print("Usuarios sospechosos de ser bots:", bots_sospechosos)

# Cierra el navegador después de realizar las operaciones necesarias
driver.quit()
