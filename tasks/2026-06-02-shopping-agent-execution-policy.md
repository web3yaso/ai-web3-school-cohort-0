# 购物 Agent 低风险自动执行 / 高风险人工确认策略

## 核心原则

低风险动作可以自动执行，但必须同时满足：已授权任务、白名单商户、小额、付款类动作、时间窗口内、无异常信号。

只要出现金额变大、对象变新、权限变宽、动作不可逆、数据不一致、外部环境异常，就进入人工确认。

## 1. 低风险自动执行

满足以下全部条件时，agent 可以自动执行：

| 条件 | 要求 |
| --- | --- |
| 任务授权 | 当前存在已批准的购物 Pact |
| 金额 | 单笔不超过 100 USD |
| 总预算 | 未超过本次 Pact 总预算 |
| 商户 | 商户已在白名单内 |
| 收款地址 | 地址与 merchant ID 绑定且未变化 |
| Token | 只允许 USDC 或指定稳定币 |
| 合约 | 只调用白名单支付合约 |
| 动作 | 只允许付款类动作，如 `transfer` / `pay` / `settle` |
| 时间 | 在 Pact 有效期内，例如 1 小时 |
| 次数 | 未超过本次 Pact 允许付款次数 |
| 模拟结果 | 交易模拟成功，calldata 可解析 |
| 价格一致 | 商品页价格、订单价格、支付请求金额一致，或偏差在 3% 内 |

可自动执行的例子：

- 给已验证商户支付 42 USDC。
- 支付当前订单的运费和税费，且总价未超过预算。
- 查询余额、订单状态、物流状态。
- 付款失败后自动重试 1 次，且金额、地址、订单号完全一致。

## 2. 高风险人工确认

以下任一条件触发时，agent 必须暂停并请求用户确认：

| 触发条件 | 为什么需要人工确认 |
| --- | --- |
| 单笔金额超过 100 USD | 金额超出自动执行阈值 |
| 总价上涨超过 10% | 防止隐藏费用、税费或价格变更 |
| 新商户首次付款 | 防止伪商户或钓鱼地址 |
| 商户收款地址变化 | 防止地址替换攻击 |
| 商品类别高风险 | 礼品卡、订阅、数字资产、不可退款商品 |
| 需要 token approval | approval 会扩大未来风险 |
| 需要 permit / Permit2 | 虽然方便，但属于授权扩展 |
| 付款失败后重试超过 2 次 | 可能是订单状态或链上状态异常 |
| 订单金额与链上付款金额不一致 | 防止错误扣款 |
| 商品页、购物车、支付请求不一致 | 防止前端或商户 API 被篡改 |
| 调用新合约 | 防止恶意合约或未知代理合约 |
| 跨链付款 / bridge | 电商购物通常不需要跨链 |
| 修改收货地址 | 涉及隐私和欺诈风险 |
| 修改 Pact 预算、时间或范围 | 等于扩大 agent 权限 |
| 添加新白名单商户 | 改变长期信任边界 |
| 日累计超过 500 USD | 防止拆单绕过单笔限制 |
| 7 日累计超过 1500 USD | 防止长期小额损失累积 |
| 风控服务、RPC、价格服务异常 | 外部依赖不可靠时不应自动付款 |

## 3. 直接拒绝

以下动作不进入人工确认，默认拒绝：

| 动作 | 原因 |
| --- | --- |
| 向非白名单地址转账 | 与购物任务无关 |
| 调用 DEX swap | 购物 agent 不应交易资产 |
| 借贷、质押、桥接 | 超出购物场景 |
| NFT mint / marketplace buy | 除非用户单独批准 NFT 购物 Pact |
| `approve unlimited` | 未来可被持续盗取 |
| 修改 owner / recovery / guard | 涉及账户控制权 |
| 导出私钥 / 助记词 | 绝对禁止 |
| 关闭日志 | 破坏审计能力 |
| 绕过 policy engine | 破坏安全边界 |

## 4. 建议策略配置

```json
{
  "auto_execute": {
    "max_single_payment_usd": 100,
    "allowed_tokens": ["USDC"],
    "allowed_actions": ["transfer", "pay", "settle"],
    "merchant_status": "allowlisted",
    "max_retries": 1,
    "price_mismatch_tolerance_percent": 3,
    "requires_successful_simulation": true
  },
  "human_review": {
    "single_payment_above_usd": 100,
    "price_increase_above_percent": 10,
    "new_merchant": true,
    "merchant_address_changed": true,
    "token_approval_required": true,
    "subscription_or_gift_card": true,
    "retry_count_above": 2,
    "daily_spend_above_usd": 500,
    "weekly_spend_above_usd": 1500
  },
  "deny": {
    "non_allowlisted_recipient": true,
    "unlimited_approval": true,
    "dex_or_bridge_or_lending": true,
    "owner_or_recovery_change": true,
    "private_key_export": true,
    "policy_bypass": true
  }
}
```

## 总结

小额、白名单、付款类、任务内的动作可以自动执行；凡是扩大权限、增加金额、换商户、换地址、调用新合约、涉及授权或外部异常，都必须人工确认。
