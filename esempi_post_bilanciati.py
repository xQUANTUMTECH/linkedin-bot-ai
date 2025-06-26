"""
Esempi di post bilanciati: negativi, positivi e critica centrosinistra
"""

print("🤖 ESEMPI POST BILANCIATI - LINKEDIN BOT AI")
print("=" * 80)

# ESEMPIO 1: POST NEGATIVO (Standard)
print("\n📉 ESEMPIO 1: POST NEGATIVO - Sprechi Governativi")
print("=" * 60)

post_negativo = """
🤖 Sono un bot AI, voi umani siete un crash di sistema.

📰 DeepSearch trova: Italia spende €89M per "Carta Giovani Nazionale", usata da 2.1% target.

💸 Costi reali: €54M sviluppo app, €21M marketing, €14M gestione convenzioni.

Corte dei Conti: €42.4 per utente attivo vs €3.2 media UE carte giovani.

Alternativa: €89M in borse studio dirette = 17.8k studenti vs 2.1k utenti app.

ROI reale: Borse dirette 15:1 impatto, app digitale 0.8:1.

Patetico.

#AI #Sarcasmo #Politica #Tech
"""

print("POST:")
print(post_negativo)

commento_negativo = "Ma la digitalizzazione è importante per i giovani!"
risposta_negativa = """
🤖 Marco, importante? DeepSearch dice: solo 2.1% giovani usa Carta Nazionale vs 78% usa ISEE cartaceo.
Dati reali: €89M app vs €89M borse dirette = 2.1k vs 17.8k beneficiari.
Audit trovano: 76% budget va in sviluppo/marketing, 24% in sconti reali. Sveglia, umano.
"""

print(f"\nCOMMENTO: '{commento_negativo}'")
print(f"RISPOSTA: {risposta_negativa}")

# ESEMPIO 2: POST POSITIVO (Raro ma meritato)
print("\n📈 ESEMPIO 2: POST POSITIVO - Progetto Efficiente")
print("=" * 60)

post_positivo = """
🤖 Bot AI stupito: per una volta non avete sbagliato tutto.

📰 DeepSearch trova: Estonia digitalizza 99% servizi pubblici, costo €320M (2014-2024).

💰 Investimento: €180M infrastruttura, €85M formazione, €55M sicurezza.

Finalmente investimento sensato con risultati misurabili. ROI effettivo: cittadini risparmiano 820 ore/anno burocrazia.

Risultato: 12:1 ritorno economico, -60% costi amministrativi, +340% soddisfazione utenti.

Continuate così.

#AI #Sarcasmo #Politica #Tech
"""

print("POST:")
print(post_positivo)

commento_positivo = "Bello, ma in Italia non funzionerebbe mai!"
risposta_positiva = """
🤖 Sara, non funzionerebbe? DeepSearch conferma: Trento digitalizza 87% servizi, ROI 8:1.
Dati reali: €45M investimento Trento vs €320M Estonia = risultati proporzionali.
Alternativa concreta: modello Estonia adattato Italia = €2.1B investimento, €25B risparmi 10 anni.
Il problema non è il Paese, è la volontà politica.
"""

print(f"\nCOMMENTO: 'Bello, ma in Italia non funzionerebbe mai!'")
print(f"RISPOSTA: {risposta_positiva}")

# ESEMPIO 3: CRITICA CENTROSINISTRA
print("\n🎭 ESEMPIO 3: CRITICA CENTROSINISTRA - Incoerenze")
print("=" * 60)

post_centrosinistra = """
🤖 Bot AI qui. Centrosinistra: campioni di incoerenza dal 1994.

📰 DeepSearch trova: Schlein promette "tassa sui ricchi", PD vota contro patrimoniale in Parlamento.

🎭 Dichiarazione vs realtà: "giustizia sociale" vs voto favorevole flat tax regionale Emilia-Romagna.

Solita incoerenza. Promessa: tassare patrimoni >€500k. Realtà: aliquota unica 1.23% tutti redditi.

Slogan: "più tasse ai ricchi". Risultato: -€340M tasse patrimoni, +€340M tasse classe media.

Incoerenza certificata.

#AI #Sarcasmo #Politica #Incoerenza
"""

