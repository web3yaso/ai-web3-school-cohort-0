# CAW + x402 Agent Commerce Paywall Demo

这个实验搭一个最小的 agent 自主支付闭环：

1. 服务提供方暴露 `GET /api/inference`。
2. 未付款请求收到 HTTP `402 Payment Required` 和 x402 风格付款要求。
3. 消费方 agent 读取付款条件，按 Pact/policy/budget 做本地预检。
4. 条件通过后，agent 付款并重试请求。
5. 服务端返回结果，并把要求、结算、结果和异常写入审计日志。

## 为什么接 CAW

Cobo Agentic Wallet 的核心是 Pact：用户批准某个具体任务的 intent、execution plan、policies 和 completion conditions。CAW 文档强调，agent 的每次操作都会先经过 Pact/policy 检查，超出预算、链、合约或时间窗口会被拒绝；操作也会留下完整 audit trail。

这里的 `policies/caw-pact-x402-base-sepolia.json` 是一个最小 Pact 模板：

- 单次 x402 付款最高 `$0.005`
- 日预算最高 `$0.02`
- 只允许 Base Sepolia：`eip155:84532`
- 只允许支付给 demo 收款地址
- 只允许访问 `GET /api/inference`
- 1 小时或 1 笔交易后自动结束

## 本地 mock 跑通

mock 模式不做真实链上付款，适合先验证协议控制流和审计记录。

```bash
cd experiments/caw-x402-paywall
npm run demo:mock
```

预期输出会包含：

- `result.signal`
- `receipt.paymentId`
- `receipt.settlementTx`

审计日志在：

```text
experiments/caw-x402-paywall/audit/events.jsonl
```

## 切到真实 x402 服务端

安装依赖：

```bash
cd experiments/caw-x402-paywall
npm install
```

复制环境变量：

```bash
cp .env.example .env
```

把 `.env` 改成真实收款地址：

```text
X402_MODE=real
PAY_TO=<你的 Base Sepolia EVM 收款地址>
NETWORK=eip155:84532
PRICE_USD=0.001
FACILITATOR_URL=https://x402.org/facilitator
```

启动服务端：

```bash
npm run server
```

x402 官方 seller quickstart 使用 `@x402/express`、`ExactEvmScheme` 和测试 facilitator。未付款请求会由 middleware 返回 402；付款后 middleware 负责验证和 settlement，再把请求放行到业务 handler。

## 用 CAW agent 支付

先按 CAW 文档/recipe 完成钱包创建、pairing、Pact 审批，并确保钱包在 Base Sepolia 上有测试 USDC。CAW 的 x402 recipe 建议使用 `caw fetch` 调用 x402 endpoint，并用 `--max-amount` 限制单次付款。

```bash
cd experiments/caw-x402-paywall
AGENT_MODE=caw npm run agent:caw
```

这个脚本会执行：

```bash
caw fetch http://127.0.0.1:4021/api/inference --max-amount 0.005
```

真实付款路径中，CAW 负责：

- 按已批准 Pact 检查付款是否在预算、链和收款方范围内
- 对符合条件的 x402 payment 进行签名/提交
- 让 facilitator 完成 settlement
- 保留 CAW 侧审计记录

本 demo 侧仍会把服务端结果和本地调用记录写入 `audit/events.jsonl`，方便复盘。

## 文件结构

```text
src/server.js                         # x402 paywall 服务端：mock 或真实 middleware
src/agent.js                          # 消费方 agent：mock policy check 或 caw fetch
src/mock-payment.js                   # 本地演示用付款 challenge/receipt 编码
src/audit.js                          # JSONL 审计日志
policies/caw-pact-x402-base-sepolia.json
```

## 参考资料

- CAW introduction: https://www.cobo.com/products/agentic-wallet/manual/start-here/introduction
- CAW Pact: https://www.cobo.com/products/agentic-wallet/manual/start-here/what-is-a-pact
- CAW Pact flow: https://www.cobo.com/products/agentic-wallet/manual/start-here/pact-flow
- CAW x402 recipe: https://www.cobo.com/agentic-wallet/recipes/x402-payment
- x402 docs index: https://docs.x402.org/llms.txt
- x402 seller quickstart: https://docs.x402.org/getting-started/quickstart-for-sellers
- x402 buyer quickstart: https://docs.x402.org/getting-started/quickstart-for-buyers
