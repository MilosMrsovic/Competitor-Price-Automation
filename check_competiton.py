import requests
import csv
import json
import os

# CONFIGURATION
API_KEY = "***********************************8"  # Your SerpAPI key
EU_REGIONS = ["de", "fr", "it", "es", "nl"]  # European regions to search
MAX_RESULTS_PER_PRODUCT = 20  # Maximum results per product
JSON_PATH = os.path.join("Web_Example", "product_data.json")  # Path to your JSON file

# Fixed CSV name for n8n workflow
CSV_NAME = "eu_products_prices.csv"

# Keywords to filter out unwanted items
BAD_KEYWORDS = ["used", "refurbished", "polovno", "second hand", "outlet", "renewed", "pre-owned"]

# FUNCTIONS
def is_valid_item(item):
    """
    Check if a shopping item is valid:
    - Does not contain bad keywords
    - Has an extracted price
    """
    title = item.get("title", "").lower()
    if any(bad in title for bad in BAD_KEYWORDS):
        return False
    if not item.get("extracted_price"):
        return False
    return True


def serpapi_search(query, region):
    """
    Perform a Google Shopping search using SerpAPI for a given query and region.
    Returns a list of shopping results.
    """
    params = {
        "api_key": API_KEY,
        "engine": "google_shopping",
        "q": query,
        "gl": region,
        "hl": "en",
        "num": 20
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=30)
        if response.status_code != 200:
            print(f"⚠️ HTTP error {response.status_code} for query '{query}' in region '{region.upper()}'")
            return []
        data = response.json()
        return data.get("shopping_results", [])
    except Exception as e:
        print(f"❌ Exception during search '{query}' in region '{region.upper()}': {e}")
        return []


# MAIN SCRIPT
def main():
    # Load product data from JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        product = json.load(f)

    product_name = product.get("title")
    sku = product.get("sku", "")  # Optional SKU from JSON
    queries = [f"{product_name} {sku}".strip(), product_name.strip()]

    results_for_product = []
    seen = set()

    for query in queries:
        for region in EU_REGIONS:
            if len(results_for_product) >= MAX_RESULTS_PER_PRODUCT:
                break

            items = serpapi_search(query, region)
            if not items:
                continue

            for item in items:
                if len(results_for_product) >= MAX_RESULTS_PER_PRODUCT:
                    break
                if not is_valid_item(item):
                    continue

                # Avoid duplicate results (same seller + price)
                key = (item.get("source"), item.get("extracted_price"))
                if key in seen:
                    continue
                seen.add(key)

                results_for_product.append({
                    "product": product_name,  # Keep product name fixed
                    "sku": sku,
                    "price_eur": item.get("extracted_price"),
                    "seller": item.get("source"),
                    "region": region.upper(),
                    "link": item.get("product_link", "")
                })

    # Save all results to CSV (overwrite every time)
    with open(CSV_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["product", "sku", "price_eur", "seller", "region", "link"]
        )
        writer.writeheader()
        writer.writerows(results_for_product)

    print(f"\n📁 CSV saved (overwritten if existed): {CSV_NAME}")
    print(f"✅ Found {len(results_for_product)} results for '{product_name}'")


if __name__ == "__main__":
    main()
