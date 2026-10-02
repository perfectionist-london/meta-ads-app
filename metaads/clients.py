"""Жорстка прив'язка рекламних кабінетів до сторінок І КАТАЛОГІВ.

Причина існування: 29.09.2026 реклама бутіка Gasanova вийшла в ефір від
імені kaia_fincher — 85 тис. показів під чужим брендом. Сталось тому, що
META_PAGE_ID у .env вказував на сторінку Kaia, а кабінет передавався
окремо через --account-id. Кабінет одного клієнта, сторінка іншого, і
ніщо про це не попереджало.

02.10.2026 те саме повторилось із каталогами: `catalogs` віддає каталоги
ВСІХ бізнесів, які бачить токен, я взяв перший за індексом і це був
umahanova.com. Олег: «ніяких ЧУЖИХ КАТАЛОГІВ, ніяких ЧУЖИХ АККАУНТІВ,
це критично».

Тепер сторінку і каталог треба передавати явно, і обидва звіряються з
кабінетом. Кабінети, сторінки й каталоги НЕ ПЛУТАЮТЬСЯ НІКОЛИ.
"""

# @gasanova_elvira / сторінка 103029658977853 — ТІЛЬКИ КОЛАБ З БРЕНДОМ.
#
# Правило Олега: рекламу Gasanova крутимо з інстаграму бренду. Але
# Ельвіра буває співавтором колаб-постів, і такий пост — легітимний
# носій: у стрічці він підписаний «Elvira Gasanova and Gasanova», бренд
# там присутній. Саме так ішла реклама події 25.09 у Львові.
#
# Тому сторінка в реєстрі є, але призначення в неї одне:
#   МОЖНА   колаб-пост, де Gasanova співавтор
#   НЕ МОЖНА  сольна реклама з її акаунту
#
# Перевірити, що це справді колаб, можна лише прев'ю оголошення: у
# підписі має бути «… and Gasanova». Через API цього не видно —
# `effective_object_story_id` віддає тільки одного автора, її.
# Її сторінку токен не читає взагалі ((#10) missing permission), тому
# резолвити назву не намагайся, це нормально.

CLIENTS = {
    "act_961161750939400": {
        "client": "Gasanova",
        "pages": {
            "1411574982408904": "Gasanova — FB @gasanovabrand",
            "107878508293639": "gasanova.brand — IG-backed @gasanova.brand",
            "103334898803095": "Damirli — FB @damirliofficial",
            "103029658977853": "Elvira Gasanova — ТІЛЬКИ колаб із брендом",
        },
        "pixels": {
            "781801142376766": "GASANOVA.ONLINE — основний",
            "363514556616300": "damirli — ТІЛЬКИ для Damirli",
        },
        "catalogs": {
            "1538189433343749": "GASANOVA MAIN CATALOG",
            "926562882443475": "DAMIRLI Catalogue 2025 — ТІЛЬКИ для Damirli",
        },
        "ig_accounts": {
            "17841401446172859": "@gasanova.brand — основний",
            "17841445985178737": "@damirli_official — ТІЛЬКИ для Damirli",
            "17841400342184672": "@gasanova_elvira — ТІЛЬКИ колаб із брендом",
        },
    },
    "act_1731887314115067": {
        "client": "Kaia Fincher",
        "pages": {
            "558580180666271": "Kaia Fincher — FB @kaiafincher",
        },
        "pixels": {
            "771819848597790": "Kaia Fincher's Pixel",
        },
        "catalogs": {
            "1272310927972788": "Shopify Product Catalog (Kaia Fincher)",
        },
        "ig_accounts": {
            "17841472188821272": "@kaia_fincher",
        },
    },
}


# Обʼєкти, дозволені лише за умови. Ключ → текст умови, який показуємо
# щоразу. Пропускаємо, але НЕ МОВЧКИ.
CONDITIONAL = {
    # ── сторінки ──────────────────────────────────────────────────────
    "103029658977853":
        "⚠ Сторінка Ельвіри дозволена ТІЛЬКИ для колаб-постів, де Gasanova "
        "співавтор.\n"
        "  Відкрий прев'ю оголошення і переконайся, що підпис — "
        "«Elvira Gasanova and Gasanova».\n"
        "  Сольна реклама з її акаунту — ні. Через API співавторства не "
        "видно, тільки прев'ю.",
    "103334898803095":
        "⛔ DAMIRLI. `CLAUDE.md` §7: обʼєкти DAMIRLI не чіпати НІКОЛИ без "
        "окремого рішення Олега.\n"
        "  Бренд ділить з Gasanova Business Manager, Shopify і KeyCRM, тому "
        "лежить у тому ж кабінеті —\n"
        "  але це ОКРЕМИЙ бренд, і випадкова правка тут непомітна.",
    # ── IG ────────────────────────────────────────────────────────────
    "17841400342184672":
        "⚠ @gasanova_elvira — ТІЛЬКИ колаб із брендом, див. сторінку "
        "103029658977853.",
    "17841445985178737":
        "⛔ @damirli_official — DAMIRLI, не чіпати без окремого рішення.",
    # ── пікселі ───────────────────────────────────────────────────────
    "363514556616300":
        "⛔ Піксель damirli. Інтерфейс Meta підставляє його ЗА ЗАМОВЧУВАННЯМ "
        "при створенні аудиторій\n"
        "  у цьому кабінеті (`CLAUDE.md` §2) — завжди міняти на "
        "GASANOVA.ONLINE 781801142376766.",
    # ── каталоги ──────────────────────────────────────────────────────
    "926562882443475":
        "⛔ DAMIRLI Catalogue 2025 — не чіпати без окремого рішення.",
}


