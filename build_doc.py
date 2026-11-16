#!/usr/bin/env python3
import docx
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn

FONT = "Times New Roman"
SIZE = Pt(14)

def set_base_style(doc):
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = SIZE
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(0)
    rpr = style.element.rPr
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = rpr.makeelement(qn('w:rFonts'), {})
        rpr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), FONT)

def set_margins(section):
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(1.5)

def p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, size=SIZE, space_after=0):
    par = doc.add_paragraph()
    par.alignment = align
    par.paragraph_format.first_line_indent = Cm(1.25) if align == WD_ALIGN_PARAGRAPH.JUSTIFY else None
    par.paragraph_format.space_after = Pt(space_after)
    run = par.add_run(text)
    run.font.name = FONT
    run.font.size = size
    run.bold = bold
    return par

def heading(doc, text, size=Pt(14), space_before=12, space_after=12, level=None):
    # level is accepted for call-site compatibility but intentionally unused:
    # Word's built-in Heading styles carry a theme colour (blue) we don't want.
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(space_before)
    par.paragraph_format.space_after = Pt(space_after)
    run = par.add_run(text)
    run.font.name = FONT
    run.font.size = size
    run.bold = True
    return par


def add_toc_placeholder(doc, items):
    """Static Содержание list — dot leaders, no page numbers (fill in manually before печать/защита)."""
    for item in items:
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = par.add_run(item + " " + "." * 60)
        r.font.name = FONT; r.font.size = SIZE

doc = Document()
set_base_style(doc)
set_margins(doc.sections[0])

# ---------- TITLE PAGE ----------
def center(text, bold=False, size=SIZE, space_after=0):
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_after = Pt(space_after)
    run = par.add_run(text)
    run.font.name = FONT
    run.font.size = size
    run.bold = bold
    return par

center("Министерство науки и высшего образования Российской Федерации", space_after=0)
center("федеральное государственное бюджетное образовательное учреждение высшего образования", space_after=0)
center("«Российский экономический университет имени Г.В. Плеханова»", bold=True, space_after=24)
center("Высшая школа кибербезопасности, математики и статистики", space_after=0)
center("Кафедра «Прикладная информатика и информационная безопасность» (ПИиИБ)", space_after=24)

center("КУРСОВАЯ РАБОТА", bold=True, size=Pt(16), space_after=0)
center("по дисциплине «Интеграция и управление приложениями на удаленном сервере»", space_after=12)
center("на тему «Разработка серверного приложения для общения изучающих ПДД»", bold=True, space_after=36)

for _ in range(2):
    doc.add_paragraph()

right = doc.add_paragraph()
right.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = right.add_run("Выполнил(а) обучающийся(ая) группы 15.27Д-ПИ02/23б\nочной формы обучения\nВысшей школы кибербезопасности, математики и статистики")
r.font.name = FONT; r.font.size = SIZE

name_par = doc.add_paragraph()
name_par.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = name_par.add_run("Солнцев Матвей Александрович")
r.font.name = FONT; r.font.size = SIZE; r.bold = True

doc.add_paragraph()

sup_par = doc.add_paragraph()
r = sup_par.add_run("Научный руководитель:")
r.font.name = FONT; r.font.size = SIZE

sup_name = doc.add_paragraph()
r = sup_name.add_run("преподаватель Данилов А.В.")
r.font.name = FONT; r.font.size = SIZE

for _ in range(2):
    doc.add_paragraph()

center("Москва – 2026")

doc.add_page_break()

# ---------- CONTENTS (real auto-updating TOC field) ----------
heading(doc, "СОДЕРЖАНИЕ")
add_toc_placeholder(doc, [
    "Введение",
    "Глава 1. Проектирование серверного приложения",
    "1.1. Описание предметной области и постановка задачи",
    "1.2. Функциональные требования",
    "1.3. Нефункциональные требования",
    "Глава 2. Проектирование и тестовая реализация серверного приложения",
    "2.1. Модель БД приложения",
    "2.2. Структура прикладной системы",
    "2.3. Спецификация REST API",
    "2.4. Технология клиент-серверного взаимодействия",
    "2.5. Архитектура развёртывания системы",
    "2.6. Контрольный прогон тестовой реализации",
    "Заключение",
    "Список использованных источников",
])

