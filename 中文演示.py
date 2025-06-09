#!/usr/bin/env python3
"""
营销代理AI中文演示脚本

这个脚本演示营销代理系统的完整功能，包括：
- 域名建议
- 网站创建
- 营销策略开发
- 标志设计
"""

import asyncio
import textwrap
from google.adk.runners import InMemoryRunner
from marketing_agency.agent import root_agent
from google.genai.types import Part, UserContent
import dotenv

# 加载环境变量
dotenv.load_dotenv()

async def 运行营销代理演示():
    """运行营销代理的完整演示。"""
    
    用户输入 = textwrap.dedent(
        """
        我想开一家名为"甜蜜梦想烘焙坊"的面包店。
        我们专门制作定制婚礼蛋糕、手工面包和精品糕点。
        我们的目标市场是重视品质和工艺的高端客户。
        
        请帮我创建一个完整的营销包，包括：
        1. 域名建议 - 请直接提供10个可用的域名选项
        2. 网站设计 - 创建完整的网站代码
        3. 营销策略 - 制定详细的营销计划
        4. 标志设计 - 生成品牌标志
        
        关键词：甜蜜、梦想、烘焙、手工、精品、婚礼蛋糕、高端、品质、工艺
        
        请不要询问更多信息，直接基于以上信息创建完整的营销包。
        """
    ).strip()

    print("🍰 营销代理AI演示 - 甜蜜梦想烘焙坊")
    print("=" * 60)
    print(f"输入请求: {用户输入[:100]}...")
    print("=" * 60)
    
    try:
        runner = InMemoryRunner(agent=root_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="中文演示用户"
        )
        
        content = UserContent(parts=[Part(text=用户输入)])
        响应文本 = ""
        
        print("🤖 营销代理正在处理您的请求...")
        print("⏳ 这可能需要几分钟时间...\n")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                响应文本 = event.content.parts[0].text
                print(f"📝 收到响应片段: {len(响应文本)} 字符")
        
        print("\n" + "=" * 60)
        print("🎉 营销代理AI响应:")
        print("=" * 60)
        print(响应文本)
        print("=" * 60)
        print("✅ 演示完成！")
        
        # 分析响应内容
        if "域名" in 响应文本 or "domain" in 响应文本.lower():
            print("\n✅ 域名建议: 已生成")
        if "网站" in 响应文本 or "website" in 响应文本.lower():
            print("✅ 网站设计: 已包含")
        if "营销" in 响应文本 or "marketing" in 响应文本.lower():
            print("✅ 营销策略: 已制定")
        if "标志" in 响应文本 or "logo" in 响应文本.lower():
            print("✅ 标志设计: 已生成")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()

async def 测试简单域名请求():
    """测试简单的域名请求。"""
    
    用户输入 = "我需要为我的科技创业公司'创新科技'生成10个可用的域名建议。请直接提供域名列表，不要询问更多信息。"
    
    print("🌐 测试域名生成功能")
    print("=" * 40)
    
    try:
        runner = InMemoryRunner(agent=root_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="域名测试用户"
        )
        
        content = UserContent(parts=[Part(text=用户输入)])
        响应文本 = ""
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                响应文本 = event.content.parts[0].text
        
        print("🎯 域名建议响应:")
        print("-" * 40)
        print(响应文本)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ 错误: {e}")

def 选择演示模式():
    """选择演示模式。"""
    
    print("🎯 营销代理AI中文演示")
    print("=" * 50)
    print("请选择演示模式:")
    print("1. 完整营销包演示 (烘焙坊案例)")
    print("2. 域名生成测试")
    print("3. 退出")
    
    try:
        选择 = input("\n请输入选择 (1-3): ").strip()
        
        if 选择 == '1':
            print("\n🍰 开始完整营销包演示...")
            return asyncio.run(运行营销代理演示())
        elif 选择 == '2':
            print("\n🌐 开始域名生成测试...")
            return asyncio.run(测试简单域名请求())
        elif 选择 == '3':
            print("👋 再见！")
            return
        else:
            print("无效选择，请重新运行脚本。")
            
    except (ValueError, KeyboardInterrupt):
        print("\n退出中...")

if __name__ == "__main__":
    print("🚀 启动营销代理AI中文演示...")
    选择演示模式()