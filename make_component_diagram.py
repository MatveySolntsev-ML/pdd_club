#!/usr/bin/env python3
"""UML component diagram of the Django app packages, with dependency arrows."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13, 10))
ax.axis("off")


def component(x, y, w, h, title, lines, fs_title=11, fs_line=9.2, color="#C8E6C9"):
    box = Rectangle((x, y), w, h, fill=True, facecolor=color, edgecolor="black", linewidth=1.3, zorder=2)
    ax.add_patch(box)
    # UML component "plug" icon in the top-right corner
    px, py = x + w - 0.55, y + h - 0.3
    ax.add_patch(Rectangle((px, py), 0.32, 0.14, fill=True, facecolor="white", edgecolor="black", linewidth=1.0, zorder=3))
    ax.add_patch(Rectangle((px, py - 0.22), 0.32, 0.14, fill=True, facecolor="white", edgecolor="black", linewidth=1.0, zorder=3))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontsize=fs_title, fontweight="bold", zorder=3)
    ty = y + h - 0.68
    for ln in lines:
        ax.text(x + w / 2, ty, ln, ha="center", va="center", fontsize=fs_line, zorder=3)
        ty -= 0.3
    return dict(x=x, y=y, w=w, h=h, cx=x + w / 2, cy=y + h / 2)


def dep_arrow(src, dst, src_side="bottom", dst_side="top", label=""):
    sx = src["cx"]
    sy = src["y"] if src_side == "bottom" else src["y"] + src["h"]
    dx = dst["cx"]
    dy = dst["y"] + dst["h"] if dst_side == "top" else dst["y"]
    arrow = FancyArrowPatch((sx, sy), (dx, dy), arrowstyle="-|>", mutation_scale=14,
                             linewidth=1.1, linestyle=(0, (4, 3)), color="black", zorder=1,
                             shrinkA=2, shrinkB=2)
    ax.add_patch(arrow)
    if label:
        ax.text((sx + dx) / 2 + 0.25, (sy + dy) / 2, label, fontsize=8, style="italic",
                ha="left", va="center", zorder=4,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))


# ---------- components ----------
api = component(4.3, 8.0, 4.4, 1.6, "«package» api",
                 ["DRF: сериализаторы,", "вьюсеты, роутеры"], color="#BBDEFB")

questions = component(1.0, 5.4, 3.4, 1.9, "«package» questions",
                       ["модели: Question,", "Comment, Topic"])
favorites = component(5.1, 5.4, 3.4, 1.9, "«package» favorites",
                       ["модели: Favorite,", "ReviewList"])
subscriptions = component(9.0, 5.4, 4.0, 1.9, "«package» subscriptions",
                           ["модель: Subscription"], fs_title=10)

users = component(5.1, 2.8, 3.4, 1.7, "«package» users",
                   ["модель: User,", "аутентификация"], color="#FFE0B2")

core = component(1.0, 0.3, 11.6, 1.5, "«package» core",
                  ["общие утилиты, базовые классы, константы — используется всеми пакетами выше"],
                  color="#ECEFF1", fs_line=9.0)

# ---------- dependencies ----------
dep_arrow(api, questions)
dep_arrow(api, favorites)
dep_arrow(api, subscriptions)

dep_arrow(questions, users, label="author (FK)")
dep_arrow(favorites, users)
dep_arrow(favorites, questions)
dep_arrow(subscriptions, users)

ax.set_xlim(0, 13.4)
ax.set_ylim(0, 10.2)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("/home/analyst/kursovaya_pdd/component_diagram.png", dpi=170, bbox_inches="tight")
print("saved component_diagram.png")
