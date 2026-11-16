#!/usr/bin/env python3
"""Container deployment diagram (Docker Compose) — UML node notation."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Ellipse

fig, ax = plt.subplots(figsize=(12, 8))
ax.axis("off")


def node(x, y, w, h, title, lines, fs_title=10.5, fs_line=9, color="white"):
    r = Rectangle((x, y), w, h, fill=True, facecolor=color, edgecolor="black", linewidth=1.3, zorder=2)
    ax.add_patch(r)
    d = 0.18
    ax.plot([x, x + d, x + w + d, x + w + d, x + w], [y + h, y + h + d, y + h + d, y + d, y],
            color="black", linewidth=1.0, zorder=2)
    ax.plot([x + w, x + w + d], [y + h, y + h + d], color="black", linewidth=1.0, zorder=2)
    ax.text(x + w / 2, y + h - 0.28, title, ha="center", va="top", fontsize=fs_title, fontweight="bold", zorder=3)
    ty = y + h - 0.62
    for ln in lines:
        ax.text(x + w / 2, ty, ln, ha="center", va="top", fontsize=fs_line, zorder=3)
        ty -= 0.28
    return dict(x=x, y=y, w=w, h=h, cx=x + w / 2, cy=y + h / 2)


def volume(x, y, w, h, label):
    e_top = Ellipse((x + w / 2, y + h), w, 0.3, fill=True, facecolor="#ECEFF1", edgecolor="black", linewidth=1.1, zorder=2)
    body = Rectangle((x, y), w, h, fill=True, facecolor="#ECEFF1", edgecolor="none", zorder=1)
    e_bot = Ellipse((x + w / 2, y), w, 0.3, fill=True, facecolor="#ECEFF1", edgecolor="black", linewidth=1.1, zorder=2)
    ax.add_patch(body)
    ax.add_patch(e_bot)
    ax.plot([x, x], [y, y + h], color="black", linewidth=1.1, zorder=2)
    ax.plot([x + w, x + w], [y, y + h], color="black", linewidth=1.1, zorder=2)
    ax.add_patch(e_top)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=8.3, zorder=3)
    return dict(x=x, y=y, w=w, h=h, cx=x + w / 2, cy=y + h / 2)


def arrow(p1, p2, label="", dashed=False, lw=1.2, label_side=False):
    ls = (0, (4, 3)) if dashed else "-"
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13, linewidth=lw,
                         linestyle=ls, color="black", zorder=1, shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        if label_side:
            ax.text(mx + 0.9, my, label, ha="left", va="center", fontsize=8.3, zorder=4,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
        else:
            ax.text(mx, my + 0.3, label, ha="center", va="bottom", fontsize=8.3, zorder=4,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))


# ---------- client (outside the server) ----------
client = node(0.4, 4.6, 2.6, 1.8, "Браузер", ["клиента"], color="#FFE0B2")

# ---------- Docker host boundary ----------
host = Rectangle((3.6, 0.5), 8.0, 6.6, fill=False, edgecolor="black", linewidth=1.4, linestyle=(0, (6, 3)), zorder=1)
ax.add_patch(host)
ax.text(7.6, 7.15, "Сервер — хост Docker Compose", ha="center", va="bottom", fontsize=10.5, fontweight="bold")

nginx = node(4.1, 4.5, 2.8, 1.8, "nginx", ["контейнер: nginx:latest", "порт 80/443"], color="#BBDEFB")
backend = node(4.1, 2.2, 2.8, 1.9, "backend", ["контейнер: Gunicorn+Django", "порт 8000 (внутр.)"], color="#C8E6C9")
db = node(8.2, 2.2, 2.8, 1.9, "db", ["контейнер: postgres:15", "порт 5432 (внутр.)"], color="#D1C4E9")

static_vol = volume(8.5, 5.0, 1.2, 1.0, "static_\nmedia")
pg_vol = volume(8.5, 0.6, 1.2, 0.9, "postgres_\ndata")

# ---------- connections ----------
arrow((client["x"] + client["w"], client["cy"]), (nginx["x"], nginx["cy"]), "HTTPS (80/443)")
arrow((nginx["cx"], nginx["y"]), (backend["cx"], backend["y"] + backend["h"]), "proxy_pass :8000", label_side=True)
arrow((backend["x"] + backend["w"], backend["cy"]), (db["x"], db["cy"]), "SQL :5432")
arrow((nginx["x"] + nginx["w"] - 0.3, nginx["y"]), (static_vol["x"] + 0.2, static_vol["y"] + static_vol["h"]), dashed=True)
arrow((backend["x"] + backend["w"] - 0.3, backend["y"] + backend["h"]), (static_vol["x"] + 0.2, static_vol["y"]), dashed=True)
arrow((db["cx"], db["y"]), (pg_vol["cx"], pg_vol["y"] + pg_vol["h"]), dashed=True)

ax.set_xlim(0, 12)
ax.set_ylim(0.2, 7.6)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("/home/analyst/kursovaya_pdd/deployment_container.png", dpi=170, bbox_inches="tight")
print("saved deployment_container.png")
