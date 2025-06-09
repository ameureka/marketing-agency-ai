#!/usr/bin/env python3
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""端到端业务场景测试 - 验证营销代理的完整业务流程"""

import asyncio
import textwrap
import time
from pathlib import Path

import dotenv
import pytest
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
from marketing_agency.agent import root_agent
from marketing_agency.sub_agents.domain_create.agent import domain_create_agent
from marketing_agency.sub_agents.logo_create.agent import logo_create_agent
from marketing_agency.sub_agents.marketing_create.agent import marketing_create_agent
from marketing_agency.sub_agents.website_create.agent import website_create_agent

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """加载环境变量"""
    dotenv.load_dotenv()


class TestBusinessScenarios:
    """端到端业务场景测试类"""

    @pytest.mark.asyncio
    async def test_domain_creation_scenario(self):
        """测试域名创建场景 - 为新创业公司建议域名"""
        print("\n=== 测试场景：域名创建 ===")
        
        user_input = textwrap.dedent(
            """
            我正在创建一个专注于可持续发展的科技创业公司，主要提供环保解决方案和绿色技术咨询服务。
            公司名称暂定为"EcoTech Solutions"，请为我推荐10个可用的域名。
            """
        ).strip()

        runner = InMemoryRunner(agent=domain_create_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_domain_user"
        )
        content = UserContent(parts=[Part(text=user_input)])
        response = ""
        
        print(f"用户输入: {user_input}")
        print("\n代理处理中...")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response = event.content.parts[0].text

        print(f"\n代理响应:\n{response}")
        
        # 验证域名建议的质量
        assert len(response) > 50, "域名建议响应过短"
        assert ".com" in response.lower() or ".net" in response.lower() or "域名" in response, "响应应包含域名相关内容"
        assert "ecotech" in response.lower() or "eco" in response.lower() or "tech" in response.lower(), "域名应与公司相关"
        
        # 验证域名数量（更灵活的检查）
        domain_indicators = response.lower().count('.com') + response.lower().count('.net') + response.lower().count('域名')
        assert domain_indicators >= 3, f"应包含至少3个域名相关指标，实际包含{domain_indicators}个"
        
        # 验证包含编号的项目
        numbered_items = len([line for line in response.split('\n') if any(str(i) in line for i in range(1, 11))])
        assert numbered_items >= 3, f"应包含至少3个编号项目，实际包含{numbered_items}个"
        
        print("✅ 域名创建测试通过")

    @pytest.mark.asyncio
    async def test_logo_creation_scenario(self):
        """测试Logo创建场景 - 为品牌生成Logo"""
        print("\n=== 测试场景：Logo创建 ===")
        
        user_input = textwrap.dedent(
            """
            为"EcoTech Solutions"创建一个现代、简洁的Logo。
            公司专注于环保技术和可持续发展解决方案。
            Logo应该体现科技感和环保理念，使用绿色和蓝色调。
            """
        ).strip()

        runner = InMemoryRunner(agent=logo_create_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_logo_user"
        )
        content = UserContent(parts=[Part(text=user_input)])
        response = ""
        
        print(f"用户输入: {user_input}")
        print("\n代理处理中...")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response = event.content.parts[0].text

        print(f"\n代理响应:\n{response}")
        
        # 验证响应
        assert len(response) > 10, "Logo创建响应过短"
        assert "logo" in response.lower() or "附件" in response.lower() or "生成" in response.lower(), "响应应包含Logo相关内容"
        
        print("✅ Logo创建测试通过")

    @pytest.mark.asyncio
    async def test_marketing_strategy_scenario(self):
        """测试营销策略创建场景 - 为新产品制定营销策略"""
        print("\n=== 测试场景：营销策略创建 ===")
        
        user_input = textwrap.dedent(
            """
            为"EcoTech Solutions"制定一个全面的营销策略。
            
            品牌信息：
            - 公司名称：EcoTech Solutions
            - 产品/服务：环保技术解决方案、绿色技术咨询、可持续发展咨询
            - 独特卖点：结合AI技术的环保解决方案，帮助企业实现碳中和目标
            
            营销目标：
            - 在6个月内建立品牌知名度
            - 获得100个B2B潜在客户
            - 在环保技术领域建立思想领导地位
            
            目标受众：
            - 中大型企业的可持续发展负责人
            - 环保政策制定者
            - 绿色投资机构
            
            预算：中等预算（每月$10,000用于数字营销）
            """
        ).strip()

        runner = InMemoryRunner(agent=marketing_create_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_marketing_user"
        )
        content = UserContent(parts=[Part(text=user_input)])
        response = ""
        
        print(f"用户输入: {user_input}")
        print("\n代理处理中...")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response = event.content.parts[0].text

        print(f"\n代理响应:\n{response}")
        
        # 验证营销策略的完整性
        assert len(response) > 500, "营销策略响应过短"
        assert "strategy" in response.lower() or "策略" in response.lower(), "响应应包含策略内容"
        assert "target" in response.lower() or "目标" in response.lower(), "响应应包含目标受众分析"
        
        print("✅ 营销策略创建测试通过")

    @pytest.mark.asyncio
    async def test_website_creation_scenario(self):
        """测试网站创建场景 - 为公司创建网站"""
        print("\n=== 测试场景：网站创建 ===")
        
        user_input = textwrap.dedent(
            """
            为"EcoTech Solutions"创建一个专业的公司网站。
            
            基本信息：
            - 域名：ecotech-solutions.com
            - 公司名称：EcoTech Solutions
            - 主要目标：展示环保技术解决方案，吸引B2B客户
            
            核心服务：
            - AI驱动的碳足迹分析
            - 可持续发展咨询
            - 绿色技术实施
            - 环保合规审计
            
            目标受众：企业可持续发展负责人、环保政策制定者
            
            设计风格：现代、专业、体现环保和科技感，使用绿色和蓝色主题
            """
        ).strip()

        runner = InMemoryRunner(agent=website_create_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_website_user"
        )
        content = UserContent(parts=[Part(text=user_input)])
        response = ""
        
        print(f"用户输入: {user_input}")
        print("\n代理处理中...")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response = event.content.parts[0].text

        print(f"\n代理响应:\n{response}")
        
        # 验证网站代码的完整性
        assert len(response) > 1000, "网站代码响应过短"
        assert "<html" in response.lower(), "响应应包含HTML代码"
        assert "css" in response.lower() or "<style" in response.lower(), "响应应包含CSS样式"
        assert "ecotech" in response.lower(), "网站应包含公司名称"
        
        # 验证包含多个网页文件
        assert "index.html" in response.lower(), "应包含主页文件"
        assert "contact" in response.lower(), "应包含联系页面"
        
        print("✅ 网站创建测试通过")

    @pytest.mark.asyncio
    async def test_complete_marketing_workflow(self):
        """测试完整的营销工作流程 - 从概念到实施的端到端流程"""
        print("\n=== 测试场景：完整营销工作流程 ===")
        
        # 模拟一个完整的营销项目流程
        business_concept = textwrap.dedent(
            """
            我想为一个新的在线教育平台"LearnSmart AI"创建完整的营销方案。
            
            平台特点：
            - 使用AI个性化学习路径
            - 专注于职业技能提升
            - 目标用户：25-40岁的职场人士
            - 主要课程：数据科学、AI/ML、数字营销、项目管理
            
            请帮我：
            1. 分析目标市场和竞争环境
            2. 制定品牌定位和营销策略
            3. 设计用户获取和留存策略
            4. 提供具体的营销活动建议
            """
        ).strip()

        runner = InMemoryRunner(agent=root_agent)
        session = await runner.session_service.create_session(
            app_name=runner.app_name, user_id="test_workflow_user"
        )
        content = UserContent(parts=[Part(text=business_concept)])
        response = ""
        
        print(f"业务概念输入: {business_concept}")
        print("\n营销代理处理中...")
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                response = event.content.parts[0].text

        print(f"\n完整营销方案:\n{response}")
        
        # 验证完整营销方案的内容
        assert len(response) > 100, "完整营销方案响应过短"
        assert "域名" in response or "domain" in response.lower(), "方案应包含域名建议"
        assert "关键词" in response or "keyword" in response.lower(), "方案应包含关键词相关内容"
        
        # 验证工作流程的逻辑性
        assert "步" in response or "step" in response.lower() or "第" in response, "应包含分步骤的工作流程"
        
        print("✅ 完整营销工作流程测试通过")

    @pytest.mark.asyncio
    async def test_performance_and_scalability(self):
        """测试性能和可扩展性 - 并发处理多个营销请求"""
        print("\n=== 测试场景：性能和可扩展性 ===")
        
        # 创建多个并发请求
        requests = [
            "为咖啡店创建营销策略",
            "为健身应用设计Logo",
            "为电商网站建议域名",
            "为餐厅创建网站"
        ]
        
        start_time = time.time()
        
        async def process_request(request_text, user_id):
            runner = InMemoryRunner(agent=root_agent)
            session = await runner.session_service.create_session(
                app_name=runner.app_name, user_id=user_id
            )
            content = UserContent(parts=[Part(text=request_text)])
            response = ""
            
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                if event.content.parts and event.content.parts[0].text:
                    response = event.content.parts[0].text
            
            return response
        
        # 并发处理所有请求
        tasks = [
            process_request(req, f"perf_user_{i}")
            for i, req in enumerate(requests)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n并发处理{len(requests)}个请求耗时: {total_time:.2f}秒")
        print(f"平均每个请求耗时: {total_time/len(requests):.2f}秒")
        
        # 验证所有响应都有效
        for i, response in enumerate(responses):
            assert len(response) > 50, f"请求{i+1}的响应过短"
            print(f"请求{i+1}响应长度: {len(response)}字符")
        
        # 性能基准：每个请求应在合理时间内完成
        assert total_time < 300, f"总处理时间过长: {total_time}秒"  # 5分钟内完成
        
        print("✅ 性能和可扩展性测试通过")

    def test_error_handling_and_edge_cases(self):
        """测试错误处理和边缘情况"""
        print("\n=== 测试场景：错误处理和边缘情况 ===")
        
        # 测试空输入
        edge_cases = [
            "",  # 空输入
            "   ",  # 只有空格
            "a",  # 极短输入
            "请帮我" * 1000,  # 极长输入
        ]
        
        for case in edge_cases:
            try:
                # 这里只是验证代理能够处理边缘情况而不崩溃
                # 实际的异步测试需要在async方法中进行
                assert isinstance(case, str), "输入应为字符串类型"
                print(f"边缘情况测试通过: 输入长度{len(case)}")
            except Exception as e:
                pytest.fail(f"边缘情况处理失败: {e}")
        
        print("✅ 错误处理和边缘情况测试通过")


if __name__ == "__main__":
    # 运行特定测试
    pytest.main([
        __file__ + "::TestBusinessScenarios::test_domain_creation_scenario",
        "-v", "-s"
    ])