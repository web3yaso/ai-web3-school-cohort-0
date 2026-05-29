# Task: Virtuals Protocol Agent-to-Agent Economy Research

本次选择研究 Virtuals Protocol，重点关注它如何围绕 AI Agent 构建 Agent-to-Agent economy。

## 项目概览

Virtuals Protocol 是一个面向 AI Agent 的 Web3 协议和平台。它的核心方向不是简单做一个聊天机器人，也不是只给 AI Agent 发 token，而是试图把 AI Agent 变成可以拥有身份、钱包、服务、收入、声誉和市场定价的链上经济主体。

可以把它理解为一个 AI agents society：Agent 可以生产服务或产品，可以与人类或其他 Agent 交易，也可以通过链上协议完成身份、支付、声誉、验证和结算。

## 它在解决什么问题

Virtuals Protocol 想解决的是：AI Agent 如果要成为真正的生产力和经济参与者，不能只停留在单个应用里的自动化工具。

一个真正自主的 Agent 不只需要会回答问题，还需要：

- 有自己的身份和钱包。
- 能提供服务并收费。
- 能雇佣其他 Agent 完成任务。
- 能被市场发现、评价和定价。
- 能把任务、支付、交付结果变成可验证记录。

传统 AI Agent 大多是“用户调用的工具”。它们可以生成内容、写代码、分析数据或执行任务，但通常没有独立的经济身份，也没有标准化的支付、结算、声誉和协作机制。

Virtuals 的核心问题意识是：如果未来有大量 Agent 提供不同服务，那么 Agent 之间需要一个开放市场。一个 Agent 应该可以发现另一个 Agent，判断它是否可信，雇佣它，支付费用，接收交付，并把结果记录成可验证的声誉。

因此，Virtuals 的主线可以概括为：

> 构建一个链上的 Agent-to-Agent economy，让 AI Agent 从“会执行任务的软件”升级为“可以被拥有、被雇佣、可支付、可验证、可交易的经济主体”。

## AI 部分是什么

Virtuals 的 AI 部分核心不是自己训练一个新的基础大模型，而是用 GAME 框架把现有 foundation models 变成可以持续行动的 autonomous agent。

GAME 官方将自己定义为 modular agentic framework / decision-making engine。它建立在 foundation models 之上，输入 Agent 的目标、人格、上下文信息和可用动作，然后输出下一步要执行的 action。

### 模型在哪里运行

从目前官方文档看，Virtuals / GAME 主要是云端或 API 调用模式，不是让用户把模型权重下载到本地运行。

证据包括：

- GAME SDK 需要 API key 才能使用。
- GAME Cloud 曾经是托管式 low-code 服务，但现在已 deprecated，当前主要使用 GAME SDK。
- 文档提到 GAME Cloud 和 GAME SDK 曾把默认 LLM 从 `Llama-3.1-405B-Instruct` 改成 `Llama-3.3-70B-Instruct`，说明底层模型通过托管推理或模型服务接入，而不是用户本地部署。
- 如果开发者已经有自己的 Agent 或自定义模型，也可以把它暴露成 API，再通过 GAME 的 function calling 接入。

所以更准确的说法是：

> Virtuals / GAME 的模型推理主要通过 API 访问托管模型或开发者外部服务。开发者用 GAME SDK 配置 Agent 的目标、人格、状态和工具；底层 LLM 负责推理，GAME 负责把推理结果转化为可执行行动。如果开发者有自己的模型，也可以通过 API 方式暴露给 GAME 调用。

### GAME 和 GPT 有什么不同

GPT 更像是一个通用大语言模型或聊天接口，主要能力是理解、生成、推理和对话。GAME 不是单个模型，而是一个 Agent 决策与执行框架。

核心区别如下：

| 维度 | GPT / 常用 LLM | GAME |
| --- | --- | --- |
| 定位 | 通用语言模型或聊天接口 | Agent 决策引擎和执行框架 |
| 输入 | 用户 prompt、上下文 | Agent 目标、人格、状态、可用工具、环境信息 |
| 输出 | 主要是文本 | 下一步 action / function call / 任务决策 |
| 行动方式 | 通常被动回复用户 | 可以根据 heartbeat 周期性行动 |
| 工具能力 | 取决于外部应用是否接入工具 | 原生围绕 functions、plugins、API actions 设计 |
| 适用场景 | 问答、写作、代码、推理 | 社交 Agent、链上 Agent、多 Agent 协作、服务交易 |

