"""Shared command-line renderer for account usage helpers."""

from __future__ import annotations

import sys
from typing import Sequence

from agent.account_usage import fetch_account_usage, render_account_usage_lines


PROVIDER_ALIASES = {
    "anthropic": "anthropic",
    "claude": "anthropic",
    "claude-usage": "anthropic",
    "claude_usage": "anthropic",
    "codex": "openai-codex",
    "codex-usage": "openai-codex",
    "codex_usage": "openai-codex",
    "openai-codex": "openai-codex",
    "openrouter": "openrouter",
    "openrouter-balance": "openrouter",
    "openrouter_balance": "openrouter",
}


def _usage() -> str:
    choices = ", ".join(sorted(PROVIDER_ALIASES))
    return f"usage: account-usage <provider>\nproviders: {choices}"


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if len(args) != 1 or args[0] in {"-h", "--help"}:
        print(_usage(), file=sys.stderr)
        return 2

    requested = args[0].strip().lower()
    provider = PROVIDER_ALIASES.get(requested)
    if not provider:
        print(f"unknown provider: {requested}", file=sys.stderr)
        print(_usage(), file=sys.stderr)
        return 2

    snapshot = fetch_account_usage(provider)
    if snapshot is None:
        print(f"Usage unavailable for {provider}: no configured credentials found.", file=sys.stderr)
        return 1

    lines = render_account_usage_lines(snapshot)
    if not lines:
        print(f"Usage unavailable for {provider}: provider returned no displayable data.", file=sys.stderr)
        return 1

    print("\n".join(lines))
    return 0 if not snapshot.unavailable_reason else 1


if __name__ == "__main__":
    raise SystemExit(main())
