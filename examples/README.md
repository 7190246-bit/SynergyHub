# 📚 SynergyHub 示例

这里提供多种场景的多 Agent 协作示例，帮助你快速上手。

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/7190246-bit/SynergyHub.git
cd SynergyHub

# 运行示例
python examples/multi_agent_demo.py
```

## 📦 示例列表

| 示例 | 场景 | 文件 |
|------|------|------|
| 多 Agent 基础 | 多 Agent 协作基础架构 | `multi_agent_demo.py` |
| 智能客服 | 企业客服场景 | `customer_service_demo.py` |
| 内容团队 | 内容生产流水线 | `content_team_demo.py` |

## 🎯 使用场景

### 1. 智能客服
```
客户咨询 → 意图识别 → 智能分流 → Agent 处理 → 满意度回访
```

### 2. 内容生产
```
选题策划 → AI 写作 → 人工审核 → 多平台发布
```

### 3. 数据分析
```
数据采集 → 清洗处理 → 分析洞察 → 报告生成
```

## 🔧 自定义示例

参考现有示例，创建你自己的场景：

```python
from synergy_core import Orchestrator

# 创建编排器
orchestrator = Orchestrator()

# 注册你的 Agent
orchestrator.register_agent("Agent名称", "角色", ["技能列表"])

# 分发任务
orchestrator.assign_task("Agent名称", "任务描述")
```

---

更多示例持续更新中！
