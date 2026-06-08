# Week 3 Sponsor SDK / API Integration Plan

> 任务：Week 3｜Sponsor Workshop｜Sponsor SDK / API Integration Plan
> 项目来源：`~/Documents/cobo-agent-wallet`
> 项目名：Citely Reader
> Sponsor 对齐：Cobo / Agentic Commerce / Agentic Wallet

## 一句话计划

Citely Reader 会接入 Cobo Agentic Wallet / Pact 作为 AI Agent 的支付执行与权限边界，再通过 x402 读取 x402write 上的付费 Web3 法律、合规、安全风险报告。Week 4 的目标不是做完整内容平台，而是跑通一个最小闭环：用户提问 -> Agent 搜索报告 -> 命中 x402 paywall -> 校验付款要求 -> 通过 Cobo Agentic Wallet 支付 -> 重新请求拿到全文 -> 基于付费内容生成带引用的中文回答。

## 当前项目现状

本地项目 `~/Documents/cobo-agent-wallet` 已经是一个 Next.js 应用，核心模块如下：

| 模块 | 当前作用 | 状态 |
| --- | --- | --- |
| `app/api/agent/route.ts` | Agent 入口，接收用户问题，调用付费报告读取流程并流式返回结果 | 已实现基础流程 |
| `lib/x402write.ts` | 搜索报告、请求付费文章、处理 402、重试付费请求、缓存报告 | 已实现 |
| `lib/payment-requirements.ts` | 解析 `Payment-Required` header，并校验 network、asset、amount、self-send | 已实现并有测试 |
| `lib/cobo.ts` | 查询 Cobo pact 状态、生成 pact draft、通过 Cobo payment API 或 `caw fetch` 执行 x402 支付 | 已实现初版 |
| `app/api/pacts/draft/route.ts` | 输出 Citely Reader 的 Cobo Pact 草案 | 已实现 |
| `app/api/pacts/status/route.ts` | 查询 Cobo 钱包 / Pact 配置和状态 | 已实现 |
| `CITELY_READER_AGENT_PLAN.md` | 产品目标、x402 读取流程、Pact 设计、Agent 工具和行为规则 | 已完成设计文档 |
| `tests/payment-requirements.test.mjs` | 覆盖 Base USDC、Solana Devnet USDC、金额上限和 self-send 拒绝 | 已有测试 |

## 要接入什么

### 1. Cobo Agentic Wallet

接入目的：

- 让 Citely Reader Agent 可以在用户授权范围内为付费报告支付 USDC。
- 避免 Agent 直接持有私钥或无限制支配资金。
- 把“AI 可建议 / Agent 可执行 / 钱包强制边界”分开。

项目中对应模块：

- `lib/cobo.ts`
- `app/api/pacts/status/route.ts`
- `app/api/pacts/draft/route.ts`

需要配置：

- `COBO_API_KEY`
- `COBO_WALLET_UUID`
- `COBO_PACT_ID`
- `COBO_BASE_URL`
- `CAW_BIN`

### 2. Cobo Pact

接入目的：

- 限制 Agent 只能为 x402write 报告付款。
- 限制网络、资产、单笔金额、每日预算和每日次数。
- 拒绝 self-send、超额支付、非允许资产和非允许网络。

当前计划中的 Pact 边界：

- 协议：x402。
- 资产：USDC。
- 网络：Base mainnet 或 Solana Devnet；后续根据 Cobo 支持资产确认。
- 单篇报告上限：`0.50 USDC`。
- 24 小时预算：`5.00 USDC`。
- 24 小时付款次数：`50`。
- 有效期：7 天。

项目中已有 `buildCitelyReaderPactDraft()` 用于生成 Pact 草案。

### 3. x402write API

接入目的：

- 免费搜索报告目录。
- 访问付费报告时触发 HTTP `402 Payment Required`。
- 付款成功后返回全文、companion、作者和 EAS attestation 信息。

当前使用的 API：

```text
GET https://x402write.vercel.app/api/v1/articles
GET https://x402write.vercel.app/api/v1/articles?q=<query>
GET https://x402write.vercel.app/api/v1/articles/<slug>
```

项目中对应模块：

- `lib/x402write.ts`
- `lib/report-cache.ts`
- `lib/report-files.ts`

### 4. Vercel AI SDK / OpenAI

接入目的：

- 负责 Agent orchestration。
- 将用户自然语言问题映射到报告 slug 或搜索 query。
- 在读到付费报告后，基于报告内容生成中文解释。

边界：

- AI SDK 不负责支付权限。
- AI SDK 不接触私钥。
- AI SDK 不能绕过 Pact 或 payment requirement validation。

项目中对应模块：

- `app/api/agent/route.ts`
- `lib/answer.ts`
- `lib/ai-tools.ts`

## 怎么接

## Step 1: 用户输入与报告检索

用户可以输入：

- 报告 slug。
- 报告 URL。
- 自然语言问题，例如“为 Web3 公司工作有什么风险？”

Agent 流程：