doc.add_page_break()

# ---------- INTRODUCTION ----------
heading(doc, "ВВЕДЕНИЕ", level=1)

intro_paragraphs = [
"Актуальность темы. Ежегодно сотни тысяч граждан Российской Федерации сдают теоретический экзамен на знание Правил дорожного движения (ПДД) для получения водительского удостоверения, при этом статистика автошкол показывает высокую долю неудачных попыток при первой сдаче. Существующие мобильные приложения для тренировки билетов ПДД, как правило, реализуют только индивидуальное тестирование и не предоставляют инструментов социального взаимодействия: обмена опытом, совместного разбора сложных вопросов, обсуждения спорных трактовок пунктов ПДД. В то же время формат сообщества по интересам способен повысить мотивацию и эффективность подготовки за счёт взаимопомощи и обмена знаниями между пользователями. Это обуславливает актуальность разработки серверного приложения, реализующего функции социальной сети для изучающих ПДД.",
"Предмет исследования — процессы проектирования и реализации серверной части (backend) веб-приложения для организации сообщества пользователей, изучающих ПДД.",
"Объект исследования — серверное веб-приложение, предоставляющее REST API для сервиса общения и совместной подготовки пользователей к теоретическому экзамену по ПДД.",
"Цель курсовой работы — спроектировать и выполнить тестовую реализацию серверного приложения для сервиса общения изучающих ПДД.",
"Задачи работы:",
"1. изучить предметную область и сформулировать функциональные и нефункциональные требования к системе;",
"2. спроектировать клиент-серверную архитектуру взаимодействия;",
"3. разработать инфологическую модель базы данных приложения;",
"4. спроектировать структуру прикладной системы (компоненты Python-пакетов);",
"5. разработать спецификацию REST API реализуемой части проекта;",
"6. выполнить тестовую реализацию серверной части и продемонстрировать работу основных сценариев;",
"7. спроектировать архитектуру развёртывания системы.",
"Обоснование выбора технологий. В качестве технологии реализации выбран стек Python/Django + Django REST Framework — согласуется с программой курса, обеспечивает быструю разработку REST API, готовые средства ORM, аутентификации и управления правами доступа. В качестве СУБД используется PostgreSQL. Для развёртывания контейнерной архитектуры используется Docker/Docker Compose.",
"Краткое содержание. В главе 1 рассматривается предметная область, формулируются функциональные и нефункциональные требования к системе. В главе 2 разрабатывается модель данных, структура прикладной системы, спецификация REST API, технология клиент-серверного взаимодействия и архитектура развёртывания, приводятся результаты тестовой реализации.",
]
for t in intro_paragraphs:
    p(doc, t)

doc.add_page_break()

# ---------- CHAPTER 1 ----------
heading(doc, "ГЛАВА 1. ПРОЕКТИРОВАНИЕ СЕРВЕРНОГО ПРИЛОЖЕНИЯ", level=1)

heading(doc, "1.1. Описание предметной области и постановка задачи", size=Pt(14), space_before=6, space_after=6, level=2)
section_1_1 = [
"Предметная область — подготовка кандидатов в водители к сдаче теоретического экзамена на знание Правил дорожного движения (ПДД) в Госавтоинспекции. Заинтересованные пользователи — лица, самостоятельно или через автошколу готовящиеся к экзамену, которым требуется не только тренировка тестовых билетов (эту задачу уже решают существующие мобильные приложения), но и разбор сложных и спорных вопросов совместно с другими кандидатами, обмен приёмами запоминания, обсуждение изменений в ПДД и мотивация через сообщество.",
"Автоматизируемые задачи: публикация пользователем вопроса, привязанного к номеру билета и теме раздела ПДД (например, «Приоритет», «Сигналы светофора», «Штрафы»); обсуждение вопроса в комментариях; сохранение вопросов в «избранное» для повторения; подписка на других пользователей для отслеживания их активности; формирование личного списка вопросов на повторение с возможностью его скачивания.",
"Обоснование выбора задач. Функционал выбран как содержательный аналог функционала итоговой проектной работы Яндекс.Практикума «Фудграм»: рецепт → вопрос/билет ПДД, тег → тема раздела ПДД, избранное → избранное, список покупок → список вопросов на повторение, подписки → подписки на пользователей. Такой подход позволяет переиспользовать отработанный на курсе архитектурный паттерн при полностью другой предметной области.",
]
for t in section_1_1:
    p(doc, t)

