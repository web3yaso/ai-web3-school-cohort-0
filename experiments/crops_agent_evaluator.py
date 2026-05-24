"""
CROPS evaluator minimal practice.

This script scores an AI x Web3 idea across four dimensions:
Censorship Resistant, Open Source, Private, and Secure.
It uses simple keyword heuristics so it can run offline without API keys.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


DIMENSIONS = {
    "censorship_resistant": {
        "positive": [
            "ethereum",
            "onchain",
            "decentralized",
            "permissionless",
            "ipfs",
            "ens",
            "open protocol",
            "self-custody",
        ],
        "negative": ["single platform", "centralized", "closed api", "custodial"],
        "question": "Can the agent still work if one platform blocks it?",
    },
    "open_source": {
        "positive": ["open source", "public repo", "auditable", "standard", "sdk"],
        "negative": ["proprietary", "closed source", "black box"],
        "question": "Can builders inspect, fork, and reuse the system?",
    },
    "private": {
        "positive": [
            "local",
            "encrypted",
            "zero knowledge",
            "zk",
            "minimal disclosure",
            "user consent",
        ],
        "negative": ["collect all", "tracking", "leak", "raw intent", "public by default"],
        "question": "Does the design protect user intent and sensitive data?",
    },
    "secure": {
        "positive": [
            "policy",
            "simulation",
            "human confirmation",
            "spending limit",
            "trace",
            "revoke",
            "allowlist",
        ],
        "negative": ["infinite approve", "no confirmation", "unlimited", "private key"],
        "question": "Can the agent lose user assets or take irreversible actions?",
    },
}


@dataclass
class DimensionResult:
    score: int
    positives: list[str]
    negatives: list[str]
    question: str
    recommendation: str


@dataclass
class Evaluation:
    idea: str
    total_score: int
    max_score: int
    verdict: str
    dimensions: dict[str, DimensionResult]


def find_matches(text: str, keywords: list[str]) -> list[str]:
    lower_text = text.lower()
    return [keyword for keyword in keywords if keyword in lower_text]


def score_dimension(idea: str, dimension: str, config: dict[str, object]) -> DimensionResult:
    positives = find_matches(idea, list(config["positive"]))
    negatives = find_matches(idea, list(config["negative"]))
    score = max(0, min(5, 2 + len(positives) - len(negatives)))

    if score >= 4:
        recommendation = "Strong enough for a first prototype."
    elif score >= 2:
        recommendation = "Usable, but clarify the missing boundary before building."
    else:
        recommendation = "High-risk gap. Redesign this dimension first."

    return DimensionResult(
        score=score,
        positives=positives,
        negatives=negatives,
        question=str(config["question"]),
        recommendation=recommendation,
    )


def evaluate_idea(idea: str) -> Evaluation:
    dimensions = {
        name: score_dimension(idea, name, config)
        for name, config in DIMENSIONS.items()
    }
    total_score = sum(result.score for result in dimensions.values())
    max_score = len(DIMENSIONS) * 5

    if total_score >= 16:
        verdict = "promising"
    elif total_score >= 10:
        verdict = "needs_design_work"
    else:
        verdict = "too_risky_or_too_closed"

    return Evaluation(
        idea=idea,
        total_score=total_score,
        max_score=max_score,
        verdict=verdict,
        dimensions=dimensions,
    )


def default_idea() -> str:
    return (
        "An open source agent payment assistant on Ethereum. It uses an allowlist, "
        "spending limit, simulation, human confirmation, and trace logs before any "
        "onchain transaction. User intent is stored locally and only minimal data is "
        "shared with services."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate an AI x Web3 idea with CROPS.")
    parser.add_argument("--idea", default=default_idea(), help="Idea text to evaluate.")
    args = parser.parse_args()

    evaluation = evaluate_idea(args.idea)
    print(json.dumps(asdict(evaluation), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
