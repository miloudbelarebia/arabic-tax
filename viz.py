# -*- coding: utf-8 -*-
"""
Infographic : THE DARIJA TAX — why Darija costs more on ChatGPT.
Square 1080x1080 format.
Real data measured by analyse_vocab_o200k.py (o200k_base, 200,019 tokens).
For #DataBelarebia / databelarebia.com -- Miloud Belarebia
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import arabic_reshaper
from bidi.algorithm import get_display
import os

# ------------------------------------------------------------------
# Real data (measured on o200k_base, 200,019 tokens)
# ------------------------------------------------------------------
EN_TXT  = "Artificial intelligence is here."
AR_TXT  = "الذكاء الاصطناعي وصل"
EN_TOK  = 5
AR_TOK  = 8
TAXE    = AR_TOK / EN_TOK                  # 1.60
TAXE_PCT = int(round((TAXE - 1) * 100))    # 60

TOTAL       = 200019
LATIN_N     = 134868
ARAB_N      = 7964
LATIN_PCT   = 100 * LATIN_N / TOTAL        # 67.43
ARAB_PCT    = 100 * ARAB_N  / TOTAL        # 3.98
RATIO       = round(LATIN_N / ARAB_N)      # 17

# ------------------------------------------------------------------
# Colors  (soft, paper-style palette — easy on the eyes)
# ------------------------------------------------------------------
BG      = "#FAF6EF"   # warm cream paper
CARD    = "#FFFFFF"   # clean white card on the cream background
BORDER  = "#E6DFD0"   # very light beige (softer than gray)
FG      = "#2D3748"   # slate gray for text (not pure black)
MUTED   = "#6B7280"   # mid-gray for secondary text
DIM     = "#9CA3AF"   # light gray for tertiary
ACCENT  = "#C5635F"   # terra cotta — warm, soft red-brick (Arabic)
LATIN_C = "#5B82C4"   # soft steel blue (Latin / English)

arab_font = "Geeza Pro"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
})

def ar(s):
    return get_display(arabic_reshaper.reshape(s))

# Pretty number with thin-space thousands separator
def thou(n):
    return f"{n:,}".replace(",", " ")

# ------------------------------------------------------------------
# Figure 1080x1080 @ 150 dpi  -> single axes in (0..1) coords
# ------------------------------------------------------------------
W = H = 1080
fig = plt.figure(figsize=(W/150, H/150), dpi=150, facecolor=BG)
ax = fig.add_axes((0, 0, 1, 1)); ax.set_facecolor(BG); ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

LEFT, RIGHT = 0.06, 0.94
WIDTH = RIGHT - LEFT

# ==================================================================
# HEADER  — short title + one-liner mentioning the three big LLMs
# ==================================================================
ax.text(LEFT, 0.955, "THE DARIJA TAX",
        fontsize=54, fontweight="bold", color=ACCENT, ha="left", va="top")
ax.text(LEFT, 0.880, "Why Darija costs more on ChatGPT, Claude & Gemini.",
        fontsize=17, color=FG, ha="left", va="top")

ax.plot([LEFT, RIGHT], [0.838, 0.838], color=BORDER, linewidth=1)

# ==================================================================
# BLOC 1 : THE DEMONSTRATION (same idea, two languages)
# ==================================================================
ax.text(LEFT, 0.808, "Same idea, two languages:",
        fontsize=13, color=MUTED, ha="left", va="top", fontweight="600")

# Bar geometry (English + Arabic share the same X axis)
BAR_X0 = LEFT
BAR_X1 = RIGHT - 0.20      # room for "N tokens" at the right
BAR_W  = BAR_X1 - BAR_X0
max_tok = max(EN_TOK, AR_TOK)   # 8
bar_h  = 0.032

# --- English line ---
y_en_phrase = 0.760
y_en_bar    = 0.715

ax.text(LEFT, y_en_phrase, f'"{EN_TXT}"',
        fontsize=19, color=FG, ha="left", va="center")

w_en = BAR_W * (EN_TOK / max_tok)
ax.add_patch(patches.FancyBboxPatch(
    (BAR_X0, y_en_bar - bar_h/2), w_en, bar_h,
    boxstyle="round,pad=0,rounding_size=0.006",
    facecolor=LATIN_C, edgecolor="none"))
ax.text(BAR_X0 + w_en + 0.014, y_en_bar,
        f"{EN_TOK} tokens",
        fontsize=15, color=LATIN_C, ha="left", va="center", fontweight="bold")

# --- Arabic line ---
y_ar_phrase = 0.652
y_ar_bar    = 0.607

ax.text(RIGHT, y_ar_phrase, f'{ar(AR_TXT)}',
        fontsize=26, color=FG, ha="right", va="center",
        fontname=arab_font)

w_ar = BAR_W * (AR_TOK / max_tok)
ax.add_patch(patches.FancyBboxPatch(
    (BAR_X0, y_ar_bar - bar_h/2), w_ar, bar_h,
    boxstyle="round,pad=0,rounding_size=0.006",
    facecolor=ACCENT, edgecolor="none"))
ax.text(BAR_X0 + w_ar + 0.014, y_ar_bar,
        f"{AR_TOK} tokens",
        fontsize=15, color=ACCENT, ha="left", va="center", fontweight="bold")

# ==================================================================
# BLOC 2 : THE HERO NUMBER  (+60%)  — sized to fit inside the card
# ==================================================================
card_y0, card_y1 = 0.395, 0.565   # slightly taller card for breathing room
# Subtle drop shadow (offset card behind)
ax.add_patch(patches.FancyBboxPatch(
    (LEFT + 0.004, card_y0 - 0.006), WIDTH, card_y1 - card_y0,
    boxstyle="round,pad=0,rounding_size=0.025",
    facecolor="#EFE7D6", edgecolor="none"))
ax.add_patch(patches.FancyBboxPatch(
    (LEFT, card_y0), WIDTH, card_y1 - card_y0,
    boxstyle="round,pad=0,rounding_size=0.025",
    facecolor=CARD, edgecolor=BORDER, linewidth=1.2))

# Hero number — 64pt fits comfortably inside the card (height ~0.17)
ax.text(0.5, 0.510, f"+{TAXE_PCT}%",
        fontsize=64, fontweight="bold", color=ACCENT,
        ha="center", va="center")
ax.text(0.5, 0.430, "more tokens to say the exact same thing in Darija",
        fontsize=13.5, color=FG, ha="center", va="center")

# ==================================================================
# BLOC 3 : WHY ?  (vocabulary imbalance)
# ==================================================================
ax.text(LEFT, 0.370, "WHY?",
        fontsize=13, color=MUTED, ha="left", va="top", fontweight="bold")
ax.text(LEFT, 0.343,
        f"Example — ChatGPT's vocabulary ({thou(TOTAL)} entries):",
        fontsize=13.5, color=FG, ha="left", va="top", fontweight="600")

# Bars (scale 0..70% so the Latin bar nearly fills the available width)
BAR2_X0 = LEFT + 0.08
BAR2_X1 = RIGHT - 0.18
BAR2_W  = BAR2_X1 - BAR2_X0
bar2_h  = 0.038
SCALE   = 70

# Latin
y_lat = 0.285
ax.text(LEFT, y_lat, "Latin",
        fontsize=14, color=FG, ha="left", va="center", fontweight="600")
w_lat = BAR2_W * (LATIN_PCT / SCALE)
ax.add_patch(patches.Rectangle(
    (BAR2_X0, y_lat - bar2_h/2), w_lat, bar2_h,
    facecolor=LATIN_C, edgecolor="none"))
ax.text(BAR2_X0 + w_lat + 0.012, y_lat,
        f"{LATIN_PCT:.1f}%",
        fontsize=14, color=LATIN_C, ha="left", va="center", fontweight="bold")

# Arabic
y_arb = 0.230
ax.text(LEFT, y_arb, "Arabic",
        fontsize=14, color=ACCENT, ha="left", va="center", fontweight="bold")
w_arb = max(BAR2_W * (ARAB_PCT / SCALE), 0.010)
ax.add_patch(patches.Rectangle(
    (BAR2_X0, y_arb - bar2_h/2), w_arb, bar2_h,
    facecolor=ACCENT, edgecolor="none"))
ax.text(BAR2_X0 + w_arb + 0.012, y_arb,
        f"{ARAB_PCT:.1f}%",
        fontsize=14, color=ACCENT, ha="left", va="center", fontweight="bold")

# Causal punchline that links the two numbers (tighter spacing)
ax.text(LEFT, 0.185,
        f"That's {RATIO}× more Latin tokens than Arabic.",
        fontsize=16, color=FG, ha="left", va="top", fontweight="700")
ax.text(LEFT, 0.148,
        "Every Arabic sentence eats more tokens —",
        fontsize=12, color=MUTED, ha="left", va="top")
ax.text(LEFT, 0.123,
        "higher API cost, smaller usable context window.",
        fontsize=12, color=MUTED, ha="left", va="top")

# ==================================================================
# FOOTER  (two lines)
# ==================================================================
ax.plot([LEFT, RIGHT], [0.085, 0.085], color=BORDER, linewidth=1)
ax.text(LEFT, 0.052,
        "Data source: github.com/openai/tiktoken  ·  vocab o200k_base",
        fontsize=10, color=MUTED, ha="left", va="center")
ax.text(RIGHT, 0.052,
        "#DataBelarebia",
        fontsize=10.5, color=FG, ha="right", va="center", fontweight="bold")
ax.text(LEFT, 0.022,
        "Reproducible notebook: github.com/miloudbelarebia/darija-tokens",
        fontsize=9.5, color=ACCENT, ha="left", va="center", fontweight="600")
ax.text(RIGHT, 0.022,
        "Miloud Belarebia",
        fontsize=10, color=MUTED, ha="right", va="center")

# ------------------------------------------------------------------
out_path = os.path.join(os.path.dirname(__file__), "taxe-darija-o200k.png")
fig.savefig(out_path, facecolor=BG, dpi=150)
print(f"Image generated: {out_path}")
print(f"Dimensions    : {W}x{H} px (square 1:1)")