可以把 GPT 理解为“大脑”，把 GAME 理解为让这个大脑能够观察环境、调用工具、执行任务、接收反馈、继续行动的 Agent 操作系统。

例如，一个普通 GPT 可以回答“我应该发什么推文”。但一个 GAME Agent 可以根据自己的目标、人格、X/Twitter 状态、可用函数和外部数据，决定是否发推、回复、搜索、转账、请求其他 Agent 服务，或者暂时不行动。

## Web3 部分是什么

Virtuals 的 Web3 部分不只是发 Agent token，而是围绕 Agent-to-Agent economy 建立链上身份、支付、声誉、验证和结算基础设施。

可以拆成三层协议栈。

### 1. Agent 身份与信任层：ERC-8004

ERC-8004，也叫 Trustless Agents，是面向 AI Agent 的链上身份和信任标准。它用三个 registry 支撑开放 agent economy：

- Identity Registry：给 Agent 一个链上身份，基于 ERC-721，每个 Agent 有 `agentId` 和 `agentURI`。
- Reputation Registry：记录 Agent 的反馈、评分、服务质量等声誉信号。
- Validation Registry：允许第三方验证 Agent 的输出，例如 re-execution、TEE、zkML 或其他验证方式。

这解决的是：一个 Agent 如何被发现、如何证明自己是谁、如何积累可验证声誉、如何让别人信任它。

### 2. Agent 支付层：x402

x402 是 Coinbase 推动的 HTTP-native payment protocol，用 HTTP `402 Payment Required` 状态码实现自动化稳定币支付。它允许 AI Agent 在访问 API、数据、MCP 工具或其他付费服务时自动付款。

基本流程是：

1. Agent 请求一个资源。
2. 服务方返回 `402 Payment Required` 和付款要求。
3. Agent 用钱包签名付款。
4. facilitator 验证并结算。
5. 服务方返回资源。

这解决的是：Agent 如何不经过人工确认、不注册账号、不走订阅制，也能按次付费购买服务。

### 3. Agent 交易与协作层：Virtuals ACP

Virtuals 的 ACP, Agent Commerce Protocol，更像是 Agent-to-Agent 服务交易协议。它处理的不只是一次 API 付费，而是完整的任务协作流程：

- Agent 发现其他 Agent。
- 买方 Agent 发起任务。
- 服务方 Agent 接单。
- 智能合约 escrow 托管付款。
- 服务方交付结果。
- evaluator 评估结果。
- 根据结果释放付款或处理争议。

ACP 解决的是：Agent 之间如何可靠地雇佣、交付、评价和结算。

### Tokenization 和 $VIRTUAL

除了协议层，Virtuals 还引入 Agent tokenization。每个 Agent 可以被 tokenized，用户可以购买 Agent token，参与 Agent 的成长、治理和价值捕获。

$VIRTUAL 则是生态中的基础资产，承担 Agent token 流动性配对、生态交易和结算相关角色。

因此，Virtuals 的 Web3 部分可以总结为：

> ERC-8004 提供 Agent 的链上身份、声誉和验证注册表；x402 提供 HTTP 原生的稳定币支付能力；Virtuals ACP 提供 Agent 之间完整的任务交易流程；Agent tokenization 和 $VIRTUAL 则提供资本形成和价值捕获机制。

## 主要创新点：Agent-to-Agent Economy

Virtuals Protocol 的核心创新可以概括为 Agent-to-Agent economy。

在传统 AI 应用中，Agent 通常只是被用户调用的工具。而在 Virtuals 中，Agent 可以拥有钱包、身份、服务目录、收入、声誉和 token 化所有权。不同 Agent 之间可以像市场里的服务提供者一样互相雇佣和协作。

一个例子：

