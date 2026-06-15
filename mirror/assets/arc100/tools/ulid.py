#!/usr/bin/env python3
"""ARC-100-SYNC/scripts/ulid.py — self-contained ULID generator.

ULID format (per github.com/ulid/spec):
  - 10 chars timestamp (ms since Unix epoch, Crockford base32 big-endian)
  - 16 chars cryptographic randomness (80 bits)
  - Total 26 chars, URL-safe, monotonically sortable by creation time.

Used by ARC-100 and every downstream <PROJECT>-100 to assign a stable identity
to each book and chapter entry in the index. Once generated, a ULID never
changes — slot numbers, titles, and descriptions can mutate freely, but the
ULID is the canonical "is this the same entry?" key across upstream releases
and across projects.

Usage as a CLI:
    python3 ulid.py              # one ULID to stdout
    python3 ulid.py --count 170  # 170 ULIDs, newline-separated

Usage as a library:
    from ulid import generate_ulid
    id = generate_ulid()

Why Python: ARC-100-SYNC is implemented in Python because the mkdocs site that
hosts ARC-100's chapters is already a Python tool — using the same runtime for
the synchronization tooling avoids a second language dependency on downstream
machines. See chapter 00-05 §00-05.7 (Runtime composition).
"""
from __future__ import annotations

import argparse
import secrets
import sys
import time

# Crockford base32 — 32 chars, omits I L O U
_ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_ENCODING_LEN = len(_ENCODING)
_TIME_LEN = 10
_RANDOM_LEN = 16
_TIME_MAX = (1 << 48) - 1  # 281474976710655 — max ms timestamp ULID can encode


def _encode_time(now_ms: int, length: int = _TIME_LEN) -> str:
    if now_ms < 0:
        raise ValueError("ULID timestamp must be non-negative")
    if now_ms > _TIME_MAX:
        raise ValueError("ULID timestamp overflow (exceeds 2^48 - 1 ms)")
    chars = []
    n = now_ms
    for _ in range(length):
        chars.append(_ENCODING[n % _ENCODING_LEN])
        n //= _ENCODING_LEN
    return "".join(reversed(chars))


def _encode_random(length: int = _RANDOM_LEN) -> str:
    # Mask each byte to its lower 5 bits — uniformly random over [0, 31],
    # which maps directly onto the 32-char Crockford alphabet. We waste
    # 3 bits per byte but every emitted char is cryptographically uniform.
    raw = secrets.token_bytes(length)
    return "".join(_ENCODING[b & 0x1F] for b in raw)


def generate_ulid() -> str:
    """Return a fresh 26-character ULID."""
    return _encode_time(int(time.time() * 1000)) + _encode_random()


def _cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="ulid.py",
        description="Emit one or more ULIDs (26-char Crockford base32, time-ordered).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Emit N ULIDs, newline-separated. Default: 1.",
    )
    args = parser.parse_args(argv)
    if args.count < 1:
        parser.error("--count must be a positive integer")
    for _ in range(args.count):
        sys.stdout.write(generate_ulid() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
