"""E2B Code Interpreter POC 测试脚本"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import code_interpreter_sync
from e2b.connection_config import ConnectionConfig


def main():
    # 加载 .env 文件（从当前目录）
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    
    # 从环境变量获取配置
    api_key = os.getenv('E2B_API_KEY')
    api_url = os.getenv('E2B_API_URL')
    domain = os.getenv('E2B_DOMAIN')
    
    if not api_key:
        print("错误: 未找到 E2B_API_KEY")
        print("请在 .env 文件中设置: E2B_API_KEY=your-api-key")
        return
    
    # 创建连接配置
    print("启动 E2B 沙箱...")
    print(f"API Key: {api_key[:20]}...")
    print(f"API URL: {api_url or '默认'}")
    print(f"Domain: {domain or '默认'}")
    
    # 构建创建参数
    create_kwargs = {'api_key': api_key}
    if api_url:
        create_kwargs['api_url'] = api_url
    if domain:
        create_kwargs['domain'] = domain
    
    # 创建沙箱
    sandbox = code_interpreter_sync.Sandbox.create(**create_kwargs)
    print(f"沙箱 ID: {sandbox.sandbox_id}\n")
    
    try:
        # 测试 1: 基础代码执行
        print("=== 测试 1: 基础代码执行 ===")
        result = sandbox.run_code("print('Hello from E2B!'); 2 + 2")
        print(f"输出: {result.text}")
        print(f"返回值: {result.results}\n")

        # 测试 2: 文件操作
        print("=== 测试 2: 文件操作 ===")
        sandbox.run_code("with open('test.txt', 'w') as f: f.write('Hello E2B!')")
        result = sandbox.run_code("open('test.txt').read()")
        print(f"文件内容: {result.results}\n")
        
        # 测试 3: 数据处理
        print("=== 测试 3: 数据处理 ===")
        code = """
import pandas as pd
df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
print(df)
df['age'].mean()
"""
        result = sandbox.run_code(code)
        print(f"输出: {result.text}")
        print(f"平均年龄: {result.results}\n")
        
        # 测试 4: 错误处理
        print("=== 测试 4: 错误处理 ===")
        result = sandbox.run_code("1 / 0")
        if result.error:
            print(f"捕获到错误: {result.error.name}\n")
        
        print("所有测试完成！")
        
    finally:
        sandbox.kill()
        print("沙箱已关闭")


if __name__ == "__main__":
    main()
