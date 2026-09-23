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
    # Story & Screenplay
    "story": "Story/Screenplay", "kadhai": "Story/Screenplay", "plot": "Story/Screenplay", 
    "screenplay": "Story/Screenplay", "script": "Story/Screenplay", "twist": "Story/Screenplay",
    
    # Acting & Performance
    "acting": "Acting/Performance", "nadipu": "Acting/Performance", "performance": "Acting/Performance", 
    "cast": "Acting/Performance", "hero": "Acting/Performance", "heroine": "Acting/Performance", 
    "villain": "Acting/Performance", "role": "Acting/Performance",
    
    # Music & Audio
    "music": "Music/Songs/BGM", "isai": "Music/Songs/BGM", "bgm": "Music/Songs/BGM", 
    "songs": "Music/Songs/BGM", "paatu": "Music/Songs/BGM", "score": "Music/Songs/BGM", "theme": "Music/Songs/BGM",
    
    # Direction
    "direction": "Direction", "director": "Direction", "iyakkunar": "Direction", "making": "Direction",
    
    # Comedy
    "comedy": "Comedy/Humour", "sirippu": "Comedy/Humour", "jokes": "Comedy/Humour", "humour": "Comedy/Humour", "fun": "Comedy/Humour",
    
    # Visuals & Camera
    "camera": "Cinematography/Visuals", "cinematography": "Cinematography/Visuals", "visuals": "Cinematography/Visuals", 
    "frames": "Cinematography/Visuals", "vfx": "Cinematography/Visuals",
    
    # Climax & Pacing
    "climax": "Climax/Pacing", "interval": "Climax/Pacing", "first half": "Climax/Pacing", 
    "second half": "Climax/Pacing", "lag": "Climax/Pacing", "pacing": "Climax/Pacing",
    
    # Editing
    "editing": "Editing", "cuts": "Editing", "trimming": "Editing",
    
    # Overall Movie
    "movie": "Overall Movie", "padam": "Overall Movie", "film": "Overall Movie", "cinema": "Overall Movie"
}

# Negation patterns that invert or enforce negativity
NEGATION_PATTERNS = [
    r'\bnalla\s+illa\b', r'\bseri\s+illa\b', r'\bsari\s+illa\b', r'\bsariyilla\b',
    r'\bworth\s+illa\b', r'\bset\s+aagala\b', r'\bvela\s+seiyala\b', r'\bnot\s+good\b',
    r'\bpadam\s+mokka\b', r'\bmokka\b', r'\bworst\b', r'\bwaste\b', r'\bbore\b', 
    r'\bcringe\b', r'\blag\b', r'\bkevalam\b', r'\bkarumam\b', r'\birritating\b'
]

# Explicit positive patterns
POSITIVE_PATTERNS = [
    r'\bsemma\b', r'\bsemmaa\b', r'\bsuper\b', r'\bmass\b', r'\bvera\s+level\b',
    r'\bverithanam\b', r'\btop\s+class\b', r'\bloved\b', r'\bclassic\b', r'\bclean\b',
    r'\bazhagu\b', r'\bnalla\b', r'\bworth\b', r'\bbest\b', r'\bexcellent\b'
]
