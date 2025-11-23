"""
Strands Agent with E2B Code Interpreter Test

Verify that Strands Agent can correctly invoke E2B Code Interpreter tool
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from strands import Agent
from strands.models.openai import OpenAIModel
from strands_sandbox import E2BCodeInterpreter


# Create model instance
def get_model():
    """Get configured model instance"""
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
    """Test 1: Agent Basic Code Execution"""
    print("\n" + "=" * 60)
    print("Test 1: Agent Basic Code Execution")
    print("=" * 60)
    
    # Create E2B Code Interpreter
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    # Create Agent
    agent = Agent(
        name="CodeExecutor",
        system_prompt="You are a code execution assistant that can help users execute Python code.",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    # Test execution
    print("\nRequest: Execute Python code to calculate 2+2")
    response = agent("Please execute Python code: print('Hello from Agent!'); 2 + 2")
    
    print(f"\nAgent Response: {response.message['content'][0]['text']}")
    return True


def test_agent_data_analysis():
    """Test 2: Agent Data Analysis"""
    print("\n" + "=" * 60)
    print("Test 2: Agent Data Analysis")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="DataAnalyst",
        system_prompt="You are a data analyst who can perform data analysis using Python.",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\nRequest: Create a dataset and calculate averages")
    response = agent("""
Please use pandas to create a DataFrame with the following data:
- Name: Alice, Bob, Charlie
- Age: 25, 30, 35
- Score: 85, 90, 88

Then calculate the average age and average score.
""")
    
    print(f"\nAgent Response: {response.message['content'][0]['text']}")
    return True


def test_agent_multi_language():
    """Test 3: Agent Multi-Language Support"""
    print("\n" + "=" * 60)
    print("Test 3: Agent Multi-Language Support")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="MultiLangExecutor",
        system_prompt="You are a multi-language code execution assistant supporting Python, JavaScript, TypeScript, and more.",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\nRequest: Calculate sum of squares from 1 to 5 in Python and JavaScript")
    response = agent("""
Please calculate the sum of squares from 1 to 5 using both Python and JavaScript.
First use Python, then JavaScript.
""")
    
    print(f"\nAgent Response: {response.message['content'][0]['text']}")
    return True


def test_agent_file_operations():
    """Test 4: Agent File Operations"""
    print("\n" + "=" * 60)
    print("Test 4: Agent File Operations")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="FileManager",
        system_prompt="You are a file management assistant that can create, read, and manage files.",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\nRequest: Create a file and read its content")
    response = agent("""
Please create a file named 'greeting.txt' with the content 'Hello from Strands Agent!',
then read the content of this file.
""")
    
    print(f"\nAgent Response: {response.message['content'][0]['text']}")
    return True


def test_agent_session_persistence():
    """Test 5: Agent Session Persistence"""
    print("\n" + "=" * 60)
    print("Test 5: Agent Session Persistence")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="SessionManager",
        system_prompt="You are a session management assistant that can maintain variable state across multiple interactions.",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\nFirst Request: Define a variable")
    response1 = agent("Please define a variable x = 100")
    print(f"Response 1: {response1.message['content'][0]['text']}")
    
    print("\nSecond Request: Use the previously defined variable")
    response2 = agent("Please use the previously defined variable x and calculate x * 2")
    print(f"Response 2: {response2.message['content'][0]['text']}")
    
    return True


def test_agent_error_handling():
    """Test 6: Agent Error Handling"""
    print("\n" + "=" * 60)
    print("Test 6: Agent Error Handling")
    print("=" * 60)
    
    api_key = os.getenv("E2B_API_KEY")
    e2b_interpreter = E2BCodeInterpreter(api_key=api_key)
    
    agent = Agent(
        name="ErrorHandler",
        system_prompt="You are a code execution assistant. When code errors occur, you should explain the error and provide fix suggestions.",
        tools=[e2b_interpreter.code_interpreter],
        model=get_model()
    )
    
    print("\nRequest: Execute code that will cause an error")
    response = agent("Please execute this code: result = 10 / 0")
    
    print(f"\nAgent Response: {response.message['content'][0]['text']}")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Strands Agent + E2B Code Interpreter Tests")
    print("=" * 60)
    
    # Check required environment variables
    if not os.getenv("E2B_API_KEY"):
        print("\n❌ Error: Please set E2B_API_KEY environment variable")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: Please set OPENAI_API_KEY environment variable")
        return
    
    print(f"Using model: {os.getenv('MODEL_NAME', 'default')}")
    print(f"API Base URL: {os.getenv('OPENAI_BASE_URL', 'default')}")
    
    tests = [
        ("Agent Basic Code Execution", test_agent_basic_code_execution),
        ("Agent Data Analysis", test_agent_data_analysis),
        ("Agent Multi-Language Support", test_agent_multi_language),
        ("Agent File Operations", test_agent_file_operations),
        ("Agent Session Persistence", test_agent_session_persistence),
        ("Agent Error Handling", test_agent_error_handling),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
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
