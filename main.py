from google_search import search_text
from search_filter import search_results_score

query = "climate change is a hoax"

results = search_text(query)
rating = search_results_score(results)

for r in rating:
    print(r["credibility"], "-", r["title"])

if rating:
    avg_score = sum([i["credibility"] for i in rating]) / len(rating)
    print(round(avg_score, 3))
else:
    print("No results found.")
