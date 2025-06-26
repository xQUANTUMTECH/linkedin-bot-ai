"""
Database models e gestione per PostgreSQL su Railway
"""
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

from config import DATABASE_PRIVATE_URL, IS_PRODUCTION

Base = declarative_base()

class Post(Base):
    """
    Modello per i post pubblicati
    """
    __tablename__ = 'posts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    linkedin_post_id = Column(String(255), unique=True, nullable=True)
    content = Column(Text, nullable=False)
    topic = Column(String(255), nullable=False)
    word_count = Column(Integer, nullable=False)
    hashtags_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    published_at = Column(DateTime(timezone=True), nullable=True)
    is_published = Column(Boolean, default=False)
    engagement_processed = Column(Boolean, default=False)
    
    def to_dict(self) -> Dict:
        return {
            'id': str(self.id),
            'linkedin_post_id': self.linkedin_post_id,
            'content': self.content,
            'topic': self.topic,
            'word_count': self.word_count,
            'hashtags_count': self.hashtags_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'is_published': self.is_published,
            'engagement_processed': self.engagement_processed
        }

class Comment(Base):
    """
    Modello per i commenti e risposte
    """
    __tablename__ = 'comments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), nullable=False)  # FK to Post
    linkedin_comment_id = Column(String(255), nullable=True)
    commenter_name = Column(String(255), nullable=False)
    comment_text = Column(Text, nullable=False)
    our_reply = Column(Text, nullable=True)
    reply_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    replied_at = Column(DateTime(timezone=True), nullable=True)
    
    def to_dict(self) -> Dict:
        return {
            'id': str(self.id),
            'post_id': str(self.post_id),
            'linkedin_comment_id': self.linkedin_comment_id,
            'commenter_name': self.commenter_name,
            'comment_text': self.comment_text,
            'our_reply': self.our_reply,
            'reply_sent': self.reply_sent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None
        }

