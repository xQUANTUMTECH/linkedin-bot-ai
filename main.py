"""
LinkedIn Bot AI con DeepSearch - Script Principale
Deploy su Railway con PostgreSQL
Pubblica 2-3 post sarcastici al giorno e risponde ai commenti
"""
import schedule
import time
import logging
import random
import sys
import threading
from datetime import datetime, timedelta
from typing import Optional

from linkedin_bot import LinkedInBot
from grok_api import GrokDeepSearch
from content_generator import SarcasticContentGenerator
from database import db_manager
from web_dashboard import app as dashboard_app
from config import POST_TIMES, SEARCH_TOPICS, LOG_LEVEL, LOG_FILE, PORT, IS_PRODUCTION

# Configurazione logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

class LinkedInBotManager:
    def __init__(self):
        self.linkedin_bot = LinkedInBot()
        self.grok_search = GrokDeepSearch()
        self.content_generator = SarcasticContentGenerator()
        self.is_running = False
        self.last_posts = []  # Traccia ultimi post per engagement
        
    def initialize(self) -> bool:
        """
        Inizializza il bot e autentica (continua anche se LinkedIn fallisce)
        """
        logging.info("🤖 Inizializzazione LinkedIn Bot AI...")

        # Autentica LinkedIn (non bloccante)
        linkedin_ok = self.linkedin_bot.authenticate()
        if not linkedin_ok:
            logging.warning("⚠️ Autenticazione LinkedIn fallita - continuo in modalità limitata")
            logging.warning("🔧 Il bot funzionerà ma non potrà pubblicare su LinkedIn")
        else:
            logging.info("✅ Autenticazione LinkedIn riuscita")

        # Test API Grok (non bloccante)
        try:
            test_result = self.grok_search.deep_search("test query")
            if test_result:
                logging.info("✅ API Grok funzionante")
            else:
                logging.warning("⚠️ API Grok non risponde, userò contenuti di fallback")
        except Exception as e:
            logging.warning(f"⚠️ Errore test Grok: {e}")

        logging.info("✅ Bot inizializzato con successo (modalità adattiva)")
        return True  # Sempre True - il bot si adatta alle condizioni
    
    def create_and_publish_post(self, force_type: str = None) -> Optional[str]:
        """
        Crea e pubblica un post sarcastico con salvataggio DB

        Args:
            force_type: "centrosinistra", "positive", "negative" per forzare tipo

        Returns:
            Post ID se successo
        """
        try:
            logging.info("📝 Generazione nuovo post...")

            # Scegli topic basato su tipo richiesto o casuale
            if force_type == "centrosinistra":
                centrosinistra_topics = [t for t in SEARCH_TOPICS if any(keyword in t.lower()
                    for keyword in ['centrosinistra', 'pd', 'm5s', 'sinistra'])]
                topic = random.choice(centrosinistra_topics) if centrosinistra_topics else random.choice(SEARCH_TOPICS)
                logging.info(f"Topic CENTROSINISTRA selezionato: {topic}")
            else:
                topic = random.choice(SEARCH_TOPICS)
                logging.info(f"Topic selezionato: {topic}")

            # Cerca notizie con DeepSearch
            search_data = self.grok_search.search_news_for_post(topic)

            # Forza tipo se richiesto
            if force_type:
                search_data['force_type'] = force_type

            logging.info(f"Dati ricerca: {search_data}")

            # Genera contenuto sarcastico
            post_content = self.content_generator.generate_post(search_data)

            # Statistiche post
            stats = self.content_generator.get_post_stats(post_content)
            logging.info(f"Post stats: {stats}")

            if not stats['within_limit']:
                logging.warning(f"Post fuori limite parole: {stats['words']}")

            # Salva nel database prima della pubblicazione
            db_post_id = db_manager.save_post(
                content=post_content,
                topic=topic,
                word_count=stats['words'],
                hashtags_count=stats['hashtags']
            )

            # Aggiorna statistiche
            db_manager.update_stats(posts_created=1, grok_api_calls=1)

            # Pubblica su LinkedIn
            linkedin_post_id = self.linkedin_bot.publish_post(post_content)

            if linkedin_post_id:
                # Aggiorna database con ID LinkedIn
                db_manager.update_post_published(db_post_id, linkedin_post_id)
                db_manager.update_stats(posts_published=1)

                logging.info(f"✅ Post pubblicato: {linkedin_post_id}")
                logging.info(f"Contenuto: {post_content[:100]}...")

                # Aggiungi alla lista per engagement successivo
                self.last_posts.append({
                    'id': linkedin_post_id,
                    'db_id': db_post_id,
                    'content': post_content,
                    'topic': topic,
                    'timestamp': time.time()
                })

                # Mantieni solo ultimi 5 post
                if len(self.last_posts) > 5:
                    self.last_posts.pop(0)

                return linkedin_post_id
            else:
                logging.error("❌ Pubblicazione fallita")
                db_manager.update_stats(errors_count=1)
                return None

        except Exception as e:
            logging.error(f"Errore creazione post: {str(e)}")
            db_manager.update_stats(errors_count=1)
            return None
    
    def process_engagement(self):
        """
        Processa engagement sui post recenti (commenti e risposte)
        """
        if not self.last_posts:
            logging.info("Nessun post recente per engagement")
            return
        
        logging.info("💬 Processamento engagement...")
        
        for post_data in self.last_posts.copy():
            try:
                post_id = post_data['id']
                topic = post_data['topic']
                
                # Genera funzione per risposte sarcastiche
                def reply_generator(comment_data):
                    context = self.grok_search.search_context_for_comment(
                        comment_data['text'], 
                        topic
                    )
                    return self.content_generator.generate_comment_reply(
                        comment_data, 
                        context
                    )
                
                # Processa commenti e risposte
                replies_sent = self.linkedin_bot.process_post_engagement(
                    post_id, 
                    reply_generator
                )
                
                logging.info(f"Engagement post {post_id}: {replies_sent} risposte")
                
                # Rimuovi post vecchi (>24h)
                if time.time() - post_data['timestamp'] > 86400:
                    self.last_posts.remove(post_data)
                    logging.info(f"Post {post_id} rimosso (>24h)")
                
            except Exception as e:
                logging.error(f"Errore engagement post: {str(e)}")
                continue
    
    def daily_routine(self, post_type: str = None):
        """
        Routine giornaliera: post + engagement

        Args:
            post_type: Tipo di post da creare ("centrosinistra", "positive", "negative")
        """
        logging.info(f"🚀 Esecuzione routine giornaliera - Tipo: {post_type or 'automatico'}")

        # Controlla autenticazione
        if not self.linkedin_bot.is_authenticated():
            logging.warning("Riautenticazione necessaria")
            if not self.linkedin_bot.authenticate():
                logging.error("Riautenticazione fallita")
                return

        # Crea e pubblica post del tipo richiesto
        post_id = self.create_and_publish_post(force_type=post_type)

        if post_id:
            # Attendi e processa engagement sui post precedenti
            time.sleep(600)  # 10 minuti
            self.process_engagement()

        # Statistiche
        stats = self.linkedin_bot.get_stats()
        token_stats = self.grok_search.check_token_usage()

        logging.info(f"📊 Stats LinkedIn: {stats}")
        logging.info(f"📊 Stats Grok: {token_stats}")

    def centrosinistra_routine(self):
        """
        Routine specifica per critica centrosinistra
        """
        logging.info("🎭 Routine critica centrosinistra")
        self.daily_routine(post_type="centrosinistra")
    
    def midnight_reset(self):
        """
        Reset contatori a mezzanotte
        """
        logging.info("🌙 Reset contatori mezzanotte")
        self.linkedin_bot.reset_daily_counters()
    
    def start_scheduler(self):
        """
        Avvia lo scheduler bilanciato per post automatici + dashboard web
        """
        logging.info("⏰ Configurazione scheduler bilanciato...")

        # Programma post giornalieri con rotazione tipi
        # 9:00 - Post generale (negativo/positivo)
        schedule.every().day.at("09:00").do(self.daily_routine)

        # 14:00 - Critica centrosinistra (martedì e venerdì)
        schedule.every().tuesday.at("14:00").do(self.centrosinistra_routine)
        schedule.every().friday.at("14:00").do(self.centrosinistra_routine)

        # 14:00 - Post generale altri giorni
        schedule.every().monday.at("14:00").do(self.daily_routine)
        schedule.every().wednesday.at("14:00").do(self.daily_routine)
        schedule.every().thursday.at("14:00").do(self.daily_routine)
        schedule.every().saturday.at("14:00").do(self.daily_routine)
        schedule.every().sunday.at("14:00").do(self.daily_routine)

        # 19:00 - Post serale generale
        schedule.every().day.at("19:00").do(self.daily_routine)

        logging.info("📅 Scheduler configurato:")
        logging.info("  - 9:00: Post generale quotidiano")
        logging.info("  - 14:00: Critica centrosinistra (mar/ven) + post generale altri giorni")
        logging.info("  - 19:00: Post serale generale")
        logging.info("  - Garanzia: 2 post centrosinistra/settimana")

        # Reset mezzanotte
        schedule.every().day.at("00:00").do(self.midnight_reset)

        # Engagement check ogni 2 ore
        schedule.every(2).hours.do(self.process_engagement)

        self.is_running = True
        logging.info("✅ Scheduler avviato")

        # Avvia dashboard web in thread separato
        if IS_PRODUCTION:
            dashboard_thread = threading.Thread(
                target=lambda: dashboard_app.run(host='0.0.0.0', port=PORT, debug=False),
                daemon=True
            )
            dashboard_thread.start()
            logging.info(f"🌐 Dashboard web avviata su porta {PORT}")

        # Loop principale
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check ogni minuto

        except KeyboardInterrupt:
            logging.info("🛑 Bot fermato dall'utente")
            self.is_running = False
        except Exception as e:
            logging.error(f"Errore scheduler: {str(e)}")
            self.is_running = False
    
    def manual_post(self):
        """
        Crea un post manuale per test
        """
        logging.info("🧪 Creazione post manuale...")
        post_id = self.create_and_publish_post()
        
        if post_id:
            print(f"✅ Post creato: {post_id}")
            
            # Attendi e controlla engagement
            print("⏳ Attendo 5 minuti per engagement...")
            time.sleep(300)
            self.process_engagement()
        else:
            print("❌ Errore creazione post")

