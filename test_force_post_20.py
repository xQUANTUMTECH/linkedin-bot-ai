#!/usr/bin/env python3
"""
Test per forzare un post delle 20:00 e verificare pubblicazione LinkedIn
"""

import os
import sys
import logging
from datetime import datetime

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linkedin_bot import LinkedInBot
from grok_api import GrokDeepSearch
from content_generator import SarcasticContentGenerator
from database import db_manager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_force_evening_post():
    """
    Forza un post serale delle 20:00 per testare pubblicazione
    """
    print("🧪 TEST FORZATO POST DELLE 20:00")
    print("=" * 50)
    
    try:
        # Inizializza componenti
        print("🔧 Inizializzazione componenti...")
        linkedin_bot = LinkedInBot()
        grok_search = GrokDeepSearch()
        content_generator = SarcasticContentGenerator()
        
        # Test autenticazione LinkedIn
        print("🔐 Test autenticazione LinkedIn...")
        if not linkedin_bot.authenticate():
            print("❌ Autenticazione LinkedIn fallita!")
            return False
        
        print("✅ Autenticazione LinkedIn riuscita!")
        
        # Cerca notizie per post serale
        print("🔍 Ricerca notizie per post serale...")
        search_query = "politica italiana economia governo oggi"
        news_results = grok_search.search_news(search_query)
        
        if not news_results:
            print("⚠️ Nessuna notizia trovata, uso contenuto di fallback")
            news_results = [{
                'title': 'Test Post Serale',
                'content': 'Contenuto di test per verificare pubblicazione LinkedIn',
                'url': 'https://example.com'
            }]
        
        print(f"📰 Trovate {len(news_results)} notizie")
        
        # Genera contenuto sarcastico
        print("✍️ Generazione contenuto sarcastico...")
        post_content = content_generator.generate_post(
            news_results, 
            post_type="generale",
            context="Post serale di test - critica eventi della giornata"
        )
        
        print("📝 Contenuto generato:")
        print("-" * 30)
        print(post_content)
        print("-" * 30)
        
        # Pubblica su LinkedIn
        print("🚀 Pubblicazione su LinkedIn...")
        success = linkedin_bot.publish_post(post_content)
        
        if success:
            print("🎉 POST PUBBLICATO CON SUCCESSO SU LINKEDIN!")
            
            # Salva nel database se disponibile
            try:
                post_data = {
                    'content': post_content,
                    'type': 'test_serale',
                    'timestamp': datetime.now(),
                    'published': True,
                    'platform': 'linkedin'
                }
                db_manager.save_post(post_data)
                print("💾 Post salvato nel database")
            except Exception as e:
                print(f"⚠️ Errore salvataggio database: {e}")
            
            return True
        else:
            print("❌ ERRORE NELLA PUBBLICAZIONE!")
            return False
            
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        logging.exception("Dettagli errore:")
        return False

def main():
    """
    Esegue il test forzato
    """
    print(f"🕐 Ora attuale: {datetime.now().strftime('%H:%M:%S')}")
    print("🎯 Simulazione post delle 20:00...")
    
    success = test_force_evening_post()
    
    if success:
        print("\n✅ TEST COMPLETATO CON SUCCESSO!")
        print("🔗 Controlla il tuo profilo LinkedIn per vedere il post")
    else:
        print("\n❌ TEST FALLITO!")
        print("🔧 Controlla i log per dettagli sull'errore")

if __name__ == "__main__":
    main()
