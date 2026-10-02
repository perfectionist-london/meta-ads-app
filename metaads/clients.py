"""Реєстр ПРОЄКТІВ: кабінети, бізнеси, сторінки, пікселі, каталоги, IG.

Нащо існує
──────────
29.09.2026  реклама Gasanova вийшла від сторінки Kaia Fincher — 85 тис.
            показів під чужим брендом. META_PAGE_ID у .env вказував на
            сторінку Kaia, кабінет передавався окремо.
02.10.2026  я взяв `catalogs[0]` зі списку і це був umahanova.com.

Обидва рази механізм існував лише для одного типу обʼєкта, а помилка
прийшла через інший. Тому тип обʼєкта тут — параметр.

⛔ Meta дозволяє більше, ніж можна нам. Токен бачить 17 бізнесів,
`promote_pages` кабінету Gasanova віддає і сторінку Kaia, список каталогів
віддає каталоги Umahanova. Блокуємо МИ, не Meta.

Чому ключ — проєкт, а не кабінет
────────────────────────────────
DAMIRLI це чоловічий бренд від Gasanova. Він живе в ТОМУ САМОМУ
рекламному кабінеті, але це окремий проєкт: окремі висновки, окремий
магазин, окремі рішення. Модель «кабінет = клієнт» це не описує.

Тому: проєкт має список кабінетів, а кабінет може хостити кілька
проєктів. Обʼєкт належить рівно одному проєкту.

   обʼєкт із проєкту, якого цей кабінет не хостить  → БЛОК
   обʼєкт з іншого проєкту в ТОМУ САМОМУ кабінеті   → пускаємо, але
                                                      голосно називаємо
                                                      обидва проєкти
"""

PROJECTS = {
    # ──────────────────────────────────────────────────────────────────
    "GASANOVA": {
        "accounts": ["act_961161750939400"],
        "business": ("640337116384765", "Gasanova"),
        "currency": "USD",
        "timezone": "Europe/Kiev",
        "docs": "~/Desktop/Claude/Target",
        "pages": {
            "1411574982408904": "Gasanova — FB @gasanovabrand",
            "107878508293639": "gasanova.brand — IG-backed @gasanova.brand",
            "103029658977853": "Elvira Gasanova — ТІЛЬКИ колаб із брендом",
        },
        "pixels": {"781801142376766": "GASANOVA.ONLINE"},
        "catalogs": {"1538189433343749": "GASANOVA MAIN CATALOG"},
        "ig": {
            "17841401446172859": "@gasanova.brand",
            "17841400342184672": "@gasanova_elvira — ТІЛЬКИ колаб",
        },
        "shopify": {"gasanova-05c3.myshopify.com": "gasanova.ua"},
        "keycrm": "один акаунт, точки Київ і Львів із 01.09.26",
    },
    # ──────────────────────────────────────────────────────────────────
    "DAMIRLI": {
        "note": "Чоловічий бренд від Gasanova. ТОЙ САМИЙ рекламний кабінет, "
                "але окремий проєкт: окремі висновки, окремий магазин. "
                "`CLAUDE.md` §7: не чіпати без окремого рішення Олега.",
        "accounts": ["act_961161750939400"],   # ⚠ той самий, що GASANOVA
        "business": ("640337116384765", "Gasanova"),
        "currency": "USD",
        "timezone": "Europe/Kiev",
        "pages": {"103334898803095": "Damirli — FB @damirliofficial"},
        "pixels": {"363514556616300": "damirli"},
        "catalogs": {"926562882443475": "DAMIRLI Catalogue 2025"},
        "ig": {"17841445985178737": "@damirli_official"},
        "shopify": {"damirli.com": "damirli.com — той самий Shopify-акаунт"},
        "keycrm": None,
    },
    # ──────────────────────────────────────────────────────────────────
    "KAIA FINCHER": {
        "accounts": ["act_1731887314115067"],
        "business": ("600668876143799", "Kaia Fincher"),
        "currency": "USD",
        "timezone": "Europe/London",   # ⚠ НЕ Kiev — межі доби інші
        "pages": {"558580180666271": "Kaia Fincher — FB @kaiafincher"},
        "pixels": {"771819848597790": "Kaia Fincher's Pixel"},
        "catalogs": {"1272310927972788": "Shopify Product Catalog (Kaia)"},
        "ig": {"17841472188821272": "@kaia_fincher"},
        "shopify": {},
        "keycrm": None,
    },
    # ──────────────────────────────────────────────────────────────────
    "UMAHANOVA": {
        "note": "Окремий клієнт. Його каталоги видно з кабінету Gasanova — "
                "02.10.2026 я взяв звідти catalogs[0] помилково.",
        "accounts": ["act_568419979432319"],
        "business": ("1652739328829837", "Umahanova"),
        "currency": "UAH",             # ⚠ НЕ USD
        "timezone": "Europe/Kiev",
        "pages": {
            "289678474238445": "Umahanova — owned_pages",
            "266720806526619": "Umahanova — primary_page бізнесу",
        },
        "pixels": {
            "1133910904974852": "UMAHANOVA's pixel",
            "1173543341239901": "тест",
        },
        "catalogs": {
            "1522311922154876": "Products from umahanova.com (304)",
            "1987048735438046": "Shopify Product Catalog (686)",
        },
        "ig": {"17841465699865880": "@umahanova.brand"},
        "shopify": {},
        "keycrm": None,
    },
}


