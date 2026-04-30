"""Fix 0-indent Function blocks that should be 2-space indented inside Engine."""
import re
text = open("Zero Hour GZ Project File.qxw", encoding="utf-8").read()
# Find Function blocks at 0-indent (no leading space) and add 2 spaces
fixed = re.sub(
    r'^(<Function ID="\d+" Type=")',
    r'  \1',
    text,
    flags=re.MULTILINE,
)
count = len(re.findall(r'^<Function ID=', text, re.MULTILINE))
open("Zero Hour GZ Project File.qxw", "w", encoding="utf-8").write(fixed)
print(f"Fixed {count} zero-indent Function blocks")
