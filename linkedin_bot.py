"""
Bot LinkedIn con autenticazione tramite credenziali
"""
import time
import logging
import random
from typing import List, Dict, Optional
from linkedin_api import Linkedin
from config import (
    LINKEDIN_EMAIL, LINKEDIN_PASSWORD, MAX_COMMENTS_PER_POST,
    DELAY_BETWEEN_POSTS, DELAY_BETWEEN_COMMENTS, DELAY_AFTER_ERROR
)

class LinkedInBot:
    def __init__(self):
        self.linkedin = None
        self.last_post_time = 0
        self.daily_posts = 0
        self.daily_comments = 0
        self.max_daily_posts = 3
        self.max_daily_comments = 15  # 3 posts * 5 comments max
        
    def authenticate(self) -> bool:
        """
        Autentica con LinkedIn usando credenziali (con fallback a modalità test)
        """
        # Controlla se siamo in modalità test
        if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
            logging.warning("⚠️ Credenziali LinkedIn mancanti - modalità test attiva")
            self.linkedin = None
            return True

        try:
            logging.info("Tentativo autenticazione LinkedIn...")
            
            # Configurazione ottimizzata per evitare challenge
            self.linkedin = Linkedin(
                username=LINKEDIN_EMAIL,
                password=LINKEDIN_PASSWORD,
                refresh_cookies=True,
                debug=True,  # Abilita debug per vedere cosa succede
                authenticate=True,
                request_dir='./linkedin_requests',  # Salva richieste per debug
                cookies_dir='./linkedin_cookies'    # Salva cookies persistenti
            )
            
            # Test connessione
            profile = self.linkedin.get_profile()
            if profile:
                logging.info(f"Autenticazione riuscita per: {profile.get('firstName', 'User')}")
                return True
            else:
                logging.error("Autenticazione fallita: profilo non trovato")
                return False
                
        except Exception as e:
            error_msg = str(e)
            logging.error(f"Errore autenticazione LinkedIn: {error_msg}")

            # Gestione specifica per CHALLENGE
            if "CHALLENGE" in error_msg:
                logging.warning("🔐 LinkedIn richiede verifica di sicurezza")
                logging.warning("💡 Soluzioni possibili:")
                logging.warning("   1. Accedi manualmente a LinkedIn dal browser")
                logging.warning("   2. Completa eventuali verifiche richieste")
                logging.warning("   3. Riprova tra qualche minuto")

                # Prova a continuare senza autenticazione per ora
                logging.warning("⚠️ Continuando senza autenticazione LinkedIn...")
                self.linkedin = None
                return False

            return False
    
    def publish_post(self, content: str) -> Optional[str]:
        """
        Pubblica un post su LinkedIn
        
        Args:
            content: Contenuto del post
            
        Returns:
            Post ID se successo, None se errore
        """
        if not self._can_post():
            logging.warning("Limite giornaliero post raggiunto o troppo presto")
            return None
        
        try:
            # Modalità test se LinkedIn non è disponibile
            if not self.linkedin:
                logging.info("🧪 MODALITÀ TEST - Simulazione pubblicazione post...")
                logging.info(f"📝 Contenuto post (TEST):\n{content}")

                # Simula successo
                fake_post_id = f"test_post_{int(time.time())}"
                self.last_post_time = time.time()
                self.daily_posts += 1

                logging.info(f"✅ Post TEST pubblicato con successo. ID: {fake_post_id}")
                time.sleep(2)  # Breve delay per simulare
                return fake_post_id

            logging.info("Pubblicazione post in corso...")

            # Pubblica il post reale
            response = self.linkedin.post_update(
                text=content,
                visibility='PUBLIC'
            )
            
            if response:
                post_id = response.get('id') or response.get('updateKey')
                self.last_post_time = time.time()
                self.daily_posts += 1
                
                logging.info(f"Post pubblicato con successo. ID: {post_id}")
                
                # Delay di sicurezza
                time.sleep(DELAY_BETWEEN_POSTS)
                
                return post_id
            else:
                logging.error("Errore pubblicazione: risposta vuota")
                return None
                
        except Exception as e:
            logging.error(f"Errore pubblicazione post: {str(e)}")
            time.sleep(DELAY_AFTER_ERROR)
            return None
    
    def get_post_comments(self, post_id: str) -> List[Dict]:
        """
        Recupera commenti di un post
        
        Args:
            post_id: ID del post
            
        Returns:
            Lista di commenti
        """
        try:
            logging.info(f"Recupero commenti per post {post_id}")
            
            # Attendi che i commenti arrivino
            time.sleep(300)  # 5 minuti
            
            comments = self.linkedin.get_post_comments(post_id)
            
            if comments:
                logging.info(f"Trovati {len(comments)} commenti")
                return comments[:MAX_COMMENTS_PER_POST]  # Limita a 5
            else:
                logging.info("Nessun commento trovato")
                return []
                
        except Exception as e:
            logging.error(f"Errore recupero commenti: {str(e)}")
            return []
    
    def reply_to_comment(self, post_id: str, comment_id: str, reply_text: str) -> bool:
        """
        Risponde a un commento
        
        Args:
            post_id: ID del post
            comment_id: ID del commento
            reply_text: Testo della risposta
            
        Returns:
            True se successo
        """
        if not self._can_comment():
            logging.warning("Limite giornaliero commenti raggiunto")
            return False
        
        try:
            logging.info(f"Risposta al commento {comment_id}")
            
            success = self.linkedin.comment_on_post(
                post_id=post_id,
                comment_text=reply_text
            )
            
            if success:
                self.daily_comments += 1
                logging.info("Risposta pubblicata con successo")
                
                # Delay tra commenti
                time.sleep(DELAY_BETWEEN_COMMENTS)
                return True
            else:
                logging.error("Errore pubblicazione risposta")
                return False
                
        except Exception as e:
            logging.error(f"Errore risposta commento: {str(e)}")
            time.sleep(DELAY_AFTER_ERROR)
            return False
    
    def process_post_engagement(self, post_id: str, reply_generator_func) -> int:
        """
        Processa l'engagement di un post (commenti e risposte)
        
        Args:
            post_id: ID del post
            reply_generator_func: Funzione per generare risposte
            
        Returns:
            Numero di risposte pubblicate
        """
        comments = self.get_post_comments(post_id)
        replies_sent = 0
        
        for comment in comments:
            if replies_sent >= MAX_COMMENTS_PER_POST:
                break
                
            try:
                # Estrai dati commento
                comment_data = {
                    'user': comment.get('commenter', {}).get('name', 'Utente'),
                    'text': comment.get('comment', {}).get('text', ''),
                    'id': comment.get('id', '')
                }
                
                # Genera risposta sarcastica
                reply = reply_generator_func(comment_data)
                
                if reply and self.reply_to_comment(post_id, comment_data['id'], reply):
                    replies_sent += 1
                    logging.info(f"Risposta {replies_sent}/{MAX_COMMENTS_PER_POST} inviata")
                
                # Delay tra risposte
                time.sleep(random.randint(30, 90))
                
            except Exception as e:
                logging.error(f"Errore processamento commento: {str(e)}")
                continue
        
        logging.info(f"Engagement completato: {replies_sent} risposte inviate")
        return replies_sent
    
    def _can_post(self) -> bool:
        """
        Controlla se può pubblicare un post
        """
        # Controllo limite giornaliero
        if self.daily_posts >= self.max_daily_posts:
            return False
        
        # Controllo delay minimo tra post
        time_since_last = time.time() - self.last_post_time
        if time_since_last < DELAY_BETWEEN_POSTS:
            return False
        
        return True
    
    def _can_comment(self) -> bool:
        """
        Controlla se può commentare
        """
        return self.daily_comments < self.max_daily_comments
    
    def reset_daily_counters(self):
        """
        Reset contatori giornalieri (chiamare a mezzanotte)
        """
        self.daily_posts = 0
        self.daily_comments = 0
        logging.info("Contatori giornalieri resettati")
    
    def get_stats(self) -> Dict[str, int]:
        """
        Statistiche bot
        """
        return {
            'daily_posts': self.daily_posts,
            'daily_comments': self.daily_comments,
            'max_daily_posts': self.max_daily_posts,
            'max_daily_comments': self.max_daily_comments,
            'posts_remaining': self.max_daily_posts - self.daily_posts,
            'comments_remaining': self.max_daily_comments - self.daily_comments
        }
    
    def is_authenticated(self) -> bool:
        """
        Controlla se è autenticato
        """
        try:
            if self.linkedin:
                profile = self.linkedin.get_profile()
                return profile is not None
            return False
        except:
            return False
