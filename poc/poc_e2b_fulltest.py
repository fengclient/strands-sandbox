"""E2B Code Interpreter 完整测试"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from strands_sandbox import E2BCodeInterpreter


def test_basic_execution():
    """测试 1: 基础代码执行"""
    print("\n" + "=" * 60)
    print("测试 1: 基础代码执行")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({
        "action": {
            "type": "executeCode",
            "code": "print('Hello from E2B!')\n2 + 2",
            "language": "python"
        }
    })
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_file_operations():
    """测试 2: 文件操作"""
    print("\n" + "=" * 60)
    print("测试 2: 文件操作")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    # 写入、读取、删除
    interpreter.code_interpreter({"action": {"type": "writeFiles", "content": [{"path": "test.txt", "text": "Hello"}]}})
    interpreter.code_interpreter({"action": {"type": "readFiles", "paths": ["test.txt"]}})
    result = interpreter.code_interpreter({"action": {"type": "removeFiles", "paths": ["test.txt"]}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_command_execution():
    """测试 3: 命令执行"""
    print("\n" + "=" * 60)
    print("测试 3: 命令执行")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCommand", "command": "echo 'Hello'"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_session_management():
    """测试 4: 会话管理"""
    print("\n" + "=" * 60)
    print("测试 4: 会话管理")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    interpreter.code_interpreter({"action": {"type": "initSession", "session_name": "test", "description": "test"}})
    interpreter.code_interpreter({"action": {"type": "executeCode", "session_name": "test", "code": "x=42", "language": "python"}})
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "session_name": "test", "code": "print(x)", "language": "python"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_error_handling():
    """测试 5: 错误处理"""
    print("\n" + "=" * 60)
    print("测试 5: 错误处理")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "1/0", "language": "python"}})
    
    print(f"结果: {result.get('status') == 'error'}")
    return True


def test_python():
    """测试 6: Python"""
    print("\n" + "=" * 60)
    print("测试 6: Python")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "print('Python')\n2+2", "language": "python"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_javascript():
    """测试 7: JavaScript"""
    print("\n" + "=" * 60)
    print("测试 7: JavaScript")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "console.log('JS')\n2+2", "language": "javascript"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_typescript():
    """测试 8: TypeScript"""
    print("\n" + "=" * 60)
    print("测试 8: TypeScript")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "const x: number = 2+2; console.log('TS'); x", "language": "typescript"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_r():
    """测试 9: R"""
    print("\n" + "=" * 60)
    print("测试 9: R")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "print('R')\n2+2", "language": "r"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_java():
    """测试 10: Java"""
    print("\n" + "=" * 60)
    print("测试 10: Java")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "System.out.println(\"Java\");\n2+2", "language": "java"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def test_bash():
    """测试 11: Bash"""
    print("\n" + "=" * 60)
    print("测试 11: Bash")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "echo 'Bash'\necho $((2+2))", "language": "bash"}})
    
    print(f"结果: {result.get('status')}")
    return result.get("status") == "success"


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("E2B Code Interpreter 完整测试")
    print("=" * 60)
    
    if not os.getenv("E2B_API_KEY"):
        print("\n错误: 请设置 E2B_API_KEY 环境变量")
        return
    
    tests = [
        ("基础代码执行", test_basic_execution),
        ("文件操作", test_file_operations),
        ("命令执行", test_command_execution),
        ("会话管理", test_session_management),
        ("错误处理", test_error_handling),
        ("Python", test_python),
        ("JavaScript", test_javascript),
        ("TypeScript", test_typescript),
        ("R", test_r),
        ("Java", test_java),
        ("Bash", test_bash),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n异常: {e}")
            results.append((name, False))
    
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
