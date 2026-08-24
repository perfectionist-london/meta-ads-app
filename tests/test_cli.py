"""End-to-end CLI behavior via subprocess (the student's first-contact paths)."""

import os
import subprocess
import sys

from metaads import __version__

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(APP_DIR, "meta_ads_cli.py")


def _run(*argv, token="your-long-lived-token-here"):
    """Run the CLI with placeholder credentials (dotenv never overrides os.environ)."""
    env = dict(os.environ)
    env["META_ACCESS_TOKEN"] = token
    env["META_AD_ACCOUNT_ID"] = "act_XXXXXXXXX"
    return subprocess.run(
        [sys.executable, CLI, *argv],
        capture_output=True, text=True, env=env, cwd=APP_DIR, timeout=60,
    )


def test_help_works_without_configured_env():
    r = _run("--help")
    assert r.returncode == 0
    assert "usage:" in r.stdout


def test_version_works_without_configured_env():
    r = _run("--version")
    assert r.returncode == 0
    assert __version__ in r.stdout


def test_subcommand_help_works_without_configured_env():
    r = _run("campaign-create", "--help")
    assert r.returncode == 0
    assert "--confirm" in r.stdout


def test_real_command_fails_cleanly_without_token():
    r = _run("campaigns")
    assert r.returncode == 1
    assert "META_ACCESS_TOKEN not set" in r.stderr
    assert "Traceback" not in r.stderr


def test_json_flag_suppresses_banner_noise():
    """Even the error path with --json must keep stdout empty (parseable)."""
    r = _run("campaigns", "--json")
    assert r.returncode == 1
    assert r.stdout.strip() == ""


# ---------------------------------------------------------------------------
# --status is level-aware: an ad set can be CAMPAIGN_PAUSED, an ad also
# ADSET_PAUSED. Listing only ACTIVE/PAUSED hides everything under a paused
# parent, which silently truncated config snapshots.
# ---------------------------------------------------------------------------

def test_ads_status_accepts_adset_paused():
    r = _run("ads", "--status", "ADSET_PAUSED", "--help")
    assert r.returncode == 0


def test_adsets_status_accepts_campaign_paused_list():
    r = _run("adsets", "--status", "ACTIVE,PAUSED,CAMPAIGN_PAUSED", "--help")
    assert r.returncode == 0


def test_adsets_status_rejects_ad_only_status():
    """ADSET_PAUSED is meaningless one level up — the error must say so."""
    r = _run("adsets", "--status", "ADSET_PAUSED")
    assert r.returncode != 0
    assert "'ADSET_PAUSED' is not a valid status here" in r.stderr
    assert "CAMPAIGN_PAUSED" in r.stderr


def test_campaigns_status_rejects_campaign_paused():
    r = _run("campaigns", "--status", "CAMPAIGN_PAUSED")
    assert r.returncode != 0
    assert "not a valid status here" in r.stderr


def test_status_error_names_only_the_bad_value():
    r = _run("ads", "--status", "ACTIVE,NONSENSE")
    assert r.returncode != 0
    assert "'NONSENSE' is not a valid status here" in r.stderr


def test_status_help_lists_the_statuses_for_that_level():
    r = _run("ads", "--help")
    assert "ADSET_PAUSED" in r.stdout
    r = _run("campaigns", "--help")
    assert "ADSET_PAUSED" not in r.stdout