# Мертві сторінки з історії кабінету. У реєстр НЕ входять — з них нічого
# не можна вмикати. Тут лише щоб помилка пояснювала, що це, і ніхто не
# витрачав час на повторне розслідування.
RETIRED = {
    "114821090352654":
        "«Gasanova Boutique временный» — стара тимчасова сторінка бренду "
        "(1 підписник, 0 постів). 50 креативів 2021 року.",
    "687420154798529":
        "«Elvira Gasanova» (Personal blog, 15 підписників) — СТАРА сторінка "
        "Ельвіри, не та, що в реєстрі. 2 креативи 2019 року.",
}


# Обʼєкти ІНШИХ клієнтів, видимі з наших кабінетів. У реєстр не входять —
# з них нічого не можна брати. Тут лише щоб помилка називала, чиї вони.
#
# 02.10.2026: я взяв перший каталог зі списку за індексом ([0]) і це був
# umahanova.com. Олег: «ніяких ЧУЖИХ КАТАЛОГІВ, ніяких ЧУЖИХ АККАУНТІВ,
# це критично». Той самий клас, що сторінка Kaia 29.09.
FOREIGN = {
    "1522311922154876": "каталог «Products from umahanova.com» — клієнт Umahanova",
    "1987048735438046": "каталог «Shopify Product Catalog» — клієнт Umahanova",
    "339482959740064": "каталог «Products for Perfectionist» — інший бізнес",
    "6258156120907654": "каталог «Products for zeteticsmusic» — інший бізнес",
}
# сумісність зі старою назвою
FOREIGN_CATALOGS = FOREIGN


def _norm(account_id):
    a = str(account_id or "").strip()
    return a if a.startswith("act_") else f"act_{a}"


def known(account_id):
    return _norm(account_id) in CLIENTS


def client_of(account_id):
    e = CLIENTS.get(_norm(account_id))
    return e["client"] if e else None


def pages_of(account_id):
    e = CLIENTS.get(_norm(account_id))
    return dict(e["pages"]) if e else {}


def page_label(account_id, page_id):
    return pages_of(account_id).get(str(page_id))


def owner_of_page(page_id):
    """Якому клієнту належить сторінка — щоб сказати у помилці, чия вона."""
    for acct, e in CLIENTS.items():
        if str(page_id) in e["pages"]:
            return e["client"], acct
    return None, None


def check(account_id, page_id):
    """Повертає (ok, повідомлення). Не друкує і не завершує процес.

    Кабінетів у агенції двадцять, сторінок тридцять сім — описувати всі
    наперед не треба. Логіка така:
      описаний кабінет + своя сторінка   → ok
      описаний кабінет + чужа сторінка   → БЛОК, з назвою чия вона
      кабінет не описаний                → пускаємо, але сторінку все одно
                                           вимагаємо явно і голосно попереджаємо
    Мовчки не підставляється нічого ніколи.
    """
    acct = _norm(account_id)
    if not known(acct):
        if not page_id:
            return False, (f"Сторінку треба вказати явно: --page-id.\n"
                           f"  Кабінет {acct} не описаний у metaads/clients.py,\n"
                           f"  тому підказати дозволені я не можу. Подивитись, що\n"
                           f"  цей кабінет узагалі може промотувати:\n"
                           f"    GET {acct}/promote_pages")
        return True, (f"УВАГА: кабінет {acct} не описаний у metaads/clients.py — "
                      f"сторінку {page_id} не звіряю. Якщо це постійний клієнт, "
                      f"додай його в реєстр.")
    if not page_id:
        allowed = ", ".join(f"{p} ({n})" for p, n in pages_of(acct).items())
        return False, (f"Сторінку треба вказати явно: --page-id.\n"
                       f"  Кабінет {acct} — {client_of(acct)}.\n"
                       f"  Дозволені сторінки: {allowed}")
    page_id = str(page_id)
    if page_id in pages_of(acct):
        return True, CONDITIONAL.get(page_id)

    owner, owner_acct = owner_of_page(page_id)
    allowed = ", ".join(f"{p} ({n})" for p, n in pages_of(acct).items())
    if page_id in RETIRED:
        return False, (f"❌ МЕРТВА СТОРІНКА, вмикати не можна.\n"
                       f"  {page_id}: {RETIRED[page_id]}\n"
                       f"  Кабінет {acct} — {client_of(acct)}.\n"
                       f"  Дозволені: {allowed}")
    msg = (f"❌ СТОРІНКА НЕ ВІД ЦЬОГО КЛІЄНТА.\n"
           f"  Кабінет:  {acct} — {client_of(acct)}\n"
           f"  Сторінка: {page_id}"
           + (f" — належить {owner} ({owner_acct})" if owner else " — невідома")
           + f"\n  Дозволені: {allowed}\n"
           f"  Кабінети не плутаються. Якщо це справді потрібно — "
           f"правити metaads/clients.py свідомо.")
    return False, msg


