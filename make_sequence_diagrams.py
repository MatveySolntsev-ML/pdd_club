#!/usr/bin/env python3
"""UML sequence diagrams for two typical client-server REST scenarios."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch


def sequence_diagram(lifelines, messages, out_path, fig_w=11):
    n = len(lifelines)
    lane_gap = fig_w / (n + 1)
    xs = [lane_gap * (i + 1) for i in range(n)]
    top_y = 0.3
    row_h = 0.85
    bottom_y = top_y + row_h * (len(messages) + 1)

    fig, ax = plt.subplots(figsize=(fig_w, 0.9 * len(messages) + 2.2))
    ax.axis("off")
    ax.set_xlim(0, fig_w)
    ax.invert_yaxis()
    ax.set_ylim(bottom_y + 0.6, -0.3)

    for x, name in zip(xs, lifelines):
        box = Rectangle((x - 1.1, -0.25), 2.2, 0.55, fill=True, facecolor="#BBDEFB",
                         edgecolor="black", linewidth=1.2, zorder=3)
        ax.add_patch(box)
        ax.text(x, 0.02, name, ha="center", va="center", fontsize=10.5, fontweight="bold", zorder=4)
        ax.plot([x, x], [0.3, bottom_y], color="black", linewidth=1.0, linestyle=(0, (4, 3)), zorder=1)

    y = top_y + row_h
    for src, dst, label, style in messages:
        x1, x2 = xs[lifelines.index(src)], xs[lifelines.index(dst)]
        ls = "-" if style == "solid" else (0, (5, 3))
        if src == dst:
            loop_w = 0.9
            ax.plot([x1, x1 + loop_w, x1 + loop_w, x1 + 0.08], [y - 0.18, y - 0.18, y + 0.18, y + 0.18],
                    color="black", linewidth=1.2, linestyle=ls, zorder=2)
            arrow = FancyArrowPatch((x1 + 0.2, y + 0.18), (x1, y + 0.18), arrowstyle="-|>", mutation_scale=12,
                                     linewidth=1.2, color="black", zorder=2, shrinkA=0, shrinkB=0)
            ax.add_patch(arrow)
            ax.text(x1 + loop_w + 0.15, y, label, ha="left", va="center", fontsize=8.8, zorder=4,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
        else:
            arrow = FancyArrowPatch((x1, y), (x2, y), arrowstyle="-|>", mutation_scale=14,
                                     linewidth=1.2, linestyle=ls, color="black", zorder=2,
                                     shrinkA=1, shrinkB=1)
            ax.add_patch(arrow)
            mid = (x1 + x2) / 2
            ax.text(mid, y - 0.14, label, ha="center", va="bottom", fontsize=8.8, zorder=4,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
        y += row_h

    plt.tight_layout()
    plt.savefig(out_path, dpi=170, bbox_inches="tight")
    print("saved", out_path)


lifelines = ["Клиент (React SPA)", "API (DRF)", "БД (PostgreSQL)"]

# ---------- Scenario 1: публикация вопроса ----------
msgs1 = [
    ("Клиент (React SPA)", "API (DRF)", "POST /api/questions/\n{topic, ticket_number, text, image}", "solid"),
    ("API (DRF)", "API (DRF)", "проверка токена авторизации", "solid"),
    ("API (DRF)", "БД (PostgreSQL)", "INSERT INTO questions (...)", "solid"),
    ("БД (PostgreSQL)", "API (DRF)", "вопрос сохранён, id", "dashed"),
    ("API (DRF)", "Клиент (React SPA)", "201 Created\n{id, author, topic, text, ...}", "dashed"),
]
sequence_diagram(lifelines, msgs1, "/home/analyst/kursovaya_pdd/seq_publish_question.png")

# ---------- Scenario 2: добавление в избранное / список на повторение ----------
msgs2 = [
    ("Клиент (React SPA)", "API (DRF)", "POST /api/questions/{id}/favorite/", "solid"),
    ("API (DRF)", "БД (PostgreSQL)", "SELECT вопрос по id", "solid"),
    ("БД (PostgreSQL)", "API (DRF)", "вопрос найден", "dashed"),
    ("API (DRF)", "БД (PostgreSQL)", "INSERT INTO favorites (user_id, question_id)", "solid"),
    ("БД (PostgreSQL)", "API (DRF)", "запись создана", "dashed"),
    ("API (DRF)", "Клиент (React SPA)", "201 Created\n{question, user}", "dashed"),
]
sequence_diagram(lifelines, msgs2, "/home/analyst/kursovaya_pdd/seq_add_favorite.png")
