"""Show a company's 10 most recent SEC filings. Usage: python filings.py AAPL"""

import sys   # lets us read the ticker typed after the script name
import time  # lets us pause between requests

import requests  # downloads data from the web

# The SEC requires every request to say who is asking, with a contact email.
HEADERS = {"User-Agent": "Clause Vault lk2010@gmail.com"}


def get_json(url):
    """Download a URL and return its JSON data as Python dictionaries and lists."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()  # stop with an error if the request failed (e.g., 404)
    time.sleep(0.2)  # pause briefly so we stay well under the SEC's rate limit
    return response.json()


def find_cik(ticker):
    """Look up a ticker's CIK (the SEC's ID number for each company)."""
    companies = get_json("https://www.sec.gov/files/company_tickers.json")
    for company in companies.values():
        if company["ticker"] == ticker.upper():
            return company["cik_str"]
    return None  # no company has this ticker


def main():
    # sys.argv is the list of words you typed: ["filings.py", "AAPL", "10-K"]
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python filings.py TICKER [FORM], e.g. python filings.py AAPL 10-K")
    ticker = sys.argv[1]
    form_filter = None  # None means "show every form type"
    if len(sys.argv) == 3:
        form_filter = sys.argv[2].upper()  # so "10-k" works too

    # Step 1: turn the ticker into a CIK.
    cik = find_cik(ticker)
    if cik is None:
        sys.exit(f"Ticker {ticker} not found.")

    # Step 2: fetch the company's filing history. The URL needs a 10-digit CIK.
    padded_cik = str(cik).zfill(10)  # e.g., 320193 -> "0000320193"
    data = get_json(f"https://data.sec.gov/submissions/CIK{padded_cik}.json")

    # "recent" holds side-by-side lists; position 0 in each is the newest filing.
    recent = data["filings"]["recent"]

    # Step 3: print up to 10 recent filings, skipping other forms if a filter was given.
    print(f"\nRecent filings for {data['name']} (CIK {cik})\n")
    print(f"{'Date':<12}{'Form':<10}Link")
    shown = 0  # how many rows we've printed so far
    for i in range(len(recent["form"])):
        if form_filter is not None and recent["form"][i] != form_filter:
            continue  # wrong form type: skip to the next filing
        accession = recent["accessionNumber"][i]  # e.g., "0000320193-24-000123"
        folder = accession.replace("-", "")       # same number without dashes
        link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{folder}/{accession}-index.htm"
        print(f"{recent['filingDate'][i]:<12}{recent['form'][i]:<10}{link}")
        shown = shown + 1
        if shown == 10:
            break  # we have 10 rows, so stop looking
    if shown == 0:
        print(f"No {form_filter} filings found in this company's recent history.")


if __name__ == "__main__":
    main()
