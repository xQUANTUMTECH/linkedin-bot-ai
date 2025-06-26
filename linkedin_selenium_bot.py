#!/usr/bin/env python3
"""
LinkedIn Bot usando Selenium WebDriver per evitare API restrictions
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

class LinkedInSeleniumBot:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
    def setup_driver(self):
        """
        Configura Chrome WebDriver per Railway
        """
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Modalità headless per server
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logging.info("✅ Chrome WebDriver configurato")
            return True
            
        except Exception as e:
            logging.error(f"❌ Errore configurazione WebDriver: {e}")
            return False
    
    def login(self):
        """
        Login su LinkedIn
        """
        try:
            logging.info("🔐 Login LinkedIn in corso...")
            
            # Vai alla pagina di login
            self.driver.get("https://www.linkedin.com/login")
            
            # Aspetta che la pagina si carichi
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Inserisci credenziali
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            
            username_field.send_keys(LINKEDIN_EMAIL)
            password_field.send_keys(LINKEDIN_PASSWORD)
            
            # Clicca login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Aspetta che il login sia completato
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "global-nav"))
            )
            
            self.is_logged_in = True
            logging.info("✅ Login LinkedIn completato")
            return True
            
        except TimeoutException:
            logging.error("❌ Timeout durante login LinkedIn")
            return False
        except Exception as e:
            logging.error(f"❌ Errore login LinkedIn: {e}")
            return False
    
    def publish_post(self, content: str):
        """
        Pubblica un post su LinkedIn
        """
        if not self.is_logged_in:
            logging.error("❌ Non autenticato su LinkedIn")
            return False
            
        try:
            logging.info("📝 Pubblicazione post in corso...")
            
            # Vai alla home
            self.driver.get("https://www.linkedin.com/feed/")
            
            # Aspetta che la pagina si carichi
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-box-feed-entry__trigger')]"))
            )
            
            # Clicca su "Inizia un post"
            start_post_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-box-feed-entry__trigger')]")
            start_post_button.click()
            
            # Aspetta che si apra l'editor
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ql-editor"))
            )
            
            # Inserisci il contenuto
            text_area = self.driver.find_element(By.CLASS_NAME, "ql-editor")
            text_area.send_keys(content)
            
            # Aspetta un momento
            time.sleep(2)
            
            # Clicca pubblica
            publish_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]")
            publish_button.click()
            
            # Aspetta conferma
            time.sleep(3)
            
            logging.info("🎉 Post pubblicato con successo su LinkedIn!")
            return True
            
        except Exception as e:
            logging.error(f"❌ Errore pubblicazione post: {e}")
            return False
    
    def close(self):
        """
        Chiude il browser
        """
        if self.driver:
            self.driver.quit()
            logging.info("🔒 Browser chiuso")

# Test function
def test_selenium_post():
    """
    Test del bot Selenium
    """
    bot = LinkedInSeleniumBot()
    
    try:
        # Setup driver
        if not bot.setup_driver():
            return False
        
        # Login
        if not bot.login():
            return False
        
        # Pubblica post di test
        test_content = """🤖 Test post automatico dal mio LinkedIn Bot AI!

Questo post è stato generato e pubblicato automaticamente usando:
- 🧠 AI per la generazione del contenuto
- 🔍 Ricerca notizie real-time
- 🚀 Pubblicazione automatica

#AI #Automation #LinkedIn #Bot"""

        success = bot.publish_post(test_content)
        return success
        
    finally:
        bot.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = test_selenium_post()
    print(f"Test result: {'SUCCESS' if success else 'FAILED'}")
