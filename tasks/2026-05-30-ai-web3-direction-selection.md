# Task: AI x Web3 Direction Selection

## 任务目标

完成 AI x Web3 交叉方向速览，并用方向判断矩阵选择一个 Week 2 深入探索主方向。

本次任务重点不是马上做完整项目，而是能说清楚：

- 每个方向的核心问题是什么。
- 哪些方向更适合自己的学习目标和 Hackathon 输出。
- AI 能力和 Web3 机制为什么在该问题中同时不可替代。
- 早期 proposal 最少需要包含哪些内容。

## 核心知识点

AI x Web3 的交叉方向可以从下面几个问题域理解：

- Payment / Commerce / Settlement
- Identity / Reputation / Capability / Interoperability
- Wallet / Permission / Safe Execution
- Privacy / Security / Sovereignty
- Dev Tooling / Agent Workflow
- Governance / Coordination / Public Goods

判断一个方向是否成立，不看它用了多少新词，而看 AI 能力和 Web3 机制是否同时不可替代。

真正有价值的问题通常会落在：

> 机器执行 + 经济交换 + 权限控制 + 可验证记录

早期 proposal 不需要完整实现，但必须说清楚目标用户、真实场景、最小功能、验证方式和风险边界。

## 方向速览

| 方向 | 核心问题 | 典型入口 | 适合输出 |
| --- | --- | --- | --- |
| Payment / Commerce / Settlement | agent 如何购买 API、数据、算力和服务，以及如何报价、验收、托管、争议处理和结算 | x402、invoice、escrow、receipt、agent marketplace | 产品 demo、developer tooling、protocol study |
| Identity / Reputation / Capability / Interoperability | agent 如何被发现、描述、调用、验证和协作 | MCP、A2A、ERC-8004、registry、agent profile、capability schema | protocol / standard、registry demo、research memo |
| Wallet / Permission / Safe Execution | agent 接触钱包、签名、预算和链上动作时如何分层授权、确认、撤销与审计 | Safe、account abstraction、session key、policy、guard | risk model、wallet demo、developer tooling |
| Privacy / Security / Sovereignty | 如何处理 prompt injection、tool abuse、敏感数据、模型依赖、key 暴露和本地执行 | secure agent runtime、audit log、TEE、local model、secret boundary | security checklist、risk model、research memo |
| Dev Tooling / Agent Workflow | AI 如何改善 Web3 builder 的开发工作流 | docs-to-agent、合约阅读、交易解释、部署助手、测试脚本 | developer tooling、repo skeleton、workflow demo |
| Governance / Coordination / Public Goods | AI 如何辅助 DAO、社区和公共物品项目协作 | 提案总结、会议行动项、贡献记录、预算 checklist | coordination tool、research memo、community workflow |

## Agent DeFi Execution 定位

Agent DeFi Execution 保留为第五个模块，定位为 sponsor-defined applied path。

它不是新的第七个基础方向，而是把下面几个基础方向放到 DeFi 链上执行场景中集中检验：

- Payment / Commerce / Settlement
- Wallet / Permission / Safe Execution
- Privacy / Security / Sovereignty

因此，它更适合作为 Cobo 相关 Hackathon / workshop 的优先应用路径，而不是单独替代基础方向选择。

## 两个兴趣方向

### 1. Payment / Commerce / Settlement

真实用户：

需要让 agent 购买 API、数据、算力、工具调用或小额服务的开发者、服务商、agent 平台和自动化 workflow 构建者。

如果没有 AI，为什么难以解决：

机器无法根据任务目标自主理解需求、选择服务、发起请求、检查交付结果和处理异常，只能依赖人工下单、固定脚本或静态 API 调用。

如果没有 Web3，为什么缺一块：

缺少开放的机器支付、托管、可验证结算和跨平台收据机制。陌生 agent 与服务方之间很难在没有预注册账号和中心化账期的情况下完成低摩擦交易。

更适合做：

产品 demo、developer tooling、protocol / standard study。

### 2. Wallet / Permission / Safe Execution

真实用户：

希望让 agent 辅助链上操作，但担心私钥、签名、预算、授权和误操作风险的钱包用户、DeFi 用户、DAO operator 和 Web3 builder。

如果没有 AI，为什么难以解决：

用户很难持续理解复杂交易、合约调用、授权额度、风险提示和多步骤执行流程，尤其在 DeFi、跨链和自动化场景中容易漏看关键风险。

如果没有 Web3，为什么缺一块：

权限、签名、撤销、预算、审计和不可逆执行都发生在链上或钱包系统中。传统账号权限无法表达 token allowance、session key、multisig、guard、policy 和链上交易记录。

更适合做：

risk model、developer tooling、最小 safe execution demo。

## Week 2 主方向

最终选择：

> Payment / Commerce / Settlement

选择原因：

- 和现有学习记录连续：stablecoin AI shopping assistant、x402 testnet contract、Virtuals ACP、agent-to-agent economy 都可以并入这个主线。
- 它能同时体现 AI 和 Web3 的不可替代性：AI 负责理解需求、选择服务、生成订单、检查交付；Web3 负责支付、托管、结算、收据和可验证记录。
- 一周内可以形成最小输出：流程图、invoice mock、receipt schema、交易 / 日志验证方式、repo skeleton 或 reference implementation。
- 它可以自然进入 Week 3 proposal，也能承接 Hackathon track / challenge 或长期 research backlog。

Backlog：

- Wallet / Permission / Safe Execution：作为主方向的安全和授权边界，重点关注预算、人工确认、撤销和审计。
- Identity / Reputation / Capability / Interoperability：后续用于 agent profile、服务发现、能力声明和交易对象可信度。
- Privacy / Security / Sovereignty：后续用于 prompt injection、tool abuse、敏感数据和 key 暴露风险。

## 方向判断矩阵

| 判断项 | 主方向判断 |
| --- | --- |
| 结构性需求 | 长期存在。只要 agent 需要购买 API、数据、算力、工具和服务，就需要机器可用的报价、支付、验收和结算机制 |
| 验证可能性 | 可以用流程图、invoice mock、receipt schema、交易记录、日志、用户访谈或 reference implementation 验证 |
| 最小切入点 | 一周内可以做出问题拆解、流程图、订单 / 收据 mock、repo skeleton 或最小 prototype |
| 风险边界 | 涉及付款、授权、资金、身份、敏感数据、争议处理和不可逆动作，需要限制金额、权限和自动执行范围 |
| 后续承接 | 可以进入 Week 3 proposal、Hackathon commerce / DeFi applied path、handbook / research backlog |

## 早期 Proposal 雏形

项目暂定名：

Agent Commerce Receipt Layer

目标用户：

正在构建 agent workflow 的开发者，以及希望向 agent 出售 API、数据、算力或小额服务的服务商。

真实场景：

一个 research agent 需要购买一次付费数据查询。它收到服务方报价后，在预算内完成付款，服务方交付结果，系统记录订单、付款、交付和验收日志，最终生成可验证 receipt。

最小功能：

- 服务方返回结构化报价：服务名称、价格、token、网络、过期时间、交付格式。
- agent 生成订单草稿并检查预算。
- 用户或 policy 确认付款边界。
- 支付完成后记录 tx hash 或 payment proof。
- 服务交付后生成 receipt，包含订单、付款、交付、验收和异常状态。

验证方式：

- mock 一次购买流程，输出完整日志。
- 用 receipt schema 检查字段完整性。
- 如果接入链上测试，可用交易 hash 或合约事件验证付款。
- 如果不接真实支付，可用 reference implementation 模拟报价、付款证明和交付验收。