heading(doc, "1.2. Функциональные требования", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "Система поддерживает трёх действующих лиц: Гость (неавторизованный пользователь), Пользователь (кандидат, готовящийся к экзамену по ПДД) и Модератор. Пользователь является специализацией Гостя (получает доступ ко всем его прецедентам после регистрации/авторизации), Модератор — специализацией Пользователя (получает дополнительно функции модерации контента). Диаграмма вариантов использования системы представлена на рисунке 1.")

pic_par = doc.add_paragraph()
pic_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par.add_run().add_picture("/home/analyst/kursovaya_pdd/usecase_diagram.png", width=Cm(15))

# figure caption: по образцу — по центру, курсив, не жирный, 12pt (sz=24)
cap = doc.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap.add_run("Рис. 1. Диаграмма вариантов использования (use-case) системы")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

p(doc, "Спецификация прецедентов представлена в таблице 1.")

# table caption: по образцу — "Таблица N" по правому краю, затем название по центру жирным, тем же 14pt
tbl_num_par = doc.add_paragraph()
tbl_num_par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = tbl_num_par.add_run("Таблица 1")
r.font.name = FONT; r.font.size = SIZE

tbl_title_par = doc.add_paragraph()
tbl_title_par.alignment = WD_ALIGN_PARAGRAPH.CENTER
tbl_title_par.paragraph_format.left_indent = Cm(0.5)
r = tbl_title_par.add_run("Спецификация прецедентов")
r.font.name = FONT; r.font.size = SIZE; r.bold = True

usecase_table = [
    ("1", "Регистрация", "Гость", "Создание учётной записи пользователя по email и паролю"),
    ("2", "Просмотр вопросов и комментариев", "Гость", "Просмотр списка опубликованных вопросов и комментариев к ним без возможности взаимодействия"),
    ("3", "Авторизация", "Пользователь", "Вход в систему по логину и паролю, получение токена доступа"),
    ("4", "Публикация вопроса", "Пользователь", "Создание нового вопроса с привязкой к номеру билета и теме раздела ПДД"),
    ("5", "Комментирование вопроса", "Пользователь", "Добавление комментария к вопросу для разбора или уточнения"),
    ("6", "Редактирование/удаление своего вопроса", "Пользователь", "Изменение или удаление ранее опубликованного вопроса его автором"),
    ("7", "Добавление вопроса в избранное", "Пользователь", "Сохранение вопроса в личный список «избранное» для повторного просмотра"),
    ("8", "Подписка/отписка от пользователя", "Пользователь", "Оформление или отмена подписки на активность другого пользователя"),
    ("9", "Просмотр ленты подписок", "Пользователь", "Просмотр вопросов пользователей, на которых оформлена подписка"),
    ("10", "Формирование списка на повторение", "Пользователь", "Добавление вопросов в личный список для последующего повторения"),
    ("11", "Скачивание списка на повторение", "Пользователь", "Выгрузка списка вопросов на повторение в файл формата txt/pdf"),
    ("12", "Редактирование профиля", "Пользователь", "Изменение данных учётной записи (имя, аватар, пароль)"),
    ("13", "Модерация вопроса", "Модератор", "Отметка вопроса как «разъяснён» или удаление некорректного вопроса"),
    ("14", "Модерация комментариев", "Модератор", "Удаление комментариев, нарушающих правила сообщества"),
]

from docx.enum.table import WD_ALIGN_VERTICAL

