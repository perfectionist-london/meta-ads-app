"""Product-catalogue commands: scope guard, filter validation, dry-run contracts."""

import json
from argparse import Namespace

import pytest

from metaads import api
from metaads.commands import catalog


def _scopes(monkeypatch, *scopes):
    monkeypatch.setattr(api, "_api_call",
                        lambda *a, **k: {"data": {"scopes": list(scopes)}})


def _create_args(**kw):
    base = dict(catalog_id="123", name="Футболки",
                filter='{"product_type": {"i_contains": "T-Shirt"}}',
                confirm=False, json=True)
    base.update(kw)
    return Namespace(**base)


# ---------------------------------------------------------------------------
# Scope guard — Meta's own error for a missing scope says nothing useful
# ---------------------------------------------------------------------------

def test_missing_catalog_scope_explains_instead_of_error_100(monkeypatch, capsys):
    _scopes(monkeypatch, "ads_management", "ads_read")
    with pytest.raises(SystemExit):
        catalog._require_catalog_scope()
    err = capsys.readouterr().err
    assert "catalog_management" in err
    assert "ads_management, ads_read" in err          # names what the token does have
    assert "App Review is not required" in err
    assert "Traceback" not in err


def test_catalog_scope_present_passes(monkeypatch):
    _scopes(monkeypatch, "ads_management", "catalog_management")
    catalog._require_catalog_scope()                   # must not raise


# ---------------------------------------------------------------------------
# product-set-create
# ---------------------------------------------------------------------------

def test_product_set_create_rejects_non_object_filter(monkeypatch, capsys):
    _scopes(monkeypatch, "catalog_management")
    with pytest.raises(SystemExit):
        catalog.cmd_product_set_create(_create_args(filter='["T-Shirt"]'))
    assert "--filter must be a non-empty JSON object" in capsys.readouterr().err


def test_product_set_create_rejects_empty_filter(monkeypatch, capsys):
    _scopes(monkeypatch, "catalog_management")
    with pytest.raises(SystemExit):
        catalog.cmd_product_set_create(_create_args(filter="{}"))
    assert "non-empty JSON object" in capsys.readouterr().err


def test_product_set_create_dry_run_writes_nothing(monkeypatch, capsys):
    _scopes(monkeypatch, "catalog_management")
    monkeypatch.setattr(api, "_paginate", lambda *a, **k: [{"id": "1"}, {"id": "2"}])
    writes = []

    def fake_call(method, path, params=None, **k):
        if path == "debug_token":
            return {"data": {"scopes": ["catalog_management"]}}
        writes.append(method)
        return {}

    monkeypatch.setattr(api, "_api_call", fake_call)
    catalog.cmd_product_set_create(_create_args())
    out = json.loads(capsys.readouterr().out)
    assert out["executed"] is False
    assert out["would_create"]["matched_preview"] == 2
    assert writes == []                                # no POST without --confirm


def test_product_set_create_warns_when_filter_matches_nothing(monkeypatch, capsys):
    """An empty set is accepted by the API and then delivers nothing at all."""
    _scopes(monkeypatch, "catalog_management")
    monkeypatch.setattr(api, "_paginate", lambda *a, **k: [])
    catalog.cmd_product_set_create(_create_args(json=False))
    assert "WARNING: the filter matches nothing" in capsys.readouterr().out


def test_product_set_create_confirm_posts_filter_as_json(monkeypatch, capsys):
    _scopes(monkeypatch, "catalog_management")
    monkeypatch.setattr(api, "_paginate", lambda *a, **k: [{"id": "1"}])
    seen = {}

    def fake_call(method, path, params=None, **k):
        if path == "debug_token":
            return {"data": {"scopes": ["catalog_management"]}}
        seen["method"], seen["path"], seen["params"] = method, path, params
        return {"id": "999"}

    monkeypatch.setattr(api, "_api_call", fake_call)
    catalog.cmd_product_set_create(_create_args(confirm=True))
    out = json.loads(capsys.readouterr().out)
    assert out["executed"] is True and out["product_set_id"] == "999"
    assert seen["method"] == "POST"
    assert seen["path"] == "123/product_sets"
    assert json.loads(seen["params"]["filter"]) == {"product_type": {"i_contains": "T-Shirt"}}


def test_product_set_create_filter_keeps_cyrillic_readable(monkeypatch, capsys):
    """ensure_ascii would turn 'Футболка' into \\u0424... in the stored filter."""
    _scopes(monkeypatch, "catalog_management")
    monkeypatch.setattr(api, "_paginate", lambda *a, **k: [{"id": "1"}])
    seen = {}

    def fake_call(method, path, params=None, **k):
        if path == "debug_token":
            return {"data": {"scopes": ["catalog_management"]}}
        seen["params"] = params
        return {"id": "1"}

    monkeypatch.setattr(api, "_api_call", fake_call)
    catalog.cmd_product_set_create(
        _create_args(confirm=True, filter='{"product_type": {"i_contains": "Футболка"}}'))
    assert "Футболка" in seen["params"]["filter"]
