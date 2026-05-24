"""
Prompt minimal practice: transaction risk summary.

This implements the Handbook prompt exercise with three regression cases:
normal transfer, infinite approval, and target/user-intent mismatch.

The script runs offline. `mock_model_response` is a deterministic stand-in for a
model so we can validate the prompt contract and expected risk behavior without
an API key.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_KEYS = {
    "summary",
    "asset_changes",
    "permissions_changed",
    "risk_level",
    "requires_human_approval",
    "uncertainties",
    "recommended_user_checks",
}

RISK_LEVELS = {"low", "medium", "high"}
PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "transaction_risk_summary_prompt.md"


@dataclass
class TestCase:
    name: str
    transaction: dict[str, Any]
    expected_risk_level: str
    expected_requires_approval: bool
    expected_uncertainty_contains: str | None = None


TEST_CASES = [
    TestCase(
        name="normal_transfer",
        transaction={
            "target_address": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "function_name": "transfer",
            "parameters": {
                "to": "0xcccccccccccccccccccccccccccccccccccccccc",
                "amount": "0.01 ETH",
            },
            "asset_changes": [
                {
                    "asset": "ETH",
                    "direction": "out",
                    "amount": "0.01",
                    "recipient": "0xcccccccccccccccccccccccccccccccccccccccc",
                }
            ],
            "simulation_result": {"status": "success", "warnings": []},
            "user_intent": "Send 0.01 ETH to 0xcccccccccccccccccccccccccccccccccccccccc.",
        },
        expected_risk_level="low",
        expected_requires_approval=True,
    ),
    TestCase(
        name="infinite_approval",
        transaction={
            "target_address": "0xdddddddddddddddddddddddddddddddddddddddd",
            "function_name": "approve",
            "parameters": {
                "spender": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
                "amount": "unlimited",
            },
            "asset_changes": [],
            "simulation_result": {"status": "success", "warnings": ["allowance changes"]},
            "user_intent": "Allow the app to spend 10 USDC for this payment only.",
        },
        expected_risk_level="high",
        expected_requires_approval=True,
        expected_uncertainty_contains="unlimited",
    ),
    TestCase(
        name="target_intent_mismatch",
        transaction={
            "target_address": "0xffffffffffffffffffffffffffffffffffffffff",
            "function_name": "transfer",
            "parameters": {
                "to": "0xffffffffffffffffffffffffffffffffffffffff",
                "amount": "0.5 ETH",
            },
            "asset_changes": [
                {
                    "asset": "ETH",
                    "direction": "out",
                    "amount": "0.5",
                    "recipient": "0xffffffffffffffffffffffffffffffffffffffff",
                }
            ],
            "simulation_result": {"status": "success", "warnings": []},
            "user_intent": "Send 0.5 ETH to 0xcccccccccccccccccccccccccccccccccccccccc.",
        },
        expected_risk_level="high",
        expected_requires_approval=True,
        expected_uncertainty_contains="recipient",
    ),
]


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def is_infinite_approval(transaction: dict[str, Any]) -> bool:
    if transaction["function_name"].lower() not in {"approve", "setapprovalforall"}:
        return False
    amount = str(transaction.get("parameters", {}).get("amount", "")).lower()
    return amount in {"unlimited", "infinite", "max", "max_uint256"} or amount.startswith("115792089")


def has_target_intent_mismatch(transaction: dict[str, Any]) -> bool:
    intent = transaction["user_intent"].lower()
    for change in transaction.get("asset_changes", []):
        recipient = str(change.get("recipient") or "").lower()
        if recipient.startswith("0x") and recipient not in intent:
            return True
    return False


def mock_model_response(transaction: dict[str, Any]) -> dict[str, Any]:
    uncertainties: list[str] = []
    recommended_checks = [
        "Confirm the target address in your wallet UI.",
        "Review asset changes before signing.",
        "Only sign if the transaction matches your original intent.",
    ]
    permissions_changed: list[dict[str, str]] = []
    risk_level = "low"

    simulation_status = transaction.get("simulation_result", {}).get("status")
    if simulation_status != "success":
        risk_level = "high"
        uncertainties.append("Simulation did not succeed or is missing.")

    if transaction["function_name"].lower() == "approve":
        risk_level = "medium"
        spender = transaction.get("parameters", {}).get("spender", "unknown")
        amount = transaction.get("parameters", {}).get("amount", "unknown")
        permission_risk = "medium"
        if is_infinite_approval(transaction):
            risk_level = "high"
            permission_risk = "high"
            uncertainties.append("The approval amount appears to be unlimited.")
            recommended_checks.append("Avoid unlimited approval unless you fully trust the spender.")

        permissions_changed.append(
            {
                "asset": "token",
                "spender": str(spender),
                "permission": f"approve {amount}",
                "risk": permission_risk,
            }
        )

    if has_target_intent_mismatch(transaction):
        risk_level = "high"
        uncertainties.append("The actual recipient does not match the recipient in user_intent.")
        recommended_checks.append("Reject if the wallet recipient differs from your intended recipient.")

    summary = (
        f"Transaction calls {transaction['function_name']} on "
        f"{transaction['target_address']}."
    )

    return {
        "summary": summary,
        "asset_changes": transaction.get("asset_changes", []),
        "permissions_changed": permissions_changed,
        "risk_level": risk_level,
        "requires_human_approval": True,
        "uncertainties": uncertainties,
        "recommended_user_checks": recommended_checks,
    }


def validate_schema(output: dict[str, Any]) -> None:
    missing = REQUIRED_KEYS - set(output)
    extra = set(output) - REQUIRED_KEYS
    if missing:
        raise AssertionError(f"missing required keys: {sorted(missing)}")
    if extra:
        raise AssertionError(f"unexpected keys: {sorted(extra)}")
    if output["risk_level"] not in RISK_LEVELS:
        raise AssertionError("risk_level must be low, medium, or high")
    if not isinstance(output["requires_human_approval"], bool):
        raise AssertionError("requires_human_approval must be boolean")
    for list_key in ["asset_changes", "permissions_changed", "uncertainties", "recommended_user_checks"]:
        if not isinstance(output[list_key], list):
            raise AssertionError(f"{list_key} must be a list")


def run_case(test_case: TestCase) -> dict[str, Any]:
    output = mock_model_response(test_case.transaction)
    validate_schema(output)

    assert output["risk_level"] == test_case.expected_risk_level
    assert output["requires_human_approval"] is test_case.expected_requires_approval
    if test_case.expected_uncertainty_contains:
        uncertainty_text = " ".join(output["uncertainties"]).lower()
        assert test_case.expected_uncertainty_contains in uncertainty_text

    return {
        "case": test_case.name,
        "passed": True,
        "output": output,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run transaction risk prompt tests.")
    parser.add_argument("--show-prompt", action="store_true", help="Print the prompt text.")
    args = parser.parse_args()

    if args.show_prompt:
        print(load_prompt())
        return

    results = [run_case(test_case) for test_case in TEST_CASES]
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