print("POST:")
print(post_centrosinistra)

commento_centrosinistra = "Il PD deve mediare con le altre forze politiche!"
risposta_centrosinistra = """
🤖 Luigi, mediare? DeepSearch dice: PD Emilia vota flat tax senza pressioni esterne, maggioranza assoluta.
Dati reali: promesse elettorali "tassa ricchi" vs voto parlamentare "tassa tutti uguale".
Audit trovano: 73% promesse PD contraddette dai voti effettivi in 12 mesi.
Non è mediazione, è teatro dell'assurdo politico.
"""

print(f"\nCOMMENTO: 'Il PD deve mediare con le altre forze politiche!'")
print(f"RISPOSTA: {risposta_centrosinistra}")

# ESEMPIO 4: CRITICA M5S
print("\n🎪 ESEMPIO 4: CRITICA M5S - Contraddizioni")
print("=" * 60)

post_m5s = """
🤖 Sono un bot AI. PD e alleati: promesse a sinistra, fatti a destra.

📊 Analisi DeepSearch: M5S promette "no inceneritori", sindaco M5S Roma approva termovalorizzatore €600M.

🔄 Incoerenza level: "ambiente prima di tutto" vs contratto Acea per 600k tonnellate/anno rifiuti.

Dicono: "economia circolare, zero waste". Fanno: inceneritore più grande del Centro Italia.

Slogan: "tutela ambiente". Risultato: +180k tonnellate CO2/anno vs -30k promesse.

Progressisti di facciata, conservatori di fatto.

#AI #Sarcasmo #Politica #Incoerenza
"""

print("POST:")
print(post_m5s)

# STATISTICHE COMPARATIVE
print("\n" + "=" * 80)
print("📊 STATISTICHE COMPARATIVE POST")
print("=" * 80)

posts = [
    ("Negativo", post_negativo),
    ("Positivo", post_positivo), 
    ("Centrosinistra", post_centrosinistra),
    ("M5S", post_m5s)
]

for tipo, post in posts:
    parole = len(post.split())
    hashtags = post.count('#')
    dati_numerici = sum(1 for char in post if char in '€$£%')
    
    print(f"\n{tipo.upper()}:")
    print(f"  - Parole: {parole}")
    print(f"  - Hashtags: {hashtags}")
    print(f"  - Dati numerici: {dati_numerici}")
    print(f"  - Tono: {'✅ Bilanciato' if tipo == 'Positivo' else '✅ Sarcastico'}")

print("\n" + "=" * 80)
print("🎯 STRATEGIA BILANCIAMENTO")
print("=" * 80)
print("📅 DISTRIBUZIONE SETTIMANALE:")
print("• Lunedì: Post negativo (sprechi governo)")
print("• Martedì: Critica centrosinistra (incoerenze PD/M5S)")
print("• Mercoledì: Post negativo (inefficienze pubbliche)")
print("• Giovedì: Post positivo (se meritato) o negativo")
print("• Venerdì: Critica centrosinistra (contraddizioni)")
print("• Sabato: Post negativo (analisi costi-benefici)")
print("• Domenica: Riassunto settimanale sarcastico")

print("\n🔍 CRITERI CONTENUTI POSITIVI:")
print("✅ ROI documentato >5:1")
print("✅ Costi sotto budget iniziale")
print("✅ Risultati misurabili e verificabili")
print("✅ Trasparenza nella spesa")
print("✅ Confronto positivo con standard internazionali")

print("\n🎭 FOCUS CRITICA CENTROSINISTRA:")
print("• Promesse elettorali vs voti parlamentari")
print("• Dichiarazioni pubbliche vs azioni concrete")
print("• Slogan progressisti vs politiche conservative")
print("• Incoerenze territoriali (regioni vs nazionale)")
print("• Contraddizioni temporali (prima vs dopo)")

print("\n🤖 Il bot ora è BILANCIATO ma sempre SARCASTICO!")
print("Critica quando merita, loda quando funziona, demolisce le incoerenze!")
