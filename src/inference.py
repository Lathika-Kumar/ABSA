import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .preprocessing import tanglish_preprocessor, ASPECT_TAXONOMY

NEGATION_PATTERNS = [
    r'\bnalla\s+illa\b', r'\bseri\s+illa\b', r'\bsari\s+illa\b', r'\bsariyilla\b',
    r'\bworth\s+illa\b', r'\bset\s+aagala\b', r'\bvela\s+seiyala\b', r'\bnot\s+good\b',
    r'\bpadam\s+mokka\b', r'\bmokka\b', r'\bworst\b', r'\bwaste\b', r'\bbore\b', 
    r'\bcringe\b', r'\blag\b', r'\bkevalam\b', r'\bkarumam\b', r'\birritating\b'
]

POSITIVE_PATTERNS = [
    r'\bsemma\b', r'\bsemmaa\b', r'\bsuper\b', r'\bmass\b', r'\bvera\s+level\b',
    r'\bverithanam\b', r'\btop\s+class\b', r'\bloved\b', r'\bclassic\b', r'\bclean\b',
    r'\bazhagu\b', r'\bnalla\b', r'\bworth\b', r'\bbest\b', r'\bexcellent\b'
]

def get_clause_for_aspect(sentence: str, aspect_term: str) -> str:
    """Splits sentence by contrastive conjunctions or aspect boundaries to isolate the target aspect clause."""
    clauses = re.split(r'\b(?:but|aana|aanal|however|yet|and)\b|[,;]', sentence, flags=re.IGNORECASE)
    for c in clauses:
        if re.search(r'\b' + re.escape(aspect_term) + r'\b', c, flags=re.IGNORECASE):
            return c.strip()
    return sentence

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
        clean_text = tanglish_preprocessor(sentence)
        
        # Stage 1: Aspect Term Extraction (Longest span first)
        found_aspects = []
        sorted_terms = sorted(ASPECT_TAXONOMY.keys(), key=lambda x: len(x), reverse=True)
        matched_spans = []
        
        for term in sorted_terms:
            for m in re.finditer(r'\b' + re.escape(term) + r'\b', clean_text):
                span = (m.start(), m.end())
                if not any(s[0] <= span[0] and span[1] <= s[1] for s in matched_spans):
                    matched_spans.append(span)
                    found_aspects.append((term, ASPECT_TAXONOMY[term]))
                    
        if not found_aspects:
            return {"sentence": sentence, "clean_sentence": clean_text, "aspects": []}

        results = []
        for term, category in found_aspects:
            # Stage 2: Clause Isolation & Negation-First Analysis
            clause = get_clause_for_aspect(clean_text, term)
            
            has_neg = any(re.search(pat, clause) for pat in NEGATION_PATTERNS)
            has_pos = False
            if not has_neg:
                has_pos = any(re.search(pat, clause) for pat in POSITIVE_PATTERNS)
                
            formatted_query = f"Aspect: {term} | Category: {category} | Review: {clause}"
            inputs = self.tokenizer(formatted_query, return_tensors="pt", truncation=True, max_length=128).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                prob = torch.softmax(outputs.logits, dim=-1).cpu().numpy()[0]
            prob_pos = prob[1] if len(prob) > 1 else prob[0]
            
            if has_neg:
                final_score = 0.10
            elif has_pos:
                final_score = 0.92
            else:
                final_score = prob_pos
                
            sentiment = "POSITIVE" if final_score >= 0.50 else "NEGATIVE"
            confidence = final_score if sentiment == "POSITIVE" else (1.0 - final_score)
            
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
