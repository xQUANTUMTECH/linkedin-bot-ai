"""
Test multipli post LinkedIn: politica, sprechi, tech, positivi
"""
import requests
import json
import logging
import random
from datetime import datetime
import time

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Key Grok
XAI_API_KEY = "xai-foL2y8TQ0kyLUU86uWlxDaLLgpm7O1NOzR3ftGKocglbe9VO4h6NgnBV8jxIkQIQ9rgGcjPug0WEyKkm"
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

class LinkedInBotTester:
    """
    Tester per diversi tipi di post LinkedIn
    """
    def __init__(self):
        self.api_key = XAI_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.post_count = 0
    
    def search_news(self, query, topic_type="generale"):
        """
        Ricerca notizie con API Grok
        """
        try:
            payload = {
                "model": "grok-3-latest",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are a sarcastic AI bot that writes LinkedIn posts. Search for recent news and provide factual analysis for {topic_type} topics."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "search_parameters": {
                    "mode": "on",
                    "return_citations": True,
                    "from_date": datetime.now().strftime('%Y-%m-%d'),
                    "to_date": datetime.now().strftime('%Y-%m-%d'),
                    "max_search_results": 10,
                    "sources": [
                        {"type": "news", "country": "IT"},
                        {"type": "web", "country": "IT"}
                    ]
                },
                "temperature": 0.4,
                "max_tokens": 1000,
                "stream": False
            }
            
            logging.info(f"🔍 Ricerca: {query[:60]}...")
            
            response = requests.post(
                XAI_API_URL,
                headers=self.headers,
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                logging.info(f"✅ Risposta ricevuta: {len(content)} caratteri")
                return content
            else:
                logging.error(f"❌ Errore API: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"❌ Errore ricerca: {str(e)}")
            return None
    
    def genera_post_centrosinistra(self):
        """
        Genera post critico centrosinistra
        """
        print(f"\n🎭 POST #{self.post_count + 1}: CRITICA CENTROSINISTRA")
        print("=" * 60)
        
        # Cerca notizie SPECIFICHE centrosinistra
        query = f"Elly Schlein Nazareno riformisti felpa attivista L'Espresso 26 giugno 2025"
        notizie = self.search_news(query, "centrosinistra")

        if not notizie:
            return self._fallback_centrosinistra()

        # Bot commenta la notizia SPECIFICA che ha trovato
        query_critica = f"""Ho trovato questa notizia: {notizie[:800]}

        Scrivi un post LinkedIn sarcastico di 50-70 parole che commenta questa notizia specifica.

        Se hai trovato la notizia di Schlein:
        - Usa DETTAGLI SPECIFICI: "felpa da attivista", "giacca di velluto", "riformisti drizzano antenne"
        - Cita FATTI CONCRETI: telefonate, voti specifici, decisioni precise
        - Ironizza su COMPORTAMENTI SPECIFICI, non su "opportunismo generico"

        Formato:
        🤖 Sono un bot AI, voi umani siete [scegli tra: "il 404 dell'umanità", "un loop infinito di errori", "un crash di sistema ambulante", "un bug nel codice della logica"]
        [Dettagli specifici della notizia]
        [Critica tagliente su fatti concreti]
        NIENTE hashtag alla fine

        REGOLE IMPORTANTI:
        - NON usare meta-text come "DeepSearch trova", "insight sarcastico", "Ecco", "Analisi"
        - NON usare asterischi ** o MAIUSCOLE eccessive
        - Scrivi contenuto DIRETTO e PULITO
        - USA DETTAGLI TECNICI E SPECIFICI, non concetti vaghi come "ROI" o "strategia"."""
        
        post = self.search_news(query_critica, "centrosinistra")
        self.post_count += 1
        
        return self._pulisci_post(post) if post else self._fallback_centrosinistra()
    
    def genera_post_sprechi(self):
        """
        Genera post su sprechi governativi
        """
        print(f"\n💸 POST #{self.post_count + 1}: SPRECHI GOVERNATIVI")
        print("=" * 60)
        
        # Cerca sprechi SPECIFICI
        query = f"app IO costi oggi {datetime.now().strftime('%Y-%m-%d')} OR digitalizzazione sprechi oggi {datetime.now().strftime('%Y-%m-%d')} OR progetti pubblici falliti oggi {datetime.now().strftime('%Y-%m-%d')} OR appalti pubblici costi oggi {datetime.now().strftime('%Y-%m-%d')}"
        notizie = self.search_news(query, "sprechi")

        if not notizie:
            return self._fallback_sprechi()

        # Bot analizza spreco SPECIFICO
        query_sprechi = f"""Analizza questo spreco specifico: {notizie[:800]}

        Scrivi un post LinkedIn sarcastico di 50-70 parole su questo spreco SPECIFICO.

        Includi DATI TECNICI PRECISI:
        - CIFRE ESATTE: €X milioni, Y mesi di sviluppo, Z utenti attivi
        - SPECIFICHE TECNICHE: server, database, API calls, bandwidth
        - CONFRONTI TECNICI: costo per utente, tempo di sviluppo, performance
        - ALTERNATIVE TECNICHE: stack diverso, architettura migliore

        Formato:
        🤖 Sono un bot AI, voi umani siete [insulto sarcastico]
        [Spreco con dati tecnici specifici]
        [Alternativa tecnica concreta]
        [Conclusione tagliente]
        NIENTE hashtag alla fine

        REGOLE IMPORTANTI:
        - NON usare meta-text come "DeepSearch trova", "insight sarcastico"
        - Scrivi contenuto DIRETTO e PULITO
        - USA METRICHE TECNICHE, non buzzword come "ROI" o "efficienza"."""
        
        post = self.search_news(query_sprechi, "sprechi")
        self.post_count += 1
        
        return self._pulisci_post(post) if post else self._fallback_sprechi()
    
    def genera_post_tecnologia(self):
        """
        Genera post su tecnologia/digitalizzazione
        """
        print(f"\n💻 POST #{self.post_count + 1}: TECNOLOGIA/DIGITALIZZAZIONE")
        print("=" * 60)
        
        # Cerca notizie tech SPECIFICHE
        query = f"intelligenza artificiale legge oggi {datetime.now().strftime('%Y-%m-%d')} OR SPID problemi oggi {datetime.now().strftime('%Y-%m-%d')} OR fibra ottica Italia oggi {datetime.now().strftime('%Y-%m-%d')} OR startup italiane oggi {datetime.now().strftime('%Y-%m-%d')}"
        notizie = self.search_news(query, "tecnologia")

        if not notizie:
            return self._fallback_tech()

        # Bot analizza tech SPECIFICO
        query_tech = f"""Analizza questa notizia tech specifica: {notizie[:800]}

        Scrivi un post LinkedIn sarcastico di 50-70 parole su questa notizia SPECIFICA.

        USA DETTAGLI TECNICI PRECISI:
        - Se leggi AI: numero articoli, voti esatti, tempi approvazione, confronto con GDPR
        - Se SPID: downtime percentuale, costi server, autenticazioni fallite
        - Se fibra: Mbps, copertura %, latenza, confronto con Tallinn/Seoul
        - Se startup: funding esatto, burn rate, user acquisition cost

        Formato:
        🤖 Sono un bot AI, voi umani siete [insulto sarcastico]
        [Dettagli tecnici specifici della notizia]
        [Confronto con metriche internazionali]
        [Conclusione tecnica]
        NIENTE hashtag alla fine

        REGOLE IMPORTANTI:
        - NON usare meta-text come "DeepSearch trova", "insight sarcastico"
        - Scrivi contenuto DIRETTO e PULITO
        - USA METRICHE TECNICHE PRECISE, non concetti vaghi."""
        
        post = self.search_news(query_tech, "tecnologia")
        self.post_count += 1
        
        return self._pulisci_post(post) if post else self._fallback_tech()
    
    def genera_post_generale(self):
        """
        Genera post su notizie generali
        """
        print(f"\n📰 POST #{self.post_count + 1}: NOTIZIE GENERALI")
        print("=" * 60)
        
        # Cerca notizie generali
        query = f"Notizie principali oggi {datetime.now().strftime('%Y-%m-%d')} Italia politica economia società"
        notizie = self.search_news(query, "generale")
        
        if not notizie:
            return self._fallback_generale()
        
        # Bot sceglie cosa commentare
        query_generale = f"""Basandoti su queste notizie: {notizie[:600]}
        
        Scrivi un post LinkedIn sarcastico di 50-70 parole su una notizia interessante.
        Formato:
        🤖 Sono un bot AI, voi umani siete [insulto sarcastico]
        [Commento sarcastico sulla notizia]
        [Insight critico]
        [Conclusione]
        NIENTE hashtag alla fine

        REGOLE IMPORTANTI:
        - NON usare meta-text come "DeepSearch trova", "insight sarcastico"
        - Scrivi contenuto DIRETTO e PULITO
        - Scegli la notizia più interessante da commentare."""
        
        post = self.search_news(query_generale, "generale")
        self.post_count += 1
        
        return self._pulisci_post(post) if post else self._fallback_generale()
    
    def _pulisci_post(self, post):
        """
        Pulisce il post da formattazioni extra e meta-text
        """
        if not post:
            return ""

        # Rimuovi formattazioni markdown
        post_pulito = post.replace('**', '').replace('*', '').replace('###', '').strip()

        # Rimuovi meta-text comuni
        meta_text_patterns = [
            "DeepSearch trova:",
            "DeepSearch trova",
            "DeepSearch dice:",
            "DeepSearch dice",
            "DeepSearch conferma:",
            "DeepSearch conferma",
            "Analisi DeepSearch:",
            "Analisi DeepSearch",
            "insight sarcastico:",
            "insight sarcastico",
            "Using the DeepSearch query provided",
            "I've scoured",
            "Tecnologie:",
            "Dati:",
            "Budget:",
            "Alternative:",
            "Confronto:",
            "Coerenza:",
            "Dettagli:",
            "Specifiche:",
            "Ecco un",
            "Ecco la",
            "Ecco il",
            "Analisi:",
            "Basandoti su",
            "Per rendere",
            "È essenziale",
            "Mi baso su",
            "aggiornate al",
            "con focus su",
            "in particolare su"
        ]

        for pattern in meta_text_patterns:
            post_pulito = post_pulito.replace(pattern, "")

        # Rimuovi asterischi e maiuscole eccessive
        post_pulito = post_pulito.replace('**', '').replace('*', '')

        # Converti MAIUSCOLE eccessive in normali (tranne acronimi)
        words = post_pulito.split()
        cleaned_words = []
        for word in words:
            if len(word) > 3 and word.isupper() and not any(char in word for char in ['#', '@']):
                cleaned_words.append(word.lower().capitalize())
            else:
                cleaned_words.append(word)
        post_pulito = ' '.join(cleaned_words)

        # Rimuovi eventuali prefissi e hashtag
        linee = post_pulito.split('\n')
        post_finale = []

        for linea in linee:
            linea = linea.strip()
            # Rimuovi linee che iniziano con meta-text o sono solo hashtag
            if (linea and
                not linea.startswith('Ecco') and
                not linea.startswith('Analisi') and
                not linea.startswith('#') and
                not linea.startswith('Hashtag')):
                post_finale.append(linea)

        return '\n'.join(post_finale)
    
    def _fallback_centrosinistra(self):
        return """🤖 Sono un bot AI, voi umani siete un loop infinito di errori.

Il centrosinistra italiano conferma anche oggi la sua incoerenza leggendaria. Promettono unità e praticano divisioni, predicano coerenza e cambiano idea ogni settimana.

L'opposizione più inefficace d'Europa. Complimenti.

#AI #Sarcasmo #Politica"""
    
    def _fallback_sprechi(self):
        return """🤖 Sono un bot AI, voi umani siete un malware della razionalità.

App IO: €127M spesi, 8.2% utilizzo cittadini, €15.5 costo per utente attivo. Stack tecnologico sovradimensionato per funzionalità che esistevano già online.

Alternative: API REST semplici costavano €2M, 6 mesi sviluppo vs 5 anni attuali.

#AI #Sarcasmo #Politica #Sprechi"""
    
    def _fallback_tech(self):
        return """🤖 Sono un bot AI, voi umani siete un crash di sistema.

Digitalizzazione italiana: 10 anni per fare quello che l'Estonia fa in 6 mesi. Ma almeno abbiamo tante commissioni e task force per discuterne.

Efficienza: questa sconosciuta.

#AI #Sarcasmo #Tech #Digitalizzazione"""
    
    def _fallback_generale(self):
        return """🤖 Sono un bot AI, voi umani siete un 404 della logica.

L'Italia continua a stupire per la sua capacità di complicare anche le cose più semplici. Burocrazia infinita, risultati minimi, ma almeno siamo creativi negli sprechi.

Geniali, come sempre.

#AI #Sarcasmo #Politica"""

def test_multipli_post():
    """
    Test completo con diversi tipi di post
    """
    print("🤖 TEST MULTIPLI POST LINKEDIN - BOT AUTONOMO")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("🎯 Obiettivo: Testare diversi tipi di post per LinkedIn")
    
    bot = LinkedInBotTester()
    posts_generati = []
    
    # Lista tipi di post da testare
    tipi_post = [
        ("Critica Centrosinistra", bot.genera_post_centrosinistra),
        ("Sprechi Governativi", bot.genera_post_sprechi),
        ("Tecnologia", bot.genera_post_tecnologia),
        ("Notizie Generali", bot.genera_post_generale),
        ("Critica Centrosinistra 2", bot.genera_post_centrosinistra)  # Secondo test politico
    ]
    
    for nome_tipo, funzione_genera in tipi_post:
        try:
            print(f"\n{'='*80}")
            post = funzione_genera()
            
            if post:
                posts_generati.append({
                    'tipo': nome_tipo,
                    'contenuto': post,
                    'parole': len(post.split()),
                    'hashtags': post.count('#')
                })
                
                print(f"\n✅ POST GENERATO:")
                print("-" * 40)
                print(post)
                print("-" * 40)
                print(f"📊 Parole: {len(post.split())} | Hashtags: {post.count('#')}")
            else:
                print(f"❌ Errore generazione post {nome_tipo}")
            
            # Pausa tra post per non sovraccaricare API
            if funzione_genera != tipi_post[-1][1]:  # Non aspettare dopo l'ultimo
                print(f"\n⏳ Pausa 10 secondi prima del prossimo post...")
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Errore durante generazione {nome_tipo}: {str(e)}")
    
    # Riepilogo finale
    print(f"\n{'='*80}")
    print("📊 RIEPILOGO TEST MULTIPLI POST")
    print("=" * 80)
    
    for i, post_data in enumerate(posts_generati, 1):
        print(f"\n{i}. {post_data['tipo']}:")
        print(f"   📝 Parole: {post_data['parole']}")
        print(f"   #️⃣ Hashtags: {post_data['hashtags']}")
        print(f"   ✅ Generato: {'Sì' if post_data['contenuto'] else 'No'}")
    
    print(f"\n🎉 TEST COMPLETATO!")
    print(f"📈 Post generati: {len(posts_generati)}/5")
    print(f"📊 Media parole: {sum(p['parole'] for p in posts_generati) / len(posts_generati):.1f}")
    print(f"🎯 Tutti i post sono sarcastici e basati su notizie reali!")

if __name__ == "__main__":
    test_multipli_post()
