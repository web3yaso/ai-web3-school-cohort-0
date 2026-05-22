#!/usr/bin/env sh
set -eu

echo "== Web3 Tool Use mock =="
python3 experiments/web3_tool_use_mock.py

echo
echo "== Agent Workflow mock =="
python3 experiments/agent_workflow_mock.py
