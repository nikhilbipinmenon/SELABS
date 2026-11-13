import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles

# ==========================================
# Code Coverage Test Suite (Line Coverage)
# ==========================================

def test_manifest_not_list():
    with pytest.raises(ValueError, match="Invalid manifests list or booking fee"):
        process_commute_manifest("not_a_list", 1.0)

def test_negative_booking_fee():
    with pytest.raises(ValueError, match="Invalid manifests list or booking fee"):
        process_commute_manifest([], -5.0)

def test_inactive_route():
    manifests = [{"route_active": False}]
    res = process_commute_manifest(manifests, 1.0)
    assert res["status"] == "ZERO_RIDERSHIP"
    assert res["total_fare"] == 0.0

def test_route_types_and_commuters():
    # Shuttle with student and priority boarding
    m_shuttle = {
        "route_active": True,
        "route_type": "shuttle",
        "priority_boarding": True,
        "commuters": [
            {"zones": 2, "type": "student", "blacklisted": False}
        ]
    }
    # Local with senior
    m_local = {
        "route_active": True,
        "route_type": "local",
        "priority_boarding": False,
        "commuters": [
            {"zones": 2, "type": "senior", "blacklisted": False}
        ]
    }
    # Express with regular
    m_express = {
        "route_active": True,
        "route_type": "express",
        "priority_boarding": False,
        "commuters": [
            {"zones": 2, "type": "regular", "blacklisted": False}
        ]
    }
    res = process_commute_manifest([m_shuttle, m_local, m_express], 2.0)
    assert res["status"] == "COMPLETED"
    assert res["total_fare"] > 0

def test_unknown_route_type():
    manifests = [{"route_active": True, "route_type": "hyperloop", "commuters": []}]
    res = process_commute_manifest(manifests, 1.0)
    assert res["status"] == "ZERO_RIDERSHIP"

def test_invalid_zones():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 0, "type": "regular", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 1.0)
    assert res["status"] == "ZERO_RIDERSHIP"

def test_blacklisted_card_non_express():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 2, "type": "regular", "blacklisted": True}]
    }]
    res = process_commute_manifest(manifests, 1.0)
    assert res["status"] == "ZERO_RIDERSHIP"

def test_blacklisted_card_express_breaks():
    manifests = [{
        "route_active": True,
        "route_type": "express",
        "commuters": [
            {"zones": 2, "type": "regular", "blacklisted": True},
            {"zones": 2, "type": "regular", "blacklisted": False}
        ]
    }]
    res = process_commute_manifest(manifests, 1.0)
    assert res["status"] == "ZERO_RIDERSHIP"

def test_audit_rejected():
    # Trigger rejected_rides > 4
    manifests = [
        {"route_active": True, "route_type": "invalid_1"},
        {"route_active": True, "route_type": "invalid_2"},
        {"route_active": True, "route_type": "invalid_3"},
        {"route_active": True, "route_type": "invalid_4"},
        {"route_active": True, "route_type": "invalid_5"},
    ]
    res = process_commute_manifest(manifests, 1.0)
    assert res["status"] == "AUDIT_REJECTED"

def test_turnstiles_empty():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"
    assert inspect_smartcard_turnstiles(None) == "NO_DATA"

def test_turnstiles_jam():
    # Consecutive failures > 3
    matrix = [[4, 5, 2]]
    assert inspect_smartcard_turnstiles(matrix) == "TURNSTILE_JAM"

def test_turnstiles_operational():
    # Streak resets on failures <= 3
    matrix = [[4, 2, 4, 1]]
    assert inspect_smartcard_turnstiles(matrix) == "OPERATIONAL"
