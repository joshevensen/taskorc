from app.core.auth import generate_pat, hash_pat, verify_pat


def test_generate_pat_format():
    pat = generate_pat()
    assert pat.startswith("orc_")
    # orc_ prefix + 64 hex chars
    assert len(pat) == len("orc_") + 64


def test_generate_pat_is_unique():
    assert generate_pat() != generate_pat()


def test_hash_verify_roundtrip():
    pat = generate_pat()
    hashed = hash_pat(pat)
    assert verify_pat(pat, hashed) is True


def test_verify_wrong_token():
    pat = generate_pat()
    hashed = hash_pat(pat)
    wrong = generate_pat()
    assert verify_pat(wrong, hashed) is False


def test_verify_never_raises():
    # Malformed hash should return False, not raise
    assert verify_pat("orc_anything", "not-a-valid-hash") is False
