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
    # sys.argv is the list of words you typed: ["filings.py", "AAPL"]
    if len(sys.argv) != 2:
        sys.exit("Usage: python filings.py TICKER")
    ticker = sys.argv[1]

    # Step 1: turn the ticker into a CIK.
    cik = find_cik(ticker)
    if cik is None:
        sys.exit(f"Ticker {ticker} not found.")

    # Step 2: fetch the company's filing history. The URL needs a 10-digit CIK.
    padded_cik = str(cik).zfill(10)  # e.g., 320193 -> "0000320193"
    data = get_json(f"https://data.sec.gov/submissions/CIK{padded_cik}.json")

    # "recent" holds side-by-side lists; position 0 in each is the newest filing.
    recent = data["filings"]["recent"]

    # Step 3: print a table of the 10 most recent filings.
    print(f"\n10 most recent filings for {data['name']} (CIK {cik})\n")
    print(f"{'Date':<12}{'Form':<10}Link")
    for i in range(min(10, len(recent["form"]))):
        accession = recent["accessionNumber"][i]  # e.g., "0000320193-24-000123"
        folder = accession.replace("-", "")       # same number without dashes
        link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{folder}/{accession}-index.htm"
        print(f"{recent['filingDate'][i]:<12}{recent['form'][i]:<10}{link}")


if __name__ == "__main__":
    main()
