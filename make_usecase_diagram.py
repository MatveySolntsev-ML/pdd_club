#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(10, 17.5))
ax.axis("off")

ACTOR_X = 1.35
GEN_X = 0.55

def draw_actor(ax, x, y, label):
    ax.add_patch(plt.Circle((x, y + 0.75), 0.18, fill=False, linewidth=1.3))
    ax.plot([x, x], [y + 0.57, y - 0.05], color="black", linewidth=1.3)
    ax.plot([x - 0.3, x + 0.3], [y + 0.35, y + 0.35], color="black", linewidth=1.3)
    ax.plot([x, x - 0.25], [y - 0.05, y - 0.45], color="black", linewidth=1.3)
    ax.plot([x, x + 0.25], [y - 0.05, y - 0.45], color="black", linewidth=1.3)
    ax.text(x, y - 0.65, label, ha="center", va="top", fontsize=10)

def draw_usecase(ax, x, y, text, w=4.6, h=0.78, fontsize=9.2):
    e = Ellipse((x, y), w, h, fill=True, facecolor="white", edgecolor="black", linewidth=1.1)
    ax.add_patch(e)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize)
    return (x - w / 2, y)

def assoc(ax, p1, p2):
    ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=0.9))

def draw_generalization(ax, p_child, p_parent):
    arrow = FancyArrowPatch(p_child, p_parent, arrowstyle='-|>', mutation_scale=20,
                             linewidth=1.3, edgecolor="black", facecolor="white",
                             connectionstyle="arc3,rad=0.0", shrinkA=0, shrinkB=0)
    ax.add_patch(arrow)

UC_X = 6.0  # single column of use-case ellipses, centered in the boundary

guest_cases = [
    "1. Регистрация",
    "2. Просмотр вопросов и комментариев",
]
user_cases = [
    "3. Авторизация",
    "4. Публикация вопроса",
    "5. Комментирование вопроса",
    "6. Редактирование/удаление своего вопроса",
    "7. Добавление вопроса в избранное",
    "8. Подписка/отписка от пользователя",
    "9. Просмотр ленты подписок",
    "10. Формирование списка на повторение",
    "11. Скачивание списка на повторение (txt/pdf)",
    "12. Редактирование профиля",
]
mod_cases = [
    "13. Модерация вопроса («разъяснён» / удаление)",
    "14. Модерация комментариев",
]

ROW_H = 1.15
GAP = 0.6
TOP_Y = len(guest_cases) * ROW_H + GAP + len(user_cases) * ROW_H + GAP + len(mod_cases) * ROW_H + 1.6

def layout_column(start_y, items):
    pts = []
    y = start_y
    for text in items:
        pts.append((UC_X, y, text))
        y -= ROW_H
    return pts, y

guest_layout, y_after_guest = layout_column(TOP_Y - 0.9, guest_cases)
user_layout, y_after_user = layout_column(y_after_guest - 0.6, user_cases)
mod_layout, y_after_mod = layout_column(y_after_user - 0.6, mod_cases)

guest_pts = [draw_usecase(ax, x, y, t) for x, y, t in guest_layout]
user_pts = [draw_usecase(ax, x, y, t) for x, y, t in user_layout]
mod_pts = [draw_usecase(ax, x, y, t) for x, y, t in mod_layout]

# actor y-position = vertical middle of its group's use-case column
actor_guest_y = sum(y for _, y, _ in guest_layout) / len(guest_layout)
actor_user_y = sum(y for _, y, _ in user_layout) / len(user_layout)
actor_mod_y = sum(y for _, y, _ in mod_layout) / len(mod_layout)

actor_guest = (ACTOR_X, actor_guest_y)
actor_user = (ACTOR_X, actor_user_y)
actor_mod = (ACTOR_X, actor_mod_y)

draw_actor(ax, *actor_guest, "Гость")
draw_actor(ax, *actor_user, "Пользователь")
draw_actor(ax, *actor_mod, "Модератор")

for pt in guest_pts:
    assoc(ax, actor_guest, pt)
for pt in user_pts:
    assoc(ax, actor_user, pt)
for pt in mod_pts:
    assoc(ax, actor_mod, pt)

# generalization arrows, routed on a separate vertical line left of actors
draw_generalization(ax, (GEN_X, actor_user_y + 0.9), (GEN_X, actor_guest_y - 0.9))
ax.plot([GEN_X, ACTOR_X - 0.15], [actor_user_y + 0.9, actor_guest_y - 0.3], color="black", linewidth=0.001, alpha=0)  # no-op guide
draw_generalization(ax, (GEN_X, actor_mod_y + 0.9), (GEN_X, actor_user_y - 0.9))

# short connectors from the generalization line to each actor figure
ax.plot([GEN_X, ACTOR_X - 0.2], [actor_guest_y, actor_guest_y], color="black", linewidth=0.9)
ax.plot([GEN_X, ACTOR_X - 0.2], [actor_user_y, actor_user_y], color="black", linewidth=0.9)
ax.plot([GEN_X, ACTOR_X - 0.2], [actor_mod_y, actor_mod_y], color="black", linewidth=0.9)

# ---------- system boundary + canvas sized to actual content ----------
min_y = min(y for _, y, _ in mod_layout) - 1.0   # room for bottom actor figure + label
max_y = TOP_Y + 0.1
boundary = Rectangle((2.3, min_y + 0.5), 7.2, (max_y - 0.3) - (min_y + 0.5),
                      fill=False, edgecolor="black", linewidth=1.3)
ax.add_patch(boundary)
ax.text(5.9, max_y - 0.3, "Серверное приложение для общения изучающих ПДД",
        ha="center", va="top", fontsize=11, fontweight="bold")

ax.set_xlim(0, 10)
ax.set_ylim(min_y - 0.3, max_y)

plt.tight_layout()
plt.savefig("/home/analyst/kursovaya_pdd/usecase_diagram.png", dpi=170, bbox_inches="tight")
print("saved usecase_diagram.png")