1. `app/api/agent/route.ts` 接收 `message`。
2. `readPaidReport()` 调用 `resolveReport()`。
3. 如果用户没有给明确 slug，就先请求免费目录：

```text
GET /api/v1/articles?q=<query>
```

4. 如果匹配多篇报告，Agent 返回候选列表并暂停付款，避免误付费。

真实实现状态：已实现。

## Step 2: 请求付费报告并捕获 402

Agent 请求选定报告的 read path：

```text
GET /api/v1/articles/<slug>
```

如果报告需要付款，x402write 返回：

```text
HTTP 402 Payment Required
Payment-Required: <base64-json-or-json>
```

项目中 `getPaymentRequiredHeader()` 会提取：

- `Payment-Required`
- `payment-required`
- `X-Payment-Required`

真实实现状态：已实现。

## Step 3: 本地付款要求校验

`parsePaymentRequiredHeader()` 负责解析 header，提取：

- scheme
- network
- asset
- amount
- payTo

`validatePaymentRequirement()` 负责拒绝：

- 非 `exact` scheme。
- 不在白名单里的 network。
- 不在白名单里的 USDC asset。
- 超过 `MAX_REPORT_USDC` 的金额。
- payer 与 payTo 相同的 self-send。

真实实现状态：已实现，并有测试覆盖。

## Step 4: 通过 Cobo Agentic Wallet 支付

当前项目保留两种执行路径。

### 路径 A：Cobo payment API

`payX402Requirement()` 调用：

```text
POST {COBO_BASE_URL}/v1/wallets/{wallet_uuid}/payment
```

请求体包含：

```json
{
  "protocol": "x402",
  "payment_required": "<Payment-Required header>",
  "paymentRequired": "<Payment-Required header>"
}
```

期望返回：

```text
PAYMENT-SIGNATURE
```

然后 Agent 用该 signature retry 原始 GET 请求。

### 路径 B：`caw fetch`

`cawFetchX402()` 调用本地 `caw` CLI：

```text
caw fetch <COBO_PACT_ID> <readUrl> \
  --protocol x402 \
  --network <network> \
  --asset <asset> \
  --max-amount <MAX_REPORT_BASE_UNITS> \
  --output body
```

这条路径可能直接返回付费后的 body，适合作为 Week 4 demo 的主路径或 fallback。

真实实现状态：代码已写好，仍需要用真实 Cobo wallet、Pact、测试 USDC 和 x402write endpoint 做端到端验证。

## Step 5: 付款后重试并读取报告

如果支付 adapter 返回的是完整报告 JSON，`readPaidReport()` 直接解析。

如果支付 adapter 返回的是 `PAYMENT-SIGNATURE`，Agent 会重新请求：

```text
GET <readUrl>
PAYMENT-SIGNATURE: <signature>
```

成功后返回：

```json
{
  "slug": "...",
  "title": "...",
  "content": "...",
  "companion": "...",
  "citation": {
    "author": "...",
    "attestationUID": "0x...",
    "publishedAt": "..."
  }
}
```

真实实现状态：已实现。

## Step 6: 缓存与回答生成

付款成功后：

- `report-cache` 缓存付费报告，避免同一 slug 重复付款。
- `report-files` 保存报告内容。
- `answer` 基于报告 `content` 和 `companion` 生成中文回答。
- `report-history` 记录输入、slug、title、author、payment status。

真实实现状态：已实现基础版本。

## Week 4 是否能做完

判断：可以做完一个可演示 MVP，但需要控制范围。

### Week 4 可完成的真实实现

- 免费报告搜索。
- 命中 402 paywall。
- 解析 `Payment-Required` header。
- 本地校验 network、asset、amount、self-send。
- 输出 Pact draft。
- 查询 pact status。
- 通过 Cobo payment API 或 `caw fetch` 发起 x402 支付。
- 付款成功后读取全文。
- 缓存已购买报告。
- 用付费内容生成中文风险解释。
- 保存 read history / report files。
- 用测试或 mock 数据展示失败路径。

### Week 4 不建议做的范围

- 完整作者后台。
- 多作者收入分账。
- 真实会员订阅系统。
- 动态定价。
- 多链完整资产适配。
- 复杂仲裁 / 退款。
- 法律意见生成。
- 主网大额支付。

### Week 4 每日拆解

| 日期 | 目标 | 真实实现 | Mock / Fallback |
| --- | --- | --- | --- |
| Day 1 | 固定 MVP 范围和环境变量 | README、`.env.example`、Pact draft、API flow 文档 | 如果 Cobo schema 未确认，保留字段映射 TODO |
| Day 2 | 跑通 x402write 搜索和 402 捕获 | `GET /articles`、`GET /articles/:slug`、payment header parse | 用本地 mock 402 response 覆盖失败场景 |
| Day 3 | 接 Cobo payment path | `caw fetch` 或 Cobo payment API，拿到 signature/body | 如果真实支付失败，用 mock signature + mock paid report |
| Day 4 | 做端到端 Agent demo | 用户输入 -> 搜索 -> 付款 -> 读取 -> 中文回答 | 如果 Cobo 不稳定，用缓存报告演示 answer path |
| Day 5 | 打包提交材料 | demo 截图、README、风险边界、真实/模拟说明 | 准备 CLI log / API response 截图替代视频 |

