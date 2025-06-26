# 🚂 Deploy LinkedIn Bot su Railway

Guida completa per deployare il LinkedIn Bot AI su Railway con database PostgreSQL.

## 📋 Pre-requisiti

- Account Railway ([railway.app](https://railway.app))
- Repository GitHub con il codice
- Credenziali LinkedIn
- API key xAI/Grok (già configurata nel progetto)

## 🚀 Step-by-Step Deploy

### 1. Preparazione Repository

```bash
# Clona il progetto
git clone <your-repository>
cd linkedin-bot

# Verifica file necessari
ls -la
# Dovresti vedere:
# - railway.json
# - Procfile  
# - requirements.txt
# - deploy_railway.py
```

### 2. Setup Railway

1. **Crea Account**: Vai su [railway.app](https://railway.app) e registrati
2. **Nuovo Progetto**: Click "New Project" → "Deploy from GitHub repo"
3. **Connetti Repository**: Seleziona il repository del bot
4. **Auto-Deploy**: Railway inizierà il primo deploy automaticamente

### 3. Aggiungi Database PostgreSQL

1. Nel dashboard del progetto, click **"+ New"**
2. Seleziona **"Database"** → **"Add PostgreSQL"**
3. Railway creerà automaticamente:
   - `DATABASE_URL` 
   - `DATABASE_PRIVATE_URL`
   - Credenziali database

### 4. Configura Variabili d'Ambiente

Nel dashboard Railway, vai su **"Variables"** e aggiungi:

```env
# OBBLIGATORIE
LINKEDIN_EMAIL=tua_email@example.com
LINKEDIN_PASSWORD=tua_password_linkedin

# GIÀ CONFIGURATE (non modificare)
XAI_API_KEY=xai-foL2y8TQ0kyLUU86uWlxDaLLgpm7O1NOzR3ftGKocglbe9VO4h6NgnBV8jxIkQIQ9rgGcjPug0WEyKkm

# RAILWAY AUTO-CONFIGURATE
DATABASE_URL=(auto-generata)
DATABASE_PRIVATE_URL=(auto-generata)
PORT=8080
RAILWAY_ENVIRONMENT=production

# OPZIONALI
LOG_LEVEL=INFO
POSTS_PER_DAY=3
MAX_COMMENTS_PER_POST=5
```

### 5. Deploy e Verifica

1. **Trigger Deploy**: Ogni push su GitHub triggera auto-deploy
2. **Controlla Log**: Nel dashboard Railway, tab "Deployments" → "View Logs"
3. **Verifica Servizi**:
   - ✅ Database PostgreSQL attivo
   - ✅ Web service attivo
   - ✅ Bot LinkedIn in background

### 6. Accesso Dashboard

Una volta deployato, accedi alla dashboard:
- **URL**: `https://your-project-name.railway.app`
- **Health Check**: `https://your-project-name.railway.app/api/health`

## 🔧 Configurazione Avanzata

### Custom Domain (Opzionale)

1. Nel dashboard Railway, vai su **"Settings"**
2. Sezione **"Domains"** → **"Custom Domain"**
3. Aggiungi il tuo dominio e configura DNS

### Scaling

Railway scala automaticamente, ma puoi configurare:
- **Memory**: 512MB - 8GB
- **CPU**: Condiviso o dedicato
- **Replicas**: 1-10 istanze

### Monitoring

Railway fornisce:
- **Metrics**: CPU, Memory, Network
- **Logs**: Real-time streaming
- **Alerts**: Email/Slack notifications

## 📊 Monitoraggio Post-Deploy

### 1. Dashboard Web
Accedi a `https://your-app.railway.app` per vedere:
- Statistiche giornaliere
- Post recenti
- Trend settimanali
- Log in tempo reale

### 2. API Endpoints
```bash
# Health check
curl https://your-app.railway.app/api/health

# Statistiche
curl https://your-app.railway.app/api/stats

# Post recenti
curl https://your-app.railway.app/api/posts
```

### 3. Database Access
```bash
# Connetti al database (da Railway CLI)
railway connect postgresql
```

## 🐛 Troubleshooting

### Errori Comuni

#### 1. "Module not found"
```bash
# Verifica requirements.txt
cat requirements.txt
# Assicurati che tutte le dipendenze siano elencate
```

#### 2. "Database connection failed"
```bash
# Controlla variabili d'ambiente
echo $DATABASE_URL
# Deve iniziare con postgresql://
```

#### 3. "LinkedIn authentication failed"
```bash
# Verifica credenziali
echo $LINKEDIN_EMAIL
# Controlla che email/password siano corrette
```

#### 4. "Grok API error"
```bash
# Verifica API key
echo $XAI_API_KEY
# Deve iniziare con xai-
```

### Log Debugging

```bash
# Railway CLI
railway logs

# O dalla dashboard web
https://your-app.railway.app/logs
```

### Restart Service

```bash
# Railway CLI
railway redeploy

# O dalla dashboard: Deployments → Redeploy
```

## 🔒 Sicurezza

### Variabili d'Ambiente
- ✅ Mai committare credenziali nel codice
- ✅ Usa solo variabili d'ambiente Railway
- ✅ Ruota periodicamente le password

### Rate Limiting
Il bot ha protezioni integrate:
- Max 3 post/giorno
- Max 5 risposte/post
- Delay tra azioni

### LinkedIn ToS
- Monitora per warning LinkedIn
- Rispetta i limiti di utilizzo
- Usa account dedicato per il bot

## 📈 Ottimizzazioni

### Performance
```python
# In config.py, per produzione:
DELAY_BETWEEN_POSTS = 300  # 5 minuti
DELAY_BETWEEN_COMMENTS = 60  # 1 minuto
```

### Costi Railway
- **Starter Plan**: $5/mese (sufficiente per il bot)
- **Database**: Incluso nel piano
- **Bandwidth**: 100GB/mese inclusi

### Backup Database
```bash
# Backup automatico Railway (7 giorni retention)
# Backup manuale:
railway run pg_dump $DATABASE_URL > backup.sql
```

## 🚀 Go Live!

Una volta completato il setup:

1. ✅ **Verifica Dashboard**: Accedi e controlla che tutto funzioni
2. ✅ **Test Post**: Monitora il primo post automatico
3. ✅ **Controlla Engagement**: Verifica risposte ai commenti
4. ✅ **Monitor Log**: Tieni d'occhio errori per 24h

## 📞 Supporto

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Community support
- **GitHub Issues**: Per problemi specifici del bot

---

**🎉 Il tuo LinkedIn Bot AI è ora live su Railway!**

Monitora le performance e goditi i post sarcastici automatici! 🤖
