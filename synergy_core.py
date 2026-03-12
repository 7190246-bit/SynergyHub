#!/usr/bin/env python3
"""
SynergyHub - Multi-Agent Collaboration Demo
一个简单的多Agent协作演示

功能：
1. 任务调度：分配任务给不同的Agent
2. Agent注册：支持多个Agent注册
3. 状态管理：跟踪每个Agent的状态
4. 协作执行：多个Agent并行处理任务
"""

import time
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    DONE = "done"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Agent:
    """Agent定义"""
    id: str
    name: str
    skill: str  # 技能：code/content/data/ops
    status: AgentStatus
    current_task: Optional[str] = None
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

@dataclass
class Task:
    """任务定义"""
    id: str
    title: str
    description: str
    skill_needed: str  # 需要的技能
    status: TaskStatus
    assigned_agent: Optional[str] = None
    result: Optional[str] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class AgentRegistry:
    """Agent注册中心"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
    
    def register(self, name: str, skill: str, capabilities: List[str] = None) -> Agent:
        """注册一个新的Agent"""
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        agent = Agent(
            id=agent_id,
            name=name,
            skill=skill,
            status=AgentStatus.IDLE,
            capabilities=capabilities or []
        )
        self.agents[agent_id] = agent
        print(f"✅ Agent注册成功: {name} (技能: {skill})")
        return agent
    
    def get(self, agent_id: str) -> Optional[Agent]:
        """获取Agent"""
        return self.agents.get(agent_id)
    
    def get_available(self, skill: str = None) -> List[Agent]:
        """获取可用的Agent"""
        available = [
            a for a in self.agents.values() 
            if a.status == AgentStatus.IDLE
        ]
        if skill:
            available = [a for a in available if a.skill == skill]
        return available
    
    def list_all(self) -> List[Agent]:
        """列出所有Agent"""
        return list(self.agents.values())

class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.pending: List[str] = []
    
    def add(self, title: str, description: str, skill_needed: str) -> Task:
        """添加任务"""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task = Task(
            id=task_id,
            title=title,
            description=description,
            skill_needed=skill_needed,
            status=TaskStatus.PENDING
        )
        self.tasks[task_id] = task
        self.pending.append(task_id)
        print(f"📝 任务添加: {title} (需要: {skill_needed})")
        return task
    
    def get_next(self, skill_needed: str = None) -> Optional[Task]:
        """获取下一个任务"""
        for task_id in self.pending:
            task = self.tasks[task_id]
            if task.status == TaskStatus.PENDING:
                if skill_needed is None or task.skill_needed == skill_needed:
                    return task
        return None
    
    def assign(self, task_id: str, agent_id: str):
        """分配任务"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.IN_PROGRESS
            task.assigned_agent = agent_id
            if task_id in self.pending:
                self.pending.remove(task_id)
    
    def complete(self, task_id: str, result: str):
        """完成任务"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.COMPLETED
            task.result = result
    
    def list_all(self) -> List[Task]:
        """列出所有任务"""
        return list(self.tasks.values())

class Orchestrator:
    """任务编排器 - 核心协调器"""
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.task_queue = TaskQueue()
        self.executors: Dict[str, Callable] = {}
        
        # 注册默认执行器
        self._register_default_executors()
    
    def _register_default_executors(self):
        """注册默认执行器"""
        self.executors["code"] = self._execute_code_task
        self.executors["content"] = self._execute_content_task
        self.executors["data"] = self._execute_data_task
        self.executors["ops"] = self._execute_ops_task
    
    def register_agent(self, name: str, skill: str, capabilities: List[str] = None) -> Agent:
        """注册Agent"""
        return self.registry.register(name, skill, capabilities)
    
    def add_task(self, title: str, description: str, skill_needed: str) -> Task:
        """添加任务"""
        return self.task_queue.add(title, description, skill_needed)
    
    def dispatch(self) -> bool:
        """调度任务给Agent"""
        # 获取所有可用Agent
        available_agents = self.registry.get_available()
        
        if not available_agents:
            print("⚠️ 没有可用的Agent")
            return False
        
        # 为每个可用Agent分配任务
        for agent in available_agents:
            # 查找匹配的任务
            task = self.task_queue.get_next(agent.skill)
            if task:
                # 分配任务
                self.task_queue.assign(task.id, agent.id)
                agent.status = AgentStatus.WORKING
                agent.current_task = task.id
                print(f"📤 分配任务 [{task.title}] -> {agent.name}")
                return True
        
        return False
    
    def execute_task(self, agent_id: str) -> bool:
        """执行任务"""
        agent = self.registry.get(agent_id)
        if not agent or agent.status != AgentStatus.WORKING:
            return False
        
        task = self.task_queue.tasks.get(agent.current_task)
        if not task:
            return False
        
        # 获取执行器
        executor = self.executors.get(task.skill_needed)
        if executor:
            result = executor(task)
            self.task_queue.complete(task.id, result)
            agent.status = AgentStatus.IDLE
            agent.current_task = None
            print(f"✅ 任务完成: {task.title} -> {result}")
            return True
        
        return False
    
    def _execute_code_task(self, task: Task) -> str:
        """执行代码任务"""
        return f"[代码] 已完成: {task.title}"
    
    def _execute_content_task(self, task: Task) -> str:
        """执行内容任务"""
        return f"[内容] 已完成: {task.title}"
    
    def _execute_data_task(self, task: Task) -> str:
        """执行数据任务"""
        return f"[数据] 已完成: {task.title}"
    
    def _execute_ops_task(self, task: Task) -> str:
        """执行运营任务"""
        return f"[运营] 已完成: {task.title}"
    
    def run(self, max_iterations: int = 10):
        """运行编排器"""
        print("\n" + "="*50)
        print("🚀 SynergyHub 多Agent协作系统启动")
        print("="*50 + "\n")
        
        iteration = 0
        while iteration < max_iterations:
            # 尝试分配任务
            dispatched = self.dispatch()
            
            # 执行任务
            for agent in self.registry.list_all():
                if agent.status == AgentStatus.WORKING:
                    self.execute_task(agent.id)
            
            # 检查是否还有待处理任务
            pending = [t for t in self.task_queue.list_all() 
                      if t.status == TaskStatus.PENDING]
            
            if not pending:
                print("\n✅ 所有任务已完成!")
                break
            
            time.sleep(0.5)
            iteration += 1
        
        # 打印总结
        self.print_summary()
    
    def print_summary(self):
        """打印总结"""
        print("\n" + "="*50)
        print("📊 执行总结")
        print("="*50)
        
        print(f"\n🤖 Agent数量: {len(self.registry.list_all())}")
        for agent in self.registry.list_all():
            print(f"   - {agent.name}: {agent.skill}")
        
        tasks = self.task_queue.list_all()
        print(f"\n📝 任务总数: {len(tasks)}")
        completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
        print(f"   ✅ 完成: {completed}")
        print(f"   ⏳ 待处理: {len(tasks) - completed}")


def demo():
    """演示"""
    # 创建编排器
    orchestrator = Orchestrator()
    
    # 注册Agent
    orchestrator.register_agent("小码", "code", ["Python", "JavaScript"])
    orchestrator.register_agent("小文", "content", ["写作", "编辑"])
    orchestrator.register_agent("小数", "data", ["分析", "可视化"])
    orchestrator.register_agent("小运", "ops", ["运营", "推广"])
    
    # 添加任务
    orchestrator.add_task("开发API接口", "开发一个用户管理API", "code")
    orchestrator.add_task("写一篇推文", "介绍我们的Agent平台", "content")
    orchestrator.add_task("分析用户数据", "分析本月的用户增长", "data")
    orchestrator.add_task("发布社交媒体", "在Twitter发布新功能", "ops")
    orchestrator.add_task("修复Bug", "修复登录问题", "code")
    orchestrator.add_task("写一篇博客", "技术博客关于多Agent协作", "content")
    
    # 运行
    orchestrator.run()


if __name__ == "__main__":
    demo()
