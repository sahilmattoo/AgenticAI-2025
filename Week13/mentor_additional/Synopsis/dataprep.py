import re
import json
from pypdf import PdfReader

PDF_PATH = "Vistara_AirAsia_Master_License_Agreement_30PlusPages_Final.pdf"
OUTPUT_JSON = "agreement_articles.json"

# Regex to detect ARTICLE headings
ARTICLE_PATTERN = re.compile(r"(ARTICLE\s+\d+\s+—\s+.+)", re.IGNORECASE)

def extract_articles_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    
    articles = {}
    current_article = None
    buffer = []

    for page in reader.pages:
        text = page.extract_text()
        if not text:
            continue

        lines = text.split("\n")

        for line in lines:
            article_match = ARTICLE_PATTERN.match(line.strip())

            # If new ARTICLE detected
            if article_match:
                # Save previous article
                if current_article:
                    articles[current_article] = " ".join(buffer).strip()
                    buffer = []

                current_article = article_match.group(1).strip()
            else:
                if current_article:
                    buffer.append(line.strip())

    # Save last article
    if current_article:
        articles[current_article] = " ".join(buffer).strip()

    return articles


if __name__ == "__main__":
    article_json = extract_articles_from_pdf(PDF_PATH)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(article_json, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(article_json)} articles.")
    print(f"Saved to {OUTPUT_JSON}")
