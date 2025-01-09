import requests
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download('punkt_tab')

def fetch_articles(prompt, api_key):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        "q": prompt,
        "apiKey": api_key,
        "language": "en",
        "pageSize": 10,
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch articles from NewsAPI.")

    articles = response.json().get("articles", [])
    return articles

def preprocess_text(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

def calculate_validity_score(article_text, prompt_keywords):
    if not article_text:
        return 1

    article_keywords = Counter(preprocess_text(article_text))
    prompt_keywords_set = set(preprocess_text(" ".join(prompt_keywords)))

    matched_keywords = sum(article_keywords[word] for word in prompt_keywords_set if word in article_keywords)
    total_keywords = sum(article_keywords.values())

    if total_keywords == 0:
        return 1

    score = (matched_keywords / total_keywords) * 10
    print(matched_keywords, total_keywords, score)
    return min(10, max(1, round(score)))

def main():
    prompt = input("Enter your search prompt: ")
    api_key = "fab2bd6942d5451caaa49411c987363e"

    try:
        articles = fetch_articles(prompt, api_key)
    except Exception as e:
        print(f"Error: {e}")
        return

    if not articles:
        print("No articles found.")
        return

    print(f"Found {len(articles)} articles. Scoring them for validity...\n")
    for i, article in enumerate(articles):
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        content = article.get("content", "No Content")
        url = article.get("url", "No URL")

        combined_text = f"{title} {description} {content}"
        score = calculate_validity_score(combined_text, prompt.split())

        print(f"Article {i+1}:\nTitle: {title}\nURL: {url}\nValidity Score: {score}/10\n")

if __name__ == "__main__":
    main()
