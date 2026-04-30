import re
from pathlib import Path

text = Path("Zero Hour GZ Project File.qxw").read_text(encoding="utf-8")
funcs = re.findall(r'<Function ID="(\d+)" Type="(\w+)" Name="([^"]+)"', text)
print("Total functions:", len(funcs))
ranges = [(2800, 3100), (3300, 3600)]
for lo, hi in ranges:
    ms = [f for f in funcs if lo <= int(f[0]) < hi]
    print(f"\n=== {lo}-{hi}: {len(ms)} ===")
    for f in ms:
        print(" ", f[0], f[1][:10], f[2])
