#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_environment():
    print("🔍 环境配置检查")
    print("=" * 50)
    
    # 检查 Python 版本
    python_version = sys.version
    print(f"🐍 Python 版本: {python_version}")
    
    # 检查环境变量
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_CLOUD_LOCATION',
        'GOOGLE_APPLICATION_CREDENTIALS'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != 'your-project-id' and value != '/path/to/your/service-account-key.json':
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未正确设置")
    
    # 检查服务账号密钥文件
    key_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if key_file and os.path.exists(key_file):
        print(f"✅ 服务账号密钥文件存在: {key_file}")
    else:
        print(f"❌ 服务账号密钥文件不存在或未设置: {key_file}")
    
    # 测试包导入
    packages_to_test = [
        ('google.cloud.aiplatform', 'Google Cloud AI Platform'),
        ('google.generativeai', 'Google Generative AI'),
        ('dotenv', 'Python Dotenv'),
        ('requests', 'Requests'),
        ('whois', 'Python Whois')
    ]
    
    for package, name in packages_to_test:
        try:
            __import__(package)
            print(f"✅ {name} 导入成功")
        except ImportError as e:
            print(f"❌ {name} 导入失败: {e}")
    
    # 测试 Google Cloud 连接（如果配置正确）
    if all(os.getenv(var) and os.getenv(var) not in ['your-project-id', '/path/to/your/service-account-key.json'] for var in required_vars):
        try:
            from google.cloud import aiplatform
            aiplatform.init(
                project=os.getenv('GOOGLE_CLOUD_PROJECT'),
                location=os.getenv('GOOGLE_CLOUD_LOCATION')
            )
            print("✅ Google Cloud AI Platform 连接成功")
        except Exception as e:
            print(f"❌ Google Cloud AI Platform 连接失败: {e}")
    else:
        print("⚠️  Google Cloud 配置未完成，跳过连接测试")
    
    print("\n🎉 环境检查完成！")
    print("\n📝 下一步操作：")
    print("1. 复制 .env.template 为 .env 并填入正确的配置")
    print("2. 运行 'gcloud init' 初始化 Google Cloud")
    print("3. 创建服务账号并下载密钥文件")
    print("4. 再次运行此脚本验证配置")

if __name__ == "__main__":
    test_environment()
