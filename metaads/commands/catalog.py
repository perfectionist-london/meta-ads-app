"""Commands: catalogs, product-sets, product-set-create, catalog-products.

Product catalogues live outside the ad account: a catalogue belongs to the
*business*, and a product set is a saved filter over it. Dynamic ads point at a
product set through the ad set's promoted_object.product_set_id, which is why a
catalogue-driven ad cannot be assembled with ads_management alone.

Everything here needs the `catalog_management` scope. It is not part of the
default ads token, so `metaads catalogs` on a normal token fails with a bare
"(#100) This application has not been approved to use this api" — which says
nothing about the missing permission. _require_catalog_scope() checks the token
first and explains what to do instead.
"""

from __future__ import annotations

import json
import sys

from metaads import api, clients
from metaads.commands.common import account_of, parse_json_arg
from metaads.formatting import _die, _output_json, _truncate

CATALOG_FIELDS = "id,name,product_count,vertical,business{id,name}"
PRODUCT_SET_FIELDS = "id,name,product_count,filter,auto_creation_url"
PRODUCT_FIELDS = ("id,retailer_id,name,product_type,availability,visibility,"
                  "price,sale_price,url,brand")

CATALOG_SCOPE = "catalog_management"


def _require_catalog_scope() -> None:
    """Fail with instructions rather than Meta's opaque #100."""
    data = api._api_call("GET", "debug_token", {"input_token": api.META_ACCESS_TOKEN})
    scopes = (data.get("data") or {}).get("scopes") or []
    if CATALOG_SCOPE in scopes:
        return
    _die(
        f"ERROR: the token has no '{CATALOG_SCOPE}' scope, so catalogues are unreadable.\n"
        f"  Current scopes: {', '.join(scopes) or '(none)'}\n"
        "  Fix: reissue the token with catalog_management added, then put it in .env\n"
        "  (Graph API Explorer -> Add a Permission -> catalog_management -> Generate,\n"
        "  then `metaads token-extend` for a long-lived one).\n"
        "  App Review is not required while you have a role on the app."
    )


def _businesses() -> list:
    return api._paginate("me/businesses", {"fields": "id,name", "limit": 50}, max_items=50)


def cmd_catalogs(args) -> None:
    """List product catalogues across the businesses this user can see."""
    _require_catalog_scope()
    rows = []
    for biz in _businesses():
        got = api._paginate(f"{biz['id']}/owned_product_catalogs",
                            {"fields": CATALOG_FIELDS, "limit": 50}, max_items=50)
        for c in got:
            c.setdefault("business", {"id": biz["id"], "name": biz.get("name")})
            # ⛔ список віддає і ЧУЖІ каталоги. 02.10.2026 я взяв [0] і це був
            # umahanova.com. Позначаємо явно, щоб індекс не вибирався наосліп.
            чий = clients.FOREIGN_CATALOGS.get(str(c.get("id")))
            if чий:
                c["name"] = f"⛔ ЧУЖИЙ: {c.get('name')}"
            rows.append(c)

    if args.json:
        _output_json(rows)
        return
    if not rows:
        print("No catalogues found (check that the user has a role on the business).")
        return
    print(f"{'ID':<20} {'Name':<34} {'Products':>9}  Business")
    print("-" * 92)
    for c in rows:
        print(f"{c['id']:<20} {_truncate(c.get('name'), 32):<34} "
              f"{c.get('product_count', '---'):>9}  {(c.get('business') or {}).get('name', '---')}")


def cmd_product_sets(args) -> None:
    """List product sets in a catalogue."""
    ok, msg = clients.check_catalog(account_of(args), args.catalog_id)
    if msg:
        print(msg, file=sys.stderr)
    if not ok:
        raise SystemExit(2)
    _require_catalog_scope()
    sets_ = api._paginate(f"{args.catalog_id}/product_sets",
                          {"fields": PRODUCT_SET_FIELDS, "limit": args.limit},
                          max_items=args.limit)
    if args.json:
        _output_json(sets_)
        return
    if not sets_:
        print("No product sets in this catalogue.")
        return
    print(f"{'ID':<20} {'Name':<34} {'Products':>9}  Filter")
    print("-" * 110)
    for s in sets_:
        filt = json.dumps(s.get("filter"), ensure_ascii=False) if s.get("filter") else "(all)"
        print(f"{s['id']:<20} {_truncate(s.get('name'), 32):<34} "
              f"{s.get('product_count', '---'):>9}  {_truncate(filt, 40)}")