# ── універсальна перевірка для всіх типів обʼєктів ───────────────────────
#
# Нащо одна функція замість чотирьох схожих: 29.09 переплуталась сторінка,
# 02.10 каталог. Обидва рази механізм був тільки для одного типу обʼєкта,
# а помилка прийшла через інший. Тепер тип — це параметр.

KINDS = {
    "page":     ("pages",        "СТОРІНКА",      "--page-id"),
    "pixel":    ("pixels",       "ПІКСЕЛЬ",       "--pixel-id"),
    "catalog":  ("catalogs",     "КАТАЛОГ",       "--catalog-id"),
    "ig":       ("ig_accounts",  "IG-АКАУНТ",     "--instagram-user-id"),
}


def objects_of(account_id, kind):
    key = KINDS[kind][0]
    return (CLIENTS.get(_norm(account_id)) or {}).get(key, {})


def owner_of(object_id, kind):
    """Якому клієнту належить обʼєкт цього типу. (назва, кабінет) або (None, None)."""
    key = KINDS[kind][0]
    for acct, data in CLIENTS.items():
        if str(object_id) in data.get(key, {}):
            return data[key][str(object_id)], acct
    return None, None


def check_object(account_id, kind, object_id):
    """(ok, повідомлення). Не друкує і не завершує процес.

    описаний кабінет + свій обʼєкт   → ok (+ умова, якщо є в CONDITIONAL)
    описаний кабінет + чужий обʼєкт  → БЛОК, з назвою чий він
    кабінет не описаний              → пускаємо, але голосно попереджаємо
    """
    acct = _norm(account_id)
    _, слово, флаг = KINDS[kind]
    if not object_id:
        if not known(acct):
            return False, (f"{слово} треба вказати явно: {флаг}.\n"
                           f"  Кабінет {acct} не описаний у metaads/clients.py.")
        allowed = ", ".join(f"{i} ({n})" for i, n in objects_of(acct, kind).items())
        return False, (f"{слово} треба вказати явно: {флаг}.\n"
                       f"  Кабінет {acct} — {client_of(acct)}.\n"
                       f"  Дозволені: {allowed or 'жодного в реєстрі'}")
    oid = str(object_id)
    if not known(acct):
        return True, (f"УВАГА: кабінет {acct} не описаний у clients.py — "
                      f"{слово.lower()} {oid} не звіряю. Якщо це постійний "
                      f"клієнт, додай його в реєстр.")
    if oid in objects_of(acct, kind):
        return True, CONDITIONAL.get(oid)

    allowed = ", ".join(f"{i} ({n})" for i, n in objects_of(acct, kind).items())
    if kind == "page" and oid in RETIRED:
        return False, (f"❌ МЕРТВА СТОРІНКА, вмикати не можна.\n"
                       f"  {oid}: {RETIRED[oid]}\n"
                       f"  Кабінет {acct} — {client_of(acct)}.\n"
                       f"  Дозволені: {allowed}")
    чий = FOREIGN.get(oid)
    власник, вл_акт = owner_of(oid, kind)
    опис = (f" — {чий}" if чий else
            f" — належить {власник} ({вл_акт})" if власник else
            " — невідомий, у реєстрі немає")
    хвіст = ""
    if власник and вл_акт != acct:
        хвіст = (f"\n  ⚠ Meta це ДОЗВОЛИТЬ: обʼєкт видно з цього кабінету. "
                 f"Блокуємо МИ, бо клієнти не плутаються.\n"
                 f"  Саме так 29.09.2026 реклама Gasanova вийшла від Kaia "
                 f"Fincher на 85 тис. показів.")
    return False, (f"❌ {слово} НЕ ВІД ЦЬОГО КЛІЄНТА.\n"
                   f"  Кабінет: {acct} — {client_of(acct)}\n"
                   f"  {слово.capitalize()}: {oid}{опис}\n"
                   f"  Дозволені: {allowed or 'жодного'}{хвіст}\n"
                   f"  Якщо справді потрібно — правити metaads/clients.py свідомо.")


# тонкі обгортки, щоб виклики читались
def check_page(account_id, page_id):      return check_object(account_id, "page", page_id)
def check_pixel(account_id, pixel_id):    return check_object(account_id, "pixel", pixel_id)
def check_catalog(account_id, catalog_id):return check_object(account_id, "catalog", catalog_id)
def check_ig(account_id, ig_id):          return check_object(account_id, "ig", ig_id)

def catalogs_of(account_id):  return objects_of(account_id, "catalog")
def pixels_of(account_id):    return objects_of(account_id, "pixel")
def ig_of(account_id):        return objects_of(account_id, "ig")
