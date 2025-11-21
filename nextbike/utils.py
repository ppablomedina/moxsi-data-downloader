from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date, timedelta
from mail import get_code
import pandas as pd
import time
import glob
import os


creds = os.getenv("NEXTBIKE_CREDS")
NEXTBIKE_USER  = creds.split("\n")[0]
NEXTBIKE_PASS  = creds.split("\n")[1]

def set_driver():

    # Crear carpeta temporal controlada por el script
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.command_executor.set_timeout(300)
    
    return driver, download_dir

def log_in_nextbike(url):
    
    driver.get(url)

    driver.find_element(By.ID, "parameters[username]").send_keys(NEXTBIKE_USER)
    driver.find_element(By.ID, "parameters[password]").send_keys(NEXTBIKE_PASS)
    driver.find_element(By.ID, "login_post").click()

    time.sleep(1.5)
    
    verification_code = get_code()
    
    driver.find_element(By.ID, "parameters[otp_code]").send_keys(verification_code)
    driver.find_element(By.ID, "login_post").click() 

def get_dates():
    
    today = date.today()
    last_day_prev_month = today.replace(day=1) - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    return (
        first_day_prev_month.strftime("%Y-%m-%d 00:00"),
        last_day_prev_month.strftime("%Y-%m-%d 23:59")
    )                              

def safe_get(driver, url, timeout):
    """Abre una URL pero si la página tarda demasiado no rompe el script."""
    try:   
        driver.set_page_load_timeout(timeout)
        driver.get(url)
    except TimeoutException: 
        if url.endswith("410"): pass  # link_clientes_registrados no se llega a cargar
        else:                   assert False, f"La página {url} tardó más de {timeout} segundos en cargar." 

def download_from_nextbike(url):

    if url.endswith("410"): timeout = 5    # link_clientes_registrados      -> no se llega a cargar
    else:                   timeout = 400  # link_clientes_ultimo_alquiler  -> da directamente el archivo
        
    safe_get(driver, url, timeout)

    start_date, end_date = get_dates()

    start_time = time.time()

    if url.endswith("639") or url.endswith("641") or url.endswith("640"):
        driver.find_element(By.ID, "parameters[start_time]").send_keys(start_date)
        driver.find_element(By.ID, "parameters[end_time]").send_keys(end_date)

    elif url.endswith("730") or url.endswith("129"):
        driver.find_element(By.ID, "parameters[start_date]").send_keys(start_date)
        driver.find_element(By.ID, "parameters[end_date]").send_keys(end_date)

    if not url.endswith("424"):
        driver.find_element(By.ID, "parameters[export_csv]").click()    
        driver.find_element(By.ID, "queries_view_get").click()

    timeout = 60
    file_path = None

    for _ in range(timeout):

        files = glob.glob(os.path.join(download_dir, "*.csv"))

        # Filtrar solo los nuevos (creados/modificados después de start_time)
        new_files = [f for f in files if os.path.getmtime(f) > start_time]

        if new_files:
            file_path = max(new_files, key=os.path.getmtime) # Por si acaso hay más de uno, cogemos el más reciente
            break

        time.sleep(1)

    return pd.read_csv(file_path, sep='\t', encoding='utf-8')

driver, download_dir = set_driver()