def cmd_catalog_products(args) -> None:
    """List products, optionally through a filter — dry-run a set before creating it."""
    ok, msg = clients.check_catalog(account_of(args), args.catalog_id)
    if msg:
        print(msg, file=sys.stderr)
    if not ok:
        raise SystemExit(2)
    _require_catalog_scope()
    params = {"fields": PRODUCT_FIELDS, "limit": args.limit}
    if args.filter:
        params["filter"] = json.dumps(parse_json_arg(args.filter, "--filter"),
                                      ensure_ascii=False)
    products = api._paginate(f"{args.catalog_id}/products", params, max_items=args.limit)

    if args.json:
        _output_json(products)
        return
    print(f"matched: {len(products)}")
    if not products:
        return
    print(f"{'retailer_id':<22} {'Name':<40} {'Type':<16} {'Avail':<14} Price")
    print("-" * 108)
    for p in products:
        print(f"{_truncate(p.get('retailer_id'), 20):<22} {_truncate(p.get('name'), 38):<40} "
              f"{_truncate(p.get('product_type'), 14):<16} "
              f"{_truncate(p.get('availability'), 12):<14} {p.get('price', '---')}")


def cmd_product_set_create(args) -> None:
    """Create a product set from a filter.

    The filter is Meta's product-set syntax, not a query string, e.g.
      '{"product_type": {"i_contains": "T-Shirt"}}'
      '{"and": [{"brand": {"eq": "GASANOVA"}}, {"availability": {"eq": "in stock"}}]}'
    Check it with `catalog-products --filter` first: an empty set is accepted by
    the API and then silently delivers nothing.
    """
    ok, msg = clients.check_catalog(account_of(args), args.catalog_id)
    if msg:
        print(msg, file=sys.stderr)
    if not ok:
        raise SystemExit(2)
    _require_catalog_scope()
    filt = parse_json_arg(args.filter, "--filter")
    if not isinstance(filt, dict) or not filt:
        _die("ERROR: --filter must be a non-empty JSON object, e.g.\n"
             '  --filter \'{"product_type": {"i_contains": "T-Shirt"}}\'')

    matched = api._paginate(f"{args.catalog_id}/products",
                            {"fields": "id", "filter": json.dumps(filt, ensure_ascii=False),
                             "limit": 100}, max_items=100)
    plan = {"catalog_id": str(args.catalog_id), "name": args.name,
            "filter": filt, "matched_preview": len(matched)}

    if not args.confirm:
        if args.json:
            _output_json({"executed": False, "would_create": plan,
                          "note": "Add --confirm to execute."})
            return
        print(f"DRY-RUN: would create product set \"{args.name}\" in {args.catalog_id}.")
        print("  Filter:  " + json.dumps(filt, ensure_ascii=False))
        print(f"  Matches: {len(matched)}" + (" (first 100 checked)" if len(matched) == 100 else ""))
        if not matched:
            print("  WARNING: the filter matches nothing — the set would be empty.")
        print("Add --confirm to execute.")
        return

    data = api._api_call("POST", f"{args.catalog_id}/product_sets",
                         {"name": args.name, "filter": json.dumps(filt, ensure_ascii=False)})
    result = {"executed": True, "product_set_id": data.get("id"), "name": args.name,
              "filter": filt, "matched_preview": len(matched)}
    if args.json:
        _output_json(result)
    else:
        print(f"Product set created: ID {data.get('id')} (\"{args.name}\", "
              f"~{len(matched)} products matched).")
