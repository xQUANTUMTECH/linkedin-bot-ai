"""
Test completo del sistema di posting su LinkedIn
"""
import os
import sys
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Carica environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_linkedin_authentication():
    """
    Test autenticazione LinkedIn
    """
    print("🔍 TEST AUTENTICAZIONE LINKEDIN")
    print("=" * 50)
    
    try:
        from linkedin_bot import LinkedInBot
        
        bot = LinkedInBot()
        print("✅ LinkedInBot inizializzato")
        
        # Test autenticazione
        print("🔐 Tentativo autenticazione...")
        success = bot.authenticate()
        
        if success:
            print("✅ Autenticazione LinkedIn: SUCCESSO")
            return bot
        else:
            print("❌ Autenticazione LinkedIn: FALLITA")
            return None
            
    except Exception as e:
        print(f"❌ Errore test autenticazione: {str(e)}")
        return None

def test_post_creation():
    """
    Test creazione post (senza pubblicazione)
    """
    print("\n🔍 TEST CREAZIONE POST")
    print("=" * 50)
    
    try:
        # Genera un post di test
        from test_post_reale_centrosinistra import bot_genera_post_finale
        
        print("📝 Generazione post di test...")
        
        # Dati mock per test
        critica_test = "Test critica centrosinistra per verifica sistema"
        dati_test = "Dati di test per verifica funzionalità"
        
        post_content = bot_genera_post_finale(critica_test, dati_test)
        
        if post_content:
            print("✅ Post generato con successo")
            print(f"📄 Contenuto ({len(post_content)} caratteri):")
            print("-" * 40)
            print(post_content)
            print("-" * 40)
            return post_content
        else:
            print("❌ Errore generazione post")
            return None
            
    except Exception as e:
        print(f"❌ Errore test creazione post: {str(e)}")
        return None

def test_linkedin_posting_dry_run(bot, post_content):
    """
    Test pubblicazione LinkedIn (dry run - senza pubblicare realmente)
    """
    print("\n🔍 TEST PUBBLICAZIONE LINKEDIN (DRY RUN)")
    print("=" * 50)
    
    try:
        if not bot or not post_content:
            print("❌ Bot o contenuto non disponibili")
            return False
        
        print("🚀 Simulazione pubblicazione post...")
        print(f"📝 Contenuto da pubblicare: {post_content[:100]}...")
        
        # Qui normalmente chiameremmo bot.publish_post(post_content)
        # Ma facciamo solo un dry run per sicurezza
        
        print("✅ Dry run completato - Post NON pubblicato (sicurezza)")
        print("💡 Per pubblicare realmente, rimuovi il dry run")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore test pubblicazione: {str(e)}")
        return False

def test_linkedin_posting_real(bot, post_content):
    """
    Test pubblicazione LinkedIn REALE (solo se richiesto esplicitamente)
    """
    print("\n⚠️  TEST PUBBLICAZIONE LINKEDIN REALE")
    print("=" * 50)
    
    # Chiedi conferma
    confirm = input("🚨 ATTENZIONE: Vuoi pubblicare REALMENTE su LinkedIn? (scrivi 'SI' per confermare): ")
    
    if confirm.upper() != 'SI':
        print("❌ Pubblicazione annullata dall'utente")
        return False
    
    try:
        print("🚀 Pubblicazione post su LinkedIn...")
        
        # Pubblica il post
        result = bot.publish_post(post_content)
        
        if result:
            print("✅ Post pubblicato con SUCCESSO su LinkedIn!")
            print(f"🔗 Post ID: {result}")
            return True
        else:
            print("❌ Errore pubblicazione post")
            return False
            
    except Exception as e:
        print(f"❌ Errore pubblicazione reale: {str(e)}")
        return False

def main():
    """
    Test completo sistema LinkedIn
    """
    print("🤖 TEST COMPLETO SISTEMA LINKEDIN")
    print("=" * 60)
    print(f"🕐 Ora: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    # Test 1: Autenticazione
    bot = test_linkedin_authentication()
    
    # Test 2: Creazione post
    post_content = test_post_creation()
    
    # Test 3: Dry run pubblicazione
    if bot and post_content:
        test_linkedin_posting_dry_run(bot, post_content)
        
        # Test 4: Pubblicazione reale (opzionale)
        print("\n" + "=" * 60)
        real_test = input("🤔 Vuoi testare la pubblicazione REALE? (y/N): ")
        if real_test.lower() == 'y':
            test_linkedin_posting_real(bot, post_content)
    
    print("\n🎉 TEST LINKEDIN COMPLETATO!")

if __name__ == "__main__":
    main()