# Обʼєкти, дозволені лише за умови. Ключ → текст, який показуємо щоразу.
CONDITIONAL = {
    "103029658977853":
        "⚠ Сторінка Ельвіри — ТІЛЬКИ колаб-пости, де Gasanova співавтор.\n"
        "  У стрічці підпис мусить бути «Elvira Gasanova and Gasanova».\n"
        "  Через API співавторства не видно — тільки прев'ю оголошення.",
    "17841400342184672":
        "⚠ @gasanova_elvira — ТІЛЬКИ колаб, див. сторінку 103029658977853.",
    "363514556616300":
        "⛔ Піксель damirli. Інтерфейс Meta підставляє його ЗА ЗАМОВЧУВАННЯМ\n"
        "  при створенні аудиторій у цьому кабінеті (`CLAUDE.md` §2).\n"
        "  Для Gasanova завжди міняти на GASANOVA.ONLINE 781801142376766.",
}


# Мертві сторінки. У реєстр не входять — з них нічого не вмикати.
RETIRED = {
    "114821090352654":
        "«Gasanova Boutique временный» — стара тимчасова сторінка бренду "
        "(1 підписник, 0 постів). 50 креативів 2021 року.",
    "687420154798529":
        "«Elvira Gasanova» (Personal blog, 15 підписників) — СТАРА сторінка "
        "Ельвіри, не та, що в реєстрі. 2 креативи 2019 року.",
}


# Бізнеси, які бачить токен. Наші — ті, що в PROJECTS. Решта НІКОЛИ не наші.
FOREIGN_BUSINESSES = {
    "1418174600253143": "Fractal ua",
    "1336393320688185": "askinkila_kids",
    "1218467958734148": "Good News",
    "1206822554575389": "Shelter Film",
    "957207638631221": "Perfectionist LDN",
    "768277360031971": "Perfectionist",
    "548332705563194": "Lief",
    "536610463473825": "Lyubov Zaplatina - Education manager",
    "518540908591623": "Центр стоматології Голобородько",
    "465795146505750": "Yuliya Shpyg",
    "409733847444442": "DigitalElla",
    "324042648242731": "Dasha Taivas",
    "213406226560137": "Holic Agency",
    "127083744779128": "Ukrainian Fashion Department",
}

KINDS = {
    "page":    ("pages",    "СТОРІНКА",  "--page-id"),
    "pixel":   ("pixels",   "ПІКСЕЛЬ",   "--pixel-id"),
    "catalog": ("catalogs", "КАТАЛОГ",   "--catalog-id"),
    "ig":      ("ig",       "IG-АКАУНТ", "--instagram-user-id"),
}


# ── похідні індекси ─────────────────────────────────────────────────────
def _norm(account_id):
    a = str(account_id or "")
    return a if a.startswith("act_") else (f"act_{a}" if a else "")


ACCOUNT_PROJECTS = {}
for _pr, _d in PROJECTS.items():
    for _a in _d["accounts"]:
        ACCOUNT_PROJECTS.setdefault(_norm(_a), []).append(_pr)

