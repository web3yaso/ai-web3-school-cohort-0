"""
AI 基础实验 1：Prompt + Structured Output
目标：写一个 prompt，让模型输出机器可验证的 JSON
测试场景：交易风险摘要
"""

import json
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """你是一个交易风险分析助手。
当用户输入一笔交易的信息时，你必须返回一个 JSON 对象。

输出格式：
{
  "action": "转账/授权/交互",
  "assets_involved": ["asset1", "asset2"],
  "risk_level": "low/medium/high",
  "risk_factors": ["风险因素1", "风险因素2"],
  "warnings": ["警告信息"],
  "uncertainty": "模型不确定的地方"
}

规则：
- 如果不确定，uncertainty 字段必须说明
- 永远不要编造不在输入中的信息
- 高风险 = 涉及大额资产、未知合约、无限授权
"""

def analyze_transaction(transaction_info: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-7-2025",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"交易信息：{transaction_info}"}
        ]
    )
    
    result = json.loads(response.content[0].text)
    
    # 验证输出结构
    required_keys = ["action", "assets_involved", "risk_level", "risk_factors", "warnings", "uncertainty"]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"
    
    return result

# 测试用例
if __name__ == "__main__":
    test_cases = [
        "转账 0.1 ETH 给 0x123...456，Gas 正常",
        "授权合约 0xABC... 无限使用我的 USDC",
        "与未知合约交互，调用 swap 函数"
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n测试 {i+1}: {test}")
        result = analyze_transaction(test)
        print(json.dumps(result, indent=2, ensure_ascii=False))
