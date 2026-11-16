#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
from matplotlib.transforms import Affine2D

NAVY = "#15213B"
ACCENT = "#F2B705"

def draw_mark(ax, cx, cy, size, bg=NAVY, accent=ACCENT):
    # rounded-square "squircle" background
    s = size
    bg_patch = FancyBboxPatch((cx - s/2, cy - s/2), s, s,
                               boxstyle=f"round,pad=0,rounding_size={s*0.22}",
                               facecolor=bg, edgecolor="none", zorder=1)
    ax.add_patch(bg_patch)

    # road: white trapezoid narrowing towards the top (perspective)
    bw, tw, h = s*0.62, s*0.22, s*0.64
    bx, by = cx, cy - s*0.06
    road = Polygon([
        (bx - bw/2, by - h/2), (bx + bw/2, by - h/2),
        (bx + tw/2, by + h/2), (bx - tw/2, by + h/2),
    ], closed=True, facecolor="white", edgecolor="none", zorder=2)
    ax.add_patch(road)

    # lane-marking dashes (background-colour cut-outs down the centre)
    for frac, w, h2 in [(-0.22, 0.10, 0.12), (0.08, 0.075, 0.11), (0.32, 0.055, 0.09)]:
        dy = by + frac * h
        dw = s * w
        dh = s * h2
        ax.add_patch(Rectangle((cx - dw/2, dy - dh/2), dw, dh, facecolor=bg, edgecolor="none", zorder=3))

    # small accent sun/horizon dot above the road
    ax.add_patch(plt.Circle((cx, cy + s*0.34), s*0.065, facecolor=accent, edgecolor="none", zorder=3))


fig, ax = plt.subplots(figsize=(3, 3))
ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal")
draw_mark(ax, 5, 5, 8.6)
plt.tight_layout(pad=0)
plt.savefig("/home/analyst/kursovaya_pdd/logo_icon.png", dpi=220, bbox_inches="tight",
            pad_inches=0.08, transparent=True)
plt.close(fig)

# horizontal lockup: icon + wordmark, for navbar
fig, ax = plt.subplots(figsize=(4.4, 2.1))
ax.axis("off"); ax.set_xlim(0, 15); ax.set_ylim(0, 7); ax.set_aspect("equal")
draw_mark(ax, 3.6, 3.5, 6.2)
ax.text(7.5, 4.15, "ПДД", fontsize=34, fontweight="bold", color=NAVY, family="DejaVu Sans", va="center")
ax.text(7.5, 1.55, "КЛУБ", fontsize=15, fontweight="bold", color="#6b7280", family="DejaVu Sans", va="center")
plt.tight_layout(pad=0)
plt.savefig("/home/analyst/kursovaya_pdd/logo_lockup.png", dpi=220, bbox_inches="tight",
            pad_inches=0.1, transparent=True)
plt.close(fig)
print("saved logo_icon.png, logo_lockup.png")