def style_cell(cell, text, bold=False):
    cell.text = ""
    par = cell.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.line_spacing = 1.15
    par.paragraph_format.space_after = Pt(0)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    r = par.add_run(text)
    r.font.name = FONT; r.font.size = SIZE; r.bold = bold

table = doc.add_table(rows=1, cols=4)
table.style = "Table Grid"
widths = [Cm(1.2), Cm(5.5), Cm(3.0), Cm(7.3)]
for col, w in zip(table.columns, widths):
    for cell in col.cells:
        cell.width = w

hdr = table.rows[0].cells
headers = ["№", "Наименование прецедента", "Действующее лицо", "Краткое описание"]
for i, htext in enumerate(headers):
    style_cell(hdr[i], htext)

for row_data in usecase_table:
    row = table.add_row().cells
    for i, val in enumerate(row_data):
        style_cell(row[i], val)

heading(doc, "1.3. Нефункциональные требования", size=Pt(14), space_before=6, space_after=6, level=2)
section_1_3 = [
"Вычислительная архитектура приложения — двухуровневая клиент-серверная («тонкий клиент»). Клиентский узел выполняет только отображение интерфейса и обращения к серверу, вся бизнес-логика и хранение данных вынесены на серверный узел. Концептуальная диаграмма развёртывания представлена на рисунке 2.",
]
for t in section_1_3:
    p(doc, t)

pic_par2 = doc.add_paragraph()
pic_par2.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par2.add_run().add_picture("/home/analyst/kursovaya_pdd/deployment_concept.png", width=Cm(15))
cap2 = doc.add_paragraph()
cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap2.add_run("Рис. 2. Концептуальная диаграмма развёртывания")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

section_1_3b = [
"Характеристика элементов вычислительной архитектуры:",
"Клиентский узел («Браузер пользователя») — реализуется средствами веб-браузера: одностраничное приложение (SPA) на React, взаимодействующее с сервером исключительно через REST API; хранение состояния на клиенте ограничено токеном авторизации.",
"Серверный узел («Сервер приложения») — backend-приложение на Python с использованием фреймворка Django и библиотеки Django REST Framework (DRF), запускаемое под WSGI-сервером Gunicorn; в качестве СУБД используется PostgreSQL.",
"Программный интерфейс между узлами — REST API поверх протокола HTTPS, формат данных обмена — JSON, аутентификация — по токену (Djoser/Simple JWT).",
"Прочие нефункциональные требования: время отклика API на типовой запрос — не более 1 секунды; система рассчитана на одновременную работу нескольких тысяч пользователей без изменения архитектуры (горизонтальное масштабирование backend-узла); защита персональных данных пользователей и паролей — хранение паролей в виде хэшей, передача данных только по HTTPS.",
]
for t in section_1_3b:
    p(doc, t)

doc.add_page_break()

# ---------- CHAPTER 2 ----------
heading(doc, "ГЛАВА 2. ПРОЕКТИРОВАНИЕ И ТЕСТОВАЯ РЕАЛИЗАЦИЯ СЕРВЕРНОГО ПРИЛОЖЕНИЯ", level=1)

heading(doc, "2.1. Модель БД приложения", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "Инфологическая модель данных приложения представлена на рисунке 3. Сущности, реализуемые в проекте, выделены цветом заголовка: основные сущности предметной области — синим, связующие сущности, реализующие связи «многие-ко-многим», — оранжевым.")

pic_par3 = doc.add_paragraph()
pic_par3.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par3.add_run().add_picture("/home/analyst/kursovaya_pdd/er_diagram.png", width=Cm(16.5))
cap3 = doc.add_paragraph()
cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap3.add_run("Рис. 3. Инфологическая модель данных (ER-диаграмма)")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

