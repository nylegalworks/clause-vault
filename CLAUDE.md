# Clause Vault

A search tool over public contract exhibits (e.g., EX-10 material contracts) filed with SEC EDGAR.

## About me

I'm a corporate lawyer and a beginner programmer. I know contracts and EDGAR filings well, but I'm still learning to code.

## How to work with me

- **Explain every change in plain English.** After each change, tell me what you changed, why, and what it does, without jargon (or define the jargon when you use it).
- **Prefer simple code over clever code.** Readable, straightforward code that I can follow beats short or "elegant" code. Add comments where something isn't obvious.
- **Never store passwords, API keys, or other secrets in code.** Keep them in a `.env` file (which is git-ignored) or environment variables, and tell me how to set them.
- **Ask before deleting anything** — files, folders, data, or large chunks of code.

## Project setup

- Python project using a virtual environment in `.venv/`.
- Activate it with `source .venv/bin/activate` before running code.
- Dependencies are listed in `requirements.txt`; install with `pip install -r requirements.txt`.

## EDGAR notes

- The SEC requires a descriptive `User-Agent` header (name + contact email) on every request, and limits traffic to about 10 requests per second. Respect both.
