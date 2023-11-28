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
perfil_usuario = 'FlagsMashupBot'  # Reemplaza con el nombre de usuario del perfil a analizar
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

# Cierra el navegador después de realizar las operaciones necesarias
driver.quit()