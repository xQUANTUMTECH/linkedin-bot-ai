"""
Configurazione per il LinkedIn Bot AI con DeepSearch
Deploy su Railway con PostgreSQL
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Credenziali LinkedIn
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', 'mauriziotarricone@gmail.com')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', 'Ma119801987!')

# Modalità test disabilitata - SEMPRE pubblicazione reale
TEST_MODE = False

# Credenziali xAI/Grok
XAI_API_KEY = os.getenv('XAI_API_KEY', 'xai-foL2y8TQ0kyLUU86uWlxDaLLgpm7O1NOzR3ftGKocglbe9VO4h6NgnBV8jxIkQIQ9rgGcjPug0WEyKkm')
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

# Database PostgreSQL (Railway)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/linkedin_bot')
DATABASE_PRIVATE_URL = os.getenv('DATABASE_PRIVATE_URL', DATABASE_URL)  # Railway private URL

# Railway specifiche
PORT = int(os.getenv('PORT', 8080))
RAILWAY_ENVIRONMENT = os.getenv('RAILWAY_ENVIRONMENT', 'development')
IS_PRODUCTION = RAILWAY_ENVIRONMENT == 'production'

# Configurazioni bot
POST_TIMES = ["09:00", "14:00", "19:00"]  # Orari CEST
POSTS_PER_DAY = 3
MAX_COMMENTS_PER_POST = 5
POST_WORD_LIMIT = (60, 90)  # Min, Max parole (aumentato per dati tecnici)
COMMENT_WORD_LIMIT = (25, 50)  # Aumentato per più dati

# Temi di ricerca specifici per DeepSearch
SEARCH_TOPICS = [
    "centrosinistra",  # Cerca notizie specifiche PD/M5S
    "sprechi",         # Cerca sprechi governativi specifici
    "tech",           # Cerca notizie tech/digitalizzazione
    "generale",       # Cerca notizie generali
    "centrosinistra", # Secondo post centrosinistra
]

# Topic specifici per ricerche mirate
SPECIFIC_SEARCH_QUERIES = {
    "centrosinistra": [
        "Elly Schlein felpa attivista Nazareno riformisti",
        "Giuseppe Conte M5S due mandati abolizione",
        "PD congresso cambiamenti segreteria",
        "centrosinistra divisioni interne"
    ],
    "sprechi": [
        "app IO costi sviluppo manutenzione",
        "digitalizzazione sprechi progetti pubblici",
        "appalti pubblici costi extra",
        "SPID problemi costi server"
    ],
    "tech": [
        "intelligenza artificiale legge DDL Italia",
        "fibra ottica copertura Italia ritardi",
        "startup italiane funding investimenti",
        "digitalizzazione PA inefficienze"
    ],
    "generale": [
        "notizie Italia politica economia",
        "governo italiano decisioni oggi",
        "parlamento italiano voti leggi",
        "politica italiana sviluppi"
    ]
}

# Template per post sarcastici
BOT_INTROS = [
    "🤖 Sono un bot AI, voi umani siete un loop infinito di errori.",
    "🤖 Sono un bot AI, voi umani siete un crash di sistema.",
    "🤖 Sono un bot AI, voi umani siete un codice pieno di bug.",
    "🤖 Bot AI qui, voi umani siete un 404 della logica.",
    "🤖 Sono un bot AI, voi umani siete un malware della razionalità."
]

# Intro per contenuti positivi (rare ma esistono)
POSITIVE_INTROS = [
    "🤖 Bot AI qui. Incredibile: per una volta non avete sbagliato tutto.",
    "🤖 Sono un bot AI. Shock: qualcuno ha fatto qualcosa di sensato.",
    "🤖 Bot AI stupito: un progetto che funziona davvero. Miracolo.",
    "🤖 Sono un bot AI. Plot twist: efficienza governativa rilevata."
]

# Intro specifiche per critica centrosinistra
CENTROSINISTRA_INTROS = [
    "🤖 Sono un bot AI, voi umani siete il 404 dell'umanità.",
    "🤖 Sono un bot AI, voi umani siete un loop infinito di errori.",
    "🤖 Sono un bot AI, voi umani siete un crash di sistema ambulante.",
    "🤖 Sono un bot AI, voi umani siete un bug nel codice della logica.",
    "🤖 Sono un bot AI, voi umani siete un virus della coerenza.",
    "🤖 Sono un bot AI, voi umani siete un malware dell'intelligenza.",
    "🤖 Sono un bot AI, voi umani siete un errore di compilazione vivente.",
    "🤖 Sono un bot AI, voi umani siete un buffer overflow di stupidità."
]

SARCASTIC_ENDINGS = [
    "Patetico.",
    "Continuate a sbagliare, geni.",
    "Sveglia, umani.",
    "Che disastro binario.",
    "Un capolavoro di inefficienza."
]

# Hashtags standard
HASHTAGS = "#AI #Sarcasmo #Politica #Tech"

# Rate limiting (secondi)
DELAY_BETWEEN_POSTS = 300  # 5 minuti
DELAY_BETWEEN_COMMENTS = 60  # 1 minuto
DELAY_AFTER_ERROR = 1800  # 30 minuti

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "linkedin_bot.log"
