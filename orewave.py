import hashlib, json, sys
try: import blake3
except ImportError: blake3 = None

def dual_hash(data):
    b = data.encode() if isinstance(data, str) else data
    sha = hashlib.sha256(b).hexdigest()
    return f"{sha}:{blake3.blake3(b).hexdigest() if blake3 else sha}"

def observe(claim, claims):
    ch = dual_hash(json.dumps(claim, sort_keys=True))
    hashes = [dual_hash(json.dumps(c, sort_keys=True)) for c in claims]
    hamming = lambda a, b: sum(x != y for x, y in zip(a, b))
    sibling = min((h for h in hashes if h != ch), key=lambda h: hamming(ch, h), default=ch)
    return {"claim": claim, "claim_hash": ch, "position": ch[:32], "sibling_hash": sibling, "merkle_anchor": dual_hash(ch + sibling)}

def root(claims):
    if not claims: return dual_hash(b'')
    hashes = [dual_hash(json.dumps(c, sort_keys=True)) for c in claims]
    while len(hashes) > 1:
        if len(hashes) % 2: hashes.append(hashes[-1])
        hashes = [dual_hash(hashes[i] + hashes[i+1]) for i in range(0, len(hashes), 2)]
    return hashes[0]

if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'observe': print(json.dumps(observe(json.loads(args[0]), json.load(open(args[1])))))
    elif cmd == 'root': print(root(json.load(open(args[0]))))
    elif cmd == 'verify': sys.exit(0 if observe(json.loads(args[0]), json.load(open(args[1]))) == json.loads(args[0]) else 1)
