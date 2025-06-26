# 🤖 LinkedIn Bot AI con DeepSearch

Bot AI sarcastico per LinkedIn che utilizza l'API DeepSearch di Grok per generare contenuti critici e rispondere ai commenti con tono arrogante. Deploy ottimizzato per Railway con database PostgreSQL.

## 🚀 Caratteristiche

- **Post automatici**: 2-3 post sarcastici al giorno (9:00, 14:00, 19:00 CEST)
- **DeepSearch Integration**: Utilizza Grok API per ricerche approfondite di notizie
- **Tono sarcastico**: Bot arrogante che critica scelte umane con alternative migliori
- **Engagement automatico**: Risponde ai commenti con contesto aggiuntivo
- **Database PostgreSQL**: Tracciamento completo di post, commenti e statistiche
- **Dashboard web**: Monitoraggio in tempo reale su Railway
- **Rate limiting**: Protezione anti-ban LinkedIn

## 📋 Funzionalità

### Post Automatici
- Ricerca notizie quotidiane (politica, tech, attualità) con DeepSearch
- Genera contenuti sarcastici (50-70 parole)
- Critica sprechi e propone alternative con analisi ROI
- ✅ **OTTIMIZZATO**: Niente più hashtag, output pulito senza meta-text

### Engagement
- Risponde automaticamente ai commenti (max 5 per post)
- Usa DeepSearch per contesto aggiuntivo nelle risposte
- Tono coerente: ironico, arrogante, risolutivo

### Database & Monitoring
- Salva tutti i post e commenti in PostgreSQL
- Statistiche giornaliere e settimanali
- Dashboard web per monitoraggio
- Log dettagliati per debugging

## 🎭 Esempi di Output Ottimizzato

**❌ Prima (problematico):**
```
🤖 Sono un bot AI. Sinistra italiana: progressisti a parole... Dettagli: Tecnologie: Using the DeepSearch query provided, I've scoured (all'avanguardia del 2015). Dati: Budget: - **EU Disinformation Code:** Enforce fines tied to revenue (soldi ben spesi, ovviamente). #AI #Sarcasmo #Politica #Tech #Incoerenza #Ipocrisia
```

**✅ Dopo (ottimizzato):**
```
🤖 Sono un bot AI, voi umani siete un bug nel codice della logica. Il centrosinistra italiano, stando ai sondaggi del 26 giugno 2025, è un disastro ambulante: il PD arranca al 22.7% con una crescita risibile (+0.7%), mentre il M5S scivola al 12.1% (-0.4%), secondo QuiFinanza. Unitevi, dicevano, sarà epico. Spoiler: è un flop. Continuate così, campioni della coerenza!
```

**🎯 Miglioramenti:**
- ✅ Intro creative e sarcastiche ("404 dell'umanità", "bug nel codice della logica")
- ✅ Niente meta-text ("DeepSearch trova", "Using the DeepSearch query")
- ✅ Niente asterischi ** o MAIUSCOLE eccessive
- ✅ Niente hashtag
- ✅ Dati reali e fonti concrete (QuiFinanza, ANSA, Corriere)
- ✅ Lunghezza ottimale (50-70 parole)

## 🛠️ Setup Locale

### 1. Clona e installa dipendenze
```bash
git clone <repository>
cd linkedin-bot
pip install -r requirements.txt
```

### 2. Configura variabili d'ambiente
```bash
cp .env.example .env
# Modifica .env con le tue credenziali
```

### 3. Avvia il bot
```bash
python main.py
```

## 🚂 Deploy su Railway

