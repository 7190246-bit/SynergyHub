#!/usr/bin/env python3
"""
SynergyHub - Task Scheduler
任务调度器

功能：
1. 优先级调度
2. 时间片轮转
3. 负载均衡
4. 故障恢复
"""

import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import heapq

class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ScheduledTask:
    """调度任务"""
    id: str
    name: str
    priority: Priority
    state: TaskState
    created_at: datetime
    scheduled_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    worker_id: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    result: Optional[str] = None
    error: Optional[str] = None

class Worker:
    """工作节点"""
    def __init__(self, id: str, name: str, capacity: int = 1):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.current_tasks: List[str] = []
        self.busy = False
    
    def can_accept(self) -> bool:
        return len(self.current_tasks) < self.capacity
    
    def assign(self, task_id: str):
        self.current_tasks.append(task_id)
        self.busy = True
    
    def complete(self, task_id: str):
        if task_id in self.current_tasks:
            self.current_tasks.remove(task_id)
        self.busy = len(self.current_tasks) > 0

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.workers: Dict[str, Worker] = {}
        self.priority_queue: List[tuple] = []  # (priority, time, task_id)
    
    def add_worker(self, worker_id: str, name: str, capacity: int = 1):
        """添加工作节点"""
        worker = Worker(worker_id, name, capacity)
        self.workers[worker_id] = worker
        print(f"✅ Worker添加: {name} (容量: {capacity})")
    
    def submit(self, name: str, priority: Priority = Priority.NORMAL, 
               scheduled_at: datetime = None, 
               dependencies: List[str] = None,
               max_retries: int = 3) -> str:
        """提交任务"""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        if scheduled_at is None:
            scheduled_at = datetime.now()
        
        task = ScheduledTask(
            id=task_id,
            name=name,
            priority=priority,
            state=TaskState.PENDING,
            created_at=datetime.now(),
            scheduled_at=scheduled_at,
            dependencies=dependencies or [],
            max_retries=max_retries
        )
        
        self.tasks[task_id] = task
        heapq.heappush(self.priority_queue, (
            -priority.value,  # 负数实现最大堆
            scheduled_at.timestamp(),
            task_id
        ))
        
        print(f"📝 任务提交: {name} (优先级: {priority.name})")
        return task_id
    
    def schedule(self) -> Optional[tuple]:
        """调度任务"""
        now = datetime.now()
        
        # 查找可用的worker
        available_workers = [w for w in self.workers.values() if w.can_accept()]
        if not available_workers:
            return None
        
        # 从优先级队列中获取任务
        while self.priority_queue:
            priority, timestamp, task_id = heapq.heappop(self.priority_queue)
            task = self.tasks.get(task_id)
            
            if not task or task.state != TaskState.PENDING:
                continue
            
            # 检查依赖
            if task.dependencies:
                deps_met = all(
                    self.tasks.get(dep_id) and 
                    self.tasks[dep_id].state == TaskState.COMPLETED
                    for dep_id in task.dependencies
                )
                if not deps_met:
                    # 重新放回队列
                    heapq.heappush(self.priority_queue, (priority, timestamp, task_id))
                    continue
            
            # 检查时间
            if task.scheduled_at > now:
                heapq.heappush(self.priority_queue, (priority, timestamp, task_id))
                continue
            
            # 分配给worker
            worker = available_workers[0]
            task.state = TaskState.RUNNING
            task.started_at = datetime.now()
            task.worker_id = worker.id
            worker.assign(task.id)
            
            return task, worker
        
        return None
    
    def execute_task(self, task_id: str, executor) -> bool:
        """执行任务"""
        task = self.tasks.get(task_id)
        if not task or task.state != TaskState.RUNNING:
            return False
        
        try:
            # 执行任务
            result = executor(task)
            task.result = result
            task.state = TaskState.COMPLETED
            task.completed_at = datetime.now()
            
            # 释放worker
            if task.worker_id and task.worker_id in self.workers:
                self.workers[task.worker_id].complete(task.id)
            
            print(f"✅ 任务完成: {task.name}")
            return True
            
        except Exception as e:
            task.error = str(e)
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                # 重试
                task.state = TaskState.PENDING
                heapq.heappush(self.priority_queue, (
                    -task.priority.value,
                    datetime.now().timestamp(),
                    task.id
                ))
                print(f"🔄 任务重试: {task.name} (第{task.retry_count}次)")
            else:
                task.state = TaskState.FAILED
                if task.worker_id and task.worker_id in self.workers:
                    self.workers[task.worker_id].complete(task.id)
                print(f"❌ 任务失败: {task.name}")
            
            return False
    
    def get_status(self) -> str:
        """获取调度器状态"""
        total = len(self.tasks)
        pending = sum(1 for t in self.tasks.values() if t.state == TaskState.PENDING)
        running = sum(1 for t in self.tasks.values() if t.state == TaskState.RUNNING)
        completed = sum(1 for t in self.tasks.values() if t.state == TaskState.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.state == TaskState.FAILED)
        
        return f"""
📊 任务调度器状态
━━━━━━━━━━━━━━━━
📝 总任务数: {total}
⏳ 待执行: {pending}
🔄 执行中: {running}
✅ 已完成: {completed}
❌ 失败: {failed}

👷 Workers: {len(self.workers)}
"""
    
    def run(self, max_iterations: int = 20):
        """运行调度器"""
        print("\n" + "="*50)
        print("🚀 任务调度器启动")
        print("="*50)
        
        iteration = 0
        while iteration < max_iterations:
            # 尝试调度任务
            result = self.schedule()
            
            if result:
                task, worker = result
                print(f"▶️  执行: {task.name} -> {worker.name}")
                
                # 模拟执行
                time.sleep(0.1)
                self.execute_task(task.id, lambda t: f"结果: {t.name}完成")
            
            # 检查是否还有任务
            pending = sum(1 for t in self.tasks.values() 
                        if t.state in [TaskState.PENDING, TaskState.RUNNING])
            if pending == 0:
                break
            
            time.sleep(0.1)
            iteration += 1
        
        print(self.get_status())


def demo():
    """演示"""
    scheduler = TaskScheduler()
    
    # 添加workers
    scheduler.add_worker("worker_1", "Worker-1", capacity=2)
    scheduler.add_worker("worker_2", "Worker-2", capacity=2)
    
    # 提交任务
    scheduler.submit("数据抓取", Priority.HIGH)
    scheduler.submit("数据分析", Priority.NORMAL)
    scheduler.submit("生成报告", Priority.NORMAL, dependencies=["数据分析"])
    scheduler.submit("发送邮件", Priority.LOW, dependencies=["生成报告"])
    scheduler.submit("紧急修复", Priority.URGENT)
    
    # 运行
    scheduler.run()


if __name__ == "__main__":
    demo()
