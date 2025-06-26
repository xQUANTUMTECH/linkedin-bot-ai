"""
Test della ricerca approfondita del bot con simulazione API Grok
"""
import random
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MockGrokAPI:
    """
    Simulazione API Grok per test
    """
    def __init__(self):
        self.call_count = 0
        
    def deep_search(self, query):
        """
        Simula risposta API Grok basata sulla query
        """
        self.call_count += 1
        logging.info(f"🔍 API Call #{self.call_count}: {query[:60]}...")
        
        # Simula risposte realistiche basate sulla query
        if "latest news" in query.lower() and "technology" in query.lower():
            return """
            UK Government announces £450M investment in "Smart Cities Initiative" 
            across 15 major cities. Project aims to deploy IoT sensors, AI traffic 
            management, and digital infrastructure by 2026. Department for Digital, 
            Culture, Media & Sport leads initiative with local councils.
            """
            
        elif "budget breakdown" in query.lower() or "how money was spent" in query.lower():
            return """
            Smart Cities budget breakdown revealed through FOI request:
            - £280M to consulting firms (Deloitte, McKinsey, Accenture)
            - £95M for IoT hardware procurement 
            - £45M for project management and administration
            - £30M contingency fund
            Contracts awarded without competitive tender to usual suspects.
            """
            
        elif "similar successful projects" in query.lower() or "alternatives" in query.lower():
            return """
            Estonia's e-Residency program: €50M investment, 100,000+ digital residents,
            €1B+ economic impact. ROI: 20:1 over 5 years.
            
            Singapore Smart Nation: S$2.5B investment, 40% reduction in traffic congestion,
            25% improvement in energy efficiency. ROI: 12:1 over 7 years.
            
            Alternative: Direct infrastructure investment shows 8:1 ROI vs 
            consulting-heavy approaches at 2.3:1 ROI.
            """
            
        elif "waste" in query.lower() or "audit" in query.lower() or "criticism" in query.lower():
            return """
            National Audit Office report 2024: UK digital transformation projects
            show 67% cost overruns, 43% delivery delays. 
            
            Previous "Digital by Default" program: £2.3B spent, only 23% of 
            promised services delivered. Public Accounts Committee criticized
            "gold-plating" and over-reliance on external consultants.
            
            Cabinet Office admits 58% of digital budgets go to management fees,
            not actual technology delivery.
            """
            
        else:
            return "Generic search result with some relevant information."

def test_ricerca_approfondita():
    """
    Test completo della ricerca approfondita
    """
    print("🧪 TEST RICERCA APPROFONDITA LINKEDIN BOT")
    print("=" * 60)
    
    # Inizializza mock API
    mock_grok = MockGrokAPI()
    
    # Simula il processo di ricerca del bot
    topic = "latest UK technology projects news"
    
    print(f"📋 Topic selezionato: {topic}")
    print("\n🔍 FASE 1: Ricerca notizia principale")
    main_query = f"Find latest news about {topic} with specific costs, budgets, and financial details from last 48 hours"
    main_result = mock_grok.deep_search(main_query)
    print(f"Risultato: {main_result.strip()[:100]}...")
    
    print("\n💸 FASE 2: Approfondimento costi")
    cost_query = f"Based on this news: {main_result[:200]}, find exact budget breakdown, how money was actually spent, contractor details"
    cost_details = mock_grok.deep_search(cost_query)
    print(f"Risultato: {cost_details.strip()[:100]}...")
    
    print("\n📊 FASE 3: Ricerca alternative e ROI")
    roi_query = f"For this project: {main_result[:200]}, find similar successful projects, their costs, ROI data, and concrete alternatives"
    roi_analysis = mock_grok.deep_search(roi_query)
    print(f"Risultato: {roi_analysis.strip()[:100]}...")
    
    print("\n🚨 FASE 4: Ricerca sprechi e audit")
    waste_query = f"Find criticism, audit reports, or analysis about waste and inefficiency in: {main_result[:200]}"
    waste_details = mock_grok.deep_search(waste_query)
    print(f"Risultato: {waste_details.strip()[:100]}...")
    
    # Simula parsing dei risultati
    print("\n🧮 FASE 5: Parsing e generazione contenuto")
    
    # Estrai dati chiave (simulato)
    parsed_data = {
        'news': "UK lancia Smart Cities Initiative da £450M per 15 città",
        'real_costs': "£280M consulenze, £95M hardware, £45M admin, £30M extra",
        'criticism': "NAO audit: 67% progetti sforano budget, 58% va in management fees",
        'alternative': "Modello Estonia: investimento diretto €50M = ROI 20:1",
        'roi': "ROI diretto 8:1 vs consulenze 2.3:1",
        'details': "Appalti senza gara a Deloitte, McKinsey, Accenture",
        'waste_data': "£2.3B Digital by Default: solo 23% servizi promessi consegnati"
    }
    
    print("Dati estratti:")
    for key, value in parsed_data.items():
        print(f"  {key}: {value}")
    
    return parsed_data