def main():
    """
    Funzione principale
    """
    print("🤖 LinkedIn Bot AI con DeepSearch")
    print("=" * 40)
    
    bot_manager = LinkedInBotManager()
    
    # Inizializza
    if not bot_manager.initialize():
        print("❌ Inizializzazione fallita")
        return
    
    # Menu interattivo
    while True:
        print("\n📋 Opzioni:")
        print("1. Avvia bot automatico")
        print("2. Crea post manuale")
        print("3. Controlla stats")
        print("4. Test DeepSearch")
        print("5. Esci")
        
        choice = input("\nScegli opzione (1-5): ").strip()
        
        if choice == "1":
            print("🚀 Avvio bot automatico...")
            bot_manager.start_scheduler()
            
        elif choice == "2":
            bot_manager.manual_post()
            
        elif choice == "3":
            stats = bot_manager.linkedin_bot.get_stats()
            token_stats = bot_manager.grok_search.check_token_usage()
            print(f"📊 LinkedIn Stats: {stats}")
            print(f"📊 Grok Stats: {token_stats}")
            
        elif choice == "4":
            query = input("Query DeepSearch: ")
            result = bot_manager.grok_search.deep_search(query)
            print(f"🔍 Risultato: {result}")
            
        elif choice == "5":
            print("👋 Arrivederci!")
            break
            
        else:
            print("❌ Opzione non valida")

if __name__ == "__main__":
    main()
