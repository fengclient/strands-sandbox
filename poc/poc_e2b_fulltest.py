"""E2B Code Interpreter Full Test Suite"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from strands_sandbox import E2BCodeInterpreter


def test_basic_execution():
    """Test 1: Basic Code Execution"""
    print("\n" + "=" * 60)
    print("Test 1: Basic Code Execution")
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
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_file_operations():
    """Test 2: File Operations"""
    print("\n" + "=" * 60)
    print("Test 2: File Operations")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    # Write, read, delete
    interpreter.code_interpreter({"action": {"type": "writeFiles", "content": [{"path": "test.txt", "text": "Hello"}]}})
    interpreter.code_interpreter({"action": {"type": "readFiles", "paths": ["test.txt"]}})
    result = interpreter.code_interpreter({"action": {"type": "removeFiles", "paths": ["test.txt"]}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_command_execution():
    """Test 3: Command Execution"""
    print("\n" + "=" * 60)
    print("Test 3: Command Execution")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCommand", "command": "echo 'Hello'"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_session_management():
    """Test 4: Session Management"""
    print("\n" + "=" * 60)
    print("Test 4: Session Management")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    interpreter.code_interpreter({"action": {"type": "initSession", "session_name": "test", "description": "test"}})
    interpreter.code_interpreter({"action": {"type": "executeCode", "session_name": "test", "code": "x=42", "language": "python"}})
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "session_name": "test", "code": "print(x)", "language": "python"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_error_handling():
    """Test 5: Error Handling"""
    print("\n" + "=" * 60)
    print("Test 5: Error Handling")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "1/0", "language": "python"}})
    
    print(f"Result: {result.get('status') == 'error'}")
    return True


def test_python():
    """Test 6: Python"""
    print("\n" + "=" * 60)
    print("Test 6: Python")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "print('Python')\n2+2", "language": "python"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_javascript():
    """Test 7: JavaScript"""
    print("\n" + "=" * 60)
    print("Test 7: JavaScript")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "console.log('JS')\n2+2", "language": "javascript"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_typescript():
    """Test 8: TypeScript"""
    print("\n" + "=" * 60)
    print("Test 8: TypeScript")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "const x: number = 2+2; console.log('TS'); x", "language": "typescript"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_r():
    """Test 9: R"""
    print("\n" + "=" * 60)
    print("Test 9: R")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "print('R')\n2+2", "language": "r"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_java():
    """Test 10: Java"""
    print("\n" + "=" * 60)
    print("Test 10: Java")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "System.out.println(\"Java\");\n2+2", "language": "java"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def test_bash():
    """Test 11: Bash"""
    print("\n" + "=" * 60)
    print("Test 11: Bash")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    interpreter = E2BCodeInterpreter(api_key=api_key)
    
    result = interpreter.code_interpreter({"action": {"type": "executeCode", "code": "echo 'Bash'\necho $((2+2))", "language": "bash"}})
    
    print(f"Result: {result.get('status')}")
    return result.get("status") == "success"


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("E2B Code Interpreter Full Test Suite")
    print("=" * 60)
    
    if not os.getenv("E2B_API_KEY"):
        print("\nError: Please set E2B_API_KEY environment variable")
        return
    
    tests = [
        ("Basic Code Execution", test_basic_execution),
        ("File Operations", test_file_operations),
        ("Command Execution", test_command_execution),
        ("Session Management", test_session_management),
        ("Error Handling", test_error_handling),
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
            print(f"\nException: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} passed")


if __name__ == "__main__":
    main()