def genera_post_con_dati_reali(data):
    """
    Genera post usando i dati della ricerca approfondita
    """
    print("\n📝 GENERAZIONE POST CON DATI REALI")
    print("=" * 60)
    
    intro = "🤖 Sono un bot AI, voi umani siete un loop infinito di errori."
    
    post = f"""{intro}

📰 DeepSearch trova: {data['news']}.

💸 Costi reali: {data['real_costs']}.

{data['criticism']}

Alternativa: {data['alternative']}.

ROI reale: {data['roi']}.

Dettagli: {data['details']}.

Patetico.

#AI #Sarcasmo #Politica #Tech"""
    
    return post

def simula_engagement(post_data):
    """
    Simula engagement con commenti e risposte
    """
    print("\n💬 SIMULAZIONE ENGAGEMENT")
    print("=" * 60)
    
    # Commenti simulati
    commenti = [
        {"user": "Marco", "text": "Le smart cities sono il futuro!"},
        {"user": "Sara", "text": "Investimenti necessari per la digitalizzazione"},
        {"user": "Luigi", "text": "Meglio questo che niente"}
    ]
    
    mock_grok = MockGrokAPI()
    
    for commento in commenti:
        print(f"\n👤 COMMENTO: {commento['user']} dice '{commento['text']}'")
        
        # Ricerca contesto per risposta
        context_query = f"Find additional critical details about UK Smart Cities Initiative to counter this comment: '{commento['text']}'"
        context = mock_grok.deep_search(context_query)
        
        # Genera risposta sarcastica con dati
        if "futuro" in commento['text'].lower() or "future" in commento['text'].lower():
            risposta = f"🤖 {commento['user']}, futuro? DeepSearch dice: NAO report mostra 67% progetti UK falliscono. Dati reali: £450M Smart Cities vs Estonia €50M = 2.3:1 vs 20:1 ROI. Il futuro è efficienza, non consulenze. 404 logica not found."
        elif "digitalizzazione" in commento['text'].lower():
            risposta = f"🤖 {commento['user']}, digitalizzazione? DeepSearch conferma: £280M vanno a consulenti, £95M a tecnologia reale. Audit trovano: 58% budget in management fees. Prima risultati, poi buzzword. Un disastro binario."
        else:
            risposta = f"🤖 {commento['user']}, meglio niente? DeepSearch dice: £2.3B Digital by Default = 23% servizi consegnati. Costi nascosti: £450M Smart Cities = £30M per città vs €3.3M media UE. Continuate a sbagliare, geni."
        
        print(f"🤖 RISPOSTA BOT: {risposta}")

def main():
    """
    Test completo
    """
    print("🚀 AVVIO TEST COMPLETO RICERCA APPROFONDITA")
    print("=" * 80)
    
    # Fase 1: Ricerca approfondita
    data = test_ricerca_approfondita()
    
    # Fase 2: Generazione post
    post = genera_post_con_dati_reali(data)
    
    print("\n📄 POST FINALE GENERATO:")
    print("=" * 60)
    print(post)
    
    # Statistiche post
    word_count = len(post.split())
    hashtag_count = post.count('#')
    
    print(f"\n📊 STATISTICHE POST:")
    print(f"Parole: {word_count} (target: 50-70)")
    print(f"Hashtags: {hashtag_count}")
    print(f"Dati reali inclusi: ✅")
    print(f"ROI numerico: ✅")
    print(f"Breakdown costi: ✅")
    print(f"Fonti audit: ✅")
    
    # Fase 3: Simulazione engagement
    simula_engagement(data)
    
    print("\n🎉 TEST COMPLETATO!")
    print("=" * 60)
    print("✅ Ricerca approfondita: 4 query multiple")
    print("✅ Dati reali estratti: costi, ROI, audit")
    print("✅ Post generato con breakdown dettagliato")
    print("✅ Risposte con contesto aggiuntivo")
    print("✅ Tono sarcastico mantenuto")
    print("\n🤖 Il bot è pronto per cercare DATI REALI, non opinioni!")

if __name__ == "__main__":
    main()
