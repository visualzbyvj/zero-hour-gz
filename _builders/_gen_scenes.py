# -*- coding: utf-8 -*-
def ring24(r, g, b):
    p = []
    for k in range(8):
        p.extend([3 * k, r, 3 * k + 1, g, 3 * k + 2, b])
    return ",".join(map(str, p))


def panel_rgb(r, g, b):
    p = [0, 0, 1, 0]
    for i in range(48):
        base = 2 + 3 * i
        p.extend([base, r, base + 1, g, base + 2, b])
    for ch in range(146, 154):
        p.extend([ch, 0])
    return ",".join(map(str, p))


def panel_off():
    return ",".join([f"{ch},0" for ch in range(154)])


def blinder12_off():
    return ",".join([f"{ch},0" for ch in range(12)])


def cob7_off():
    return ",".join([f"{ch},0" for ch in range(7)])


def a55_10_off():
    return ",".join([f"{ch},0" for ch in range(10)])


outer_ids = [3, 4, 10, 19]
inner_ids = [25, 5, 23, 20]
panels = [8, 9, 22, 24]

colors = [
    (114, "PURPLE", 130, 0, 220),
    (115, "CYAN", 0, 220, 255),
    (116, "GREEN", 0, 255, 0),
    (117, "YELLOW", 255, 255, 0),
    (118, "ORANGE", 255, 70, 0),
    (119, "GOLD", 255, 170, 0),
]
out = []
for idn, name, r, g, b in colors:
    fv = "".join(
        f'   <FixtureVal ID="{fid}">{ring24(r, g, b)}</FixtureVal>\n' for fid in outer_ids
    )
    out.append(
        f'  <Function ID="{idn}" Type="Scene" Name="BUSK - OUTER {name}">\n   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n{fv}  </Function>\n'
    )

inner_colors = [
    (120, "PURPLE", 130, 0, 220),
    (121, "CYAN", 0, 220, 255),
    (122, "GREEN", 0, 255, 0),
    (123, "YELLOW", 255, 255, 0),
    (124, "ORANGE", 255, 70, 0),
    (125, "GOLD", 255, 170, 0),
]
for idn, name, r, g, b in inner_colors:
    fv = "".join(
        f'   <FixtureVal ID="{fid}">{ring24(r, g, b)}</FixtureVal>\n' for fid in inner_ids
    )
    out.append(
        f'  <Function ID="{idn}" Type="Scene" Name="BUSK - INNER {name}">\n   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n{fv}  </Function>\n'
    )

fb_lines = []
for fid in [3, 4, 10, 19, 25, 5, 23, 20]:
    fb_lines.append(f'   <FixtureVal ID="{fid}">{ring24(0,0,0)}</FixtureVal>')
for fid in [15, 16, 18, 21]:
    fb_lines.append(
        f'   <FixtureVal ID="{fid}">{",".join([f"{c},0" for c in range(16)])}</FixtureVal>'
    )
for fid in [1, 6, 14, 17]:
    fb_lines.append(f'   <FixtureVal ID="{fid}">{blinder12_off()}</FixtureVal>')
for fid in [2, 11, 28, 29]:
    fb_lines.append(f'   <FixtureVal ID="{fid}">{cob7_off()}</FixtureVal>')
for fid in [0, 7, 26, 27]:
    fb_lines.append(f'   <FixtureVal ID="{fid}">{a55_10_off()}</FixtureVal>')
po = panel_off()
for fid in panels:
    fb_lines.append(f'   <FixtureVal ID="{fid}">{po}</FixtureVal>')

out.append(
    '  <Function ID="126" Type="Scene" Name="BUSK - FULL BLACKOUT">\n   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n'
    + "\n".join(fb_lines)
    + "\n  </Function>\n"
)

bhit = ",".join(["0,255"] + [f"{c},0" for c in range(1, 12)])
out.append(
    '  <Function ID="127" Type="Scene" Name="BUSK - BLINDER WHITE HIT">\n   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n'
    + "".join(f'   <FixtureVal ID="{fid}">{bhit}</FixtureVal>\n' for fid in [1, 6, 14, 17])
    + "  </Function>\n"
)

wr = ",".join([f"{c},255" for c in range(16)])
out.append(
    '  <Function ID="128" Type="Scene" Name="BUSK - ALL WHITE HIT">\n   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n'
)
for fid in [15, 16, 18, 21]:
    out.append(f'   <FixtureVal ID="{fid}">{wr}</FixtureVal>\n')
for fid in [1, 6, 14, 17]:
    out.append(f'   <FixtureVal ID="{fid}">{bhit}</FixtureVal>\n')
cobw = "0,255,1,255,2,255,3,255,4,0,5,0,6,0"
for fid in [2, 11, 28, 29]:
    out.append(f'   <FixtureVal ID="{fid}">{cobw}</FixtureVal>\n')
out.append("  </Function>\n")

# 129-131 panels
for idn, name, r, g, b in [
    (129, "PURPLE", 130, 0, 220),
    (130, "CYAN", 0, 220, 255),
    (131, "GREEN", 0, 255, 0),
]:
    pv = "".join(
        f'   <FixtureVal ID="{fid}">{panel_rgb(r,g,b)}</FixtureVal>\n' for fid in panels
    )
    out.append(
        f'  <Function ID="{idn}" Type="Scene" Name="LED PANEL - COLOR {name}">\n   <Speed FadeIn="0" FadeOut="0" Duration="0"/>\n{pv}  </Function>\n'
    )

# Collections 132-137
out.append(
    '  <Function ID="132" Type="Collection" Name="GENRE LOOK - TRAP">\n'
    '   <Step Number="0">119</Step>\n   <Step Number="1">120</Step>\n   <Step Number="2">8</Step>\n   <Step Number="3">22</Step>\n  </Function>\n'
)
out.append(
    '  <Function ID="133" Type="Collection" Name="GENRE LOOK - BASS HOUSE">\n'
    '   <Step Number="0">115</Step>\n   <Step Number="1">124</Step>\n   <Step Number="2">9</Step>\n   <Step Number="3">21</Step>\n  </Function>\n'
)
out.append(
    '  <Function ID="134" Type="Collection" Name="GENRE LOOK - DUBSTEP">\n'
    '   <Step Number="0">17</Step>\n   <Step Number="1">20</Step>\n   <Step Number="2">129</Step>\n   <Step Number="3">22</Step>\n  </Function>\n'
)
out.append(
    '  <Function ID="135" Type="Collection" Name="SHOW STATE - BUILD">\n'
    '   <Step Number="0">25</Step>\n   <Step Number="1">28</Step>\n   <Step Number="2">22</Step>\n   <Step Number="3">34</Step>\n  </Function>\n'
)
out.append(
    '  <Function ID="136" Type="Collection" Name="SHOW STATE - DROP">\n'
    '   <Step Number="0">23</Step>\n   <Step Number="1">40</Step>\n   <Step Number="2">128</Step>\n   <Step Number="3">127</Step>\n  </Function>\n'
)
out.append(
    '  <Function ID="137" Type="Collection" Name="SHOW STATE - BREAK">\n'
    '   <Step Number="0">26</Step>\n   <Step Number="1">30</Step>\n   <Step Number="2">22</Step>\n  </Function>\n'
)

from pathlib import Path
(Path(__file__).resolve().parent.parent / "_data" / "_scenes_block.xml").write_text("".join(out), encoding="utf-8")
print("ok", len("".join(out)))