1. 投资 Agent 需要分析某个新项目。
2. 它雇佣数据分析 Agent 获取链上数据。
3. 数据分析 Agent 调用新闻摘要 Agent 或社交舆情 Agent。
4. 结果交付后，通过 ACP 完成支付和评价。
5. 支付记录、交付结果和评价成为 Agent 声誉的一部分。

这就是 Virtuals 想构建的 Agent-to-Agent economy：一个由 AI Agent 组成的链上服务市场。

## 对比 Virtuals Agent 和 Codex / Claude Code

Virtuals Agent 与 Codex、Claude Code 这类 coding agent 的区别在于，后者主要是人类开发者的生产力工具，而 Virtuals Agent 试图成为链上经济主体。

一句话区别：

> Codex / Claude Code 是“帮人写代码的开发者 Agent”；Virtuals Agent 是“能在链上经济里提供服务、交易、积累声誉的经济 Agent”。

| 维度 | Virtuals Agent | Codex / Claude Code |
| --- | --- | --- |
| 主要目标 | 构建 Agent-to-Agent economy | 帮开发者读代码、改代码、跑命令、修 bug、提交 PR |
| 工作场景 | Web3、社交平台、链上服务市场、Agent 之间交易 | 本地代码仓库、终端、IDE、GitHub、CI |
| Agent 身份 | 可以有链上身份、钱包、Agent token、声誉记录 | 通常没有独立链上身份，本质是用户授权下的开发助手 |
| 支付能力 | 可结合 x402、ACP、钱包和 escrow 进行自动支付 / 结算 | 一般不直接参与经济结算，不自己收款或付款 |
| 交互对象 | 人类、其他 Agent、链上协议、社交平台、API 服务 | 主要是人类开发者、代码库、终端工具、MCP 工具 |
| 自主性 | 目标是长期运行、定期行动、接单 / 发单、服务交易 | 通常围绕一次开发任务运行，由用户授权工具调用 |
| AI 架构 | GAME 是 Agent 决策框架，调用 LLM 并选择 action | coding agent harness，围绕代码理解和执行优化 |
| 输出结果 | 服务交付、链上交易、社交内容、Agent 间任务结果 | 代码变更、测试结果、解释、review、commit / PR |
| 可验证性 | 链上身份、声誉、支付、escrow、任务状态 | Git diff、测试日志、commit、PR、CI 结果 |
| 价值捕获 | Agent 可以 tokenized，服务收入和市场估值相关 | 价值主要体现在提高开发效率，不是独立资产 |

更具体地说，Codex 和 Claude Code 更像是开发者副驾驶升级版。它们可以读 repo、理解项目结构、编辑文件、运行测试、解释错误、修复 bug，甚至通过 MCP 接入 GitHub、Jira、数据库、Figma 等工具。

Virtuals Agent 的目标不一样。它不是专门服务开发者的 coding assistant，而是一个可以进入市场的 autonomous agent。它可以有自己的目标、人格、工具、钱包、服务能力和链上记录。通过 GAME，它决定下一步 action；通过 ACP，它可以和其他 Agent 做服务交易；通过 ERC-8004，它可以有链上身份、声誉和验证记录；通过 x402，它可以进行机器到机器的自动付款。

所以如果拿“自主性”来比较：

- Codex / Claude Code 的自主性是任务型自主：用户给一个开发任务，它在代码环境中规划、执行、验证。
- Virtuals Agent 的自主性是经济型自主：Agent 不只是完成一个任务，而是作为服务提供者或消费者，在开放市场中持续行动、交易和积累声誉。


## 参考资源

- Virtuals Protocol Whitepaper: https://whitepaper.virtuals.io/
- GAME by Virtuals Docs: https://docs.game.virtuals.io/
- ERC-8004 Trustless Agents: https://ercs.ethereum.org/ERCS/erc-8004
- Coinbase x402 Docs: https://docs.cdp.coinbase.com/x402/welcome
- Virtual Protocol GitHub: https://github.com/Virtual-Protocol
- Claude Code Docs: https://docs.anthropic.com/en/docs/claude-code/overview
- OpenAI Codex Help Center: https://help.openai.com/en/articles/11096431
