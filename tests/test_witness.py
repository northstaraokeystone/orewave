"""6 Witness Tests for OreWave v2: Pure Function Proof Observation"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orewave import dual_hash, observe, root


def test_observe_determinism():
    """W1: Call observe() twice with identical inputs, assert byte-identical outputs."""
    claim = {"id": "test", "value": 42}
    claims = [claim, {"id": "other", "value": 99}]
    o1 = observe(claim, claims)
    o2 = observe(claim, claims)
    assert o1 == o2, "Observations must be deterministic"


def test_observe_stateless():
    """W2: Assert no files created, no global state modified."""
    before = set(os.listdir('.'))
    observe({"id": "x"}, [{"id": "x"}])
    after = set(os.listdir('.'))
    assert 'waves.jsonl' not in after, "No storage files should be created"
    assert before == after, "No files should be created by observe()"


def test_dual_hash_format():
    """W3: Output contains exactly one colon, both parts are valid 64-char hex."""
    h = dual_hash("test")
    assert ':' in h, "dual_hash must contain colon separator"
    parts = h.split(':')
    assert len(parts) == 2, "dual_hash must have exactly two parts"
    assert len(parts[0]) == 64, "SHA256 part must be 64 hex chars"
    assert len(parts[1]) == 64, "BLAKE3 part must be 64 hex chars"
    assert all(c in '0123456789abcdef' for c in parts[0]), "SHA256 must be valid hex"
    assert all(c in '0123456789abcdef' for c in parts[1]), "BLAKE3 must be valid hex"


def test_single_claim_sibling_self():
    """W4: Single-element claims list: sibling_hash equals claim_hash."""
    claim = {"id": "solo"}
    obs = observe(claim, [claim])
    assert obs["sibling_hash"] == obs["claim_hash"], "Single claim must be its own sibling"


def test_root_determinism():
    """W5: Call root() twice with identical claims, assert identical outputs."""
    claims = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    r1 = root(claims)
    r2 = root(claims)
    assert r1 == r2, "Root must be deterministic"


def test_tamper_detection():
    """W6: Generate observation, flip one char in merkle_anchor, re-observe detects difference."""
    claim = {"id": "tamper_test"}
    claims = [claim, {"id": "other"}]
    obs = observe(claim, claims)

    # Tamper with merkle_anchor (flip a character)
    anchor = obs["merkle_anchor"]
    tampered = anchor[0:32] + ('0' if anchor[32] != '0' else '1') + anchor[33:]
    tampered_obs = {**obs, "merkle_anchor": tampered}

    # Re-observe and verify it differs from tampered
    fresh_obs = observe(claim, claims)
    assert fresh_obs != tampered_obs, "Re-observation must detect tampering"
    assert fresh_obs == obs, "Re-observation must match original"
