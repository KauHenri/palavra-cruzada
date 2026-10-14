import urllib.request
import re

# Let's get a large list of Portuguese words or build a solver
# We can download a clean Brazilian Portuguese word list if online, or use an offline generator.
# Let's test if we have internet access to fetch a clean pt-BR wordlist, or write a dedicated solver.

try:
    url = "https://raw.githubusercontent.com/python-pt/palavras-portugues/master/palavras.txt"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as response:
        content = response.read().decode('utf-8')
        words = [w.strip().upper() for w in content.splitlines() if 2 <= len(w.strip()) <= 9]
        print(f"Downloaded {len(words)} pt-BR words!")
except Exception as e:
    print(f"Online download failed: {e}")
