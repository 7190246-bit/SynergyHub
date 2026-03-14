#!/usr/bin/env python3
"""
企业智能客服示例
展示如何使用 SynergyHub 构建客服场景的多 Agent 协作
"""

from synergy_core import Orchestrator
from memory_system import AgentMemorySystem
from task_scheduler import TaskScheduler, Priority
import time


class CustomerServiceDemo:
    """智能客服系统演示"""
    
    def __init__(self):
        self.orchestrator = Orchestrator()
        self.memory = AgentMemorySystem()
        self.scheduler = TaskScheduler()
        
        # 注册客服 Agent 团队
        self._register_agents()
        
    def _register_agents(self):
        """注册客服团队成员"""
        # 接待 Agent - 负责初步沟通
        self.orchestrator.register_agent(
            "小接待",
            "reception",
            ["问候", "需求识别", "分流"]
        )
        
        # 销售 Agent - 负责产品咨询
        self.orchestrator.register_agent(
            "小销售",
            "sales",
            ["产品介绍", "报价", "促成交易"]
        )
        
        # 技术 Agent - 负责问题解答
        self.orchestrator.register_agent(
            "小技术",
            "tech",
            ["技术支持", "故障排查", "使用指导"]
        )
        
        # 质检 Agent - 负责服务质量
        self.orchestrator.register_agent(
            "小质检",
            "quality",
            ["满意度调查", "问题记录", "改进建议"]
        )
        
        print("✅ 客服团队已就位")
        
    def handle_customer(self, customer_query: str):
        """处理客户咨询"""
        print(f"\n📞 收到客户咨询: {customer_query}")
        
        # 步骤1: 接待分流
        print("\n🔄 步骤1: 智能分流...")
        intent = self._analyze_intent(customer_query)
        print(f"   识别意图: {intent}")
        
        # 步骤2: 分发给对应 Agent
        if intent == "销售咨询":
            print("\n🔄 步骤2: 转接销售 Agent...")
            result = self.orchestrator.assign_task(
                "小销售", 
                f"处理销售咨询: {customer_query}"
            )
        elif intent == "技术问题":
            print("\n🔄 步骤2: 转接技术 Agent...")
            result = self.orchestrator.assign_task(
                "小技术",
                f"处理技术问题: {customer_query}"
            )
        else:
            result = "感谢您的咨询，请稍等..."
            
        # 步骤3: 记录到记忆系统
        self.memory.share_experience("客服系统", {
            "query": customer_query,
            "intent": intent,
            "result": result
        })
        
        # 步骤4: 质检反馈
        print("\n🔄 步骤3: 满意度跟进...")
        
        return result
    
    def _analyze_intent(self, query: str) -> str:
        """简单的意图识别"""
        keywords_sales = ["价格", "报价", "购买", "多少钱", "优惠"]
        keywords_tech = ["怎么用", "故障", "报错", "问题", "设置"]
        
        for kw in keywords_sales:
            if kw in query:
                return "销售咨询"
        for kw in keywords_tech:
            if kw in query:
                return "技术问题"
        return "其他"


def demo():
    """演示入口"""
    print("=" * 50)
    print("🏢 SynergyHub 企业智能客服系统演示")
    print("=" * 50)
    
    cs = CustomerServiceDemo()
    
    # 模拟客户咨询
    test_queries = [
        "你们的产品多少钱？",
        "系统登录报错了怎么办？",
        "有优惠活动吗？"
    ]
    
    for query in test_queries:
        result = cs.handle_customer(query)
        print(f"\n📝 回复: {result}")
        print("-" * 30)
        time.sleep(0.5)
    
    print("\n✅ 演示完成")


if __name__ == "__main__":
    demo()
