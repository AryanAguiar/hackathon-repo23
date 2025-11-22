from urllib.parse import urlparse
from extract_text import extract_article_text

HIGH_TRUST = [
    "nih.gov", "ncbi.nlm.nih.gov", "cdc.gov", "fda.gov", "ema.europa.eu",
    "ecdc.europa.eu", "who.int", "gov.uk", "canada.ca", "un.org",

    "harvard.edu", "stanford.edu", "ox.ac.uk", "cam.ac.uk", "mit.edu",
    "ucl.ac.uk", "johnshopkins.edu", "berkeley.edu", "columbia.edu",
    "yale.edu", "princeton.edu", "uchicago.edu",

    "mayoclinic.org", "clevelandclinic.org", "hopkinsmedicine.org",
    "mdanderson.org", "mskcc.org",

    "nature.com", "science.org", "thelancet.com", "nejm.org", "jama.com",

    "apnews.com", "scientificamerican.com","nationalgeographic.com"
]


MEDIUM_TRUST = [
    "bbc.com", "reuters.com", "healthline.com",
    "webmd.com", "sciencedaily.com"
]

LOW_TRUST_KEYWORDS = [
    "blogspot", "wordpress", "substack",
    "naturalnews", "herbal", "holistic"
]

MISINFO_KEYWORDS = [
    "miracle cure", "flat earth", "secret method",
    "detox", "no side effects", "cancer cure"
]

FACT_CHECK_KEYWORDS = [
    "evidence", "study", "research", "fact check", "verified"
]


def get_domain(url):
    return urlparse(url).netloc.lower()

def is_high_trust(domain):
    return any(domain.endswith(t) for t in HIGH_TRUST)

def score_source(title, snippet, url):
    text = (title + " " + snippet).lower()
    domain = get_domain(url)

    score = 0.5  # start score

    # DOMAIN TRUST
    if any(k in domain for k in HIGH_TRUST):
        score += 0.4
    elif any(k in domain for k in MEDIUM_TRUST):
        score += 0.2
    elif any(k in domain for k in LOW_TRUST_KEYWORDS):
        score -= 0.3

    if any(k in text for k in FACT_CHECK_KEYWORDS):
        score += 0.2

    if any(k in text for k in MISINFO_KEYWORDS):
        score -= 0.3
    
    return max(0, min(1, score))


def full_article_score(url, base_score):
    article_text = extract_article_text(url).lower()

    if not article_text:
        return base_score  # cannot read no change

    if any(k in article_text for k in MISINFO_KEYWORDS):
        base_score -= 0.4

    if any(k in article_text for k in FACT_CHECK_KEYWORDS):
        base_score += 0.2

    return max(0, min(1, base_score))


def search_results_score(results):
    output = []

    for r in results:
        base_score = score_source(r["title"], r["snippet"], r["link"])
        domain = get_domain(r["link"])

        final_score = base_score

        if is_high_trust(domain):
            final_score = full_article_score(r["link"], base_score)

        output.append({
            "title": r["title"],
            "link": r["link"],
            "snippet": r["snippet"],
            "credibility": final_score
        })

    output.sort(key=lambda x: x["credibility"], reverse=True)
    return output
