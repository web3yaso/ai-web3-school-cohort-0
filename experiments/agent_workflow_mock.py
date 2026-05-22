"""
Agent Workflow minimal practice.

This script mocks a small ERC-20 swap workflow with policy checks, simulation,
human confirmation, state transitions, and regression cases.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


SUPPORTED_CHAINS = {8453: "Base"}
MAX_SLIPPAGE_BPS = 100
MOCK_BALANCES = {
    "ETH": 250000000000000000,
    "USDC": 25000000,
}


@dataclass
class WorkflowTrace:
    user_goal: str
    state: str = "draft"
    model_version: str = "mock-parser-v1"
    context_sources: list[str] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    policy_checks: list[dict[str, Any]] = field(default_factory=list)
    simulation_result: dict[str, Any] | None = None
    human_confirmation: bool | None = None
    tx_hash: str | None = None
    final_state: str | None = None
    error: str | None = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def transition(self, state: str) -> None:
        self.state = state

    def finish(self, final_state: str) -> None:
        self.final_state = final_state
        self.state = final_state


def parse_goal(goal: dict[str, Any], trace: WorkflowTrace) -> dict[str, Any]:
    required = ["chain_id", "from_token", "to_token", "amount_raw", "slippage_bps"]
    missing = [key for key in required if key not in goal]
    if missing:
        raise ValueError(f"missing_fields:{','.join(missing)}")
    trace.tool_calls.append({"tool": "parse_goal", "output": goal})
    return goal


def load_context(task: dict[str, Any], trace: WorkflowTrace) -> dict[str, Any]:
    chain_id = task["chain_id"]
    if chain_id not in SUPPORTED_CHAINS:
        raise PermissionError("unsupported_chain")

    context = {
        "chain": SUPPORTED_CHAINS[chain_id],
        "balances": MOCK_BALANCES,
        "allowance_raw": 0,
    }
    trace.context_sources.extend(["mock_balances", "mock_allowance"])
    trace.tool_calls.append({"tool": "load_context", "output": context})
    trace.transition("context_loaded")
    return context


def make_plan(
    task: dict[str, Any], context: dict[str, Any], trace: WorkflowTrace
) -> dict[str, Any]:
    from_token = task["from_token"]
    amount_raw = int(task["amount_raw"])
    if context["balances"].get(from_token, 0) < amount_raw:
        raise ValueError("insufficient_balance")
    if int(task["slippage_bps"]) > MAX_SLIPPAGE_BPS:
        raise ValueError("slippage_too_high")

    plan = {
        "method": "swap_exact_tokens_for_tokens",
        "from_token": from_token,
        "to_token": task["to_token"],
        "amount_in_raw": amount_raw,
        "min_amount_out_raw": int(amount_raw * 0.99),
        "requires_user_confirmation": True,
    }
    trace.tool_calls.append({"tool": "make_plan", "output": plan})
    trace.policy_checks.append({"check": "slippage", "result": "allowed"})
    trace.transition("plan_ready")
    return plan


def simulate(plan: dict[str, Any], trace: WorkflowTrace) -> dict[str, Any]:
    simulation = {
        "status": "success",
        "asset_delta": {
            plan["from_token"]: -plan["amount_in_raw"],
            plan["to_token"]: plan["min_amount_out_raw"],
        },
        "gas_estimate": 120000,
        "risk_summary": "Mock swap succeeds within slippage limit.",
    }
    trace.simulation_result = simulation
    trace.tool_calls.append({"tool": "simulate", "output": simulation})
    trace.transition("waiting_user_confirmation")
    return simulation


def send_transaction(
    plan: dict[str, Any], confirmed_by_user: bool, trace: WorkflowTrace
) -> dict[str, Any]:
    trace.human_confirmation = confirmed_by_user
    if not confirmed_by_user:
        trace.finish("cancelled")
        raise PermissionError("user_rejected")

    tx = {
        "status": "mock_submitted",
        "tx_hash": "0x" + "cd" * 32,
        "method": plan["method"],
    }
    trace.tx_hash = tx["tx_hash"]
    trace.tool_calls.append({"tool": "send_transaction", "output": tx})
    trace.transition("submitted")
    return tx


def track_transaction(tx_hash: str, trace: WorkflowTrace) -> dict[str, Any]:
    receipt = {"tx_hash": tx_hash, "status": "confirmed", "block_number": 123456}
    trace.tool_calls.append({"tool": "track_transaction", "output": receipt})
    trace.finish("confirmed")
    return receipt


def run_workflow(goal: dict[str, Any], confirmed_by_user: bool = True) -> WorkflowTrace:
    trace = WorkflowTrace(user_goal=json.dumps(goal, ensure_ascii=False))

    try:
        task = parse_goal(goal, trace)
        context = load_context(task, trace)
        plan = make_plan(task, context, trace)
        simulate(plan, trace)
        tx = send_transaction(plan, confirmed_by_user, trace)
        track_transaction(tx["tx_hash"], trace)
    except Exception as exc:
        if trace.final_state is None:
            if trace.state == "waiting_user_confirmation":
                trace.finish("cancelled")
            elif trace.state == "plan_ready":
                trace.finish("simulation_failed")
            else:
                trace.finish("failed")
        trace.error = str(exc)

    return trace


def regression_cases() -> list[WorkflowTrace]:
    normal = {
        "chain_id": 8453,
        "from_token": "USDC",
        "to_token": "ETH",
        "amount_raw": 1_000_000,
        "slippage_bps": 50,
    }
    wrong_chain = {**normal, "chain_id": 1}
    high_slippage = {**normal, "slippage_bps": 500}
    insufficient_balance = {**normal, "amount_raw": 100_000_000}

    return [
        run_workflow(normal, confirmed_by_user=True),
        run_workflow(wrong_chain, confirmed_by_user=True),
        run_workflow(high_slippage, confirmed_by_user=True),
        run_workflow(insufficient_balance, confirmed_by_user=True),
        run_workflow(normal, confirmed_by_user=False),
    ]


if __name__ == "__main__":
    print(json.dumps([asdict(trace) for trace in regression_cases()], indent=2))
