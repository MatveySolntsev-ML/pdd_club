#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(9, 3.6))
ax.axis("off")
ax.set_xlim(0, 12)
ax.set_ylim(0.3, 6.3)

def node_box(ax, x, y, w, h):
    r = Rectangle((x, y), w, h, fill=False, edgecolor="black", linewidth=1.4)
    ax.add_patch(r)
    d = 0.22
    ax.plot([x, x+d, x+w+d, x+w+d, x+w], [y+h, y+h+d, y+h+d, y+d, y], color="black", linewidth=1.1)
    ax.plot([x+w, x+w+d], [y+h, y+h+d], color="black", linewidth=1.1)

def centered_text(ax, x, y, text, fs=10, bold=False, va="center"):
    ax.text(x, y, text, ha="center", va=va, fontsize=fs, fontweight="bold" if bold else "normal")

# ---------- client node ----------
cx, cy, cw, ch = 0.6, 2.6, 3.7, 2.3
node_box(ax, cx, cy, cw, ch)
centered_text(ax, cx + cw/2, cy + ch - 0.28, "Клиентский узел", fs=11, bold=True)
centered_text(ax, cx + cw/2, cy + ch - 0.58, "«Браузер пользователя»", fs=11, bold=True)
centered_text(ax, cx + cw/2, cy + ch - 1.25, "Веб-клиент (HTML/CSS/JS,\nSPA на React)", fs=9.5)

# ---------- server node ----------
sx, sy, sw, sh = 7.3, 0.6, 4.3, 5.3
node_box(ax, sx, sy, sw, sh)
centered_text(ax, sx + sw/2, sy + sh - 0.28, "Серверный узел", fs=11, bold=True)
centered_text(ax, sx + sw/2, sy + sh - 0.58, "«Сервер приложения»", fs=11, bold=True)

inner1 = Rectangle((sx + 0.3, sy + sh - 1.9), sw - 0.6, 1.1, fill=False, edgecolor="black", linewidth=1.1)
ax.add_patch(inner1)
centered_text(ax, sx + sw/2, sy + sh - 1.35, "Backend-приложение\n(Python, Django + DRF,\nGunicorn)", fs=9)

inner2 = Rectangle((sx + 0.3, sy + sh - 3.5), sw - 0.6, 1.1, fill=False, edgecolor="black", linewidth=1.1)
ax.add_patch(inner2)
centered_text(ax, sx + sw/2, sy + sh - 2.95, "СУБД PostgreSQL", fs=9)

ax.plot([sx + sw/2, sx + sw/2], [sy + sh - 1.9, sy + sh - 2.4], color="black", linewidth=1.0)

# ---------- interface between client and server ----------
arrow = FancyArrowPatch((cx + cw + 0.1, cy + ch/2 + 0.3), (sx - 0.1, cy + ch/2 + 0.3),
                         arrowstyle='<->', mutation_scale=16, linewidth=1.2, color="black")
ax.add_patch(arrow)
centered_text(ax, (cx + cw + sx) / 2, cy + ch/2 + 0.65, "программный интерфейс:", fs=9.5)
centered_text(ax, (cx + cw + sx) / 2, cy + ch/2 - 0.05, "REST API\n(HTTPS, JSON)", fs=9.5)

plt.tight_layout()
plt.savefig("/home/analyst/kursovaya_pdd/deployment_concept.png", dpi=170, bbox_inches="tight")
print("saved deployment_concept.png")
