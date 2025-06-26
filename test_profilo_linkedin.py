#!/usr/bin/env python3
"""
Test per verificare su quale profilo LinkedIn pubblichiamo
"""

import os
import sys
import logging
from datetime import datetime

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linkedin_bot import LinkedInBot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_profilo_linkedin():
    """
    Verifica su quale profilo LinkedIn pubblichiamo
    """
    print("🔍 TEST PROFILO LINKEDIN")
    print("=" * 50)
    
    try:
        # Inizializza bot
        print("🔧 Inizializzazione LinkedIn Bot...")
        linkedin_bot = LinkedInBot()
        
        # Test autenticazione
        print("🔐 Test autenticazione LinkedIn...")
        if not linkedin_bot.authenticate():
            print("❌ Autenticazione LinkedIn fallita!")
            return False
        
        print("✅ Autenticazione LinkedIn riuscita!")
        
        # Ottieni informazioni profilo
        print("👤 Recupero informazioni profilo...")
        try:
            # Ottieni il profilo dell'utente autenticato
            profile = linkedin_bot.linkedin.get_profile()
            
            print("\n📋 INFORMAZIONI PROFILO:")
            print("-" * 30)
            print(f"Nome: {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')}")
            print(f"Headline: {profile.get('headline', 'N/A')}")
            print(f"Public ID: {profile.get('public_id', 'N/A')}")
            print(f"URN: {profile.get('member_urn', 'N/A')}")
            
            # Controlla se è un profilo aziendale o personale
            if 'company' in str(profile.get('member_urn', '')):
                print("🏢 TIPO: Profilo AZIENDALE")
            else:
                print("👤 TIPO: Profilo PERSONALE")
            
            print("-" * 30)
            
            # Test post di prova (NON pubblicare)
            print("\n🧪 Test contenuto post (SENZA pubblicare):")
            test_content = f"""🧪 Test post dal LinkedIn Bot AI

Questo è un post di test generato automaticamente alle {datetime.now().strftime('%H:%M:%S')}.

⚠️ QUESTO POST NON VERRÀ PUBBLICATO - È SOLO UN TEST!

#Test #LinkedInBot #AI"""

            print("📝 Contenuto che verrebbe pubblicato:")
            print("-" * 30)
            print(test_content)
            print("-" * 30)
            
            # Chiedi se pubblicare realmente
            print("\n🚨 VUOI PUBBLICARE QUESTO POST DI TEST?")
            confirm = input("Scrivi 'SI' per pubblicare, qualsiasi altro tasto per annullare: ")
            
            if confirm.upper() == 'SI':
                print("🚀 Pubblicazione post di test...")
                result = linkedin_bot.publish_post(test_content)
                
                if result:
                    print("🎉 POST DI TEST PUBBLICATO CON SUCCESSO!")
                    print(f"🔗 Post ID: {result}")
                    print("👀 Controlla il tuo profilo LinkedIn per vedere dove è apparso!")
                    return True
                else:
                    print("❌ Errore nella pubblicazione")
                    return False
            else:
                print("❌ Pubblicazione annullata")
                return True
                
        except Exception as e:
            print(f"❌ Errore recupero profilo: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Errore generale: {e}")
        logging.exception("Dettagli errore:")
        return False

def main():
    """
    Esegue il test del profilo
    """
    print(f"🕐 Ora attuale: {datetime.now().strftime('%H:%M:%S')}")
    print("🎯 Verificando su quale profilo LinkedIn pubblichiamo...")
    
    success = test_profilo_linkedin()
    
    if success:
        print("\n✅ TEST PROFILO COMPLETATO!")
        print("📋 Controlla le informazioni sopra per vedere:")
        print("   - Se è un profilo personale o aziendale")
        print("   - Dove apparirà il post quando pubblichi")
    else:
        print("\n❌ TEST PROFILO FALLITO!")
        print("🔧 Controlla i log per dettagli sull'errore")

if __name__ == "__main__":
    main()