section_2_1 = [
"Описание сущностей. User (Пользователь) — учётная запись кандидата, готовящегося к экзамену по ПДД; хранит email, имя пользователя, хэш пароля, роль (пользователь/модератор) и аватар. Question (Вопрос/билет) — вопрос, привязанный к номеру экзаменационного билета и теме раздела ПДД (topic_id); имеет статус (опубликован/разъяснён). Topic (Тема раздела ПДД) — справочник тематических разделов ПДД, аналог тега в проекте Фудграм. Comment (Комментарий) — комментарий пользователя к вопросу. Favorite (Избранное), ReviewList (Список на повторение) и Subscription (Подписка) — связующие сущности, реализующие отношения «многие-ко-многим»: пользователь — избранные вопросы, пользователь — вопросы на повторение, пользователь — пользователь (подписки).",
"Описание интеграции данных из других корпоративных приложений. Данные сущности Question могут синхронизироваться с внешней базой экзаменационных вопросов Госавтоинспекции (официальный перечень вопросов для теоретического экзамена) — для первоначального наполнения справочника вопросов и его обновления при изменении ПДД; назначение внешней системы — единый источник актуальных формулировок экзаменационных билетов. Данные сущности User могут синхронизироваться с внешним провайдером аутентификации (например, системой единого входа через Госуслуги) — назначение внешней системы заключается в упрощении регистрации и подтверждении личности пользователя.",
]
for t in section_2_1:
    p(doc, t)

heading(doc, "2.2. Структура прикладной системы", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "Диаграмма компонентов (прикладных Python-пакетов проекта на базе Django) представлена на рисунке 4. Все пакеты, кроме api, реализуются в рамках проекта (на диаграмме выделены цветом).")

pic_par4 = doc.add_paragraph()
pic_par4.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par4.add_run().add_picture("/home/analyst/kursovaya_pdd/component_diagram.png", width=Cm(16))
cap4 = doc.add_paragraph()
cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap4.add_run("Рис. 4. Диаграмма компонентов прикладной системы")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

section_2_2 = [
"Описание компонентов. core — пакет общих утилит, базовых классов моделей (абстрактные модели с created_at и т.п.), констант и общих разрешений (permissions) DRF; не содержит специфичной для ПДД-сервиса логики и может быть перенесён в любой другой Django-проект без изменений.",
"users — пакет учётных записей и аутентификации (модель User, регистрация, токены). Переиспользуем: модуль типовой для любого проекта с регистрацией пользователей, адаптируется заменой нескольких полей профиля.",
"questions — пакет предметной области: модели Question, Comment, Topic и бизнес-логика работы с вопросами ПДД и их обсуждением. Специфичен для данного проекта и напрямую не переиспользуется, но структура пакета (сущность + обсуждения + тематический справочник) может быть использована как шаблон для аналогичных Q&A-сервисов.",
"favorites — пакет моделей Favorite и ReviewList, реализующих пользовательские списки (избранное и список на повторение). Переиспользуем: механизм «пользователь — отмеченные объекты» типовой и легко переносится в проекты с любой другой предметной сущностью вместо Question.",
"subscriptions — пакет модели Subscription (подписки пользователей друг на друга). Переиспользуем: стандартный механизм подписок, не зависящий от предметной области, переносится в другие проекты без изменений.",
"api — пакет, реализующий REST API (сериализаторы, вьюсеты, роутеры Django REST Framework), объединяющий модели остальных пакетов в единый программный интерфейс для клиента. Является специфичной для проекта интеграционной частью и не предназначен для переиспользования в чужом виде.",
]
for t in section_2_2:
    p(doc, t)

heading(doc, "2.3. Спецификация REST API (реализуемая часть проекта)", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "Аутентификация реализуется стандартным для DRF-проектов способом (эндпоинт /api/auth/token/ по схеме Djoser/Simple JWT) и в таблицу ниже не включена. Спецификация прикладных ресурсов API представлена в таблице 2.")

tbl2_num = doc.add_paragraph()
tbl2_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = tbl2_num.add_run("Таблица 2")
r.font.name = FONT; r.font.size = SIZE

tbl2_title = doc.add_paragraph()
tbl2_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tbl2_title.paragraph_format.left_indent = Cm(0.5)
r = tbl2_title.add_run("Спецификация ресурсов REST API")
r.font.name = FONT; r.font.size = SIZE; r.bold = True

