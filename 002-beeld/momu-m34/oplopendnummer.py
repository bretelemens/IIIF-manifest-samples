import re

i = 0

with open("test-manifest.json", encoding="utf-8") as f:
    text = f.read()

def repl(match):
    global i
    i += 1
    return f"/momu-m34/test-manifest/page/{i}"

text = re.sub(r'/momu-m34/test-manifest/page/', repl, text)

with open("output.json", "w", encoding="utf-8") as f:
    f.write(text)
