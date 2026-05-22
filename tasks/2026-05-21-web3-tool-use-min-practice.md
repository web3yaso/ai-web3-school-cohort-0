# Task: Web3 Tool Use Minimal Practice

## 任务目标

根据 Handbook 的 Web3 Tool Use 最小实践，设计一组 Agent 可调用的 Web3 工具，把读、写、签名、确认和日志边界分清楚。

## 工具设计

### 1. `get_eth_balance`

只读工具：读取某地址在某链上的 ETH 余额。

输入：

```json
{
  "chain_id": 1,
  "address": "0x..."
}
```

输出：

```json
{
  "chain_id": 1,
  "address": "0x...",
  "block_number": "latest",
  "balance_wei": "0",
  "balance_eth": "0"
}
```

错误类型：

- `invalid_address`
- `unsupported_chain`
- `rpc_error`

### 2. `read_erc20_allowance`

合约读取工具：读取 ERC-20 `allowance(owner, spender)`。

输入：

```json
{
  "chain_id": 1,
  "token": "0x...",
  "owner": "0x...",
  "spender": "0x..."
}
```

输出：

```json
{
  "chain_id": 1,
  "token": "0x...",
  "owner": "0x...",
  "spender": "0x...",
  "allowance_raw": "0",
  "block_number": "latest"
}
```

错误类型：

- `invalid_address`
- `abi_mismatch`
- `contract_read_failed`

### 3. `draft_erc20_approve`

交易草稿工具：生成 ERC-20 `approve(spender, amount)` calldata，但不发送交易。

输入：

```json
{
  "chain_id": 1,
  "token": "0x...",
  "spender": "0x...",
  "amount_raw": "1000000"
}
```

输出：

```json
{
  "to": "0x...",
  "method": "approve",
  "args": ["0x...", "1000000"],
  "calldata": "0x...",
  "requires_user_confirmation": true
}
```

错误类型：

- `policy_denied`
- `invalid_amount`
- `encoding_failed`

### 4. `send_policy_limited_transaction`

写交易工具：只允许白名单 token、白名单 spender、额度上限内的 approve。

权限规则：

```yaml
allowed_chain_ids:
  - 1
  - 8453
allowed_methods:
  - approve
allowed_tokens:
  - 0xTokenWhitelistExample
allowed_spenders:
  - 0xSpenderWhitelistExample
max_amount_usd: 10
requires_simulation: true
requires_user_confirmation: true
deny_infinite_approve: true
```

## 日志字段

每次工具调用至少记录：

- `timestamp`
- `user_goal`
- `tool_name`
- `chain_id`
- `input`
- `output`
- `error`
- `block_number`
- `policy_decision`
- `confirmed_by_user`
- `tx_hash`

## 完成情况

- 已完成工具边界设计。
- 已实现本地 mock 脚本：`experiments/web3_tool_use_mock.py`
- 未连接真实 RPC，也未生成或发送真实交易。

## 运行方式

```bash
python3 experiments/web3_tool_use_mock.py
```

也可以运行今天全部最小实践：

```bash
sh scripts/run_min_practices.sh
```

## 参考资源

- https://aiweb3.school/zh/handbook/bridge/web3-tool-use/
