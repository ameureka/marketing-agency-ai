#!/usr/bin/env python3

import asyncio
from marketing_agency.sub_agents.logo_create.agent import logo_create_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

async def test_logo_generation():
    """直接测试logo生成功能"""
    print("[DEBUG] 开始测试logo生成功能...")
    
    try:
        # 创建Runner
        runner = InMemoryRunner(agent=logo_create_agent)
        print(f"[DEBUG] 创建Runner成功，代理名称: {logo_create_agent.name}")
        
        # 创建会话
        session = await runner.session_service.create_session(
            app_name=runner.app_name, 
            user_id='test_user'
        )
        print(f"[DEBUG] 创建会话成功: {session.id}")
        
        # 准备请求内容
        content = UserContent(parts=[Part(text='Create a logo for FitTracker Pro fitness app')])
        print("[DEBUG] 发送logo生成请求...")
        
        # 运行代理
        response_text = ""
        async for event in runner.run_async(
            user_id=session.user_id, 
            session_id=session.id, 
            new_message=content
        ):
            if event.content.parts and event.content.parts[0].text:
                response_text = event.content.parts[0].text
                print(f"[DEBUG] 收到响应: {response_text[:100]}...")
        
        print("\n=== Logo代理完整响应 ===")
        print(response_text)
        print("=" * 50)
        
        # 检查artifacts目录
        import os
        artifacts_dir = "/Users/amerlin/Desktop/market_agent_google/marketing-agency/artifacts"
        if os.path.exists(artifacts_dir):
            files = os.listdir(artifacts_dir)
            print(f"\n[DEBUG] artifacts目录内容: {files}")
        else:
            print("\n[DEBUG] artifacts目录不存在")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_logo_generation())