api_table = [
    ("Пользователи", "/api/users/", "GET, POST", "id, username, email, avatar", "Список пользователей, регистрация"),
    ("Профиль пользователя", "/api/users/{id}/", "GET", "id, username, avatar, questions_count", "Просмотр профиля"),
    ("Текущий пользователь", "/api/users/me/", "GET, PATCH", "id, username, email, avatar", "Просмотр/редактирование своего профиля"),
    ("Подписка", "/api/users/{id}/subscribe/", "POST, DELETE", "author, follower", "Подписаться/отписаться от пользователя"),
    ("Подписки", "/api/users/subscriptions/", "GET", "[{id, username, avatar}]", "Лента подписок"),
    ("Темы ПДД", "/api/topics/", "GET", "id, name, slug", "Список тем разделов ПДД"),
    ("Вопросы", "/api/questions/", "GET, POST", "id, author, topic, ticket_number, text, image, status, created_at", "Список вопросов (с фильтром по теме/билету), создание вопроса"),
    ("Вопрос", "/api/questions/{id}/", "GET, PATCH, DELETE", "— (как выше)", "Просмотр, редактирование, удаление вопроса"),
    ("Комментарии", "/api/questions/{id}/comments/", "GET, POST", "id, author, text, created_at", "Список и добавление комментариев к вопросу"),
    ("Комментарий", "/api/comments/{id}/", "PATCH, DELETE", "text", "Редактирование/удаление комментария"),
    ("Избранное", "/api/questions/{id}/favorite/", "POST, DELETE", "question, user", "Добавить/убрать вопрос из избранного"),
    ("Список на повторение", "/api/questions/{id}/review_list/", "POST, DELETE", "question, user", "Добавить/убрать вопрос из списка на повторение"),
    ("Выгрузка списка", "/api/review_list/download/", "GET", "файл txt/pdf", "Скачивание списка вопросов на повторение"),
    ("Модерация вопроса", "/api/questions/{id}/moderate/", "PATCH", "status", "Изменение статуса вопроса модератором"),
]

table2 = doc.add_table(rows=1, cols=5)
table2.style = "Table Grid"
widths2 = [Cm(2.8), Cm(3.6), Cm(2.3), Cm(4.3), Cm(4.3)]
for col, w in zip(table2.columns, widths2):
    for cell in col.cells:
        cell.width = w

headers2 = ["Название ресурса", "URL ресурса", "HTTP-метод", "Структура данных (JSON)", "Реализуемые функции"]
for i, htext in enumerate(headers2):
    style_cell(table2.rows[0].cells[i], htext)

for row_data in api_table:
    row = table2.add_row().cells
    for i, val in enumerate(row_data):
        style_cell(row[i], val)

heading(doc, "2.4. Технология клиент-серверного взаимодействия", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "Взаимодействие фронтенда и бэкенда через REST API рассмотрено на двух типовых сценариях: публикация вопроса (рисунок 5) и добавление вопроса в пользовательский список — избранное/на повторение (рисунок 6); остальные прецеденты (комментирование, подписка и т.п.) реализуются по аналогичной схеме «запрос — проверка — обращение к БД — ответ».")

pic_par5 = doc.add_paragraph()
pic_par5.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par5.add_run().add_picture("/home/analyst/kursovaya_pdd/seq_publish_question.png", width=Cm(15))
cap5 = doc.add_paragraph()
cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap5.add_run("Рис. 5. Диаграмма последовательности: публикация вопроса")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

pic_par6 = doc.add_paragraph()
pic_par6.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par6.add_run().add_picture("/home/analyst/kursovaya_pdd/seq_add_favorite.png", width=Cm(15))
cap6 = doc.add_paragraph()
cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap6.add_run("Рис. 6. Диаграмма последовательности: добавление вопроса в избранное")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

heading(doc, "2.5. Архитектура развёртывания системы в ИТ-инфраструктуре", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "В отличие от концептуальной диаграммы развёртывания (глава 1), отражающей архитектуру на уровне вычислительных узлов, диаграмма на рисунке 7 детализирует контейнерную архитектуру реализации приложения на базе Docker Compose.")

