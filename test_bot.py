"""
Test script per verificare il funzionamento del bot
"""
import os
import sys
import logging
from datetime import datetime

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_grok_api():
    """
    Test API Grok DeepSearch
    """
    try:
        from grok_api import GrokDeepSearch
        
        logging.info("🧪 Test API Grok...")
        grok = GrokDeepSearch()
        
        # Test ricerca semplice
        result = grok.deep_search("latest technology news")
        
        if result:
            logging.info(f"✅ API Grok funziona: {result[:100]}...")
            return True
        else:
            logging.error("❌ API Grok non risponde")
            return False
            
    except Exception as e:
        logging.error(f"❌ Errore test Grok: {str(e)}")
        return False

def test_content_generator():
    """
    Test generatore contenuti
    """
    try:
        from content_generator import SarcasticContentGenerator
        
        logging.info("🧪 Test generatore contenuti...")
        generator = SarcasticContentGenerator()
        
        # Dati di test
        test_data = {
            'news': 'Governo spende milioni per progetto tech',
            'criticism': 'Soldi buttati in tecnologia obsoleta',
            'alternative': 'investire in R&D AI',
            'roi': 'innovazione reale vs burocrazia'
        }
        
        post = generator.generate_post(test_data)
        stats = generator.get_post_stats(post)
        
        logging.info(f"✅ Post generato ({stats['words']} parole): {post[:100]}...")
        
        # Test risposta commento
        comment_data = {'user': 'TestUser', 'text': 'Interessante!'}
        reply = generator.generate_comment_reply(comment_data, 'Contesto aggiuntivo')
        
        logging.info(f"✅ Risposta generata: {reply}")
        return True
        
    except Exception as e:
        logging.error(f"❌ Errore test generatore: {str(e)}")
        return False

def test_database():
    """
    Test connessione database
    """
    try:
        from database import db_manager
        
        logging.info("🧪 Test database...")
        
        # Test salvataggio post
        post_id = db_manager.save_post(
            content="Test post content",
            topic="test",
            word_count=50,
            hashtags_count=3
        )
        
        logging.info(f"✅ Post salvato nel DB: {post_id}")
        
        # Test statistiche
        stats = db_manager.get_daily_stats()
        logging.info(f"✅ Statistiche recuperate: {stats}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Errore test database: {str(e)}")
        return False

def test_configuration():
    """
    Test configurazione
    """
    try:
        from config import XAI_API_KEY, LINKEDIN_EMAIL, POST_TIMES
        
        logging.info("🧪 Test configurazione...")
        
        # Verifica API key
        if XAI_API_KEY and XAI_API_KEY.startswith('xai-'):
            logging.info("✅ API key Grok configurata")
        else:
            logging.warning("⚠️ API key Grok non configurata correttamente")
        
        # Verifica orari
        logging.info(f"✅ Orari post configurati: {POST_TIMES}")
        
        # Verifica email LinkedIn (senza mostrare password)
        if LINKEDIN_EMAIL and '@' in LINKEDIN_EMAIL:
            logging.info(f"✅ Email LinkedIn configurata: {LINKEDIN_EMAIL[:3]}***")
        else:
            logging.warning("⚠️ Email LinkedIn non configurata")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Errore test configurazione: {str(e)}")
        return False

def run_all_tests():
    """
    Esegue tutti i test
    """
    logging.info("🚀 Avvio test completi LinkedIn Bot")
    logging.info("=" * 50)
    
    tests = [
        ("Configurazione", test_configuration),
        ("API Grok", test_grok_api),
        ("Generatore Contenuti", test_content_generator),
        ("Database", test_database)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logging.info(f"\n📋 Test: {test_name}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            logging.error(f"❌ Test {test_name} fallito: {str(e)}")
            results[test_name] = False
    
    # Riepilogo
    logging.info("\n" + "=" * 50)
    logging.info("📊 RIEPILOGO TEST")
    logging.info("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logging.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logging.info(f"\nRisultato: {passed}/{total} test passati")
    
    if passed == total:
        logging.info("🎉 Tutti i test sono passati! Bot pronto per il deploy.")
        return True
    else:
        logging.warning("⚠️ Alcuni test sono falliti. Controlla la configurazione.")
        return False

def test_manual_post():
    """
    Test creazione post manuale
    """
    try:
        from main import LinkedInBotManager
        
        logging.info("🧪 Test creazione post manuale...")
        
        bot_manager = LinkedInBotManager()
        
        # Non autentica LinkedIn per il test
        logging.info("⚠️ Saltando autenticazione LinkedIn per test")
        
        # Test solo generazione contenuto
        topic = "latest technology news"
        search_data = bot_manager.grok_search.search_news_for_post(topic)
        post_content = bot_manager.content_generator.generate_post(search_data)
        
        logging.info(f"✅ Post di test generato:")
        logging.info(f"Topic: {topic}")
        logging.info(f"Contenuto: {post_content}")
        
        stats = bot_manager.content_generator.get_post_stats(post_content)
        logging.info(f"Stats: {stats}")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Errore test post manuale: {str(e)}")
        return False

def main():
    """
    Menu principale test
    """
    print("🤖 LinkedIn Bot - Test Suite")
    print("=" * 40)
    print("1. Esegui tutti i test")
    print("2. Test API Grok")
    print("3. Test generatore contenuti")
    print("4. Test database")
    print("5. Test configurazione")
    print("6. Test post manuale")
    print("7. Esci")
    
    while True:
        choice = input("\nScegli opzione (1-7): ").strip()
        
        if choice == "1":
            run_all_tests()
        elif choice == "2":
            test_grok_api()
        elif choice == "3":
            test_content_generator()
        elif choice == "4":
            test_database()
        elif choice == "5":
            test_configuration()
        elif choice == "6":
            test_manual_post()
        elif choice == "7":
            print("👋 Test completati!")
            break
        else:
            print("❌ Opzione non valida")

if __name__ == "__main__":
    main()
