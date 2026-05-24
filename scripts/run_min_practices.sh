#!/usr/bin/env sh
set -eu

echo "== Web3 Tool Use mock =="
python3 experiments/web3_tool_use_mock.py

echo
echo "== Agent Workflow mock =="
python3 experiments/agent_workflow_mock.py

echo
echo "== CROPS Agent Evaluator =="
python3 experiments/crops_agent_evaluator.py

echo
echo "== Transaction Risk Summary Prompt =="
python3 experiments/transaction_risk_summary_prompt.py