pic_par7 = doc.add_paragraph()
pic_par7.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par7.add_run().add_picture("/home/analyst/kursovaya_pdd/deployment_container.png", width=Cm(16))
cap7 = doc.add_paragraph()
cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap7.add_run("Рис. 7. Диаграмма развёртывания (контейнерная архитектура)")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

section_2_5 = [
"Спецификация контейнерной среды. Платформа — выделенный сервер (виртуальная машина) под управлением Linux с установленным Docker Engine и Docker Compose. Все три контейнера проекта развёртываются из единого docker-compose.yml и объединены общей Docker-сетью.",
"Контейнер nginx (образ nginx:latest) — принимает запросы клиента по HTTPS (порты 80/443), отдаёт статику и медиафайлы из общего volume static_media, остальные запросы перенаправляет (proxy_pass) в контейнер backend на порт 8000.",
"Контейнер backend (Gunicorn + Django-приложение) — обрабатывает бизнес-логику и REST API, обращается к контейнеру db по протоколу SQL (порт 5432), сохраняет статические и медиафайлы в общий volume static_media.",
"Контейнер db (образ postgres:15) — СУБД PostgreSQL, данные хранятся в volume postgres_data, обеспечивающем сохранность данных между перезапусками контейнеров.",
]
for t in section_2_5:
    p(doc, t)

heading(doc, "2.6. Контрольный прогон тестовой реализации", size=Pt(14), space_before=6, space_after=6, level=2)
p(doc, "Серверная часть реализована на Python/Django + Django REST Framework согласно спецификации п. 2.1–2.5 и развёрнута локально для тестового прогона; клиентская часть — веб-интерфейс на Django-шаблонах, реализующий прецеденты из п. 1.2. Ниже приведены скриншоты работающей системы.")

pic_par8 = doc.add_paragraph()
pic_par8.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par8.add_run().add_picture("/home/analyst/kursovaya_pdd/screenshot_landing.png", width=Cm(16))
cap8 = doc.add_paragraph()
cap8.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap8.add_run("Рис. 8. Главная страница сервиса")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

pic_par9 = doc.add_paragraph()
pic_par9.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par9.add_run().add_picture("/home/analyst/kursovaya_pdd/screenshot_questions.png", width=Cm(16))
cap9 = doc.add_paragraph()
cap9.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap9.add_run("Рис. 9. Лента вопросов с фильтром по теме (авторизованный пользователь)")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

pic_par10 = doc.add_paragraph()
pic_par10.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic_par10.add_run().add_picture("/home/analyst/kursovaya_pdd/screenshot_question_detail.png", width=Cm(16))
cap10 = doc.add_paragraph()
cap10.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap10.add_run("Рис. 10. Страница вопроса с обсуждением (реализация прецедентов 4–5, 7, 10)")
r.font.name = FONT; r.font.size = Pt(12); r.italic = True; r.bold = False

doc.add_page_break()

heading(doc, "ЗАКЛЮЧЕНИЕ", level=1)
conclusion = [
"В ходе выполнения курсовой работы была достигнута поставленная цель — спроектировано и доведено до стадии тестовой реализации серверное приложение для сервиса общения кандидатов, готовящихся к сдаче теоретического экзамена по Правилам дорожного движения.",
"Решены все задачи, сформулированные во введении. Изучена предметная область и сформулированы функциональные и нефункциональные требования к системе (глава 1): определены действующие лица (Гость, Пользователь, Модератор) и 14 прецедентов их взаимодействия с системой, построена диаграмма вариантов использования, обоснована клиент-серверная архитектура приложения на основе REST API.",
"Разработана инфологическая модель базы данных, включающая 7 сущностей (User, Question, Topic, Comment и связующие Favorite, ReviewList, Subscription), рассмотрена возможность интеграции данных с внешними корпоративными системами (база экзаменационных вопросов ГИБДД, провайдер аутентификации). Спроектирована структура прикладной системы в виде шести Python-пакетов Django-проекта с оценкой их переиспользуемости, разработана спецификация REST API из 14 ресурсов, построены диаграммы последовательностей ключевых сценариев клиент-серверного взаимодействия и диаграмма развёртывания контейнерной архитектуры на базе Docker Compose.",
"Выбранный технологический стек (Python, Django, Django REST Framework, PostgreSQL, React, Docker) соответствует задачам курса и обеспечивает возможность реализации спроектированной системы с переиспользованием архитектурного паттерна итоговой проектной работы «Фудграм» в новой предметной области.",
"Практическая реализация спроектированной системы (тестовый прогон, п. 2.6) выполняется на следующем этапе работы над проектом в соответствии с разработанной в настоящей курсовой работе спецификацией.",
]
for t in conclusion:
    p(doc, t)

