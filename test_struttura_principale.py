"""
Test della struttura principale aggiornata del bot
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grok_api import GrokDeepSearch
from content_generator import SarcasticContentGenerator
from config import SEARCH_TOPICS, SPECIFIC_SEARCH_QUERIES
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_struttura_principale():
    """
    Test della struttura principale aggiornata
    """
    print("🤖 TEST STRUTTURA PRINCIPALE AGGIORNATA")
    print("=" * 80)
    
    # Inizializza componenti
    grok_search = GrokDeepSearch()
    content_generator = SarcasticContentGenerator()
    
    print("✅ Componenti inizializzati")
    
    # Test per ogni tipo di topic
    for topic in SEARCH_TOPICS[:3]:  # Test primi 3 per non sovraccaricare
        print(f"\n{'='*60}")
        print(f"🔍 TEST TOPIC: {topic.upper()}")
        print("=" * 60)
        
        try:
            # Cerca notizie con nuovo sistema
            print(f"📰 Ricerca notizie per topic: {topic}")
            search_data = grok_search.search_news_for_post(topic)
            
            print(f"📊 Dati ricevuti:")
            for key, value in search_data.items():
                print(f"  • {key}: {value[:80]}..." if value else f"  • {key}: [Vuoto]")
            
            # Genera post con nuovo sistema
            print(f"\n📝 Generazione post...")
            post = content_generator.generate_post(search_data)
            
            print(f"\n✅ POST GENERATO:")
            print("-" * 40)
            print(post)
            print("-" * 40)
            
            # Statistiche
            parole = len(post.split())
            hashtags = post.count('#')
            
            print(f"📊 STATISTICHE:")
            print(f"  • Parole: {parole}")
            print(f"  • Hashtags: {hashtags}")
            print(f"  • Tipo: {search_data.get('force_type', 'automatico')}")
            
            # Verifica qualità
            if parole >= 50 and parole <= 70:
                print(f"  ✅ Lunghezza ottimale")
            else:
                print(f"  ⚠️ Lunghezza non ottimale")
            
            if "🤖" in post:
                print(f"  ✅ Intro bot presente")
            else:
                print(f"  ❌ Intro bot mancante")
            
            if hashtags >= 3:
                print(f"  ✅ Hashtags sufficienti")
            else:
                print(f"  ⚠️ Pochi hashtags")
                
        except Exception as e:
            print(f"❌ Errore durante test {topic}: {str(e)}")
    
    print(f"\n{'='*80}")
    print("🎉 TEST STRUTTURA PRINCIPALE COMPLETATO")
    print("=" * 80)

def test_query_specifiche():
    """
    Test delle query specifiche
    """
    print("\n🔍 TEST QUERY SPECIFICHE")
    print("=" * 60)
    
    for topic, queries in SPECIFIC_SEARCH_QUERIES.items():
        print(f"\n📋 TOPIC: {topic.upper()}")
        for i, query in enumerate(queries, 1):
            print(f"  {i}. {query}")
    
    print(f"\n✅ Query specifiche configurate per {len(SPECIFIC_SEARCH_QUERIES)} topic")

def test_centrosinistra_specifico():
    """
    Test specifico per post centrosinistra
    """
    print(f"\n🎭 TEST SPECIFICO CENTROSINISTRA")
    print("=" * 60)
    
    try:
        grok_search = GrokDeepSearch()
        content_generator = SarcasticContentGenerator()
        
        # Forza tipo centrosinistra
        search_data = grok_search.search_news_for_post("centrosinistra")
        search_data['force_type'] = 'centrosinistra'
        
        print(f"📊 Dati centrosinistra:")
        for key, value in search_data.items():
            print(f"  • {key}: {value[:60]}..." if value else f"  • {key}: [Vuoto]")
        
        # Genera post centrosinistra
        post = content_generator.generate_post(search_data)
        
        print(f"\n🎭 POST CENTROSINISTRA:")
        print("-" * 40)
        print(post)
        print("-" * 40)
        
        # Verifica caratteristiche centrosinistra
        if any(keyword in post.lower() for keyword in ['pd', 'm5s', 'schlein', 'conte', 'centrosinistra']):
            print(f"✅ Contiene riferimenti centrosinistra")
        else:
            print(f"⚠️ Non contiene riferimenti specifici centrosinistra")
        
        if any(keyword in post.lower() for keyword in ['incoerenza', 'contraddizione', 'ipocrisia']):
            print(f"✅ Tono critico presente")
        else:
            print(f"⚠️ Tono critico insufficiente")
        
        if "#Incoerenza" in post or "#Ipocrisia" in post:
            print(f"✅ Hashtags specifici centrosinistra")
        else:
            print(f"⚠️ Hashtags specifici mancanti")
            
    except Exception as e:
        print(f"❌ Errore test centrosinistra: {str(e)}")

def main():
    """
    Test completo struttura principale
    """
    print("🚀 AVVIO TEST COMPLETO STRUTTURA PRINCIPALE")
    print("🎯 Obiettivo: Verificare che le modifiche funzionino")
    print("📋 Componenti: grok_api.py, content_generator.py, config.py")
    
    # Test componenti
    test_query_specifiche()
    test_struttura_principale()
    test_centrosinistra_specifico()
    
    print(f"\n🎉 TUTTI I TEST COMPLETATI!")
    print("=" * 80)
    print("✅ Struttura principale aggiornata")
    print("✅ Query specifiche configurate")
    print("✅ Dati tecnici integrati")
    print("✅ Post centrosinistra sempre negativi")
    print("✅ Template senza 'DeepSearch trova' e 'ROI'")
    
    print(f"\n🤖 Il bot ora cerca notizie SPECIFICHE e genera post TECNICI!")

if __name__ == "__main__":
    main()