## Fallback Plan

### Fallback 1: Cobo API schema 或权限未完全确认

处理方式：

- 保留 `app/api/pacts/draft/route.ts` 输出 Pact 草案。
- 用 `caw fetch` CLI 作为优先验证路径。
- README 中标注：Cobo API 字段仍需按官方最终 schema 校准。

可展示内容：

- Pact policy 设计。
- 支付前本地校验。
- `caw fetch` 命令形态。
- 失败日志与需要 sponsor 确认的问题。

### Fallback 2: 真实 USDC / 测试网支付失败

处理方式：

- 使用 mock payment adapter。
- mock adapter 返回 paid report JSON 或 mock `PAYMENT-SIGNATURE`。
- 保留真实 `Payment-Required` 解析和校验。

可展示内容：

- 未付款返回 402。
- 校验通过后进入支付阶段。
- mock payment 生成 receipt。
- retry 后读取报告。

### Fallback 3: x402write 服务不稳定

处理方式：

- 准备本地 fixture：
  - catalog response
  - 402 response
  - paid report response
- 用相同接口形状跑 demo。

可展示内容：

- Agent flow 不变。
- 只替换 provider endpoint。
- README 明确说明 provider 使用 fixture。

### Fallback 4: 模型 API 不可用

处理方式：

- 跳过 LLM answer generation。
- 直接返回报告 `content`、`companion` 和 citation。
- 用预生成中文回答作为演示材料。

可展示内容：

- 支付和报告读取链路仍然成立。
- AI 回答层暂时降级。

## 风险与待确认问题

| 风险 / 问题 | 影响 | 当前处理 |
| --- | --- | --- |
| Cobo Pact 字段是否完全匹配官方 API | Pact 可能无法直接创建 | 先用 draft route 输出设计，实际字段与 sponsor / docs 对齐 |
| Base mainnet / Solana Devnet asset id 是否与 Cobo 支持列表一致 | payment 可能被拒绝 | `COBO_X402_CHAIN_IDS` 和 `COBO_X402_TOKEN_REFS` 做成 env 可配置 |
| x402write 是否稳定返回 `Payment-Required` header | 无法进入支付阶段 | 支持多个 header name，并准备 fixture fallback |
| `payment API` 返回字段可能不同 | 无法拿到 `PAYMENT-SIGNATURE` | 兼容 `payment_signature`、`paymentSignature`、`PAYMENT_SIGNATURE`、headers |
| 误付费 / 重复付费 | 浪费预算 | report cache、候选歧义暂停、本地校验、Pact budget |
| self-send | x402write 拒绝或形成无效支付 | 本地校验 payer address 与 payTo，不允许相同 |
| 法律回答越界 | 用户误以为是法律建议 | `answer` 层只基于报告内容回答，并加入风险教育 / 非法律建议边界 |

## 需要 Sponsor / Mentor 帮忙确认的问题

1. Cobo Agentic Wallet x402 payment API 的最终请求 / 响应字段是否以 `payment_required` 和 `PAYMENT-SIGNATURE` 为准？
2. Pact policy 中表达 x402-only、USDC-only、单笔上限、每日预算、每日次数的推荐字段是什么？
3. Base mainnet / Base Sepolia / Solana Devnet 在 Cobo 中推荐使用哪些 chain id 和 token id？
4. `caw fetch` 和 REST payment API 在 Hackathon demo 中哪条路径更推荐？
5. 如果 x402write 返回的是 Base mainnet USDC payment requirement，测试环境应该用真实小额 Base USDC，还是 sponsor 提供测试 endpoint？

## 最小验收标准

Week 4 最低可交付版本必须能展示：

1. 用户提出一个报告阅读问题。
2. Agent 搜索免费 catalog。
3. Agent 选择报告或要求用户澄清。
4. Agent 请求报告并收到 402。
5. Agent 解析并校验 payment requirement。
6. Agent 通过 Cobo path 或 fallback path 完成支付。
7. Agent 读取全文并缓存。
8. Agent 基于全文生成中文回答。
9. README 标明真实实现、mock/fallback、风险边界和下一步。

## 结论

Citely Reader 与 Cobo Sponsor Workshop 的对齐点非常清楚：它不是泛泛展示“AI + 钱包”，而是展示一个 Agent 在受控 Pact 边界内为 x402 付费内容完成小额 USDC 支付，并把支付结果转化为可引用的知识回答。

Week 4 可完成一个可演示的 MVP。真实实现重点应放在 x402 payment requirement 解析、本地校验、Cobo payment / `caw fetch` 接入、报告读取和中文回答生成；CAW API schema、真实链上支付、完整 Pact 创建和多链资产细节可以作为 fallback 或 sponsor 待确认项，不阻塞 demo 主线。

