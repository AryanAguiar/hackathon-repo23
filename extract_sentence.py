import re
from extract_article import extract_article_text
from config import Config

claim = Config.query

POSITIVE_KEYWORDS = [
    "effective", "safe", "shown to", "evidence", "proven", "clinical trial",
    "study shows", "study found", "research shows"
]

NEGATIVE_KEYWORDS = [
    "dangerous", "cause harm", "cause cancer", "hoax", "myth",
    "serious side effect", "unproven", "no evidence"
]

STOPWORDS = {
    "the","a","an","of","to","in","on","and","or","is","are","was",
    "were","be","being","been","for","with","as","at","by","it",
    "that","this","those","these","from","but","if","then","so"
}


def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

def extract_keywords(claim):
    words = re.findall(r"[a-zA-Z]+", claim.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 4]


def match_density_multiplier(fraction):
    if fraction > 0.7:
        return 1.5
    if fraction > 0.5:
        return 1.3
    if fraction > 0.3:
        return 1.1
    return 1.0

def sentence_matches_claim(sentence, claim_keywords, min_fraction=0.15):
    sentence_lower = sentence.lower()
    matches = sum(1 for word in claim_keywords if word in sentence_lower)
    min_required = max(2, int(len(claim_keywords) * min_fraction))
    if matches < min_required:
        return 0
    
    base_fraction = matches / len(claim_keywords)
    boosted_score = base_fraction * match_density_multiplier(base_fraction)
    boosted_score = min(1.0, boosted_score)
    return boosted_score

def context_score(sentence):
    sentence_lower = sentence.lower()
    score = 0
    if any(k in sentence_lower for k in POSITIVE_KEYWORDS):
        score += 0.4
    if any(k in sentence_lower for k in NEGATIVE_KEYWORDS):
        score -= 0.4
    return score

"""Combine claim match and context score."""
def score_sentence(sentence, claim_keywords):
    match_score = sentence_matches_claim(sentence, claim_keywords)
    if match_score == 0:
        return 0

    context = context_score(sentence)

    final_score = match_score * (1 + context)
    return max(0, min(1, final_score))

def article_sentence_score(url, base_score, claim):
    article_text = extract_article_text(url)
    if not article_text:
        return base_score  # cannot read, return original

    sentences = split_into_sentences(article_text)
    claim_keywords = extract_keywords(claim)

    scores = []
    for s in sentences:
        sc = score_sentence(s, claim_keywords)
        if sc > 0:
            scores.append(sc)

    if scores:
        article_score = sum(scores) / len(scores)
        
        return max(0, min(1, article_score))
    
    return base_score
