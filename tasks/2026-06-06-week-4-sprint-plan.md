# Week 4 Sprint Plan: Citely Hackathon MVP

> 项目：Citely
> 赛道：Cobo / Agentic Commerce
> 目标：5 天内跑通一个可演示的 Agent-Native Paid Content MVP。

## 项目目标

Citely 要验证的最小闭环是：

1. 作者发布一篇专业内容，并留下可验证出处。
2. 读者或 AI Agent 可以免费发现文章列表。
3. 当 Agent 请求阅读付费全文时，服务端返回 HTTP 402 payment required。
4. Agent 在预算与权限边界内完成 USDC 支付。
5. 支付成功后，服务端返回全文、作者信息、支付 receipt 和内容出处证明。

## Demo 成功标准

- 可以打开一个最小前端或 API demo，展示文章发现、付费解锁、证明查看三段流程。
- 未付款访问全文时稳定返回 `402 Payment Required`。
- 付款成功后返回 `200 OK`，包含全文、作者、支付记录和证明信息。
- README 说明哪些部分是真实实现，哪些是 mock / fallback。
- 能解释 CAW / Pact 如何限制预算、域名、单笔金额、时间窗口和可调用接口。

## Day 1: MVP Scope & Data Contract

### 今日目标

- 冻结 Citely Week 4 的 MVP 范围。
- 明确 API、数据结构、演示路径和不做事项。
- 把项目从“概念 proposal”切到“可跑 demo”。

### 真实实现

- 整理 README 的 MVP 章节：
  - problem
  - users
  - demo flow
  - tech stack
  - real vs mock boundary
  - risks
- 定义最小数据模型：
  - `Article`
  - `Author`
  - `PaymentReceipt`
  - `ContentProof`
  - `AgentPolicy`
- 定义 API 草图：
  - `GET /api/v1/articles?q=`
  - `GET /api/v1/articles/:slug/read`
  - `POST /api/v1/payments/verify`
  - `GET /api/v1/articles/:slug/proof`
- 准备 2-3 篇 seed article，用于 demo。

### Mock / Fallback

- 作者发布后台可以不做，先用静态 seed data。
- 搜索可以先做关键词过滤，不接真实向量数据库。
- 内容 proof 可以先用固定的 attestation hash / mock EAS record。

### 验收标准

- README 能让评委在 2 分钟内理解 Citely 是什么。
- API contract 和 demo flow 写清楚。
- 至少有 2 篇可发现文章和 1 篇付费文章。

## Day 2: x402 Paywall Flow

### 今日目标

- 跑通未付款访问返回 402、付款后解锁全文的核心 paywall 逻辑。
- 让 Agent 或脚本能完整复现一次请求流程。

### 真实实现

- 实现 `GET /api/v1/articles`：
  - 返回文章标题、摘要、作者、价格、read URL。
- 实现 `GET /api/v1/articles/:slug/read`：
  - 无有效 payment proof 时返回 `402`。
  - 返回 payment requirement，包括金额、币种、收款地址或 receiver、network、resource。
  - 有有效 proof 时返回全文。
- 实现最小 payment verification：
  - 校验 receipt id / tx hash / signed payload 是否存在。
  - 将成功记录写入本地 JSON / SQLite / memory store。
- 写一个 `demo-agent` 脚本：
  - 发现文章
  - 请求全文
  - 收到 402
  - 提交 payment proof
  - 重新请求并拿到全文

### Mock / Fallback

- 如果真实 x402 SDK 接入卡住，可以先用兼容 x402 语义的 mock payment requirement。
- 如果测试网支付不稳定，可以用本地 signed receipt 代替真实链上交易。
- 如果钱包签名流程未完成，可以手动生成 mock receipt。

### 验收标准

- 未付款请求必定返回 402。
- 付款 proof 成功后可以返回全文。
- demo-agent 脚本可以从头到尾跑通一次。

## Day 3: CAW / Pact Permission Boundary

### 今日目标

- 展示 Agent 不是“无限自动付款”，而是在用户授权的 pact / policy 边界内执行。
- 把预算、域名、时间窗口、单笔金额和操作范围写进可读配置。

### 真实实现

- 定义 `AgentPolicy`：
  - allowed domain
  - max amount per transaction
  - daily / session budget
  - token / network
  - allowed action
  - expires at
- 在 demo-agent 付款前增加 policy check：
  - 超出预算则拒绝付款。
  - 非白名单 domain 则拒绝付款。
  - 超出时间窗口则拒绝付款。
  - 非文章解锁 action 则拒绝付款。
- 在 README 中写清 CAW / Pact 在真实版本里的职责：
  - 用户授权
  - Agent 执行
  - 钱包强制策略
  - 交易与审计记录

### Mock / Fallback

- 如果 CAW SDK 无法在 Week 4 完整接入，可以用 `policy.json` + 本地校验模拟 Pact。
- 如果无法真实持有 USDC，可以用 testnet receipt 或 mock wallet event 展示流程。
- 如果 Base 主网 / 测试网集成不稳定，可以保留 CAW API 调用伪代码和失败截图。

### 验收标准

