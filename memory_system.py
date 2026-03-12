#!/usr/bin/env python3
"""
SynergyHub - Agent Memory System
Agent记忆管理系统

功能：
1. 短期记忆：当前任务上下文
2. 长期记忆：Agent能力和经验
3. 共享记忆：Agent之间共享信息
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Memory:
    """记忆条目"""
    key: str
    value: str
    timestamp: str
    agent_id: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class ShortTermMemory:
    """短期记忆 - 当前任务上下文"""
    
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.items: List[Memory] = []
    
    def add(self, key: str, value: str, agent_id: str = None):
        """添加记忆"""
        memory = Memory(key=key, value=value, agent_id=agent_id)
        self.items.append(memory)
        
        # 保持最大数量
        if len(self.items) > self.max_items:
            self.items.pop(0)
        
        return memory
    
    def get(self, key: str) -> Optional[str]:
        """获取记忆"""
        for item in reversed(self.items):
            if item.key == key:
                return item.value
        return None
    
    def get_recent(self, n: int = 5) -> List[Memory]:
        """获取最近N条记忆"""
        return self.items[-n:]
    
    def clear(self):
        """清空短期记忆"""
        self.items.clear()

class LongTermMemory:
    """长期记忆 - Agent能力和经验"""
    
    def __init__(self):
        self.memories: Dict[str, List[Memory]] = {}
    
    def add(self, agent_id: str, key: str, value: str, tags: List[str] = None):
        """添加记忆"""
        if agent_id not in self.memories:
            self.memories[agent_id] = []
        
        memory = Memory(key=key, value=value, agent_id=agent_id, tags=tags)
        self.memories[agent_id].append(memory)
        return memory
    
    def get(self, agent_id: str, key: str = None) -> List[Memory]:
        """获取记忆"""
        if agent_id not in self.memories:
            return []
        
        if key:
            return [m for m in self.memories[agent_id] if m.key == key]
        return self.memories[agent_id]
    
    def search(self, query: str) -> List[Memory]:
        """搜索记忆"""
        results = []
        for memories in self.memories.values():
            for memory in memories:
                if query.lower() in memory.value.lower():
                    results.append(memory)
        return results
    
    def get_skills(self, agent_id: str) -> List[str]:
        """获取Agent技能"""
        memories = self.get(agent_id, "skill")
        return [m.value for m in memories]
    
    def add_skill(self, agent_id: str, skill: str):
        """添加技能"""
        self.add(agent_id, "skill", skill, tags=["skill"])
    
    def add_experience(self, agent_id: str, experience: str):
        """添加经验"""
        self.add(agent_id, "experience", experience, tags=["experience"])

class SharedMemory:
    """共享记忆 - Agent之间共享信息"""
    
    def __init__(self):
        self.global_memory: List[Memory] = []
        self.agent_relations: Dict[str, List[str]] = {}
    
    def share(self, agent_id: str, key: str, value: str):
        """共享信息"""
        memory = Memory(key=key, value=value, agent_id=agent_id, tags=["shared"])
        self.global_memory.append(memory)
        return memory
    
    def get_shared(self, key: str = None) -> List[Memory]:
        """获取共享信息"""
        if key:
            return [m for m in self.global_memory if m.key == key]
        return self.global_memory
    
    def add_relation(self, agent_id_1: str, agent_id_2: str, relation: str):
        """添加Agent之间的关系"""
        if agent_id_1 not in self.agent_relations:
            self.agent_relations[agent_id_1] = []
        self.agent_relations[agent_id_1].append(relation)
        
        if agent_id_2 not in self.agent_relations:
            self.agent_relations[agent_id_2] = []
        self.agent_relations[agent_id_2].append(relation)
    
    def get_relations(self, agent_id: str) -> List[str]:
        """获取Agent的关系"""
        return self.agent_relations.get(agent_id, [])

class AgentMemorySystem:
    """完整的Agent记忆系统"""
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.shared = SharedMemory()
    
    def remember(self, agent_id: str, key: str, value: str, memory_type: str = "short"):
        """记住信息"""
        if memory_type == "short":
            self.short_term.add(key, value, agent_id)
        elif memory_type == "long":
            self.long_term.add(agent_id, key, value)
        elif memory_type == "shared":
            self.shared.share(agent_id, key, value)
    
    def recall(self, agent_id: str, key: str = None, memory_type: str = "short") -> any:
        """回忆信息"""
        if memory_type == "short":
            if key:
                return self.short_term.get(key)
            return self.short_term.get_recent()
        elif memory_type == "long":
            return self.long_term.get(agent_id, key)
        elif memory_type == "shared":
            return self.shared.get_shared(key)
    
    def learn_skill(self, agent_id: str, skill: str):
        """学习新技能"""
        self.long_term.add_skill(agent_id, skill)
        # 共享这个信息
        self.shared.share(agent_id, "new_skill", f"{agent_id} learned {skill}")
    
    def share_experience(self, agent_id: str, experience: str):
        """分享经验"""
        self.long_term.add_experience(agent_id, experience)
        self.shared.share(agent_id, "experience", experience)
    
    def find_collaborators(self, agent_id: str, skill: str = None) -> List[str]:
        """找到协作者"""
        collaborators = []
        
        # 从共享记忆中查找
        shared_skills = self.shared.get_shared("new_skill")
        for memory in shared_skills:
            if memory.agent_id != agent_id and skill in memory.value:
                collaborators.append(memory.agent_id)
        
        return collaborators
    
    def get_status(self, agent_id: str) -> dict:
        """获取Agent状态"""
        skills = self.long_term.get_skills(agent_id)
        recent = self.short_term.get_recent(3)
        relations = self.shared.get_relations(agent_id)
        
        return {
            "agent_id": agent_id,
            "skills": skills,
            "recent_memory": [{"key": m.key, "value": m.value[:50]} for m in recent],
            "collaborators": relations
        }
    
    def summary(self) -> str:
        """获取记忆系统摘要"""
        total_short = len(self.short_term.items)
        total_long = sum(len(m) for m in self.long_term.memories.values())
        total_shared = len(self.shared.global_memory)
        
        return f"""
🧠 Agent记忆系统状态
━━━━━━━━━━━━━━━━
📝 短期记忆: {total_short} 条
📚 长期记忆: {total_long} 条
🔗 共享记忆: {total_shared} 条
🤝 Agent数量: {len(self.long_term.memories)}
"""


# 演示
def demo():
    """记忆系统演示"""
    memory_system = AgentMemorySystem()
    
    # Agent注册技能
    memory_system.learn_skill("agent_001", "Python")
    memory_system.learn_skill("agent_001", "数据分析")
    memory_system.learn_skill("agent_002", "内容创作")
    memory_system.learn_skill("agent_002", "社交媒体")
    
    # Agent记录经验
    memory_system.share_experience("agent_001", "完成了用户分析项目")
    memory_system.share_experience("agent_002", "策划了10篇爆款文章")
    
    # 短期记忆
    memory_system.remember("agent_001", "current_task", "开发API", "short")
    memory_system.remember("agent_001", "deadline", "今天完成", "short")
    
    # 查看状态
    print(memory_system.summary())
    
    print("\n📊 Agent 001 状态:")
    status = memory_system.get_status("agent_001")
    print(f"   技能: {', '.join(status['skills'])}")
    print(f"   最近: {status['recent_memory']}")
    
    # 找协作者
    print("\n🤝 找协作者:")
    collab = memory_system.find_collaborators("agent_001")
    print(f"   找到: {collab}")


if __name__ == "__main__":
    demo()