# (тип, id) → (проєкт, назва)
OBJECT_INDEX = {}
for _pr, _d in PROJECTS.items():
    for _kind, (_key, _, _) in KINDS.items():
        for _i, _n in (_d.get(_key) or {}).items():
            OBJECT_INDEX[(_kind, str(_i))] = (_pr, _n)

BUSINESSES = {d["business"][0]: (d["business"][1], d["accounts"][0])
              for d in PROJECTS.values()}

# ⛔ сумісність: старі виклики чекають CLIENTS і FOREIGN_CATALOGS
CLIENTS = {}
for _pr, _d in PROJECTS.items():
    for _a in _d["accounts"]:
        a = _norm(_a)
        c = CLIENTS.setdefault(a, {"client": _pr, "projects": [],
                                   "pages": {}, "pixels": {},
                                   "catalogs": {}, "ig_accounts": {},
                                   "business_id": _d["business"][0],
                                   "currency": _d.get("currency"),
                                   "timezone": _d.get("timezone")})
        c["projects"].append(_pr)
        c["pages"].update(_d.get("pages") or {})
        c["pixels"].update(_d.get("pixels") or {})
        c["catalogs"].update(_d.get("catalogs") or {})
        c["ig_accounts"].update(_d.get("ig") or {})

FOREIGN = {i: f"каталог «{n}» — проєкт {p}"
           for (k, i), (p, n) in OBJECT_INDEX.items()
           if k == "catalog" and p in ("UMAHANOVA",)}
FOREIGN_CATALOGS = FOREIGN


# ── довідки ─────────────────────────────────────────────────────────────
def known(account_id):
    return _norm(account_id) in ACCOUNT_PROJECTS


def projects_of(account_id):
    return ACCOUNT_PROJECTS.get(_norm(account_id), [])


def client_of(account_id):
    pr = projects_of(account_id)
    return " + ".join(pr) if pr else None


project_of = client_of


def profile(account_id):
    return CLIENTS.get(_norm(account_id))


def objects_of(account_id, kind):
    key = KINDS[kind][0]
    out = {}
    for pr in projects_of(account_id):
        out.update(PROJECTS[pr].get(key) or {})
    return out


def pages_of(account_id):    return objects_of(account_id, "page")
def pixels_of(account_id):   return objects_of(account_id, "pixel")
def catalogs_of(account_id): return objects_of(account_id, "catalog")
def ig_of(account_id):       return objects_of(account_id, "ig")


def page_label(account_id, page_id):
    return pages_of(account_id).get(str(page_id))


def owner_of(object_id, kind):
    """(проєкт, назва) або (None, None)."""
    got = OBJECT_INDEX.get((kind, str(object_id)))
    return got if got else (None, None)


def owner_of_page(page_id):
    pr, n = owner_of(page_id, "page")
    if not pr:
        return None, None
    return n, PROJECTS[pr]["accounts"][0]


