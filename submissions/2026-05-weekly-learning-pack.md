# Week 1 Learning Pack: AI x Web3 School

周期：2026-05-18 至 2026-05-27  
总入口：本文件  
公开仓库：https://github.com/web3yaso/ai-web3-school-cohort-0

## 一句话总结

本周完成了 AI 基础、Web3 基础、Agent Workflow、Web3 Tool Use、测试网交易、x402 风格合约草稿、交易风险摘要 prompt 和一个 AI x Web3 最小工作流图。

核心收获是：AI Agent 可以帮助理解目标、调用只读工具、生成交易草稿和风险摘要，但链上签名、授权、付款和高风险操作必须保留人工确认、钱包确认、策略限制和可追踪日志。

## 1. AI 学习记录和概念卡片

| 材料 | 说明 |
| --- | --- |
| [AI Foundation Concepts](../tasks/2026-05-24-ai-foundation-concepts.md) | 整理 LLM、Prompt、Context Window、Workflow、Agent、Tool Use、AI Coding、Guardrails、Tracing、Human-in-the-loop。 |
| [Daily 2026-05-18](../daily/2026-05-18.md) | 复习 AI 基础：LLM、Prompt Engineering、Context Management、RAG、Agent、Frameworks、MCP、Evaluation。 |
| [Transaction Risk Summary Prompt](../tasks/2026-05-25-prompt-transaction-risk-summary.md) | 把交易信息转成固定 JSON 风险摘要，并设计三组 regression cases。 |
| [Prompt 文件](../prompts/transaction_risk_summary_prompt.md) | 交易风险摘要 prompt，要求输出资产变化、权限变化、风险等级、人工确认要求和不确定性。 |
| [Prompt 测试脚本](../experiments/transaction_risk_summary_prompt.py) | 离线 mock model + schema 校验 + regression cases。 |

## 2. Learning Agent / AI 工具实践记录

| 材料 | 说明 |
| --- | --- |
| [Agent / AI Tool Proof Record](./2026-05-24-agent-ai-tool-proof.md) | 记录使用 Codex Desktop / GPT-5 coding agent 协助整理学习任务、生成 mock 实验和补充提交记录。 |
| [Web3 Tool Use Minimal Practice](../tasks/2026-05-21-web3-tool-use-min-practice.md) | 设计只读工具、合约读取工具、交易草稿工具和受 policy 限制的写交易工具。 |
| [Agent Workflow Minimal Practice](../tasks/2026-05-21-agent-workflow-min-practice.md) | 设计小额 ERC-20 swap workflow：读取目标、查余额、报价、生成草稿、模拟、展示风险、等待确认、发送、追踪。 |
| [web3_tool_use_mock.py](../experiments/web3_tool_use_mock.py) | 本地 mock：验证地址、链、allowance、approve 草稿、policy check 和 trace。 |
| [agent_workflow_mock.py](../experiments/agent_workflow_mock.py) | 本地 mock：验证 workflow 状态机、滑点、余额、不支持链、用户拒绝等边界。 |
| [run_min_practices.sh](../scripts/run_min_practices.sh) | 一键运行本周最小实践脚本。 |

## 3. Web3 概念卡片和测试网记录

| 材料 | 说明 |
| --- | --- |
| [Web3 Foundation Concepts](../tasks/2026-05-24-web3-foundation-concepts.md) | 整理 Account、Address、Wallet、Seed Phrase、Private Key、Signature、Transaction、Gas、Smart Contract、Testnet、Block Explorer、EOA / Smart Account / Multisig。 |
| [EOA / Smart Account / Multisig Comparison](../tasks/2026-05-25-account-permission-comparison.md) | 比较三类账户的控制权、发起者、批准者、恢复、限额、自动化策略和风险。 |
| [Testnet Transaction Record](../tasks/2026-05-24-testnet-transaction.md) | Base Sepolia 测试网交易记录，包含交易哈希、调用合约地址、区块浏览器链接和 gas 信息。 |
| [x402 Receipt Registry Practice](../tasks/2026-05-25-x402-testnet-contract.md) | 准备 x402 风格最小合约部署和写入验证流程。 |
| [X402ReceiptRegistry.sol](../contracts/X402ReceiptRegistry.sol) | 独立 Solidity 合约，用于记录 x402 风格付款凭证摘要，不托管资产、不转账、不 approve。 |

## 4. 已验证的链上信息

