# -*- coding: utf-8 -*-
"""Test de la logique de classification Unicode avant livraison."""
import unicodedata

def classify_token(s):
    """Classe un token decode selon le script DOMINANT de ses lettres.
    Retourne: 'arabic', 'latin', 'cjk', 'digit', 'other', 'empty'."""
    counts = {"arabic": 0, "latin": 0, "cjk": 0}
    has_letter = False
    for ch in s:
        if not ch.isalpha():
            continue
        has_letter = True
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if "ARABIC" in name:
            counts["arabic"] += 1
        elif "LATIN" in name:
            counts["latin"] += 1
        elif "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name or "HANGUL" in name:
            counts["cjk"] += 1
    if not has_letter:
        if any(c.isdigit() for c in s):
            return "digit"
        return "other"
    dom = max(counts, key=counts.get)
    if counts[dom] == 0:
        return "other"
    return dom

# --- Auto-test sur donnees synthetiques connues ---
cases = [
    ("ال", "arabic"), ("كيتعلم", "arabic"), (" السلام", "arabic"),
    ("hello", "latin"), (" the", "latin"), ("ization", "latin"),
    ("中文", "cjk"), ("こんにちは", "cjk"), ("한국어", "cjk"),
    ("123", "digit"), ("   ", "other"), ("===", "other"),
    ("def", "latin"), ("café", "latin"),
]
ok = 0
for tok, expected in cases:
    got = classify_token(tok)
    status = "OK " if got == expected else "FAIL"
    if got == expected:
        ok += 1
    print(f"  [{status}] {tok!r:20} -> {got:8} (attendu {expected})")
print(f"\nResultat: {ok}/{len(cases)} tests passes")
