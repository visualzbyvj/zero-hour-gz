# -*- coding: utf-8 -*-
"""Set Master Dimmer (ch0) to 0 in all COB/A55/Blinder/Panel FixtureVals.

Exceptions: PANIC (3060) and intensity fader scenes (43,47,51,55,67) keep dim=255.
This separates intensity control from color/FX so the sidebar faders
have sole authority over fixture brightness.
"""
import re

DIMMER_FIXTURES = {0, 1, 2, 6, 7, 8, 9, 11, 14, 17, 22, 24, 26, 27, 28, 29}
EXEMPT_FUNCTIONS = {3060, 43, 47, 51, 55, 67}

FN_PAT = re.compile(
    r'(<Function ID="(\d+)" Type="Scene"[^>]*>)(.*?)(</Function>)',
    re.DOTALL,
)
FV_PAT = re.compile(
    r'(<FixtureVal ID="(\d+)">)(0,255)(,|<)'
)


def fix(text: str) -> tuple[str, int]:
    count = 0

    def replace_fn(m: re.Match) -> str:
        nonlocal count
        fn_open, fid_str, body, fn_close = m.group(1), m.group(2), m.group(3), m.group(4)
        fid = int(fid_str)
        if fid in EXEMPT_FUNCTIONS:
            return m.group(0)

        def replace_fv(fvm: re.Match) -> str:
            nonlocal count
            fv_open, fix_id_str, _dim, sep = fvm.group(1), fvm.group(2), fvm.group(3), fvm.group(4)
            fix_id = int(fix_id_str)
            if fix_id in DIMMER_FIXTURES:
                count += 1
                return f"{fv_open}0,0{sep}"
            return fvm.group(0)

        new_body = FV_PAT.sub(replace_fv, body)
        return fn_open + new_body + fn_close

    return FN_PAT.sub(replace_fn, text), count


def main() -> None:
    path = "Zero Hour GZ Project File.qxw"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, count = fix(text)
    if count:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"Fixed {count} FixtureVal Master Dimmer entries (255 -> 0)")
    else:
        print("No changes needed")


if __name__ == "__main__":
    main()
