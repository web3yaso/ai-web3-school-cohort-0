"""
Web3 Tool Use minimal practice.

This script mocks read tools, transaction drafting, policy checks, and trace logs.
It never connects to a real RPC endpoint and never sends a transaction.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
SUPPORTED_CHAINS = {1: "Ethereum", 8453: "Base"}
MAX_UINT256 = 2**256 - 1


POLICY = {
    "allowed_chain_ids": {1, 8453},
    "allowed_methods": {"approve"},
    "allowed_tokens": {"0x1111111111111111111111111111111111111111"},
    "allowed_spenders": {"0x2222222222222222222222222222222222222222"},
    "max_amount_raw": 10_000_000,
    "requires_simulation": True,
    "requires_user_confirmation": True,
    "deny_infinite_approve": True,
}


MOCK_BALANCES = {
    (8453, "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"): 250000000000000000,
}

MOCK_ALLOWANCES = {
    (
        8453,
        "0x1111111111111111111111111111111111111111",
        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "0x2222222222222222222222222222222222222222",
    ): 0,
}


@dataclass
class ToolTrace:
    timestamp: str
    user_goal: str
    tool_name: str
    chain_id: int
    input: dict[str, Any]
    output: dict[str, Any] | None
    error: str | None
    block_number: str
    policy_decision: str
    confirmed_by_user: bool
    tx_hash: str | None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_address(address: str) -> None:
    if not ADDRESS_RE.match(address):
        raise ValueError("invalid_address")


def record_trace(
    *,
    user_goal: str,
    tool_name: str,
    chain_id: int,
    tool_input: dict[str, Any],
    output: dict[str, Any] | None = None,
    error: str | None = None,
    policy_decision: str = "not_required",
    confirmed_by_user: bool = False,
    tx_hash: str | None = None,
) -> ToolTrace:
    return ToolTrace(
        timestamp=now_iso(),
        user_goal=user_goal,
        tool_name=tool_name,
        chain_id=chain_id,
        input=tool_input,
        output=output,
        error=error,
        block_number="mock-latest",
        policy_decision=policy_decision,
        confirmed_by_user=confirmed_by_user,
        tx_hash=tx_hash,
    )


def get_eth_balance(chain_id: int, address: str) -> dict[str, Any]:
    validate_address(address)
    if chain_id not in SUPPORTED_CHAINS:
        raise ValueError("unsupported_chain")

    balance_wei = MOCK_BALANCES.get((chain_id, address.lower()), 0)
    return {
        "chain_id": chain_id,
        "address": address,
        "block_number": "mock-latest",
        "balance_wei": str(balance_wei),
        "balance_eth": f"{balance_wei / 10**18:.6f}",
    }


def read_erc20_allowance(
    chain_id: int, token: str, owner: str, spender: str
) -> dict[str, Any]:
    for address in (token, owner, spender):
        validate_address(address)
    if chain_id not in SUPPORTED_CHAINS:
        raise ValueError("unsupported_chain")

    key = (chain_id, token.lower(), owner.lower(), spender.lower())
    return {
        "chain_id": chain_id,
        "token": token,
        "owner": owner,
        "spender": spender,
        "allowance_raw": str(MOCK_ALLOWANCES.get(key, 0)),
        "block_number": "mock-latest",
    }


def draft_erc20_approve(
    chain_id: int, token: str, spender: str, amount_raw: int
) -> dict[str, Any]:
    for address in (token, spender):
        validate_address(address)
    if amount_raw <= 0:
        raise ValueError("invalid_amount")

    calldata_seed = f"approve({spender},{amount_raw})".encode().hex()
    return {
        "chain_id": chain_id,
        "to": token,
        "method": "approve",
        "args": [spender, str(amount_raw)],
        "calldata": "0x" + calldata_seed[:64],
        "requires_user_confirmation": True,
    }


def policy_check(draft: dict[str, Any]) -> tuple[bool, str]:
    chain_id = draft["chain_id"]
    token = draft["to"].lower()
    spender = draft["args"][0].lower()
    amount_raw = int(draft["args"][1])

    if chain_id not in POLICY["allowed_chain_ids"]:
        return False, "unsupported_chain"
    if draft["method"] not in POLICY["allowed_methods"]:
        return False, "method_not_allowed"
    if token not in POLICY["allowed_tokens"]:
        return False, "token_not_allowed"
    if spender not in POLICY["allowed_spenders"]:
        return False, "spender_not_allowed"
    if POLICY["deny_infinite_approve"] and amount_raw == MAX_UINT256:
        return False, "infinite_approve_denied"
    if amount_raw > POLICY["max_amount_raw"]:
        return False, "amount_over_limit"
    return True, "allowed"


def send_policy_limited_transaction(
    draft: dict[str, Any], confirmed_by_user: bool
) -> dict[str, Any]:
    allowed, reason = policy_check(draft)
    if not allowed:
        raise PermissionError(reason)
    if POLICY["requires_user_confirmation"] and not confirmed_by_user:
        raise PermissionError("missing_user_confirmation")

    return {
        "status": "mock_submitted",
        "tx_hash": "0x" + "ab" * 32,
        "policy_decision": reason,
    }


def run_demo() -> list[ToolTrace]:
    user_goal = "Approve a small USDC spending limit on Base."
    owner = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    token = "0x1111111111111111111111111111111111111111"
    spender = "0x2222222222222222222222222222222222222222"
    chain_id = 8453
    traces: list[ToolTrace] = []

    balance_input = {"chain_id": chain_id, "address": owner}
    balance = get_eth_balance(**balance_input)
    traces.append(
        record_trace(
            user_goal=user_goal,
            tool_name="get_eth_balance",
            chain_id=chain_id,
            tool_input=balance_input,
            output=balance,
        )
    )

    allowance_input = {
        "chain_id": chain_id,
        "token": token,
        "owner": owner,
        "spender": spender,
    }
    allowance = read_erc20_allowance(**allowance_input)
    traces.append(
        record_trace(
            user_goal=user_goal,
            tool_name="read_erc20_allowance",
            chain_id=chain_id,
            tool_input=allowance_input,
            output=allowance,
        )
    )

    draft_input = {
        "chain_id": chain_id,
        "token": token,
        "spender": spender,
        "amount_raw": 1_000_000,
    }
    draft = draft_erc20_approve(**draft_input)
    traces.append(
        record_trace(
            user_goal=user_goal,
            tool_name="draft_erc20_approve",
            chain_id=chain_id,
            tool_input=draft_input,
            output=draft,
            policy_decision="draft_only",
        )
    )

    tx_input = {"draft": draft, "confirmed_by_user": True}
    tx = send_policy_limited_transaction(**tx_input)
    traces.append(
        record_trace(
            user_goal=user_goal,
            tool_name="send_policy_limited_transaction",
            chain_id=chain_id,
            tool_input=tx_input,
            output=tx,
            policy_decision=tx["policy_decision"],
            confirmed_by_user=True,
            tx_hash=tx["tx_hash"],
        )
    )

    denied_draft = draft_erc20_approve(chain_id, token, spender, MAX_UINT256)
    denied_input = {"draft": denied_draft, "confirmed_by_user": True}
    try:
        send_policy_limited_transaction(**denied_input)
    except PermissionError as exc:
        traces.append(
            record_trace(
                user_goal="Try an infinite approval.",
                tool_name="send_policy_limited_transaction",
                chain_id=chain_id,
                tool_input=denied_input,
                error=str(exc),
                policy_decision="denied",
                confirmed_by_user=True,
            )
        )

    return traces


if __name__ == "__main__":
    print(json.dumps([asdict(trace) for trace in run_demo()], indent=2))
