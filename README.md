# Clause Vault

Search public contract exhibits filed with the SEC on EDGAR.

## Setup

```bash
cd ~/code/clause-vault
python3 -m venv .venv            # create the virtual environment (one time only)
source .venv/bin/activate        # turn it on (each new terminal session)
pip install -r requirements.txt  # install the libraries this project uses
```

When you're done, type `deactivate` to turn the virtual environment off.

## Note on EDGAR access

The SEC asks every program to identify itself with a `User-Agent` header that includes a name and contact email, and to stay under 10 requests per second.