class BotStats(Base):
    """
    Statistiche giornaliere del bot
    """
    __tablename__ = 'bot_stats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime(timezone=True), nullable=False)
    posts_created = Column(Integer, default=0)
    posts_published = Column(Integer, default=0)
    comments_received = Column(Integer, default=0)
    replies_sent = Column(Integer, default=0)
    grok_api_calls = Column(Integer, default=0)
    grok_tokens_used = Column(Float, default=0.0)
    errors_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict:
        return {
            'id': str(self.id),
            'date': self.date.isoformat() if self.date else None,
            'posts_created': self.posts_created,
            'posts_published': self.posts_published,
            'comments_received': self.comments_received,
            'replies_sent': self.replies_sent,
            'grok_api_calls': self.grok_api_calls,
            'grok_tokens_used': self.grok_tokens_used,
            'errors_count': self.errors_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DatabaseManager:
    """
    Gestore database PostgreSQL
    """
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.setup_database()
    
    def setup_database(self):
        """
        Configura connessione database
        """
        try:
            # Usa URL privato su Railway per migliori performance
            db_url = DATABASE_PRIVATE_URL

            # Se non c'è DATABASE_URL (test locale), usa modalità mock
            if not db_url or db_url == "" or "localhost" in db_url:
                logging.warning("⚠️ DATABASE_URL non configurato o locale, modalità mock attiva")
                self.mock_mode = True
                return

            self.mock_mode = False

            # Configurazioni per produzione Railway
            engine_kwargs = {
                'echo': not IS_PRODUCTION,  # Log SQL solo in dev
                'pool_size': 5,
                'max_overflow': 10,
                'pool_pre_ping': True,  # Verifica connessioni
                'pool_recycle': 300  # Ricicla connessioni ogni 5 min
            }

            self.engine = create_engine(db_url, **engine_kwargs)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

            # Crea tabelle se non esistono
            Base.metadata.create_all(bind=self.engine)

            logging.info("✅ Database PostgreSQL configurato")
            
        except Exception as e:
            logging.error(f"❌ Errore configurazione database: {str(e)}")
            logging.warning("⚠️ Attivazione modalità mock per test locali")
            self.mock_mode = True
    
    def get_session(self) -> Session:
        """
        Ottieni sessione database
        """
        return self.SessionLocal()
    
    def save_post(self, content: str, topic: str, word_count: int, hashtags_count: int) -> str:
        """
        Salva un nuovo post nel database

        Returns:
            Post ID (UUID)
        """
        # Modalità mock per test locali
        if hasattr(self, 'mock_mode') and self.mock_mode:
            logging.info(f"📝 MOCK: Post salvato - Tipo: {topic}, Parole: {word_count}")
            return "mock-uuid-999"

        session = self.get_session()
        try:
            post = Post(
                content=content,
                topic=topic,
                word_count=word_count,
                hashtags_count=hashtags_count
            )

            session.add(post)
            session.commit()
            session.refresh(post)

            logging.info(f"Post salvato nel DB: {post.id}")
            return str(post.id)

        except Exception as e:
            session.rollback()
            logging.error(f"Errore salvataggio post: {str(e)}")
            raise
        finally:
            session.close()
    
    def update_post_published(self, post_id: str, linkedin_post_id: str):
        """
        Aggiorna post come pubblicato
        """
        session = self.get_session()
        try:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                post.linkedin_post_id = linkedin_post_id
                post.is_published = True
                post.published_at = datetime.now(timezone.utc)
                session.commit()
                logging.info(f"Post {post_id} marcato come pubblicato")
            
        except Exception as e:
            session.rollback()
            logging.error(f"Errore aggiornamento post: {str(e)}")
        finally:
            session.close()
    
    def save_comment(self, post_id: str, commenter_name: str, comment_text: str, 
                    linkedin_comment_id: str = None) -> str:
        """
        Salva un commento ricevuto
        """
        session = self.get_session()
        try:
            comment = Comment(
                post_id=post_id,
                linkedin_comment_id=linkedin_comment_id,
                commenter_name=commenter_name,
                comment_text=comment_text
            )
            
            session.add(comment)
            session.commit()
            session.refresh(comment)
            
            logging.info(f"Commento salvato: {comment.id}")
            return str(comment.id)
            
        except Exception as e:
            session.rollback()
            logging.error(f"Errore salvataggio commento: {str(e)}")
            raise
        finally:
            session.close()
    
    def update_comment_reply(self, comment_id: str, reply_text: str):
        """
        Aggiorna commento con la nostra risposta
        """
        session = self.get_session()
        try:
            comment = session.query(Comment).filter(Comment.id == comment_id).first()
            if comment:
                comment.our_reply = reply_text
                comment.reply_sent = True
                comment.replied_at = datetime.now(timezone.utc)
                session.commit()
                logging.info(f"Risposta salvata per commento {comment_id}")
            
        except Exception as e:
            session.rollback()
            logging.error(f"Errore aggiornamento risposta: {str(e)}")
        finally:
            session.close()
    
    def get_recent_posts(self, hours: int = 24) -> List[Dict]:
        """
        Ottieni post recenti per engagement
        """
        session = self.get_session()
        try:
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
            
            posts = session.query(Post).filter(
                Post.published_at >= cutoff_time,
                Post.is_published == True,
                Post.engagement_processed == False
            ).all()
            
            return [post.to_dict() for post in posts]
            
        except Exception as e:
            logging.error(f"Errore recupero post recenti: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_daily_stats(self, date: datetime = None) -> Dict:
        """
        Ottieni statistiche giornaliere
        """
        if not date:
            date = datetime.now(timezone.utc).date()
        
        session = self.get_session()
        try:
            stats = session.query(BotStats).filter(
                BotStats.date >= date,
                BotStats.date < date + timedelta(days=1)
            ).first()
            
            if stats:
                return stats.to_dict()
            else:
                # Crea stats vuote per oggi
                new_stats = BotStats(date=datetime.combine(date, datetime.min.time()))
                session.add(new_stats)
                session.commit()
                session.refresh(new_stats)
                return new_stats.to_dict()
                
        except Exception as e:
            logging.error(f"Errore recupero statistiche: {str(e)}")
            return {}
        finally:
            session.close()
    
    def update_stats(self, **kwargs):
        """
        Aggiorna statistiche giornaliere
        """
        today = datetime.now(timezone.utc).date()
        session = self.get_session()
        try:
            stats = session.query(BotStats).filter(
                BotStats.date >= today,
                BotStats.date < today + timedelta(days=1)
            ).first()
            
            if not stats:
                stats = BotStats(date=datetime.combine(today, datetime.min.time()))
                session.add(stats)
            
            # Aggiorna campi forniti
            for key, value in kwargs.items():
                if hasattr(stats, key):
                    current_value = getattr(stats, key) or 0
                    setattr(stats, key, current_value + value)
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            logging.error(f"Errore aggiornamento statistiche: {str(e)}")
        finally:
            session.close()

# Istanza globale
db_manager = DatabaseManager()
