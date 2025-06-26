"""
Script di deployment per Railway
Gestisce l'avvio del bot e della dashboard web
"""
import os
import sys
import logging
import threading
import time
from datetime import datetime

# Configurazione logging per Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Railway cattura stdout
    ]
)

def check_environment():
    """
    Verifica configurazione Railway
    """
    # Variabili obbligatorie
    required_vars = [
        'LINKEDIN_EMAIL',
        'LINKEDIN_PASSWORD',
        'XAI_API_KEY'
    ]

    # Variabili opzionali (con fallback)
    optional_vars = [
        'DATABASE_URL'  # Userà modalità mock se mancante
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logging.error(f"❌ Variabili d'ambiente obbligatorie mancanti: {missing_vars}")
        return False

    # Controlla variabili opzionali
    missing_optional = []
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)

    if missing_optional:
        logging.warning(f"⚠️ Variabili opzionali mancanti (userò fallback): {missing_optional}")
        logging.warning("⚠️ DATABASE_URL mancante - bot userà modalità mock per il database")

    logging.info("✅ Configurazione Railway verificata")
    return True

def start_web_dashboard():
    """
    Avvia dashboard web per Railway
    """
    try:
        from web_dashboard import app
        port = int(os.getenv('PORT', 8080))
        
        logging.info(f"🌐 Avvio dashboard web su porta {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logging.error(f"❌ Errore avvio dashboard: {str(e)}")
        sys.exit(1)

def start_linkedin_bot():
    """
    Avvia bot LinkedIn in background
    """
    try:
        from main import LinkedInBotManager
        
        logging.info("🤖 Inizializzazione LinkedIn Bot...")
        bot_manager = LinkedInBotManager()
        
        if not bot_manager.initialize():
            logging.error("❌ Inizializzazione bot fallita")
            return
        
        logging.info("✅ Bot inizializzato, avvio scheduler...")
        
        # Avvia scheduler in loop
        bot_manager.start_scheduler()
        
    except Exception as e:
        logging.error(f"❌ Errore bot LinkedIn: {str(e)}")
        time.sleep(60)  # Attendi prima di retry
        start_linkedin_bot()  # Retry

def main():
    """
    Entry point per Railway deployment
    """
    logging.info("🚂 Avvio LinkedIn Bot su Railway")
    logging.info(f"Timestamp: {datetime.now().isoformat()}")
    
    # Verifica configurazione
    if not check_environment():
        sys.exit(1)
    
    # Avvia bot in thread separato
    bot_thread = threading.Thread(target=start_linkedin_bot, daemon=True)
    bot_thread.start()
    logging.info("🤖 Bot LinkedIn avviato in background")
    
    # Avvia dashboard web (processo principale)
    # Railway richiede che il processo principale gestisca HTTP
    start_web_dashboard()

if __name__ == "__main__":
    main()
