# -*- coding: utf-8 -*-
"""
=============================================================================
 ANALYSE DU VOCABULAIRE o200k_base (GPT-4o / GPT-4.1 / o1 / o3)
 La preuve chiffree et reproductible de la sous-representation de l'arabe.
 Pour #DataBelarebia / databelarebia.com  --  Miloud Belarebia
=============================================================================

CE QUE FAIT CE SCRIPT
  1. Telecharge le VRAI fichier vocabulaire publie par OpenAI (tiktoken)
  2. Decode les ~200 000 tokens
  3. Classe chaque token par script Unicode (arabe / latin / CJK / chiffre / autre)
  4. Affiche le decompte + les pourcentages
  5. Mesure la "taxe" : meme phrase en EN vs arabe (MSA + Darija), nb de tokens reel

PREREQUIS (a lancer une fois dans ton terminal) :
    pip install tiktoken

PUIS :
    python3 analyse_vocab_o200k.py

NOTE : la 1re execution telecharge ~ qq Mo (cache ensuite par tiktoken).
       Aucune cle API necessaire, tout est public.
=============================================================================
"""

import sys
import unicodedata
from collections import Counter

# --------------------------------------------------------------------------
# 1) CHARGEMENT DU VRAI TOKENIZER OPENAI
# --------------------------------------------------------------------------
try:
    import tiktoken
except ImportError:
    sys.exit("ERREUR : tiktoken non installe.  ->  pip install tiktoken")

print("Chargement de o200k_base (telechargement la 1re fois)...")
enc = tiktoken.get_encoding("o200k_base")
N = enc.n_vocab
print(f"Vocabulaire charge : {N} tokens\n")


# --------------------------------------------------------------------------
# 2) CLASSIFICATION PAR SCRIPT UNICODE  (logique validee 14/14)
# --------------------------------------------------------------------------
def classify_token(s: str) -> str:
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
        elif ("CJK" in name or "HIRAGANA" in name or "KATAKANA" in name
              or "HANGUL" in name):
            counts["cjk"] += 1
    if not has_letter:
        if any(c.isdigit() for c in s):
            return "digit"
        return "other"          # ponctuation, espaces, code, symboles
    dom = max(counts, key=counts.get)
    return dom if counts[dom] > 0 else "other"


# --------------------------------------------------------------------------
# 3) PARCOURS DE TOUT LE VOCABULAIRE
# --------------------------------------------------------------------------
buckets = Counter()
arabic_examples = []
undecodable = 0

for tok_id in range(N):
    try:
        raw = enc.decode_single_token_bytes(tok_id)
        text = raw.decode("utf-8")
    except Exception:
        undecodable += 1
        buckets["undecodable"] += 1
        continue
    cat = classify_token(text)
    buckets[cat] += 1
    if cat == "arabic" and len(arabic_examples) < 30:
        arabic_examples.append(text)


# --------------------------------------------------------------------------
# 4) RESULTATS
# --------------------------------------------------------------------------
print("=" * 62)
print("  REPARTITION DU VOCABULAIRE o200k_base PAR SCRIPT")
print("=" * 62)
order = ["latin", "cjk", "arabic", "digit", "other", "undecodable"]
labels = {
    "latin": "Latin (anglais, code, langues latines)",
    "cjk": "CJK (chinois, japonais, coreen)",
    "arabic": "ARABE  (<- la donnee qui nous interesse)",
    "digit": "Chiffres",
    "other": "Autre (ponctuation, symboles, espaces)",
    "undecodable": "Non decodable (fragments d'octets bruts)",
}
for k in order:
    n = buckets.get(k, 0)
    pct = 100.0 * n / N
    bar = "#" * int(pct / 2)
    print(f"  {labels[k]:42} {n:7d}  {pct:5.2f}%  {bar}")

arab = buckets.get("arabic", 0)
latin = buckets.get("latin", 0)
print("\n" + "=" * 62)
print("  LE CHIFFRE QUI FRAPPE")
print("=" * 62)
print(f"  Tokens latins  : {latin:>7d}  ({100.0*latin/N:.2f}%)")
print(f"  Tokens arabes  : {arab:>7d}  ({100.0*arab/N:.2f}%)")
if arab:
    print(f"  Ratio          : le latin a {latin/arab:.0f}x plus de tokens "
          f"dedies que l'arabe")
print("\n  Exemples de tokens arabes presents dans le vocabulaire :")
print("   ", "  ".join(arabic_examples[:20]) if arabic_examples
      else "(aucun)")


# --------------------------------------------------------------------------
# 5) LA TAXE MESUREE : meme idee, EN vs arabe (MSA + Darija)
# --------------------------------------------------------------------------
# Trois paires choisies sur le registre AI / tech / business : c'est LA
# ou la taxe mord le plus fort, et c'est exactement le registre qui
# compte pour un produit IA, une API, un chatbot.
#
# Note honnete : sur des salutations courantes ("salam", "kifash"), la
# taxe est nettement plus faible, parfois proche de 1.0x. Le 2x n'est
# PAS uniforme sur toute la langue arabe -- il frappe le vocabulaire
# moderne/technique. C'est documente dans le README.
#
# Mix MSA + Darija intentionnel : les deux registres paient la taxe.
print("\n" + "=" * 62)
print("  LA TAXE LINGUISTIQUE, MESUREE SUR LE VRAI TOKENIZER")
print("  (registre AI / tech -- voir README pour la nuance par registre)")
print("=" * 62)
pairs = [
    # MSA -- hero phrase de l'infographie : 4 vs 8 tokens exactement
    ("Artificial intelligence is here",        "الذكاء الاصطناعي وصل"),
    # MSA -- vocabulaire produit / API
    ("The algorithm processes user requests",  "الخوارزمية تعالج طلبات المستخدمين"),
    # Darija marocaine -- emprunts AI (موديل / داتا)
    ("The model learns from data",             "الموديل كيتعلم من الداتا"),
]
print(f"  {'EN tok':>7} | {'AR tok':>7} | {'Taxe':>6} | phrase arabe (MSA/Darija)")
print("  " + "-" * 58)
tot_en = tot_ar = 0
for en, ar in pairs:
    ne = len(enc.encode(en))
    na = len(enc.encode(ar))
    tot_en += ne
    tot_ar += na
    print(f"  {ne:7d} | {na:7d} | {na/ne:5.2f}x | {ar}")
print("  " + "-" * 58)
print(f"  {tot_en:7d} | {tot_ar:7d} | {tot_ar/tot_en:5.2f}x | TOTAL  "
      f"-> l'arabe coute {tot_ar/tot_en:.2f}x plus cher sur ce registre")

print("\n" + "=" * 62)
print("  CONCLUSION")
print("=" * 62)
print(f"""  Sur {N} tokens, l'arabe en represente ~{100.0*arab/N:.1f}%.
  Sur le registre AI/tech, la meme idee coute ~{tot_ar/tot_en:.2f}x plus de
  tokens en arabe qu'en anglais. Fenetre utile reduite d'autant,
  cout API multiplie d'autant. Ce n'est pas une opinion : c'est
  le contenu du fichier vocabulaire officiel d'OpenAI, mesure ici.

  Nuance importante : la taxe n'est PAS uniforme. Sur des phrases
  courantes faites de mots tres frequents (salutations, verbes de
  base), elle peut s'approcher de la parite. Elle mord le plus fort
  sur le vocabulaire moderne, technique, business -- exactement le
  registre qui compte pour les produits IA. Cf README pour le detail.

  Source primaire : github.com/openai/tiktoken
  Reproductible : relance ce script, tu auras les memes chiffres.
=============================================================================
""")
