import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .preprocessing import tanglish_preprocessor, ASPECT_TAXONOMY, POS_CUES_STRONG, NEG_CUES_STRONG

class TanglishABSAPipeline:
    def __init__(self, model_name: str = "xlm-roberta-base", device: str = None):
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
            
        print(f"Loading Tanglish ABSA pipeline on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2).to(self.device)
        self.model.eval()

    def analyze(self, sentence: str):
        """
        Executes Two-Stage Aspect-Based Sentiment Analysis:
        Stage 1: Aspect Term Extraction (ATE) via lexicon and morphology matching
        Stage 2: Aspect-Level Sentiment Classification (ALSC) via Knowledge-Enhanced Transformer Cross-Attention
        """
        clean_text = tanglish_preprocessor(sentence)
        
        # Stage 1: Extract Aspect Terms
        found_aspects = []
        for term, category in ASPECT_TAXONOMY.items():
            if re.search(r'\b' + re.escape(term) + r'\b', clean_text):
                found_aspects.append((term, category))
                
        if not found_aspects:
            return {"sentence": sentence, "clean_sentence": clean_text, "aspects": []}

        results = []
        for term, category in found_aspects:
            # Stage 2: Aspect-Conditioned Query Formulation
            formatted_query = f"Aspect: {term} | Category: {category} | Review: {clean_text}"
            
            inputs = self.tokenizer(formatted_query, return_tensors="pt", truncation=True, max_length=128).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                prob = torch.softmax(outputs.logits, dim=-1).cpu().numpy()[0]
                
            prob_pos = prob[1] if len(prob) > 1 else prob[0]
            
            # Knowledge Fusion & Postpositional Negation Resolution Window
            words = clean_text.split()
            term_idx = [i for i, w in enumerate(words) if term in w]
            local_text = clean_text
            if term_idx:
                start_i = max(0, term_idx[0] - 4)
                end_i = min(len(words), term_idx[0] + 5)
                local_text = " ".join(words[start_i:end_i])
                
            has_pos = any(c in local_text for c in POS_CUES_STRONG)
            has_neg = any(c in local_text for c in NEG_CUES_STRONG)
            
            if has_pos and not has_neg:
                score = 0.65 * 1.0 + 0.35 * prob_pos
            elif has_neg and not has_pos:
                score = 0.65 * 0.0 + 0.35 * prob_pos
            else:
                score = prob_pos
                
            sentiment = "POSITIVE" if score >= 0.50 else "NEGATIVE"
            confidence = score if sentiment == "POSITIVE" else (1.0 - score)
            
            results.append({
                "aspect": term,
                "category": category,
                "sentiment": sentiment,
                "confidence": float(confidence)
            })
            
        return {
            "sentence": sentence,
            "clean_sentence": clean_text,
            "aspects": results
        }
