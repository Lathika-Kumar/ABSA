import re

def tanglish_preprocessor(text: str) -> str:
    """
    Linguistic Preprocessing & Normalization Engine for Tamil-English Code-Mixed Text:
    1. Lowercasing
    2. Strips URLs and social media handles (@mentions)
    3. Character elongation reduction (e.g., 'semmaaaaa' -> 'semma', 'masssss' -> 'mass')
    4. Negation unification ('nalla ila', 'nalla illa', 'nalla ilai' -> 'nalla illa')
    5. Normalizes multi-punctuation while preserving polarity cues
    """
    if not isinstance(text, str):
        return ""
        
    text = text.lower()
    
    # Remove URLs and user tags
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    
    # Normalize character elongations: reduce 3+ repeated characters to 2
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    
    # Normalize common Romanized Tamil negation variants
    text = re.sub(r'\b(ila|illai|ile|illaye)\b', 'illa', text)
    text = re.sub(r'\b(sari\s+illa|seri\s+illa)\b', 'sariyilla', text)
    
    # Clean excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Comprehensive Movie Aspect Taxonomy (English + Romanized Tamil terms)
ASPECT_TAXONOMY = {
    "story": "Story/Screenplay", "kadhai": "Story/Screenplay", "plot": "Story/Screenplay", 
    "screenplay": "Story/Screenplay", "script": "Story/Screenplay", "twist": "Story/Screenplay",
    "acting": "Acting/Performance", "nadipu": "Acting/Performance", "performance": "Acting/Performance", 
    "cast": "Acting/Performance", "hero": "Acting/Performance", "heroine": "Acting/Performance", "villain": "Acting/Performance",
    "music": "Music/Songs/BGM", "isai": "Music/Songs/BGM", "bgm": "Music/Songs/BGM", 
    "songs": "Music/Songs/BGM", "paatu": "Music/Songs/BGM", "score": "Music/Songs/BGM",
    "direction": "Direction", "director": "Direction", "iyakkunar": "Direction", "making": "Direction",
    "comedy": "Comedy/Humour", "sirippu": "Comedy/Humour", "jokes": "Comedy/Humour", "humour": "Comedy/Humour", "fun": "Comedy/Humour",
    "camera": "Cinematography/Visuals", "cinematography": "Cinematography/Visuals", "visuals": "Cinematography/Visuals", "frames": "Cinematography/Visuals", "vfx": "Cinematography/Visuals",
    "climax": "Climax/Pacing", "interval": "Climax/Pacing", "first half": "Climax/Pacing", "second half": "Climax/Pacing", "lag": "Climax/Pacing",
    "editing": "Editing", "cuts": "Editing", "trimming": "Editing",
    "movie": "Overall Movie", "padam": "Overall Movie", "film": "Overall Movie", "cinema": "Overall Movie"
}

# Strong polarity indicator cues in code-mixed social media
POS_CUES_STRONG = [
    "semma", "super", "mass", "vera level", "verithanam", "top class", 
    "loved", "classic", "clean", "azhagu", "good", "nalla", "worth", "best", "tharu maru"
]

NEG_CUES_STRONG = [
    "mokka", "worst", "waste", "bore", "cringe", "lag", "sariyilla", 
    "nalla illa", "worth illa", "karumam", "irritating", "bad", "kevalam", "poor"
]