### Base Sepolia 测试网交易

| 项目 | 内容 |
| --- | --- |
| 网络 | Base Sepolia |
| Chain ID | `84532` |
| 交易哈希 | `0xefc3562a5c697a4bc7c454a97eee9209ca0f7de9a32060f2a6ec14ba3632e1ba` |
| 区块浏览器 | https://sepolia.basescan.org/tx/0xefc3562a5c697a4bc7c454a97eee9209ca0f7de9a32060f2a6ec14ba3632e1ba |
| 发起地址 | `0x6Cd01c0F55ce9E0Bf78f5E90f72b4345b16d515d` |
| 接收地址 | `0x8dF5f05aB4E88d70ED0F0714b7210c5840F38e1D` |
| 调用合约地址 | `0x3e4ed2D6d6235f9D26707fd5d5AF476fb9C91B0F` |
| 状态 | `Success` |
| 区块高度 | `41948837` |
| 内部转账 | `0.0001 ETH` |
| 交易费 | `0.000000336081653571 ETH` |

### x402 风格最小合约

本周已完成合约源码和部署/验证说明，链上部署记录仍需在人工部署后补充到 [x402 Receipt Registry Practice](../tasks/2026-05-25-x402-testnet-contract.md)。

待补充项包括：

- 部署钱包地址
- 合约地址
- 部署交易哈希
- BaseScan 合约链接
- `recordPayment(...)` 写入交易哈希
- `quote()` / `paymentCount()` / `getReceipt(bytes32)` 读取验证结果

## 5. AI x Web3 最小交叉实验

| 实验 | 交叉点 | 验证方式 |
| --- | --- | --- |
| [AI x Web3 Workflow Boundary](../tasks/2026-05-26-ai-web3-workflow-boundary.md) | AI 生成交易草稿，钱包和用户保留最终签名边界。 | Mermaid 流程图 + 边界表，覆盖发起者、执行者、签名/付款/授权、人工确认、验证方式和风险点。 |
| [Transaction Risk Summary Prompt](../tasks/2026-05-25-prompt-transaction-risk-summary.md) | AI 把交易信息总结成固定 JSON 风险摘要。 | 三组 regression cases：普通转账、无限授权、目标地址与意图不匹配。 |
| [Agent Workflow Mock](../experiments/agent_workflow_mock.py) | Agent workflow 准备小额 swap，但通过策略、模拟和用户确认控制风险。 | 本地离线状态机测试，不执行真实交易。 |
| [Web3 Tool Use Mock](../experiments/web3_tool_use_mock.py) | 把链上读写能力拆成受限工具接口。 | 本地离线 policy check 和 trace。 |
| [CROPS Agent Evaluator](../tasks/2026-05-25-crops-agent-evaluator.md) | 用 CROPS 框架评估 AI x Web3 项目想法。 | 本地关键词启发式 evaluator，输出四个维度评分和风险提示。 |

## 6. 本周遇到的问题和人工修正

### 问题

本来以为可以用提交 PR 的方式来完成打卡，但是实际操作后发现不可行。

### 人工修正

我把打卡 proof 从“依赖 PR 合并”修正为“整理一个公开可访问的总入口链接”，也就是本文件。这样审核者可以直接看到本周学了什么、做了什么、验证了什么，以及哪些链上信息已经完成、哪些还需要后续补充。

修正后的 proof 入口：

- [Week 1 Learning Pack](./2026-05-weekly-learning-pack.md)
- [Submissions README](./README.md)
- [Repository README](../README.md)

## 7. 可运行验证

本仓库中的最小实践脚本都设计为离线运行，不需要 API key、私钥、RPC URL 或真实链上交易。

```bash
sh scripts/run_min_practices.sh
python3 experiments/transaction_risk_summary_prompt.py
python3 experiments/crops_agent_evaluator.py
```

安全边界：

- 不提交 API key、私钥、助记词或 `.env` 文件。
- mock 脚本不连接真实 RPC。
- prompt 测试不调用真实模型。
- x402 合约不托管资产、不转账、不 approve。

## 8. 下周待补充

- 人工部署 `X402ReceiptRegistry` 到 Base Sepolia，并补充合约地址、部署交易哈希和写入交易哈希。
- 给 Agent Workflow mock 增加更清晰的测试输出摘要。
- 把本周 Pack 链接提交到 WCB / 打卡平台作为 proof。
