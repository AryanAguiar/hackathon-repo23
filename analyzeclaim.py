from search_claim import search_claim_on_google

TRUSTED_DOMAINS = [
    "bbc.com", "reuters.com", "apnews.com", "nytimes.com",
    "theguardian.com", "wikipedia.org", "who.int", "cdc.gov",
    ".gov", ".edu", ".org"
]

NEGATIVE_KEYWORDS = [
    "false", "hoax", "myth", "not true", "fake", "disproven",
    "debunked", "conspiracy", "satire", "incorrect", "misleading"
]

POSITIVE_KEYWORDS = [
    "true", "confirmed", "scientifically proven", "verified", "evidence supports"
]

def filter_results(results):
    res = []
    for result in results:
        link = result.get("link", "").lower()

        if any(domain in link for domain in TRUSTED_DOMAINS):
            res.append(result)
    return res

def credibility_score(filtered_results):
    if not filtered_results:
        return 0

    score = 0
    negative_hits = 0
    base = 0
    for result in filtered_results:
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()

        if ".gov" in result["link"] or ".edu" in result["link"]:
            base += 30
        elif ".org" in result["link"] or "wikipedia" in result["link"]:
            base += 20
        elif any(x in result["link"] for x in ["bbc", "reuters", "apnews", "guardian", "nytimes"]):
            base += 25
        else:
            base += 0

        if any(kw in snippet or kw in title for kw in NEGATIVE_KEYWORDS):
            base -= 40
            negative_hits += 1
        elif any(kw in snippet for kw in POSITIVE_KEYWORDS):
            base += 20

        score += base

    avg_score = score / len(filtered_results)

    # If more than half sources contain negative signals, lower confidence drastically
    if negative_hits / len(filtered_results) > 0.5:
        avg_score = min(avg_score, 40)

    return round(max(0, min(100, avg_score)))


def verdict_from_score_and_keywords(score, results):
    text_data = " ".join(
        (res.get("title", "") + " " + res.get("snippet", "")).lower()
        for res in results
    )

    if any(kw in text_data for kw in NEGATIVE_KEYWORDS):
        return "Likely False"
    elif score > 75:
        return "Likely True"
    elif score > 50:
        return "Partially True"
    elif score > 30:
        return "Unverified"
    else:
        return "Likely False"

def analyze_claim(claim):
    raw_res = search_claim_on_google(claim)
    filtered_res = filter_results(raw_res)
    score = credibility_score(filtered_res)
    verdict = verdict_from_score_and_keywords(score, filtered_res)
    return {
        "claim": claim,
        "verdict": verdict,
        "score": score,
        "total_results": len(raw_res),
        "trusted_results": len(filtered_res),
        "sources": filtered_res
    }
