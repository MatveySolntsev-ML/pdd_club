#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, RegularPolygon, FancyBboxPatch

fig, axes = plt.subplots(1, 4, figsize=(16, 4.4))
for ax in axes:
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")

# A — текущий: предупреждающий треугольник с "ПДД"
ax = axes[0]
ax.add_patch(Polygon([(5, 9), (0.7, 1), (9.3, 1)], closed=True, fill=True, facecolor="white",
                      edgecolor="#1a1a1a", linewidth=5, joinstyle="round"))
ax.text(5, 3.1, "ПДД", ha="center", va="center", fontsize=30, fontweight="bold", color="#1a1a1a")
ax.set_title("A. Знак «Внимание»", fontsize=11)

# B — запрещающий круг со значком руля (иконка без текста)
ax = axes[1]
ax.add_patch(Circle((5, 5), 4.3, facecolor="white", edgecolor="#d62828", linewidth=6))
ax.add_patch(Circle((5, 5), 2.6, facecolor="none", edgecolor="#1a1a1a", linewidth=4))
for ang in range(0, 360, 60):
    import math
    x2 = 5 + 2.6 * math.cos(math.radians(ang))
    y2 = 5 + 2.6 * math.sin(math.radians(ang))
    ax.plot([5, x2], [5, y2], color="#1a1a1a", linewidth=3)
ax.set_title("B. Руль в красном круге", fontsize=11)

# C — буква "П" из дорожной разметки + светофор-точка
ax = axes[2]
ax.add_patch(FancyBboxPatch((2, 1.5), 1.4, 7, boxstyle="round,pad=0,rounding_size=0.3", facecolor="#1a1a1a"))
ax.add_patch(FancyBboxPatch((6.6, 1.5), 1.4, 7, boxstyle="round,pad=0,rounding_size=0.3", facecolor="#1a1a1a"))
ax.add_patch(FancyBboxPatch((2, 7.1), 6, 1.4, boxstyle="round,pad=0,rounding_size=0.3", facecolor="#1a1a1a"))
ax.add_patch(Circle((5, 5.6), 0.55, facecolor="#e63946"))
ax.add_patch(Circle((5, 4.1), 0.55, facecolor="#f4a300"))
ax.add_patch(Circle((5, 2.6), 0.55, facecolor="#2a9d8f"))
ax.set_title("C. Буква «П» + светофор", fontsize=11)

# D — значок-бейдж "сдал экзамен" с галочкой
ax = axes[3]
ax.add_patch(RegularPolygon((5, 5.3), numVertices=8, radius=4.2, orientation=0.39,
                             facecolor="#2a6df4", edgecolor="#1a1a1a", linewidth=3))
ax.plot([3.2, 4.6, 7.0], [5.0, 3.2, 6.8], color="white", linewidth=5, solid_capstyle="round", solid_joinstyle="round")
ax.add_patch(Polygon([(3.5, 1.2), (6.5, 1.2), (5.7, -0.6), (4.3, -0.6)], closed=True, facecolor="#2a6df4", edgecolor="#1a1a1a", linewidth=2))
ax.set_ylim(-1, 10)
ax.set_title("D. Бейдж «сдал» с галочкой", fontsize=11)

plt.tight_layout()
plt.savefig("/home/analyst/kursovaya_pdd/logo_concepts.png", dpi=160, bbox_inches="tight", facecolor="white")
print("saved")
