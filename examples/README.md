# 示例代码

本目录包含 SynergyHub 的示例代码，演示多 Agent 协作的核心功能。

## 文件说明

| 文件 | 说明 |
|------|------|
| `multi_agent_demo.py` | 多 Agent 协作完整示例 |
| `README.md` | 本文件 |

## 运行示例

```bash
# 确保 Python 版本 >= 3.8
python3 examples/multi_agent_demo.py
```

## 示例输出

```
==================================================
🚀 SynergyHub 多 Agent 协作流程启动
==================================================

🤔 需求诊断师 正在思考: 我们需要一个小红书运营助手，能自动发笔记、回复评论、数据分析

📋 需求诊断结果: {'demand_type': 'custom_agent', 'required_skills': ['social_media', 'content_generation', 'data_analysis'], 'complexity': 'high', 'suggested_agents': 3}

🤔 能力评测师 正在思考: {...}

📊 能力评测结果: {...}

⚙️ 集群配置结果: {...}

==================================================
✅ 流程完成！
==================================================
```

## 扩展阅读

- [技术架构详解](../docs/architecture.md)
- [Agent 评测体系](../docs/evaluation/)
