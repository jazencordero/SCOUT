from data.scrapers import scrape_sample_commercial_founders

if __name__ == "__main__":
    founders = scrape_sample_commercial_founders(limit=2)
    for f in founders:
        print(f"{f.name} — {f.current_role} — {f.key_signals}")
