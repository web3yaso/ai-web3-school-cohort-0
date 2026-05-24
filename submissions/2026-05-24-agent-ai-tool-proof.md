# Agent / AI Tool Proof Record

提交日期：2026-05-24

## 1. 选择的 Agent / AI 工具

- **Codex Desktop / GPT-5 coding agent**：用于协助整理学习任务、生成可运行的 mock 实验、补充提交记录。
- **本地 deterministic mock agent**：仓库中的 Python 脚本模拟 Agent tool use、Agent workflow 和 prompt 输出，避免调用真实链上交易、真实 RPC 或外部模型 API。

相关文件：

- `experiments/web3_tool_use_mock.py`
- `experiments/agent_workflow_mock.py`
- `experiments/transaction_risk_summary_prompt.py`
- `prompts/transaction_risk_summary_prompt.md`

## 2. 让 Agent 帮我完成的学习任务

我让 Agent 协助完成 AI x Web3 School 的最小实践记录：

1. 设计一个 Web3 Tool Use mock：读取余额、读取 allowance、生成 approve 草稿、执行 policy check、记录 trace。
2. 设计一个 Agent Workflow mock：解释并准备一笔小额 ERC-20 swap，包含 task graph、状态机、模拟交易、人工确认和结果追踪。
3. 写一个交易风险摘要 prompt：输入交易信息，输出固定 JSON 风险摘要，并用三组 regression cases 校验。

## 3. 关键 prompt / 配置说明



```text
请作为我的 AI × Web3 School Learning Agent，先阅读启动 Prompt：https://aiweb3.school/learning-agent.zh.txt，并结合 Handbook：https://aiweb3.school/zh/handbook/，帮我初始化个人学习计划、GitHub 学习仓库、每日打卡草稿和 Handbook feedback 流程。
```

## 4. 一次成功输出记录

运行命令：

```text
我今天应该学什么？
```

成功输出摘录：

```text
今天最小路径，30 分钟

读 Agent Identity + AI Security
在 daily/2026-05-23.md 写 5 条 takeaway

今天推荐学习内容

Handbook Bridge 后半段：

Agent Identity
Trust & Reputation
Verifiable AI
AI Security
工程实践：

把昨天的两个 mock demo 加一点测试
重点测试这些边界：
不支持的 chain id 必须拒绝
无限授权必须拒绝
用户未确认不能发送交易
滑点过高不能继续 workflow
trace 必须记录 final_state 和 error
Hackathon 思考：

从昨天的“稳定币 / Agent Payment”出发，想一个项目方向：
“一个 Agent 如何在小额预算内安全地完成链上支付或结算？”
```

Agent Workflow 成功确认记录：

```text
已完成初始化，轻量版先跑起来了。
已初始化
学员画像：AI 有基础 / Web3 有基础 / 会基础脚本 / Hackathon 项目方向 / 每天约 1 小时 / 中文输出
GitHub repo：https://github.com/web3yaso/ai-web3-school-cohort-0
本地目录：ai-web3-school-cohort-0
Handbook：https://aiweb3.school/zh/handbook/
WCB Learning：https://web3career.build/zh/programs/AI-Web3-School#tab=learning
已更新文件
README.md (line 1)
profile.md (line 1)
learning-plan.md (line 1)
daily/2026-05-21.md (line 1)
templates/daily-note.md (line 1)
handbook-feedback/template.md (line 1)
我也加了 .gitignore (line 1)，确认 .env.local 和 .DS_Store 已被忽略，不会误进 public repo。
今日下一步
打开 WCB Learning 页面，确认今天的正式任务和打卡入口。
使用 daily/2026-05-21.md (line 1) 里的打卡草稿手动提交。
提交后把打卡链接写回 daily note。
提醒设置：未设置。
仍需手动完成：确认画像是否准确、登录 WCB 提交打卡、确认后再 commit && push 本次初始化变更。
```

Prompt regression 成功记录：

```json
{
  "case": "infinite_approval",
  "passed": true,
  "output": {
    "risk_level": "high",
    "requires_human_approval": true,
    "uncertainties": [
      "The approval amount appears to be unlimited."
    ]
  }
}
```

## 5. 人工复核、修正或拒绝 Agent 建议的记录



## 安全说明

```
````

本记录只包含 mock 地址、mock tx hash 和本地离线脚本输出。仓库不提交 API Key、token、私钥、助记词、`.env` 文件或任何敏感信息。
