"""
Dashboard web per monitorare il bot LinkedIn
Compatibile con Railway deployment
"""
from flask import Flask, render_template, jsonify, request
import logging
from datetime import datetime, timedelta
from database import db_manager
from config import PORT, IS_PRODUCTION

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linkedin-bot-dashboard-2025'

@app.route('/')
def dashboard():
    """
    Dashboard principale
    """
    try:
        # Statistiche oggi
        today_stats = db_manager.get_daily_stats()
        
        # Post recenti
        recent_posts = db_manager.get_recent_posts(hours=48)
        
        # Statistiche ultimi 7 giorni
        weekly_stats = []
        for i in range(7):
            date = datetime.now().date() - timedelta(days=i)
            stats = db_manager.get_daily_stats(date)
            weekly_stats.append(stats)
        
        return render_template('dashboard.html', 
                             today_stats=today_stats,
                             recent_posts=recent_posts,
                             weekly_stats=weekly_stats)
    
    except Exception as e:
        logging.error(f"Errore dashboard: {str(e)}")
        return f"Errore: {str(e)}", 500

@app.route('/api/stats')
def api_stats():
    """
    API per statistiche in tempo reale
    """
    try:
        stats = db_manager.get_daily_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts')
def api_posts():
    """
    API per lista post recenti
    """
    try:
        hours = request.args.get('hours', 24, type=int)
        posts = db_manager.get_recent_posts(hours=hours)
        return jsonify(posts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """
    Health check per Railway
    """
    try:
        # Test connessione database
        stats = db_manager.get_daily_stats()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/logs')
def view_logs():
    """
    Visualizza log recenti
    """
    try:
        # Leggi ultimi 100 log dal file
        with open('linkedin_bot.log', 'r') as f:
            lines = f.readlines()
            recent_logs = lines[-100:] if len(lines) > 100 else lines
        
        return render_template('logs.html', logs=recent_logs)
    
    except FileNotFoundError:
        return "Log file non trovato", 404
    except Exception as e:
        return f"Errore lettura log: {str(e)}", 500

# Template HTML inline per semplicità
@app.route('/templates/dashboard.html')
def dashboard_template():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>LinkedIn Bot Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .stat-item { text-align: center; padding: 15px; background: #007acc; color: white; border-radius: 6px; }
        .stat-number { font-size: 2em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.9; }
        .post-item { border-left: 4px solid #007acc; padding: 10px; margin: 10px 0; background: #f9f9f9; }
        .post-content { font-style: italic; color: #666; margin: 5px 0; }
        .post-meta { font-size: 0.8em; color: #999; }
        h1, h2 { color: #333; }
        .refresh-btn { background: #007acc; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .refresh-btn:hover { background: #005a99; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 LinkedIn Bot Dashboard</h1>
        
        <div class="card">
            <h2>📊 Statistiche Oggi</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{{ today_stats.posts_published or 0 }}</div>
                    <div class="stat-label">Post Pubblicati</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ today_stats.comments_received or 0 }}</div>
                    <div class="stat-label">Commenti Ricevuti</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ today_stats.replies_sent or 0 }}</div>
                    <div class="stat-label">Risposte Inviate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ today_stats.grok_api_calls or 0 }}</div>
                    <div class="stat-label">API Calls Grok</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📝 Post Recenti</h2>
            {% for post in recent_posts %}
            <div class="post-item">
                <div class="post-content">"{{ post.content[:100] }}..."</div>
                <div class="post-meta">
                    Topic: {{ post.topic }} | 
                    Parole: {{ post.word_count }} | 
                    Pubblicato: {{ post.published_at or 'Non ancora' }}
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="card">
            <h2>📈 Trend Settimanale</h2>
            <div class="stats-grid">
                {% for day_stats in weekly_stats %}
                <div class="stat-item">
                    <div class="stat-number">{{ day_stats.posts_published or 0 }}</div>
                    <div class="stat-label">{{ day_stats.date[:10] if day_stats.date else 'N/A' }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="card">
            <button class="refresh-btn" onclick="location.reload()">🔄 Aggiorna</button>
            <a href="/logs" class="refresh-btn" style="text-decoration: none; margin-left: 10px;">📋 Visualizza Log</a>
        </div>
    </div>
    
    <script>
        // Auto-refresh ogni 30 secondi
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    # Configurazione per Railway
    if IS_PRODUCTION:
        # Produzione su Railway
        app.run(host='0.0.0.0', port=PORT, debug=False)
    else:
        # Sviluppo locale
        app.run(host='127.0.0.1', port=5000, debug=True)
