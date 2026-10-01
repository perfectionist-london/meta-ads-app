"""Жорстка прив'язка рекламних кабінетів до сторінок.

Причина існування: 29.09.2026 реклама бутіка Gasanova вийшла в ефір від
імені kaia_fincher — 85 тис. показів під чужим брендом. Сталось тому, що
META_PAGE_ID у .env вказував на сторінку Kaia, а кабінет передавався
окремо через --account-id. Кабінет одного клієнта, сторінка іншого, і
ніщо про це не попереджало.

Тепер сторінку треба передавати явно, і вона звіряється з кабінетом.
Кабінети НЕ ПЛУТАЮТЬСЯ НІКОЛИ.
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
    },
    "act_1731887314115067": {
        "client": "Kaia Fincher",
        "pages": {
            "558580180666271": "Kaia Fincher — FB @kaiafincher",
        },
    },
}


# Сторінки, дозволені лише за умови. Ключ → текст умови, який показуємо
# щоразу, коли сторінку використовують. Пропускаємо, але не мовчки.
CONDITIONAL = {
    "103029658977853":
        "⚠ Сторінка Ельвіри дозволена ТІЛЬКИ для колаб-постів, де Gasanova "
        "співавтор.\n"
        "  Відкрий прев'ю оголошення і переконайся, що підпис — "
        "«Elvira Gasanova and Gasanova».\n"
        "  Сольна реклама з її акаунту — ні. Через API співавторства не "
        "видно, тільки прев'ю.",
}


# Мертві сторінки з історії кабінету. У реєстр НЕ входять — з них нічого
# не можна вмикати. Тут вони лише для того, щоб помилка пояснювала, що це,
# і ніхто не витрачав час на повторне розслідування.
RETIRED = {
    "114821090352654":
        "«Gasanova Boutique временный» — стара тимчасова сторінка бренду "
        "(1 підписник, 0 постів). 50 креативів 2021 року.",
    "687420154798529":
        "«Elvira Gasanova» (Personal blog, 15 підписників) — СТАРА сторінка "
        "Ельвіри, не та, що в реєстрі. 2 креативи 2019 року.",
}


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
