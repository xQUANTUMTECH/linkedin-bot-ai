#!/usr/bin/env python3
"""
Test semplificato per pubblicare un post su LinkedIn
"""

import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_post_diretto():
    """
    Test pubblicazione diretta con linkedin_api
    """
    try:
        from linkedin_api import Linkedin
        
        print("🔐 Tentativo autenticazione LinkedIn...")
        
        # Credenziali
        email = "mauriziotarricone@gmail.com"
        password = "Ma19801987!"
        
        # Autenticazione con delay per evitare rate limiting
        linkedin = Linkedin(
            username=email,
            password=password,
            refresh_cookies=True,
            debug=False
        )
        
        print("✅ Autenticazione riuscita!")
        
        # Ottieni profilo per conferma
        profile = linkedin.get_profile()
        print(f"👤 Profilo: {profile.get('firstName')} {profile.get('lastName')}")
        
        # Contenuto post di test
        post_content = f"""🤖 Test LinkedIn Bot AI - {datetime.now().strftime('%H:%M')}

Questo è un post di test automatico generato dal mio LinkedIn Bot AI.

✨ Funzionalità:
- Generazione contenuti automatica
- Ricerca notizie real-time
- Pubblicazione programmata

#AI #Automation #LinkedIn #Test"""

        print("📝 Contenuto post:")
        print("-" * 30)
        print(post_content)
        print("-" * 30)
        
        # Conferma pubblicazione
        confirm = input("\n🚨 Vuoi pubblicare questo post? (scrivi 'SI'): ")
        
        if confirm.upper() == 'SI':
            print("🚀 Pubblicazione in corso...")
            
            # Pubblica il post
            response = linkedin.post_update(
                text=post_content,
                visibility='PUBLIC'
            )
            
            if response:
                print("🎉 POST PUBBLICATO CON SUCCESSO!")
                print(f"📊 Response: {response}")
                print("🔗 Controlla il tuo profilo LinkedIn!")
                return True
            else:
                print("❌ Errore nella pubblicazione")
                return False
        else:
            print("❌ Pubblicazione annullata")
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        
        # Se c'è CHALLENGE, prova con delay
        if "CHALLENGE" in str(e):
            print("🔐 LinkedIn richiede verifica di sicurezza")
            print("💡 Prova questi passi:")
            print("   1. Apri LinkedIn nel browser")
            print("   2. Fai login manualmente")
            print("   3. Completa eventuali verifiche")
            print("   4. Aspetta 5-10 minuti")
            print("   5. Riprova questo script")
        
        return False

if __name__ == "__main__":
    print("🧪 TEST PUBBLICAZIONE LINKEDIN SEMPLIFICATO")
    print("=" * 50)
    
    success = test_post_diretto()
    
    if success:
        print("\n✅ TEST COMPLETATO CON SUCCESSO!")
    else:
        print("\n❌ TEST FALLITO!")
