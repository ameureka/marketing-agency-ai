#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
营销代理智能体功能验证脚本

此脚本验证营销代理的基本结构和组件，不需要实际的Google Cloud配置。
"""

import sys
import os

# 添加营销代理路径
sys.path.append('adk-samples/python/agents/marketing-agency')

def validate_agent_structure():
    """验证代理结构"""
    print("🔍 验证营销代理智能体结构...")
    
    try:
        # 导入主代理
        from marketing_agency.agent import marketing_coordinator, root_agent
        print("✅ 主控制器导入成功")
        
        # 验证主代理属性
        assert marketing_coordinator.name == "marketing_coordinator"
        assert marketing_coordinator.model == "gemini-2.5-pro-preview-05-06"
        assert len(marketing_coordinator.tools) == 4
        print(f"✅ 主代理配置正确: {marketing_coordinator.name}")
        print(f"   - 模型: {marketing_coordinator.model}")
        print(f"   - 工具数量: {len(marketing_coordinator.tools)}")
        
        # 导入子代理
        from marketing_agency.sub_agents.domain_create import domain_create_agent
        from marketing_agency.sub_agents.website_create import website_create_agent
        from marketing_agency.sub_agents.marketing_create import marketing_create_agent
        from marketing_agency.sub_agents.logo_create import logo_create_agent
        
        print("✅ 所有子代理导入成功")
        
        # 验证子代理
        sub_agents = [
            ("域名代理", domain_create_agent),
            ("网站代理", website_create_agent),
            ("营销代理", marketing_create_agent),
            ("Logo代理", logo_create_agent)
        ]
        
        for name, agent in sub_agents:
            print(f"   - {name}: {agent.name} (模型: {agent.model})")
            
        return True
        
    except Exception as e:
        print(f"❌ 代理结构验证失败: {e}")
        return False

def validate_prompts():
    """验证提示词"""
    print("\n🔍 验证提示词配置...")
    
    try:
        from marketing_agency import prompt
        from marketing_agency.sub_agents.domain_create import prompt as domain_prompt
        from marketing_agency.sub_agents.website_create import prompt as website_prompt
        from marketing_agency.sub_agents.marketing_create import prompt as marketing_prompt
        from marketing_agency.sub_agents.logo_create import prompt as logo_prompt
        
        prompts = [
            ("主控制器", prompt.MARKETING_COORDINATOR_PROMPT),
            ("域名代理", domain_prompt.DOMAIN_CREATE_PROMPT),
            ("网站代理", website_prompt.WEBSITE_CREATE_PROMPT),
            ("营销代理", marketing_prompt.MARKETING_CREATE_PROMPT),
            ("Logo代理", logo_prompt.LOGO_CREATE_PROMPT)
        ]
        
        for name, prompt_text in prompts:
            if prompt_text and len(prompt_text.strip()) > 0:
                print(f"✅ {name}提示词配置正确 ({len(prompt_text)} 字符)")
            else:
                print(f"❌ {name}提示词为空")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ 提示词验证失败: {e}")
        return False

def validate_project_structure():
    """验证项目结构"""
    print("\n🔍 验证项目文件结构...")
    
    required_files = [
        "adk-samples/python/agents/marketing-agency/marketing_agency/agent.py",
        "adk-samples/python/agents/marketing-agency/marketing_agency/prompt.py",
        "adk-samples/python/agents/marketing-agency/pyproject.toml",
        "adk-samples/python/agents/marketing-agency/README.md"
    ]
    
    required_dirs = [
        "adk-samples/python/agents/marketing-agency/marketing_agency/sub_agents",
        "adk-samples/python/agents/marketing-agency/demo_html",
        "adk-samples/python/agents/marketing-agency/deployment",
        "adk-samples/python/agents/marketing-agency/eval",
        "adk-samples/python/agents/marketing-agency/tests"
    ]
    
    all_valid = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ 文件存在: {file_path}")
        else:
            print(f"❌ 文件缺失: {file_path}")
            all_valid = False
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ 目录存在: {dir_path}")
        else:
            print(f"❌ 目录缺失: {dir_path}")
            all_valid = False
    
    return all_valid

def validate_demo_output():
    """验证示例输出"""
    print("\n🔍 验证示例输出文件...")
    
    demo_files = [
        "adk-samples/python/agents/marketing-agency/demo_html/index.html",
        "adk-samples/python/agents/marketing-agency/demo_html/style.css",
        "adk-samples/python/agents/marketing-agency/demo_html/script.js"
    ]
    
    all_valid = True
    
    for file_path in demo_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip()) > 0:
                    print(f"✅ 示例文件有效: {file_path} ({len(content)} 字符)")
                else:
                    print(f"❌ 示例文件为空: {file_path}")
                    all_valid = False
        else:
            print(f"❌ 示例文件缺失: {file_path}")
            all_valid = False
    
    return all_valid

def main():
    """主验证函数"""
    print("🚀 开始营销代理智能体功能验证\n")
    
    results = []
    
    # 执行各项验证
    results.append(("项目结构", validate_project_structure()))
    results.append(("代理结构", validate_agent_structure()))
    results.append(("提示词配置", validate_prompts()))
    results.append(("示例输出", validate_demo_output()))
    
    # 汇总结果
    print("\n📊 验证结果汇总:")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name:15} : {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 所有验证项目通过！营销代理智能体结构完整且功能正常。")
        print("\n📋 下一步建议:")
        print("1. 配置Google Cloud项目和凭据")
        print("2. 运行完整的API测试")
        print("3. 进行端到端功能验证")
        return 0
    else:
        print("⚠️  部分验证项目失败，请检查上述错误信息。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)