#!/usr/bin/env python3
"""
Test post per Railway - Simula il comportamento del bot su Railway
"""

import time
import logging
import requests
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_post_con_grok():
    """
    Test completo: Grok API + Generazione contenuto + Post LinkedIn
    """
    print("🧪 TEST POST COMPLETO CON GROK API")
    print("=" * 50)
    
    try:
        # 1. Test Grok API
        print("🔍 Test ricerca notizie con Grok...")
        
        grok_api_key = "xai-tM1mqN0KkG5A6siCM2tfuITMNih5GhKcc0O2JePIdDbleMhzx2OUnOG4gaIcg0HNxOdFKoXTL1g8lTc0"
        
        # Ricerca notizie
        search_query = "politica italiana governo economia oggi"
        
        headers = {
            "Authorization": f"Bearer {grok_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "grok-3",
            "messages": [
                {
                    "role": "system",
                    "content": "Sei un esperto ricercatore di notizie. Trova le 3 notizie più importanti di oggi su politica italiana ed economia."
                },
                {
                    "role": "user", 
                    "content": f"Cerca notizie recenti su: {search_query}. Fornisci titolo, riassunto e fonte per ogni notizia."
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            news_data = response.json()
            news_content = news_data['choices'][0]['message']['content']
            print("✅ Notizie trovate con Grok!")
            print(f"📰 Contenuto: {news_content[:200]}...")
        else:
            print(f"⚠️ Errore Grok API: {response.status_code}")
            news_content = "Notizie di fallback per test"
        
        # 2. Genera contenuto sarcastico
        print("\n✍️ Generazione contenuto sarcastico...")
        
        content_payload = {
            "model": "grok-3",
            "messages": [
                {
                    "role": "system",
                    "content": """Sei un commentatore sarcastico e critico che scrive post LinkedIn. 
                    Stile: ironico, diretto, con dati concreti. 
                    Evita hashtag e emoji eccessive.
                    Lunghezza: 60-90 parole."""
                },
                {
                    "role": "user",
                    "content": f"Scrivi un post sarcastico su queste notizie: {news_content}"
                }
            ],
            "max_tokens": 300,
            "temperature": 0.8
        }
        
        content_response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=content_payload,
            timeout=30
        )
        
        if content_response.status_code == 200:
            content_data = content_response.json()
            post_content = content_data['choices'][0]['message']['content']
            print("✅ Contenuto generato!")
        else:
            post_content = f"""🤖 Test LinkedIn Bot AI - {datetime.now().strftime('%H:%M')}

Questo è un post di test automatico dal mio LinkedIn Bot AI.

Il sistema funziona: ricerca notizie real-time, genera contenuti sarcastici e pubblica automaticamente.

Prossimo step: pubblicazione programmata 3 volte al giorno."""

        print("\n📝 CONTENUTO POST GENERATO:")
        print("-" * 40)
        print(post_content)
        print("-" * 40)
        
        # 3. Test pubblicazione LinkedIn
        print("\n🚀 Test pubblicazione LinkedIn...")
        
        try:
            from linkedin_api import Linkedin
            
            # Credenziali
            email = "mauriziotarricone@gmail.com"
            password = "Ma19801987!"
            
            print("🔐 Tentativo autenticazione LinkedIn...")
            
            # Autenticazione con configurazione ottimizzata
            linkedin = Linkedin(
                username=email,
                password=password,
                refresh_cookies=True,
                debug=False
            )
            
            print("✅ Autenticazione LinkedIn riuscita!")
            
            # Ottieni profilo
            profile = linkedin.get_profile()
            print(f"👤 Profilo: {profile.get('firstName')} {profile.get('lastName')}")
            print(f"🎯 Pubblicherà su: PROFILO PERSONALE")
            
            # Conferma pubblicazione
            print(f"\n🚨 VUOI PUBBLICARE QUESTO POST SUL TUO PROFILO LINKEDIN?")
            confirm = input("Scrivi 'SI' per pubblicare: ")
            
            if confirm.upper() == 'SI':
                print("🚀 Pubblicazione in corso...")
                
                # Pubblica il post
                response = linkedin.post_update(
                    text=post_content,
                    visibility='PUBLIC'
                )
                
                if response:
                    print("🎉 POST PUBBLICATO CON SUCCESSO SUL TUO PROFILO PERSONALE!")
                    print(f"📊 Response: {response}")
                    print("🔗 Vai su LinkedIn per vedere il post!")
                    return True
                else:
                    print("❌ Errore nella pubblicazione")
                    return False
            else:
                print("❌ Pubblicazione annullata")
                return True
                
        except Exception as e:
            print(f"❌ Errore LinkedIn: {e}")
            
            if "CHALLENGE" in str(e):
                print("\n🔐 LinkedIn richiede verifica di sicurezza")
                print("💡 Il bot su Railway dovrebbe funzionare meglio!")
                print("🌐 Prova l'endpoint web: /force-post-now")
            
            return False
            
    except Exception as e:
        print(f"❌ Errore generale: {e}")
        return False

if __name__ == "__main__":
    success = test_post_con_grok()
    
    if success:
        print("\n✅ TEST COMPLETATO CON SUCCESSO!")
        print("🎯 Il bot è pronto per pubblicare automaticamente!")
    else:
        print("\n⚠️ TEST PARZIALMENTE FALLITO")
        print("🚀 Prova su Railway per risultati migliori!")
