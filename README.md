# Web Health & Code Validator

A lightweight, zero-dependency Python CLI tool to test website URLs, inspect HTTP status codes, verify SSL certificate validity, and audit basic HTML structure.

## Features
- **HTTP Status Verification:** Detects `200 OK`, redirects, and `4xx/5xx` error codes.
- **Latency Measurement:** Calculates exact server response time in milliseconds.
- **SSL Certificate Check:** Verifies HTTPS validity and remaining days before expiration.
- **Basic HTML Audit:** Checks for essential `<title>` and responsive `viewport` meta tags.

## Usage
Run the script directly with Python 3 (no external packages required):

```bash
python3 checker.py [https://example.com](https://example.com) [https://github.com](https://github.com)