- demo 中能展示至少 2 个失败路径：
  - 超预算拒绝
  - 非白名单资源拒绝
- 能展示 1 个成功路径：
  - policy 允许 -> payment proof 生成 -> 解锁内容。
- README 清楚区分真实实现和 CAW fallback。

## Day 4: Content Proof & Audit Trail

### 今日目标

- 让 Citely 不只是 paywall，还能证明作者、内容出处和支付记录。
- 补齐 Web3 机制在项目中的不可替代性。

### 真实实现

- 为每篇文章补充 `ContentProof`：
  - author address
  - content hash
  - attestation id 或 mock attestation id
  - chain
  - timestamp
- 实现 `GET /api/v1/articles/:slug/proof`：
  - 返回作者信息、content hash、attestation / transaction link。
- 支付成功后返回 audit trail：
  - request id
  - payment receipt
  - policy id
  - article slug
  - unlocked at
- 在前端或 README 中展示：
  - 这篇内容是谁发布的
  - 内容 hash 是什么
  - 支付记录如何对应解锁动作

### Mock / Fallback

- 如果 EAS on Base 来不及真实写入，可以用预生成 attestation hash 或 mock explorer link。
- 如果没有真实链上证明，可以用 `contentHash = sha256(markdown)` 作为本地可验证证明。
- 如果前端来不及做完整 proof view，可以用 API response + README 截图说明。

### 验收标准

- 每篇付费内容至少有一个 content hash。
- 支付解锁记录能和文章 slug、policy、receipt 关联。
- 演示中能说明：为什么这不是普通 Web2 paywall。

## Day 5: End-to-End Demo & Submission Pack

### 今日目标

- 打磨完整演示链路。
- 补齐文档、截图、风险边界和提交材料。
- 准备 Hackathon 最终展示。

### 真实实现

- 跑通完整 demo：
  - Agent 发现文章
  - Agent 请求全文
  - 服务端返回 402
  - Agent 检查 policy
  - Agent 提交 payment proof
  - 服务端返回全文
  - 返回 receipt + content proof
- 录制短 demo 或保存关键截图。
- 完善 README：
  - Quick start
  - Demo script
  - API examples
  - Architecture
  - Real vs mock
  - Risks and limitations
  - Future work
- 整理 submission pack：
  - repo link
  - demo link / screenshots
  - architecture diagram
  - risk memo
  - sponsor alignment
  - fallback explanation

### Mock / Fallback

- 如果真实支付链路仍不稳定，最终 demo 可以采用：
  - mock x402 requirement
  - mock CAW policy enforcement
  - mock receipt
  - real API flow
  - real content unlock
- 如果前端不够完整，用 CLI demo + API screenshots 作为主展示。
- 如果链上 proof 不稳定，用 content hash + mock attestation + 未来接入计划说明。

### 验收标准

- 一个新评委可以按 README 在本地或线上复现 demo。
- 至少有一条完整成功路径和两条失败路径。
- 所有 mock / fallback 都明确标注，不夸大真实完成度。
- 项目能清楚回答：
  - Agent 买了什么？
  - 谁收款？
  - 钱包权限如何限制？
  - 支付后如何解锁？
  - 内容和支付如何审计？

## 功能优先级

### 必须真实实现

- 文章发现 API。
- 未付款返回 402。
- 付款 proof 后解锁全文。
- Agent policy 本地校验。
- 支付 / 解锁 audit trail。
- README 和 demo script。

### 优先真实，必要时 fallback

- x402 SDK 或兼容实现。
- CAW / Pact 授权与支付执行。
- Base / EAS 内容证明。
- 前端 proof view。

### 可以 mock

- 作者后台发布。
- 完整搜索 / 推荐系统。
- 真实订阅计费。
- 仲裁流程。
- 多作者收入分账。
- 多 Agent marketplace。

### 暂不做

- 平台级账号系统。
- 复杂 CMS。
- 真实 KYC / 合规审核。
- 主网大额支付。
- 完整移动端适配。
- 长期订阅自动续费。

## 风险与应对

| 风险 | 影响 | 应对 |
| --- | --- | --- |
| CAW SDK 接入时间不足 | 无法展示真实钱包执行 | 用 policy.json + mock receipt 展示 Pact 语义，并保留 SDK 接入计划 |
| x402 支付链路不稳定 | 402 支付无法真实闭环 | 保留真实 API flow，用 mock payment proof 跑通演示 |
| EAS 写入或查询不稳定 | 内容出处证明不完整 | 使用 content hash + mock attestation id，说明后续替换点 |
| Scope 膨胀 | 5 天内无法交付 | 只保留发现、402、支付、解锁、证明五段 |
| Demo 环境失败 | 展示风险高 | 准备 CLI demo、API screenshots、录屏三套 fallback |

## 最终提交清单

- Citely repo / README。
- Demo script 或 demo URL。
- x402 paywall API 示例。
- CAW / Pact policy 示例。
- Payment receipt / audit trail 示例。
- Content proof 示例。
- 架构图或流程图。
- Real vs mock 边界说明。
- Week 4 总结与下一步计划。

