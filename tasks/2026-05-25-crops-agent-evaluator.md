# Task: CROPS Agent Evaluator Minimal Practice

## 任务目标

把 CROPS 框架实现成一个可运行的小工具，用来评估 AI x Web3 项目想法是否符合：

- Censorship Resistant
- Open Source
- Private
- Secure

## 工程实现

- 脚本：`experiments/crops_agent_evaluator.py`
- 输入：一段 AI x Web3 idea
- 输出：四个维度的评分、命中关键词、风险提示和总评
- 依赖：Python 标准库，无 API key

## 运行方式

默认示例：

```bash
python3 experiments/crops_agent_evaluator.py
```

自定义 idea：

```bash
python3 experiments/crops_agent_evaluator.py --idea "An open source agent payment app with spending limit, simulation and human confirmation."
```

## 完成情况

- 已实现离线 evaluator。
- 已覆盖 CROPS 四个维度。
- 当前版本使用关键词启发式，不代表严格安全审计。

## 参考资源

- `daily/2026-05-23.md`
- https://ethskills.com/
