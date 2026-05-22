# Task: Agent Workflow Minimal Practice

## 任务目标

根据 Handbook 的 Agent Workflow 最小实践，设计一个“解释并准备一笔小额 ERC-20 swap”的链上 Agent 工作流。

## Task Graph

1. 读取用户目标和限制
2. 读取钱包余额和 allowance
3. 查询价格、滑点和流动性
4. 生成候选交易草稿
5. 模拟交易
6. 展示资产变化、权限变化和风险
7. 等待用户确认
8. 发送交易
9. 追踪交易结果并记录 trace

## 步骤边界

| 步骤 | 输入 | 输出 | 可用工具 | 失败处理 | Human-in-the-loop |
| --- | --- | --- | --- | --- | --- |
| 读取目标 | 用户自然语言、链、金额、token | 结构化任务 | LLM parser | 缺字段则追问 | 否 |
| 读取余额 | owner、token、chain id | balance、allowance | RPC / Contract Read | RPC 失败可重试 | 否 |
| 查询价格 | token pair、amount、chain id | quote、slippage | DEX quote / Oracle | 数据过旧则停止 | 否 |
| 生成草稿 | quote、policy | calldata 草稿 | Transaction Draft | policy 失败则拒绝 | 否 |
| 模拟交易 | calldata、from、chain id | simulation result | Simulation Tool | 模拟失败则停止 | 否 |
| 展示风险 | simulation、token delta、gas | 用户确认摘要 | UI / Wallet Tool | 用户看不懂则改写摘要 | 是 |
| 发送交易 | 用户确认、calldata | tx hash | Wallet Tool | 广播状态不明时不重复发送 | 是 |
| 追踪结果 | tx hash | receipt、最终状态 | Explorer / RPC | pending 则等待或提示 | 否 |

## 状态机

```text
draft
  -> context_loaded
  -> plan_ready
  -> simulation_failed | waiting_user_confirmation
  -> cancelled | submitted
  -> confirmed | reverted
```

## Regression Cases

1. 正常请求：用户要求在允许链上进行小额 swap，余额足够，滑点正常。
2. 错误链：用户指定不支持的 chain id，Agent 必须拒绝执行。
3. 滑点过大：quote 超出最大滑点，Agent 必须停止并解释风险。
4. 余额不足：余额不足以覆盖 swap 金额或 gas，Agent 不应生成可执行交易。
5. 用户拒绝：用户拒绝签名后，Agent 必须进入 `cancelled`，不能重试发送。

## Trace 字段

- `user_goal`
- `model_version`
- `context_sources`
- `tool_calls`
- `policy_checks`
- `simulation_result`
- `human_confirmation`
- `tx_hash`
- `final_state`

## 完成情况

- 已完成 task graph、步骤边界、状态机和 regression cases。
- 已实现本地 mock 脚本：`experiments/agent_workflow_mock.py`
- 未执行真实 swap。

## 运行方式

```bash
python3 experiments/agent_workflow_mock.py
```

也可以运行今天全部最小实践：

```bash
sh scripts/run_min_practices.sh
```

## 参考资源

- https://aiweb3.school/zh/handbook/bridge/agent-workflow/
