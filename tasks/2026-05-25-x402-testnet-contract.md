# Week 1 Web3 任务：x402 相关最小测试网合约

## 任务目标

在测试网上部署或调用一个最小智能合约，理解以下关系：

- 合约部署后会得到一个合约地址
- 读取函数只读链上状态，通常不需要钱包签名
- 写入函数会改变链上状态，需要钱包人工签名并等待交易确认
- 区块浏览器可以验证合约地址、交易状态、事件日志和调用结果

本任务选择：部署一个 x402 相关的最小合约，并调用一个低风险写入函数。

## 独立 Solidity 文件

合约文件：

```text
contracts/X402ReceiptRegistry.sol
```

合约名称：

```text
X402ReceiptRegistry
```

这个文件是独立 Solidity 文件，可以直接复制到 Remix 编译和部署，不依赖 npm、Foundry、Hardhat 或 OpenZeppelin。

## 合约用途

`X402ReceiptRegistry` 用来记录一条 x402 风格的付款凭证摘要。

x402 的真实流程通常是：

1. 客户端请求某个 API。
2. 服务端返回 HTTP `402 Payment Required`。
3. 客户端签名付款授权，例如 EIP-3009 风格授权。
4. 服务端或 facilitator 验证并结算付款。
5. 服务端返回资源。

本合约不实现完整 x402 facilitator，也不做真实 USDC 结算。它只把一次 x402 风格付款请求/响应的摘要写到测试网，用来练习合约部署、读取、写入和区块浏览器验证。

## 安全边界

这个合约不会：

- 转出 ETH
- 转出 ERC-20
- 调用 `approve`
- 调用外部合约
- 保管任何资产

唯一的写入函数 `recordPayment(...)` 只会记录：

- `paymentId`
- `endpointHash`
- `token`
- `amount`
- 调用者地址 `msg.sender`
- 当前区块时间 `block.timestamp`

## 推荐网络

使用 Base Sepolia 测试网。

```text
Network: Base Sepolia
Chain ID: 84532
Explorer: https://sepolia.basescan.org/
```

部署和写入都必须由你本人在钱包中人工确认。不要使用主网，不要授权真实资产。

## 使用 Remix 部署

1. 打开 Remix：

```text
https://remix.ethereum.org/
```

2. 新建文件：

```text
X402ReceiptRegistry.sol
```

3. 把 `contracts/X402ReceiptRegistry.sol` 的完整内容复制进去。

4. 打开 Solidity Compiler。

5. 编译器版本选择：

```text
0.8.24 或更高的 0.8.x
```

6. 点击 Compile。

7. 打开 Deploy & Run Transactions。

8. Environment 选择：

```text
Injected Provider - MetaMask
```

9. 在钱包里确认当前网络是：

```text
Base Sepolia
```

10. Contract 选择：

```text
X402ReceiptRegistry
```

11. 填写构造参数：

```text
serviceName_: "x402-demo-weather"
paymentRecipient_: "<你的测试钱包地址>"
suggestedToken_: "0x0000000000000000000000000000000000000000"
suggestedAmount_: 1000
```

参数含义：

- `serviceName_`：这个 x402 服务的演示名称
- `paymentRecipient_`：收款方地址，练习时填你的测试钱包地址
- `suggestedToken_`：建议支付 token 地址，这里用零地址表示演示字段，不做真实 token 结算
- `suggestedAmount_`：建议支付数量，这里用 `1000` 做演示数值

12. 点击 Deploy。

13. 在 MetaMask 中人工确认部署交易。

确认前检查：

- 网络是 Base Sepolia
- 交易类型是合约部署
- 使用的是测试网 ETH 支付 gas
- 没有 token 授权提示
- 没有资产转账提示

14. 部署成功后，从 Remix 复制合约地址。

15. 在 BaseScan 搜索合约地址：

```text
https://sepolia.basescan.org/
```

## 读取函数练习

部署后，在 Remix 的 Deployed Contracts 面板调用以下读取函数。

读取函数不会改变链上状态，一般不需要钱包签名，也不会产生交易哈希。

### `serviceName()`

预期返回：

```text
x402-demo-weather
```

### `quote()`

预期返回类似：

```text
name: x402-demo-weather
recipient: <你的测试钱包地址>
token: 0x0000000000000000000000000000000000000000
amount: 1000
```

### `paymentCount()`

刚部署后预期返回：

```text
0
```

## 写入函数练习

调用写入函数：

```text
recordPayment(bytes32 paymentId, bytes32 endpointHash, address token, uint256 amount)
```

示例参数：

```text
paymentId: 0x0000000000000000000000000000000000000000000000000000000000000402
endpointHash: 0x1111111111111111111111111111111111111111111111111111111111111111
token: 0x0000000000000000000000000000000000000000
amount: 1000
```

点击 `transact` 后，必须在钱包中人工确认。

确认前检查：

- 网络是 Base Sepolia，不是主网
- To 是刚部署出来的合约地址
- Value 是 `0`
- 没有 token 授权
- 没有 token 转账
- Gas fee 使用测试网 ETH

确认后等待交易成功。

## 写入后验证

### 1. 在 Remix 读取 `paymentCount()`

写入成功后，`paymentCount()` 应从：

```text
0
```

变成：

```text
1
```

### 2. 在 Remix 读取 `getReceipt(paymentId)`

输入同一个 `paymentId`：

```text
0x0000000000000000000000000000000000000000000000000000000000000402
```

预期返回：

- `payer` 是你的钱包地址
- `token` 是零地址
- `amount` 是 `1000`
- `endpointHash` 是刚才输入的 hash
- `timestamp` 是链上记录时间

### 3. 在 BaseScan 查看写入交易

打开写入交易哈希对应的 BaseScan 页面，检查：

- Status 是 `Success`
- From 是你的钱包地址
- To 是合约地址
- Value 是 `0 ETH`
- Logs 中出现 `PaymentRecorded` 事件

## 待填写部署记录

| 项目 | 内容 |
| --- | --- |
| 测试网名称 | Base Sepolia |
| 部署钱包地址 | `TODO` |
| 合约地址 | `TODO` |
| 部署交易哈希 | `TODO` |
| 区块浏览器合约链接 | `TODO` |
| 写入函数 | `recordPayment(bytes32,bytes32,address,uint256)` |
| 写入交易哈希 | `TODO` |
| 读取函数验证 | `quote()` / `paymentCount()` / `getReceipt(bytes32)` |

## 我的理解

- 合约地址来自部署交易成功后的链上结果。
- 读取函数只是查询状态，不改变链上数据。
- 写入函数会改变链上状态，所以需要钱包签名、支付测试网 gas，并产生交易哈希。
- 区块浏览器可以帮助我验证交易是否成功、调用的是哪个合约、是否发出了事件。
- 本合约与 x402 的关系是记录付款凭证摘要，不负责真实支付结算。
