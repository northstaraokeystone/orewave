# OreWave v2: The Witness

> *The proof was always there. We just witness it.*

## CLAUDEME Laws

- **LAW_1**: Dual-hash integrity (SHA256:BLAKE3)
- **LAW_2**: Deterministic observation
- **LAW_3**: Zero side effects

## Pure Function Principles

- **Same inputs → Same outputs**: Identical claims always produce identical observations
- **No side effects**: No file writes, no prints, no network calls
- **No storage**: Hash space IS storage — the proof is encoded in geometry
- **No state**: Every observation is independent and complete

## Why No State

State is liability. Every mutable variable is a potential inconsistency. Every file write is a potential corruption. The pure function paradigm eliminates entire categories of bugs by construction. The claim's hash encodes its position in proof space. The sibling relationship emerges from geometric proximity. The merkle anchor crystallizes the witness. Storage is unnecessary because the proof is always recoverable from the claim itself.

## Why This Is Secure

Security emerges from mathematical certainty, not operational vigilance. Dual-hash prevents single-algorithm vulnerabilities. Determinism enables independent verification — any party can re-observe and confirm. The merkle anchor binds claim to context immutably. Tampering is detectable because re-observation produces different results than corrupted data. The proof cannot be forged because it was never manufactured — it was always there, waiting to be witnessed.

## Version Ladder

| Version | Paradigm | Storage | State |
|---------|----------|---------|-------|
| ore-city | Proof generation | Files | Mutable |
| OreReceipt v1 | Receipt emission | JSONL | Append-only |
| OreWave v1 | Wave compression | JSONL | Compressed |
| **OreWave v2** | **Witness observation** | **ZERO** | **ZERO** |

## API

```python
from orewave import dual_hash, observe, root

# Witness a claim
claim = {"id": "test", "value": 42}
observation = observe(claim, [claim])

# Compute merkle root
claims = [{"id": "a"}, {"id": "b"}]
merkle_root = root(claims)

# Hash anything
h = dual_hash("data")  # Returns "sha256:blake3"
```

## CLI

```bash
# Observe a claim
python orewave.py observe '{"id":"test"}' claims.json

# Compute merkle root
python orewave.py root claims.json

# Verify observation integrity
python orewave.py verify '{"claim":...}' claims.json
```

## Integration Points

- **QED telemetry**: Claims = compressed telemetry windows
- **ProofPack ledger**: Observations can be ingested as receipts
- **TruthLink packets**: merkle_anchor attachable to decision packets

---

*The marble already contained the angel.*