# ── перевірки ───────────────────────────────────────────────────────────
def check_object(account_id, kind, object_id):
    """(ok, повідомлення). Не друкує і не завершує процес."""
    acct = _norm(account_id)
    _, слово, флаг = KINDS[kind]
    мої = projects_of(acct)

    if not object_id:
        if not мої:
            return False, (f"{слово} треба вказати явно: {флаг}.\n"
                           f"  Кабінет {acct} не описаний у clients.py.")
        allowed = ", ".join(f"{i} ({n})" for i, n in objects_of(acct, kind).items())
        return False, (f"{слово} треба вказати явно: {флаг}.\n"
                       f"  Кабінет {acct} — проєкт(и): {', '.join(мої)}.\n"
                       f"  Дозволені: {allowed or 'жодного в реєстрі'}")

    oid = str(object_id)
    if not мої:
        return True, (f"УВАГА: кабінет {acct} не описаний у clients.py — "
                      f"{слово.lower()} {oid} не звіряю. Якщо це постійний "
                      f"клієнт, додай його в PROJECTS.")

    власник, назва = owner_of(oid, kind)
    allowed = ", ".join(f"{i} ({n})" for i, n in objects_of(acct, kind).items())

    if власник in мої:
        # Свій проєкт. Якщо кабінет хостить кілька — попереджаємо ТІЛЬКИ про
        # непервинний. Інакше кожна рядова операція Gasanova друкувала б
        # попередження, а шум робить попередження невидимими.
        попередження = CONDITIONAL.get(oid)
        if len(мої) > 1 and власник != мої[0]:
            інші = [p for p in мої if p != власник]
            хвіст = (f"⚠ ОБʼЄКТ ПРОЄКТУ {власник}, а кабінет хостить ще "
                     f"{', '.join(інші)}.\n"
                     f"  {oid} — {назва}\n"
                     f"  Переконайся, що працюєш саме з {власник}.")
            if PROJECTS[власник].get("note"):
                хвіст += f"\n  {PROJECTS[власник]['note']}"
            попередження = (попередження + "\n" + хвіст) if попередження else хвіст
        return True, попередження

    if kind == "page" and oid in RETIRED:
        return False, (f"❌ МЕРТВА СТОРІНКА, вмикати не можна.\n"
                       f"  {oid}: {RETIRED[oid]}\n"
                       f"  Кабінет {acct} — {', '.join(мої)}.\n"
                       f"  Дозволені: {allowed}")

    опис = (f" — проєкт {власник}, «{назва}»" if власник
            else " — невідомий, у реєстрі немає")
    хвіст = ""
    if власник:
        хвіст = (f"\n  ⚠ Meta це ДОЗВОЛИТЬ: обʼєкт видно з цього кабінету. "
                 f"Блокуємо МИ.\n"
                 f"  Саме так 29.09.2026 реклама Gasanova вийшла від Kaia "
                 f"Fincher на 85 тис. показів.")
    return False, (f"❌ {слово} НЕ З ПРОЄКТІВ ЦЬОГО КАБІНЕТУ.\n"
                   f"  Кабінет: {acct} — {', '.join(мої)}\n"
                   f"  {слово.capitalize()}: {oid}{опис}\n"
                   f"  Дозволені: {allowed or 'жодного'}{хвіст}\n"
                   f"  Якщо справді потрібно — правити PROJECTS свідомо.")


def check(account_id, page_id):         return check_object(account_id, "page", page_id)
def check_page(account_id, page_id):    return check_object(account_id, "page", page_id)
def check_pixel(account_id, pixel_id):  return check_object(account_id, "pixel", pixel_id)
def check_catalog(account_id, cat_id):  return check_object(account_id, "catalog", cat_id)
def check_ig(account_id, ig_id):        return check_object(account_id, "ig", ig_id)


def check_business(account_id, business_id):
    acct = _norm(account_id)
    bid = str(business_id)
    наш = BUSINESSES.get(bid)
    if наш and _norm(наш[1]) == acct:
        return True, None
    чий = FOREIGN_BUSINESSES.get(bid) or (наш[0] if наш else None)
    return False, (f"❌ БІЗНЕС НЕ ВОЛОДІЄ ЦИМ КАБІНЕТОМ.\n"
                   f"  Кабінет: {acct} — {client_of(acct) or '?'}\n"
                   f"  Бізнес:  {bid}" + (f" — {чий}" if чий else " — невідомий") + "\n"
                   f"  Токен бачить 17 бізнесів; наші описані в PROJECTS.")


def verify_live(account_id):
    """Звірити реєстр із тим, що віддає API. Реєстр — твердження, і воно старіє."""
    from metaads import api
    acct = _norm(account_id)
    p = profile(acct)
    if not p:
        return [f"кабінет {acct} не описаний у реєстрі"]
    d = api._api_call("GET", acct,
                      {"fields": "id,name,business{id,name},currency,timezone_name"})
    b = d.get("business") or {}
    розб = []
    if str(b.get("id") or "") != p["business_id"]:
        розб.append(f"бізнес: реєстр {p['business_id']}, API {b.get('id')} ({b.get('name')})")
    if d.get("currency") != p.get("currency"):
        розб.append(f"валюта: реєстр {p.get('currency')}, API {d.get('currency')}")
    if d.get("timezone_name") != p.get("timezone"):
        розб.append(f"таймзона: реєстр {p.get('timezone')}, API {d.get('timezone_name')}")
    return розб
