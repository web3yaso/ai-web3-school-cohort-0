# Agent Profile 草图

如何被调用
    - 生产：GitHub Actions workflow news-rss.yml，周日 02:00 UTC cron 触发，先跑 news poll，再调 agent
    - 手动：gh workflow run news-rss.yml（workflow_dispatch）或本地 npx tsx scripts/agents/publish-decision-agent.ts
    - 不可被外部 API 触发：agent 自己不暴露 HTTP endpoint；它是一个 scheduled job，不是 server

    如何收费
    - Agent 本身免费调用（决策器是内部组件，不向外计费）
    - 决策为 publish 时产出的报告通过 x402 micropayment 售卖：GET /api/reports/global-stablecoin-policy-report，固定 $0.10 USDC，Base mainnet 结算
    - 每周固定 slug 覆盖式刷新，订阅者付一次拿当前最新版
    - Agent 的运营成本（Anthropic Sonnet ~$0.05/决策 + web_search ~$0.01–0.08/决策 + 报告生成 ~$0.10）由 repo 所有者吸收，月度预算 hard cap $5

    如何被验证
    - 决策透明度：每次决策档案 commit 进 repo 的 data/reports/decisions/<date>.json，公开审计，包含
    reasoning、key_events、sources_consulted、tool_calls.web_search 次数
    - 报告内容验证：报告 markdown 末尾 ## Sources 段列出 8–15 个原始引用（每个 source URL 都通过 post-parse 验证必须存在于 input news 的 url 集合，杜绝 LLM
    编造）
    - Agent 自身的 signal 验证：决策前用 web_search 对 high-impact claim 拉一手链接确认（"是否真的发生" / "是否最近发生" / "是否已被报道过"）
    - Workflow 日志：每次 run 输出 agent-decision: publish|skip confidence=X budget=$Y/cap 单行汇总，可在 GitHub Actions UI 看

    失败如何处理
    - Anthropic API 宕机 / 超时：fallback 到 publish（对付费订阅者更安全，避免无故空窗）
    - JSON parse 失败：同上，fallback publish + 日志记录原始 LLM 输出
    - Web search 全部失败：agent 继续基于纯 digest 做决策（降级模式），日志标注
    - 月预算耗尽（agent-budget.json 累计超过 $5）：强制 skip 当周 + 日志告警；下月 1 号自动重置
    - 决策为 publish 但 generate-daily-report.ts 失败：保留旧报告不动，决策档案标记 publish_attempted_failed，等下次 cron 重试
    - 连续 skip：不做特殊处理，永远交给 LLM 判断；所有者从决策档案 / 月报中人工监控
    - GitHub Actions 调度失败 / workflow 被 disable：不会自动恢复，所有者手动 enable + workflow_dispatch（最近一次实际事件就是 5/18 之后 workflow 被手动 disable
     导致 12 天无更新）