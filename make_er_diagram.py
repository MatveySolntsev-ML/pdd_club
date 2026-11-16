#!/usr/bin/env python3
"""ER diagram in standard Crow's Foot notation, fully orthogonal routing,
generously spaced so no relationship lines ever cross or touch."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots(figsize=(16, 11))
ax.axis("off")

HEADER_COLOR = "#BBDEFB"
JUNCTION_COLOR = "#FFE0B2"
TICK = 0.14
FOOT = 0.22


def entity(x, y, w, h, title, attrs, header_color=HEADER_COLOR, header_h=0.55, fs_title=11, fs_attr=9.0):
    box = Rectangle((x, y), w, h, fill=True, facecolor="white", edgecolor="black", linewidth=1.3, zorder=2)
    ax.add_patch(box)
    header = Rectangle((x, y + h - header_h), w, header_h, fill=True, facecolor=header_color, edgecolor="black", linewidth=1.3, zorder=2)
    ax.add_patch(header)
    ax.text(x + w / 2, y + h - header_h / 2, title, ha="center", va="center", fontsize=fs_title, fontweight="bold", zorder=3)
    ty = y + h - header_h - 0.22
    for a in attrs:
        bold = a.startswith("*")
        text = a[1:] if bold else a
        ax.text(x + 0.18, ty, text, ha="left", va="top", fontsize=fs_attr,
                fontweight="bold" if bold else "normal", zorder=3)
        ty -= 0.32
    return dict(x=x, y=y, w=w, h=h, cx=x + w / 2, cy=y + h / 2)


def mark(point, approach_from, kind):
    x, y = point
    text = "1" if kind == "one" else "N"
    if approach_from in ("left", "right"):
        sign = 1 if approach_from == "left" else -1
        if kind == "one":
            ax.plot([x - sign * TICK, x - sign * TICK], [y - TICK, y + TICK], color="black", linewidth=1.2, zorder=5)
        else:
            base_x = x - sign * FOOT
            for dy in (-TICK * 1.3, 0, TICK * 1.3):
                ax.plot([base_x, x], [y + dy, y], color="black", linewidth=1.2, zorder=5)
        ax.text(x - sign * (FOOT + 0.22), y + 0.24, text, fontsize=8.6, ha="center", va="center", zorder=5)
    else:
        sign = 1 if approach_from == "top" else -1
        if kind == "one":
            ax.plot([x - TICK, x + TICK], [y + sign * TICK, y + sign * TICK], color="black", linewidth=1.2, zorder=5)
        else:
            base_y = y + sign * FOOT
            for dx in (-TICK * 1.3, 0, TICK * 1.3):
                ax.plot([x + dx, x], [base_y, y], color="black", linewidth=1.2, zorder=5)
        ax.text(x + 0.26, y + sign * (FOOT + 0.20), text, fontsize=8.6, ha="center", va="center", zorder=5)


def label_at(x, y, text, ha="center", va="center"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=8.8, style="italic", zorder=4,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


def ortho_edge(points, one_side, many_side, label="", label_pos=None):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color="black", linewidth=1.15, zorder=1)
    mark(points[0], one_side, "one")
    mark(points[-1], many_side, "many")
    if label:
        lx, ly = label_pos if label_pos else points[len(points) // 2]
        label_at(lx, ly, label)


# =========================================================
# LAYOUT — generously spaced grid, nothing is tight
# =========================================================
topic = entity(9.8, 13.9, 3.6, 1.7, "Topic (Тема раздела ПДД)", ["*id", "name", "slug"])

user = entity(0.5, 8.9, 3.6, 3.4, "User (Пользователь)",
              ["*id", "email", "username", "password_hash", "role", "avatar"])
question = entity(9.6, 8.9, 4.0, 3.4, "Question (Вопрос/билет)",
                   ["*id", "author_id (FK)", "topic_id (FK)", "ticket_number",
                    "text", "image", "status", "created_at"])
comment = entity(16.2, 9.6, 3.6, 2.7, "Comment (Комментарий)",
                  ["*id", "question_id (FK)", "author_id (FK)", "text", "created_at"])

# Subscription sits directly below User — it only relates to User, so it is
# kept fully out of the Favorite/ReviewList corridor to avoid any clutter.
subscription = entity(0.5, 5.3, 3.6, 2.3, "Subscription (Подписка)",
                       ["*id", "follower_id (FK)", "author_id (FK)"], header_color=JUNCTION_COLOR)

favorite = entity(5.3, 6.6, 3.2, 1.8, "Favorite (Избранное)",
                   ["*id", "user_id (FK)", "question_id (FK)"], header_color=JUNCTION_COLOR)
review = entity(5.3, 4.0, 3.2, 1.8, "ReviewList (На повторение)",
                 ["*id", "user_id (FK)", "question_id (FK)"], header_color=JUNCTION_COLOR)

# =========================================================
# RELATIONSHIPS
# =========================================================

# Topic (1) --- (N) Question — generous 1.6-unit gap so marks/text/label never touch
ortho_edge([(topic["cx"], topic["y"]), (topic["cx"], question["y"] + question["h"])],
           "bottom", "top", "содержит",
           label_pos=(topic["cx"] + 0.9, (topic["y"] + question["y"] + question["h"]) / 2))

# User (1) --- (N) Question  [publishes]
y_pub = user["y"] + user["h"] - 0.35
ortho_edge([(user["x"] + user["w"], y_pub), (question["x"], y_pub)],
           "right", "left", "публикует", label_pos=((user["x"] + user["w"] + question["x"]) / 2, y_pub + 0.55))

# Question (1) --- (N) Comment — generous 2.6-unit gap
y_com = question["y"] + question["h"] - 0.35
ortho_edge([(question["x"] + question["w"], y_com), (comment["x"], y_com)],
           "right", "left", "комментируется", label_pos=((question["x"] + question["w"] + comment["x"]) / 2, y_com + 0.55))

# User (1) --- (N) Comment  [writes/author] — routed over the top, clear of everything
over_y = 16.5
ux = user["x"] + user["w"] - 0.5
cx = comment["x"] + comment["w"] * 0.25
ortho_edge([(ux, user["y"] + user["h"]), (ux, over_y), (cx, over_y), (cx, comment["y"] + comment["h"])],
           "top", "top", "пишет (автор)", label_pos=((ux + cx) / 2, over_y + 0.28))

# --- Subscription: both FKs point to User — two independent straight verticals ---
sub_x1 = user["x"] + 1.1
sub_x2 = user["x"] + 2.5
ortho_edge([(sub_x1, user["y"]), (sub_x1, subscription["y"] + subscription["h"])],
           "bottom", "top", "подписчик", label_pos=(sub_x1 - 0.65, (user["y"] + subscription["y"] + subscription["h"]) / 2))
ortho_edge([(sub_x2, user["y"]), (sub_x2, subscription["y"] + subscription["h"])],
           "bottom", "top", "автор", label_pos=(sub_x2 + 0.55, (user["y"] + subscription["y"] + subscription["h"]) / 2))

# --- Favorite / ReviewList: User <-> Question, via two short side corridors ---
CORR_L = [4.4, 4.7]   # between User's right edge (4.1) and the Favorite/ReviewList column (5.3)
CORR_R = [9.0, 9.3]   # between the column's right edge (8.5) and Question's left edge (9.6)

def from_user(corridor_x, start_y, target_y, target_x, label=""):
    ortho_edge([(user["x"] + user["w"], start_y), (corridor_x, start_y),
                (corridor_x, target_y), (target_x, target_y)],
               "right", "left", label)

def from_question(corridor_x, start_y, target_y, target_x, label=""):
    ortho_edge([(question["x"], start_y), (corridor_x, start_y),
                (corridor_x, target_y), (target_x, target_y)],
               "left", "right", label)

from_user(CORR_L[0], user["y"] + 1.6, favorite["cy"], favorite["x"])
from_question(CORR_R[0], question["y"] + 1.6, favorite["cy"], favorite["x"] + favorite["w"])

from_user(CORR_L[1], user["y"] + 0.9, review["cy"], review["x"])
from_question(CORR_R[1], question["y"] + 0.9, review["cy"], review["x"] + review["w"])

ax.set_xlim(-0.3, 20.2)
ax.set_ylim(3.6, 16.9)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("/home/analyst/kursovaya_pdd/er_diagram.png", dpi=170, bbox_inches="tight")
print("saved er_diagram.png")
