from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializar el driver de Selenium
driver = webdriver.Chrome()

# Navegar a la página de Twitter
driver.get("https://twitter.com")

# Esperar a que se cargue la página
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.NAME, "session[username_or_email]")))

# Iniciar sesión en Twitter
username_input = driver.find_element(By.NAME, "session[username_or_email]")
password_input = driver.find_element(By.NAME, "session[password]")

username_input.send_keys("tu_usuario")
password_input.send_keys("tu_contraseña")

login_button = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')
login_button.click()

# Esperar a que se cargue la página de inicio
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweet"]')))

# Obtener los tweets en la página de inicio
tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')

# Analizar los tweets para detectar bots
for tweet in tweets:
    # Aquí puedes implementar tu lógica para detectar bots
    # Por ejemplo, puedes verificar si el tweet contiene ciertas palabras clave o si el usuario tiene un número excesivo de seguidores

    # Imprimir el contenido del tweet
    print(tweet.text)



# Cerrar el navegador
driver.quit()

#sleep randons de 1 a 5 s