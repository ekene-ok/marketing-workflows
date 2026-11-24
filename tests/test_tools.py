"""Tests for the deterministic checks that keep AI-written marketing copy safe to use."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check_copy import check_variant
from tools.common import approved_claims
from tools.verify_numbers import verify
from tools.audit_page import audit
from tools.campaign_anomalies import facts

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = approved_claims()


def v(fmt, **fields):
    return {"id": "t", "format": fmt, "fields": fields}


def test_clean_copy_passes():
    assert check_variant(v("linkedin", intro="Clients upload documents through a secure portal. SOC 2 Type II certified.",
                           headline="Stop chasing clients this busy season"), ALLOWED) == []


def test_length_limit_enforced():
    probs = check_variant(v("paid_search", headline="Stop chasing clients for documents this season"), ALLOWED)
    assert any("limit 30" in p for p in probs)


def test_banned_word_and_invented_number_caught():
    probs = check_variant(v("linkedin", intro="A revolutionary portal that saves 10 hours a week.", headline="Try it"), ALLOWED)
    assert any("revolutionary" in p for p in probs) and any("unapproved number: 10" in p for p in probs)


def test_security_and_ai_wording_rules():
    probs = check_variant(v("in_app", title="Secure AI document sorting", body="Fully automated.", button="Try it"), ALLOWED)
    assert any("SOC 2 Type II" in p for p in probs)
    assert any("AI-assisted" in p for p in probs)
    assert any("overstates automation" in p for p in probs)


def test_dash_and_exclamation_caught():
    probs = check_variant(v("in_app", title="New feature!", body="Faster intake \u2014 for you", button="See it"), ALLOWED)
    assert any("exclamation" in p for p in probs) and any("dash" in p for p in probs)


def test_verify_numbers_flags_untraceable():
    assert verify("Spend was 1,678.03 and CPC rose 89.1%", {"spend": 1678.03, "change": 89.1}) == []
    assert verify("CPC rose 95%", {"change": 89.1}) == ["95"]


def test_page_audit_finds_planted_problems():
    f = audit(ROOT / "inputs/landing_page_client_portal.md", ROOT / "inputs/brief_client_portal_tax_season.md")
    assert f["message_match_share"] < 0.5 and f["distinct_ctas"] == 3 and f["form_fields"] == 9
    assert "revolutionary" in f["banned_words_found"]


def test_anomalies_catch_both_planted_problems():
    f = facts(ROOT / "inputs/campaign_daily_metrics.csv")
    flagged = {(a["campaign"], a["metric"]) for a in f["anomalies"]}
    assert ("LinkedIn | Client Portal cross-sell", "cpc") in flagged
    assert ("Search | Practice management software", "conversions") in flagged


def test_approved_number_cannot_be_reused_in_a_new_claim():
    ok = check_variant(v("linkedin", intro="Firms using Client Portal collect documents 4 days faster.",
                         headline="Turn on Client Portal free until April 30"), ALLOWED)
    assert ok == []
    probs = check_variant(v("linkedin", intro="Save 4 hours a week. Trusted by 92% of firms.", headline="Try it"), ALLOWED)
    assert sum("unapproved number" in p for p in probs) == 2


def test_number_written_in_words_caught():
    probs = check_variant(v("linkedin", intro="Save ten hours a week, twice as fast.", headline="Try it"), ALLOWED)
    assert sum("number written in words" in p for p in probs) == 2
