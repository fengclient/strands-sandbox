"""
Strands Agent 调用 E2B Code Interpreter 测试

验证 Strands Agent 可以正确调用 E2B Code Interpreter 工具
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from strands import Agent
from strands.models.openai import OpenAIModel
from strands_sandbox import E2BCodeInterpreter


# 创建模型实例
def get_model():
    """获取配置好的模型实例"""
    return OpenAIModel(
        client_args={
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL"),
        },
        model_id=os.getenv("MODEL_NAME", "openai/gpt-oss-120b"),
        params={
            "max_tokens": int(os.getenv("MAX_TOKENS", "4000")),
            "temperature": float(os.getenv("TEMPERATURE", "0.3")),
        }
    )


def test_agent_basic_code_execution():
    """测试 1: Agent 基础代码执行"""
    print("\n" + "=" * 60)
    print("测试 1: Agent 基础代码执行")
    print("=" * 60)
    
    # 创建 E2B Code Interpreter
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    # 创建 Agent
    agent = Agent(
        name="CodeExecutor",
        system_prompt="你是一个代码执行助手，可以帮助用户执行 Python 代码。",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    # 测试执行
    print("\n请求: 执行 Python 代码计算 2+2")
    response = agent("请执行 Python 代码: print('Hello from Agent!'); 2 + 2")
    
    print(f"\nAgent 响应: {response.message['content'][0]['text']}")
    return True


def test_agent_data_analysis():
    """测试 2: Agent 数据分析"""
    print("\n" + "=" * 60)
    print("测试 2: Agent 数据分析")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="DataAnalyst",
        system_prompt="你是一个数据分析师，可以使用 Python 进行数据分析。",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\n请求: 创建一个数据集并计算平均值")
    response = agent("""
请使用 pandas 创建一个包含以下数据的 DataFrame：
- 姓名: Alice, Bob, Charlie
- 年龄: 25, 30, 35
- 分数: 85, 90, 88

然后计算平均年龄和平均分数。
""")
    
    print(f"\nAgent 响应: {response.message['content'][0]['text']}")
    return True


def test_agent_multi_language():
    """测试 3: Agent 多语言支持"""
    print("\n" + "=" * 60)
    print("测试 3: Agent 多语言支持")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="MultiLangExecutor",
        system_prompt="你是一个多语言代码执行助手，支持 Python, JavaScript, TypeScript 等语言。",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\n请求: 分别用 Python 和 JavaScript 计算 1 到 5 的平方和")
    response = agent("""
请分别使用 Python 和 JavaScript 计算 1 到 5 的平方和。
先用 Python，再用 JavaScript。
""")
    
    print(f"\nAgent 响应: {response.message['content'][0]['text']}")
    return True


def test_agent_file_operations():
    """测试 4: Agent 文件操作"""
    print("\n" + "=" * 60)
    print("测试 4: Agent 文件操作")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="FileManager",
        system_prompt="你是一个文件管理助手，可以创建、读取和管理文件。",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\n请求: 创建一个文件并读取内容")
    response = agent("""
请创建一个名为 'greeting.txt' 的文件，内容是 'Hello from Strands Agent!'，
然后读取这个文件的内容。
""")
    
    print(f"\nAgent 响应: {response.message['content'][0]['text']}")
    return True


def test_agent_session_persistence():
    """测试 5: Agent 会话持久化"""
    print("\n" + "=" * 60)
    print("测试 5: Agent 会话持久化")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="SessionManager",
        system_prompt="你是一个会话管理助手，可以在多次交互中保持变量状态。",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\n第一次请求: 定义变量")
    response1 = agent("请定义一个变量 x = 100")
    print(f"响应 1: {response1.message['content'][0]['text']}")
    
    print("\n第二次请求: 使用之前定义的变量")
    response2 = agent("请使用之前定义的变量 x，计算 x * 2")
    print(f"响应 2: {response2.message['content'][0]['text']}")
    
    return True


def test_agent_error_handling():
    """测试 6: Agent 错误处理"""
    print("\n" + "=" * 60)
    print("测试 6: Agent 错误处理")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="ErrorHandler",
        system_prompt="你是一个代码执行助手，当代码出错时，你应该解释错误并提供修复建议。",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\n请求: 执行会出错的代码")
    response = agent("请执行这段代码: result = 10 / 0")
    
    print(f"\nAgent 响应: {response.message['content'][0]['text']}")
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Strands Agent + E2B Code Interpreter 测试")
    print("=" * 60)
    
    # 检查必要的环境变量
    if not os.getenv("E2B_API_KEY"):
        print("\n❌ 错误: 请设置 E2B_API_KEY 环境变量")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ 错误: 请设置 OPENAI_API_KEY 环境变量")
        return
    
    print(f"使用模型: {os.getenv('MODEL_NAME', 'default')}")
    print(f"API Base URL: {os.getenv('OPENAI_BASE_URL', 'default')}")
    
    tests = [
        ("Agent 基础代码执行", test_agent_basic_code_execution),
        ("Agent 数据分析", test_agent_data_analysis),
        ("Agent 多语言支持", test_agent_multi_language),
        ("Agent 文件操作", test_agent_file_operations),
        ("Agent 会话持久化", test_agent_session_persistence),
        ("Agent 错误处理", test_agent_error_handling),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")


if __name__ == "__main__":
    main()