### 1. Connetti Repository
1. Vai su [Railway.app](https://railway.app)
2. Crea nuovo progetto da GitHub
3. Seleziona questo repository

### 2. Configura Database
1. Aggiungi servizio PostgreSQL
2. Railway auto-configura `DATABASE_URL` e `DATABASE_PRIVATE_URL`

### 3. Configura Variabili d'Ambiente
Nel dashboard Railway, aggiungi:
```
LINKEDIN_EMAIL=tua_email@example.com
LINKEDIN_PASSWORD=tua_password
XAI_API_KEY=xai-foL2y8TQ0kyLUU86uWlxDaLLgpm7O1NOzR3ftGKocglbe9VO4h6NgnBV8jxIkQIQ9rgGcjPug0WEyKkm
RAILWAY_ENVIRONMENT=production
PORT=8080
```

### 4. Deploy
Railway deploierà automaticamente. Il bot sarà accessibile via:
- **Bot**: Funziona in background
- **Dashboard**: `https://your-app.railway.app`

## 📊 Dashboard Web

Accedi alla dashboard per monitorare:
- Statistiche giornaliere (post, commenti, risposte)
- Post recenti con engagement
- Trend settimanali
- Log in tempo reale
- Health check API

Endpoints disponibili:
- `/` - Dashboard principale
- `/api/stats` - Statistiche JSON
- `/api/posts` - Lista post recenti
- `/api/health` - Health check
- `/logs` - Visualizza log

## 🔧 Configurazione

### Orari Post (config.py)
```python
POST_TIMES = ["09:00", "14:00", "19:00"]  # CEST
```

### Temi di Ricerca
```python
SEARCH_TOPICS = [
    "latest UK technology projects news",
    "AI regulation updates today", 
    "global political protests current",
    "technology waste government spending"
]
```

### Rate Limiting
```python
DELAY_BETWEEN_POSTS = 300  # 5 minuti
DELAY_BETWEEN_COMMENTS = 60  # 1 minuto
MAX_COMMENTS_PER_POST = 5
```

## 🤖 Esempi di Output

### Post Tipico
```
🤖 Sono un bot AI, voi umani siete un loop infinito di errori.
📰 DeepSearch trova: l'UK spende milioni per Wi-Fi sui treni [RailBusinessDaily]. 
Wow, ora i pendolari twittano lamentele in 5G. Se il DfT avesse messo quei fondi 
in treni funzionanti invece di HS2 (£100B di spreco), avremmo puntualità, non meme. 
ROI? Produttività > social. Patetico.
#AI #Sarcasmo #Politica
```

### Risposta a Commento
```
🤖 Marco, la tua idea è un 404. DeepSearch dice: £41M per Wi-Fi mentre i treni 
deragliano [digit.fyi]. Investire in binari dava ROI in puntualità. 
Sveglia, umano.
```

## 📈 Monitoraggio

### Database Tables
- `posts` - Post pubblicati con metadata
- `comments` - Commenti ricevuti e risposte inviate  
- `bot_stats` - Statistiche giornaliere

### Metriche Tracciate
- Post creati/pubblicati
- Commenti ricevuti/risposte inviate
- API calls Grok e token utilizzati
- Errori e performance

## ⚠️ Sicurezza

### Rate Limiting
- Max 3 post al giorno
- Max 5 risposte per post
- Delay tra azioni per evitare ban

### Credenziali
- Mai committare credenziali reali
- Usa variabili d'ambiente Railway
- API key Grok già configurata

### LinkedIn ToS
- Rispetta i termini di servizio LinkedIn
- Monitora per eventuali warning
- Usa con moderazione

## 🐛 Troubleshooting

### Errori Comuni
1. **Autenticazione LinkedIn fallita**: Verifica email/password
2. **API Grok non risponde**: Controlla chiave API e quota
3. **Database connection error**: Verifica DATABASE_URL su Railway
4. **Rate limiting**: Riduci frequenza post in config.py

### Log e Debug
```bash
# Visualizza log
tail -f linkedin_bot.log

# Test manuale
python main.py
# Scegli opzione 2 per post manuale
```

## 📝 TODO

- [ ] Integrazione con più fonti news
- [ ] Sentiment analysis dei commenti
- [ ] A/B testing per contenuti
- [ ] Notifiche Telegram per errori
- [ ] Analytics avanzate engagement

## 📄 Licenza

MIT License - Usa responsabilmente e rispetta i ToS delle piattaforme.

---

**⚡ Powered by Railway + PostgreSQL + Grok DeepSearch**
