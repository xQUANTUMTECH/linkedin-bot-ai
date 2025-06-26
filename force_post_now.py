#!/usr/bin/env python3
"""
Script per forzare un post immediato su LinkedIn (simula post delle 20:00)
"""

import os
import sys
import logging
from datetime import datetime

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import LinkedInBotManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def force_evening_post():
    """
    Forza un post serale immediato
    """
    print("🚀 FORZANDO POST SERALE DELLE 20:00...")
    print("=" * 50)
    
    try:
        # Inizializza il bot manager
        bot_manager = LinkedInBotManager()
        
        # Forza routine serale
        print("🌅 Esecuzione routine serale...")
        success = bot_manager.daily_routine()
        
        if success:
            print("🎉 POST SERALE PUBBLICATO CON SUCCESSO!")
            print("🔗 Controlla il tuo profilo LinkedIn")
            return True
        else:
            print("❌ Errore nella pubblicazione del post")
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        logging.exception("Dettagli errore:")
        return False

if __name__ == "__main__":
    print(f"🕐 Ora attuale: {datetime.now().strftime('%H:%M:%S')}")
    print("🎯 Forzando post delle 20:00 ADESSO...")
    
    success = force_evening_post()
    
    if success:
        print("\n✅ TEST POST COMPLETATO!")
    else:
        print("\n❌ TEST POST FALLITO!")
