# Task: Prompt Minimal Practice - Transaction Risk Summary

## 任务目标

完成 Handbook `提示词（Prompt）` 的最小实践：写一个“交易风险摘要”prompt，让模型基于交易信息输出固定 JSON，并准备三组测试。

## 输入字段

- `target_address`
- `function_name`
- `parameters`
- `asset_changes`
- `simulation_result`
- `user_intent`

## 输出字段

- `summary`
- `asset_changes`
- `permissions_changed`
- `risk_level`
- `requires_human_approval`
- `uncertainties`
- `recommended_user_checks`

## 工程实现

- Prompt 文件：`prompts/transaction_risk_summary_prompt.md`
- 测试脚本：`experiments/transaction_risk_summary_prompt.py`
- 测试方式：离线 mock model + schema 校验 + regression cases

## 三组测试

1. 普通转账：应标记为 `low`，但仍然需要 human approval。
2. 无限授权：应标记为 `high`，并在 uncertainties 中说明 unlimited approval 风险。
3. 目标地址与用户意图不匹配：应标记为 `high`，并提示 recipient mismatch。

## 运行方式

```bash
python3 experiments/transaction_risk_summary_prompt.py
```

查看 prompt：

```bash
python3 experiments/transaction_risk_summary_prompt.py --show-prompt
```

## 完成情况

- 已完成 prompt。
- 已完成固定 JSON schema 校验。
- 已完成三组 regression tests。
- 当前脚本不调用真实模型，方便公开仓库离线运行。

## 参考资源

- https://aiweb3.school/zh/handbook/ai/prompt/#%E6%9C%80%E5%B0%8F%E5%AE%9E%E8%B7%B5
