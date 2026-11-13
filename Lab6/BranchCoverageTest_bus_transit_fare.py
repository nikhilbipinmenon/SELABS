import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles

# =======================================================
# Branch Coverage Test Suite (Exhaustive Decision Matrix)
# =======================================================

# --- process_commute_manifest: Input Validation Branches ---

def test_branch_manifests_not_a_list():
    with pytest.raises(ValueError):
        process_commute_manifest(None, 5.0)
    with pytest.raises(ValueError):
        process_commute_manifest({"not": "a list"}, 5.0)

def test_branch_negative_booking_fee():
    with pytest.raises(ValueError):
        process_commute_manifest([], -0.01)

def test_branch_valid_input_passes():
    res = process_commute_manifest([], 0.0)
    assert res["status"] == "ZERO_RIDERSHIP"

# --- Route Active & Route Types Branches ---

def test_branch_inactive_route_skips():
    manifests = [
        {"route_active": False, "route_type": "express"},
        {"route_active": True, "route_type": "express", "commuters": []}
    ]
    res = process_commute_manifest(manifests, 0.0)
    assert res["status"] == "ZERO_RIDERSHIP"

def test_branch_route_type_express():
    manifests = [{
        "route_active": True,
        "route_type": "express",
        "commuters": [{"zones": 1, "type": "regular", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["total_fare"] == 7.0  # 6.0 + 1.0

def test_branch_route_type_shuttle():
    manifests = [{
        "route_active": True,
        "route_type": "shuttle",
        "commuters": [{"zones": 1, "type": "regular", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["total_fare"] == 5.0  # 4.0 + 1.0

def test_branch_route_type_local():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 1, "type": "regular", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["total_fare"] == 3.5  # 2.5 + 1.0

def test_branch_route_type_invalid_else():
    manifests = [
        {"route_active": True, "route_type": "unknown_metro", "commuters": []}
    ]
    res = process_commute_manifest(manifests, 0.0)
    assert res["status"] == "ZERO_RIDERSHIP"

# --- Commuter Zones & Concession Categories Branches ---

def test_branch_commuter_zones_negative_or_zero():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [
            {"zones": 0, "type": "regular", "blacklisted": False},
            {"zones": -1, "type": "regular", "blacklisted": False}
        ]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["status"] == "ZERO_RIDERSHIP"

def test_branch_blacklisted_on_express_breaks():
    manifests = [{
        "route_active": True,
        "route_type": "express",
        "commuters": [
            {"zones": 2, "type": "regular", "blacklisted": True},
            {"zones": 2, "type": "regular", "blacklisted": False}
        ]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["total_fare"] == 0.0
    assert res["status"] == "ZERO_RIDERSHIP"

def test_branch_blacklisted_on_non_express_continues():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [
            {"zones": 1, "type": "regular", "blacklisted": True},
            {"zones": 1, "type": "regular", "blacklisted": False}
        ]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["total_fare"] == 3.5  # 2nd commuter counted

def test_branch_passenger_type_student():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 2, "type": "student", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 0.0)
    # (2.5 + (2 * 0.5)) * 0.50 = 3.5 * 0.5 = 1.75
    assert res["total_fare"] == 1.75

def test_branch_passenger_type_senior():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 2, "type": "senior", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 0.0)
    # (2.5 + (2 * 0.5)) * 0.70 = 3.5 * 0.7 = 2.45
    assert res["total_fare"] == 2.45

def test_branch_priority_boarding_true_and_false():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "priority_boarding": True,
            "commuters": [{"zones": 1, "type": "regular", "blacklisted": False}]
        },
        {
            "route_active": True,
            "route_type": "local",
            "priority_boarding": False,
            "commuters": [{"zones": 1, "type": "regular", "blacklisted": False}]
        }
    ]
    res = process_commute_manifest(manifests, 3.0)
    # Manifest 1: 3.5 + 3.0 = 6.5. Manifest 2: 3.5. Total: 10.0
    assert res["total_fare"] == 10.0

# --- Audit & Status Branches ---

def test_branch_status_audit_rejected():
    manifests = [
        {"route_active": True, "route_type": "bad_route_1"},
        {"route_active": True, "route_type": "bad_route_2"},
        {"route_active": True, "route_type": "bad_route_3"},
        {"route_active": True, "route_type": "bad_route_4"},
        {"route_active": True, "route_type": "bad_route_5"},
    ]
    res = process_commute_manifest(manifests, 0.0)
    assert res["status"] == "AUDIT_REJECTED"

def test_branch_status_zero_ridership():
    res = process_commute_manifest([], 0.0)
    assert res["status"] == "ZERO_RIDERSHIP"
    assert res["total_fare"] == 0.0

def test_branch_status_completed():
    manifests = [{
        "route_active": True,
        "route_type": "local",
        "commuters": [{"zones": 1, "type": "regular", "blacklisted": False}]
    }]
    res = process_commute_manifest(manifests, 0.0)
    assert res["status"] == "COMPLETED"
    assert res["total_fare"] == 3.5

# --- inspect_smartcard_turnstiles: Branches ---

def test_branch_turnstiles_no_data():
    assert inspect_smartcard_turnstiles(None) == "NO_DATA"
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"

def test_branch_turnstiles_jam():
    # Streak reaching >= 2
    assert inspect_smartcard_turnstiles([[5, 4]]) == "TURNSTILE_JAM"

def test_branch_turnstiles_streak_reset():
    # Reading <= 3 resets streak
    assert inspect_smartcard_turnstiles([[5, 1, 5, 2]]) == "OPERATIONAL"

def test_branch_turnstiles_multiple_devices_operational():
    assert inspect_smartcard_turnstiles([[1, 2], [3, 0], [2, 1]]) == "OPERATIONAL"
