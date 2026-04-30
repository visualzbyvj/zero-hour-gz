import re
text = open("Zero Hour GZ Project File.qxw", encoding="utf-8").read()
for match in re.finditer(r"<Function ID=""(\d+)"" Name=""([^""]*)"" Path=""([^""]*)"" Type=""([^""]*)""", text):
    fid, name, ftype = match.group(1), match.group(2), match.group(4)
    nl = name.lower()
    if any(k in nl for k in ["chase", "ring", "sweep", "bounce", "in-out", "out-in"]):
        print("ID=%s  Type=%-20s  Name=%s" % (fid, ftype, name))