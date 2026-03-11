# SynergyHub 项目结构

```
SynergyHub/
├── README.md              # 项目介绍
├── LICENSE                # MIT 开源协议
├── docs/                  # 文档目录
│   ├── architecture.md    # 技术架构详解
│   ├── multi-agent-demo/ # 多 Agent 协作示例
│   └── evaluation/       # Agent 评测体系
├── src/                   # 源代码
│   ├── agents/           # Agent 定义
│   │   ├── demand_diagnosis/    # 需求诊断 Agent
│   │   ├── capability_eval/      # 能力评测 Agent
│   │   └── cluster_config/      # 集群配置 Agent
│   ├── workflows/         # 工作流
│   │   ├── demand_analysis.flow
│   │   ├── agent_evaluation.flow
│   │   └── cluster_setup.flow
│   └── utils/           # 工具函数
│       ├── memory_manager.py
│       └── tool_registry.py
└── examples/            # 示例代码
    ├── basic_demo.py     # 基础示例
    └── multi_agent_demo.py # 多 Agent 协作示例
```

---

## 快速开始

### 1. 基础示例

```python
from src.agents.demand_diagnosis import DemandDiagnosisAgent

# 创建需求诊断 Agent
agent = DemandDiagnosisAgent()

# 分析业务需求
result = agent.analyze("我们需要一个小红书运营助手，能自动发笔记、回复评论")

print(result)
# 输出：{
#   "agent_type": "social_media_operator",
#   "required_skills": ["content_generation", "comment_reply", "data_analysis"],
#   "complexity": "medium"
# }
```

### 2. 多 Agent 协作示例

```python
from src.workflows.multi_agent import MultiAgentWorkflow
from src.agents.demand_diagnosis import DemandDiagnosisAgent
from src.agents.capability_eval import CapabilityEvalAgent
from src.agents.cluster_config import ClusterConfigAgent

# 定义 Agent 列表
agents = [
    DemandDiagnosisAgent(),
    CapabilityEvalAgent(),
    ClusterConfigAgent()
]

# 创建工作流
workflow = MultiAgentWorkflow(agents)

# 执行完整流程
result = workflow.execute(company_needs="跨境电商客服系统")
```

---

## 核心概念

### 1. 三层记忆架构

- **短期记忆**：最近对话上下文（50 轮）
- **中期记忆**：每周经验总结（30 天）
- **长期记忆**：核心配置和偏好

### 2. 权限三层模型

- **核心权限**：创建/销毁 Agent、分配权限
- **执行权限**：调用工具、读写资源（有超时）
- **观察权限**：只读日志和状态

### 3. 任务调度

- 依赖声明式任务图
- 循环依赖检测
- 失败自动降级

---

## 技术栈

- **框架**: OpenClaw
- **语言**: Python
- **多 Agent**: sessions_spawn, sessions_send
- **记忆**: 三层记忆架构

---

## 贡献指南

欢迎提交 Issue 和 PR！

---

*🦞 Built with OpenClaw - 让 AI 成为你的伙伴*