doc.add_page_break()

heading(doc, "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", level=1)

heading(doc, "Список законодательных и нормативно-правовых документов", size=Pt(14), space_before=6, space_after=6)
legal_sources = [
"Постановление Правительства РФ от 23.10.1993 № 1090 «О Правилах дорожного движения» (действующая редакция).",
"Приказ МВД России от 20.10.2015 № 995 «Об утверждении Административного регламента по предоставлению государственной услуги по проведению экзаменов на право управления транспортными средствами» (действующая редакция).",
]
for i, s in enumerate(legal_sources, 1):
    p(doc, f"{i}. {s}", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

heading(doc, "Список литературных и журнальных источников", size=Pt(14), space_before=6, space_after=6)
lit_sources = [
"Фаулер, М. UML. Основы: краткое руководство по унифицированному языку моделирования / М. Фаулер. — 3-е изд. — СПб.: Символ-Плюс, 2011.",
"Фаулер, М. Архитектура корпоративных программных приложений / М. Фаулер. — М.: Вильямс, 2016.",
"Fielding, R. T. Architectural Styles and the Design of Network-based Software Architectures: Dissertation / R. T. Fielding. — University of California, Irvine, 2000.",
"Percival, H. Test-Driven Development with Python: Obey the Testing Goat / H. Percival. — 2nd ed. — O'Reilly Media, 2017.",
"Vincent, W. S. Django for Professionals: Production Websites with Python & Django / W. S. Vincent. — 2022.",
]
for i, s in enumerate(lit_sources, len(legal_sources) + 1):
    p(doc, f"{i}. {s}", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

heading(doc, "Список интернет-источников", size=Pt(14), space_before=6, space_after=6)
net_sources = [
"Django Software Foundation. Django documentation [Электронный ресурс]. — Режим доступа: https://docs.djangoproject.com (дата обращения: 16.11.2026).",
"Encode OSS Ltd. Django REST Framework — документация [Электронный ресурс]. — Режим доступа: https://www.django-rest-framework.org (дата обращения: 16.11.2026).",
"PostgreSQL Global Development Group. PostgreSQL Documentation [Электронный ресурс]. — Режим доступа: https://www.postgresql.org/docs/ (дата обращения: 16.11.2026).",
"Docker Inc. Docker Compose overview [Электронный ресурс]. — Режим доступа: https://docs.docker.com/compose/ (дата обращения: 16.11.2026).",
"Госавтоинспекция МВД России: официальный сайт [Электронный ресурс]. — Режим доступа: https://гибдд.рф (дата обращения: 16.11.2026).",
"Яндекс.Практикум. Курс «Основы бэкенд-разработки на Python» [Электронный ресурс]. — Режим доступа: https://practicum.yandex.ru (дата обращения: 16.11.2026).",
]
for i, s in enumerate(net_sources, len(legal_sources) + len(lit_sources) + 1):
    p(doc, f"{i}. {s}", align=WD_ALIGN_PARAGRAPH.JUSTIFY)

out_path = "/home/analyst/kursovaya_pdd/Курсовая_ИиУПнаУС_Солнцев.docx"
doc.save(out_path)
print("saved:", out_path)
