#!/usr/bin/env python3
"""
内容生产团队示例
展示如何使用 SynergyHub 构建内容生产的 Agent 协作流水线
"""

from synergy_core import Orchestrator
from memory_system import AgentMemorySystem
import json


class ContentTeamDemo:
    """内容生产团队演示"""
    
    def __init__(self):
        self.orchestrator = Orchestrator()
        self.memory = AgentMemorySystem()
        
        # 注册内容团队
        self._register_team()
        
    def _register_team(self):
        """注册内容团队成员"""
        # 策划 Agent - 负责选题和构思
        self.orchestrator.register_agent(
            "小策划",
            "planner",
            ["选题", "大纲", "角度"]
        )
        
        # 写作 Agent - 负责内容撰写
        self.orchestrator.register_agent(
            "小写作",
            "writer",
            ["文案", "文章", "脚本"]
        )
        
        # 审核 Agent - 负责质量把控
        self.orchestrator.register_agent(
            "小审核",
            "reviewer",
            ["校对", "优化", "质检"]
        )
        
        # 发布 Agent - 负责多平台发布
        self.orchestrator.register_agent(
            "小发布",
            "publisher",
            ["排版", "发布", "分发"]
        )
        
        print("✅ 内容团队已就位")
        
    def produce_content(self, topic: str, platform: str = "公众号"):
        """生产内容"""
        print(f"\n📝 收到内容需求: {topic}")
        print(f"📍 发布平台: {platform}")
        
        # 步骤1: 策划
        print("\n🔄 步骤1: 策划选题...")
        plan = self.orchestrator.assign_task(
            "小策划",
            f"为【{topic}】设计内容大纲"
        )
        print(f"   大纲: {plan}")
        
        # 步骤2: 写作
        print("\n🔄 步骤2: 撰写内容...")
        draft = self.orchestrator.assign_task(
            "小写作",
            f"根据大纲撰写文章: {plan}"
        )
        
        # 步骤3: 审核
        print("\n🔄 步骤3: 审核优化...")
        reviewed = self.orchestrator.assign_task(
            "小审核",
            f"审核文章并优化: {draft}"
        )
        
        # 步骤4: 发布
        print("\n🔄 步骤4: 发布上线...")
        result = self.orchestrator.assign_task(
            "小发布",
            f"发布到{platform}: {reviewed}"
        )
        
        # 记录到知识库
        self.memory.share_experience("内容团队", {
            "topic": topic,
            "platform": platform,
            "status": "已发布"
        })
        
        return result
    
    def batch_produce(self, topics: list):
        """批量生产内容"""
        print(f"\n📦 批量生产 {len(topics)} 篇文章")
        
        results = []
        for i, topic in enumerate(topics, 1):
            print(f"\n【第 {i}/{len(topics)} 篇】")
            result = self.produce_content(topic)
            results.append(result)
            
        return results


def demo():
    """演示入口"""
    print("=" * 50)
    print("📰 SynergyHub 内容生产团队演示")
    print("=" * 50)
    
    team = ContentTeamDemo()
    
    # 单篇内容生产
    print("\n" + "=" * 50)
    print("模式1: 单篇内容")
    print("=" * 50)
    team.produce_content("AI Agent 赋能中小企业")
    
    # 批量生产
    print("\n" + "=" * 50)
    print("模式2: 批量内容")
    print("=" * 50)
    topics = [
        "企业如何选择 AI 工具",
        "多 Agent 协作实战案例",
        "AI 落地避坑指南"
    ]
    team.batch_produce(topics)
    
    print("\n✅ 演示完成")


if __name__ == "__main__":
    demo()
