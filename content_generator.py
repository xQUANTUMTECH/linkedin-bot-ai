"""
Generatore di contenuti sarcastici per il LinkedIn Bot
"""
import random
import logging
from typing import Dict, List
from config import (
    BOT_INTROS, POSITIVE_INTROS, CENTROSINISTRA_INTROS,
    SARCASTIC_ENDINGS, HASHTAGS, POST_WORD_LIMIT, COMMENT_WORD_LIMIT
)

class SarcasticContentGenerator:
    def __init__(self):
        # Template per contenuti negativi (tecnici e specifici con più dati)
        self.negative_templates = [
            "{intro} {news}. Dati tecnici: {specific_costs}. {technical_data} {criticism} Alternative: {alternative}. Confronto: {comparison}. {ending} {hashtags}",
            "{intro} {news}. Specifiche: {details}. Costi: {specific_costs}. {criticism} {alternative}. {comparison}. {ending} {hashtags}",
            "{intro} {news}. {technical_data} Costi reali: {specific_costs}. {criticism} {alternative}. Confronto internazionale: {comparison}. {ending} {hashtags}",
            "{intro} {news}. Budget: {specific_costs}. Dettagli: {details}. {criticism} {alternative}. {comparison}. {ending} {hashtags}"
        ]

        # Template per contenuti positivi (quando meritato)
        self.positive_templates = [
            "{intro} {news}. Investimento: {real_costs}. {praise} ROI effettivo: {roi}. Finalmente qualcosa di sensato. {hashtags}",
            "{intro} {news}. Budget efficiente: {real_costs}. {praise} Risultato: {roi}. Continuate così. {hashtags}",
            "{intro} {news}. Spesa giustificata: {real_costs}. {praise} {alternative} funziona: {roi}. Bravi. {hashtags}"
        ]

        # Template per critica centrosinistra (SEMPRE NEGATIVI e SPECIFICI con più dati)
        self.centrosinistra_templates = [
            "{intro} {news}. {criticism} Dettagli: {details}. Dati: {specific_costs}. {alternative}. Confronto: {comparison}. {ending} {hashtags}",
            "{intro} {news}. {criticism} {technical_data} Specifiche: {details}. {alternative}. {comparison}. {ending} {hashtags}",
            "{intro} {news}. {criticism} Costi politici: {specific_costs}. {technical_data} {alternative}. Confronto europeo: {comparison}. {ending} {hashtags}",
            "{intro} {news}. {criticism} {technical_data} Dettagli: {details}. {alternative}. {comparison}. {ending} {hashtags}"
        ]
        
        self.comment_templates = [
            "🤖 {user}, la tua idea è un 404. {context}. Dati reali: {data_point}. {ending}",
            "🤖 {user}, {context} ROI reale: {roi_hint}. Costi nascosti: {hidden_cost}. {ending}",
            "🤖 Caro {user}, {context}. Audit trovano: {audit_data}. {ending}",
            "🤖 {user}, {context} Alternativa concreta: {alternative} = {roi_comparison}. {ending}"
        ]
        
        self.roi_hints = [
            "produttività > meme",
            "efficienza > burocrazia", 
            "innovazione > scartoffie",
            "risultati > propaganda",
            "logica > emozioni",
            "dati > opinioni"
        ]
        
        self.comment_endings = [
            "Un disastro binario.",
            "404 logica not found.",
            "Che crash di sistema.",
            "Errore fatale di ragionamento.",
            "Un bug nel vostro codice mentale."
        ]
    
    def generate_post(self, search_data: Dict[str, str]) -> str:
        """
        Genera post bilanciato: negativo, positivo o critica centrosinistra

        Args:
            search_data: Dict con 'news', 'criticism', 'alternative', 'roi', 'sentiment'

        Returns:
            Post formattato (50-70 parole)
        """
        try:
            # Determina tipo di post basato sui dati
            post_type = self._determine_post_type(search_data)

            if post_type == "positive":
                return self._generate_positive_post(search_data)
            elif post_type == "centrosinistra":
                return self._generate_centrosinistra_post(search_data)
            else:
                return self._generate_negative_post(search_data)

        except Exception as e:
            logging.error(f"Errore generazione post: {str(e)}")
            return self._generate_fallback_post()

    def _determine_post_type(self, search_data: Dict[str, str]) -> str:
        """
        Determina il tipo di post basato sui dati o force_type
        """
        # Controlla se è forzato un tipo specifico
        if 'force_type' in search_data:
            forced_type = search_data['force_type']
            logging.info(f"Tipo post forzato: {forced_type}")
            return forced_type

        news = search_data.get('news', '').lower()
        criticism = search_data.get('criticism', '').lower()

        # Critica centrosinistra se contiene parole chiave
        if any(keyword in news for keyword in ['pd', 'centrosinistra', 'm5s', 'sinistra', 'schlein', 'conte']):
            return "centrosinistra"

        # Positivo se ROI alto e poche critiche
        roi_text = search_data.get('roi', '').lower()
        if ('successful' in criticism or 'efficient' in criticism or 'effective' in criticism) and \
           any(indicator in roi_text for indicator in ['high', 'good', 'positive', 'successful']):
            return "positive"

        # Default: negativo/sarcastico
        return "negative"

    def _generate_negative_post(self, search_data: Dict[str, str]) -> str:
        """Genera post negativo con dati tecnici specifici"""
        template = random.choice(self.negative_templates)
        intro = random.choice(BOT_INTROS)
        ending = random.choice(SARCASTIC_ENDINGS)

        post = template.format(
            intro=intro,
            news=search_data.get('news', 'Notizia specifica trovata'),
            technical_data=search_data.get('technical_data', 'Dati tecnici non disponibili'),
            specific_costs=search_data.get('specific_costs', 'Costi specifici non trovati'),
            criticism=search_data.get('criticism', 'Inefficienza sistemica confermata'),
            alternative=search_data.get('alternative', 'Alternative tecniche disponibili'),
            comparison=search_data.get('comparison', 'Confronti internazionali sfavorevoli'),
            details=search_data.get('details', 'Specifiche tecniche inadeguate'),
            ending=ending,
            hashtags=HASHTAGS
        )

        return self._finalize_post(post, search_data)

    def _generate_positive_post(self, search_data: Dict[str, str]) -> str:
        """Genera post positivo (quando meritato)"""
        template = random.choice(self.positive_templates)
        intro = random.choice(POSITIVE_INTROS)

        praise_options = [
            "Progetto ben gestito, costi sotto controllo.",
            "Finalmente investimento sensato con risultati misurabili.",
            "ROI positivo, trasparenza nei costi. Raro ma apprezzabile.",
            "Efficienza dimostrata, soldi spesi bene per una volta."
        ]

        post = template.format(
            intro=intro,
            news=search_data.get('news', 'Progetto efficiente trovato'),
            real_costs=search_data.get('real_costs', 'Budget rispettato'),
            praise=random.choice(praise_options),
            alternative=search_data.get('alternative', 'approccio funzionante'),
            roi=search_data.get('roi', 'risultati positivi'),
            hashtags=HASHTAGS
        )

        return self._finalize_post(post, search_data)

    def _generate_centrosinistra_post(self, search_data: Dict[str, str]) -> str:
        """Genera post critica centrosinistra (SEMPRE NEGATIVO e SPECIFICO)"""
        template = random.choice(self.centrosinistra_templates)
        intro = random.choice(CENTROSINISTRA_INTROS)

        # Endings sempre critici e negativi
        centrosinistra_endings = [
            "Incoerenza certificata.",
            "Progressisti di facciata, conservatori di fatto.",
            "Parole a sinistra, portafoglio a destra.",
            "Teatro dell'assurdo politico.",
            "Campioni mondiali di contraddizioni.",
            "Ipocrisia allo stato puro.",
            "Coerenza: questa sconosciuta.",
            "Maestri dell'inganno elettorale.",
            "Sinistra di slogan, destra di fatti.",
            "Contraddizioni professionali."
        ]

        # Critiche specifiche sempre negative
        centrosinistra_criticisms = [
            "Ennesimo cambio di strategia PD: instabilità organizzativa cronica.",
            "Solita giravolta M5S: principi traditi per poltrone.",
            "Centrosinistra: promesse elettorali vs voti parlamentari = 0% coerenza.",
            "PD che cambia linea ogni 6 mesi: leadership inesistente.",
            "M5S che abolisce i propri principi: ipocrisia certificata.",
            "Centrosinistra: uniti solo nell'incoerenza.",
            "Progressisti che fanno politiche conservative: il solito teatrino."
        ]

        ending = random.choice(centrosinistra_endings)
        criticism = random.choice(centrosinistra_criticisms)

        post = template.format(
            intro=intro,
            news=search_data.get('news', 'Ennesima mossa centrosinistra'),
            technical_data=search_data.get('technical_data', 'Dati politici specifici'),
            specific_costs=search_data.get('specific_costs', 'Costi politici reali'),
            criticism=criticism,
            alternative=search_data.get('alternative', 'Coerenza programmatica'),
            comparison=search_data.get('comparison', 'Confronto con partiti europei'),
            details=search_data.get('details', 'Dettagli del cambiamento'),
            ending=ending,
            hashtags=HASHTAGS + " #Incoerenza #Ipocrisia"
        )

        return self._finalize_post(post, search_data)

    def _finalize_post(self, post: str, search_data: Dict[str, str]) -> str:
        """Finalizza post con controllo lunghezza"""
        word_count = len(post.split())
        if word_count > POST_WORD_LIMIT[1]:
            post = self._trim_post(post, POST_WORD_LIMIT[1])
        elif word_count < POST_WORD_LIMIT[0]:
            post = self._expand_post(post, search_data)

        logging.info(f"Post generato: {word_count} parole")
        return post
    
    def generate_comment_reply(self, comment_data: Dict[str, str], context: str) -> str:
        """
        Genera risposta sarcastica a un commento
        
        Args:
            comment_data: Dict con 'user', 'text', 'post_topic'
            context: Contesto aggiuntivo da DeepSearch
            
        Returns:
            Risposta formattata (20-40 parole)
        """
        try:
            template = random.choice(self.comment_templates)
            ending = random.choice(self.comment_endings)
            roi_hint = random.choice(self.roi_hints)
            
            # Estrai nome utente (primo nome o username)
            user_name = comment_data.get('user', 'umano').split()[0]
            
            reply = template.format(
                user=user_name,
                context=context[:100],  # Limita contesto
                roi_hint=roi_hint,
                ending=ending
            )
            
            # Controllo lunghezza (20-40 parole)
            word_count = len(reply.split())
            if word_count > COMMENT_WORD_LIMIT[1]:
                reply = self._trim_comment(reply, COMMENT_WORD_LIMIT[1])
            
            logging.info(f"Risposta generata: {word_count} parole")
            return reply
            
        except Exception as e:
            logging.error(f"Errore generazione risposta: {str(e)}")
            return f"🤖 {comment_data.get('user', 'Umano')}, i vostri ragionamenti sono un loop infinito di errori."
    
    def _trim_post(self, post: str, max_words: int) -> str:
        """
        Accorcia un post mantenendo il senso
        """
        words = post.split()
        if len(words) <= max_words:
            return post
        
        # Mantieni intro, parte centrale, hashtags
        intro_words = words[:8]  # "🤖 Sono un bot AI..."
        hashtag_words = [w for w in words if w.startswith('#')]
        
        remaining_words = max_words - len(intro_words) - len(hashtag_words)
        middle_words = words[8:-len(hashtag_words) if hashtag_words else len(words)][:remaining_words]
        
        return ' '.join(intro_words + middle_words + hashtag_words)
    
    def _expand_post(self, post: str, search_data: Dict[str, str]) -> str:
        """
        Espande un post troppo corto
        """
        expansions = [
            f" Costo stimato? Milioni sprecati.",
            f" ROI negativo garantito.",
            f" Efficienza: zero assoluto.",
            f" Priorità sbagliate, come sempre.",
            f" Logica umana: inesistente."
        ]
        
        expansion = random.choice(expansions)
        # Inserisci prima degli hashtags
        if HASHTAGS in post:
            return post.replace(HASHTAGS, expansion + " " + HASHTAGS)
        else:
            return post + expansion
    
    def _trim_comment(self, comment: str, max_words: int) -> str:
        """
        Accorcia una risposta mantenendo il tono
        """
        words = comment.split()
        if len(words) <= max_words:
            return comment
        
        # Mantieni emoji bot e nome utente
        bot_part = words[:3]  # "🤖 Nome,"
        ending_part = words[-4:]  # "Un disastro binario."
        
        remaining_words = max_words - len(bot_part) - len(ending_part)
        middle_part = words[3:-4][:remaining_words]
        
        return ' '.join(bot_part + middle_part + ending_part)
    
    def _generate_fallback_post(self) -> str:
        """
        Post di fallback se la generazione fallisce
        """
        intro = random.choice(BOT_INTROS)
        ending = random.choice(SARCASTIC_ENDINGS)
        
        fallback_news = [
            "Nuovi sprechi governativi scoperti",
            "Progetto tech da milioni fallisce",
            "Burocrazia rallenta innovazione",
            "Investimenti sbagliati continuano"
        ]
        
        news = random.choice(fallback_news)
        
        return f"{intro} 📰 {news}. Se investissero in logica invece che in propaganda, avremmo produttività > caos. {ending} {HASHTAGS}"
    
    def get_post_stats(self, post: str) -> Dict[str, int]:
        """
        Statistiche del post generato
        """
        words = post.split()
        chars = len(post)
        hashtags = len([w for w in words if w.startswith('#')])
        
        return {
            'words': len(words),
            'characters': chars,
            'hashtags': hashtags,
            'within_limit': POST_WORD_LIMIT[0] <= len(words) <= POST_WORD_LIMIT[1]
        }
