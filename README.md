# Strands Sandbox

[English](#english) | [中文](#中文)

---

## English

Sandbox tool integration for Strands Agents SDK

### Features

- 🔌 **Unified Interface**: Abstract base class design for consistent API
- 🚀 **E2B Backend**: Cloud-based sandbox service integration
- 🐍 **Multi-Language Support**: Python, JavaScript, TypeScript, R, Java, Bash
- 📁 **File Operations**: Read, write, list, and delete files
- 🔄 **Session Management**: Persistent sessions with state preservation
- 🛡️ **Type Safety**: Pydantic models for type-safe operations

### Supported Languages

- ✅ Python
- ✅ JavaScript
- ✅ TypeScript
- ✅ R
- ✅ Java
- ✅ Bash

### Installation

```bash
pip install e2b-code-interpreter pydantic strands-agents
```

### Quick Start

#### 1. Direct E2B Usage

```python
from strands_sandbox import E2BCodeInterpreter

# Create interpreter
interpreter = E2BCodeInterpreter(api_key="your-e2b-api-key")

# Execute code
result = interpreter.code_interpreter({
    "action": {
        "type": "executeCode",
        "code": "print('Hello, E2B!')",
        "language": "python"
    }
})
```

#### 2. Strands Agent Integration

```python
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_sandbox import E2BCodeInterpreter

# Create E2B interpreter
e2b_interpreter = E2BCodeInterpreter(api_key="your-e2b-api-key")

# Create model
model = OpenAIModel(
    client_args={
        "api_key": "your-openai-api-key",
        "base_url": "https://api.together.xyz/v1"
    },
    model_id="openai/gpt-oss-120b",
    params={"max_tokens": 4000, "temperature": 0.3}
)

# Create agent with code interpreter tool
agent = Agent(
    name="CodeExecutor",
    system_prompt="You are a code execution assistant.",
    tools=[e2b_interpreter.code_interpreter],
    model=model
)

# Use the agent
response = agent("Calculate the sum of squares from 1 to 10 using Python")
print(response.message['content'][0]['text'])
```

### Project Structure

```
strands-sandbox/
├── src/strands_sandbox/       # Core implementation
│   ├── __init__.py            # Package exports
│   ├── code_interpreter.py    # Abstract base class
│   ├── models.py              # Data models (6 languages)
│   └── e2bcodeinterpreter.py  # E2B implementation
└── poc/                       # Proof of concept tests
    ├── poc_e2b_fulltest.py        # E2B full test (11 tests)
    ├── poc_strands_e2b_test.py    # Strands Agent integration test (6 tests)
    └── README.md                  # POC documentation
```

### Testing

```bash
# E2B full test
python poc/poc_e2b_fulltest.py

# Strands Agent integration test
python poc/poc_strands_e2b_test.py
```

### Environment Configuration

Create a `.env` file in the `poc/` directory:

```bash
# E2B API Key
E2B_API_KEY=your-e2b-api-key

# Strands Agent Configuration (for Together AI)
OPENAI_API_KEY=your-together-ai-key
OPENAI_BASE_URL=https://api.together.xyz/v1
MODEL_NAME=openai/gpt-oss-120b
TEMPERATURE=0.3
MAX_TOKENS=4000
```

### Test Results

✅ All tests passed!

- E2B Full Test: 11/11 passed
- Strands Agent Integration: 6/6 passed

### License

MIT License

---

## 中文

为 Strands Agents SDK 提供的沙盒工具集成

### 特性

- 🔌 **统一接口**：基于抽象基类的一致 API 设计
- 🚀 **E2B 后端**：云端沙盒服务集成
- 🐍 **多语言支持**：Python、JavaScript、TypeScript、R、Java、Bash
- 📁 **文件操作**：读取、写入、列表、删除文件
- 🔄 **会话管理**：持久化会话，保持状态
- 🛡️ **类型安全**：使用 Pydantic 模型确保类型安全

### 支持的语言

- ✅ Python
- ✅ JavaScript
- ✅ TypeScript
- ✅ R
- ✅ Java
- ✅ Bash

### 安装

```bash
pip install e2b-code-interpreter pydantic strands-agents
```

### 快速开始

#### 1. 直接使用 E2B

```python
from strands_sandbox import E2BCodeInterpreter

# 创建解释器
interpreter = E2BCodeInterpreter(api_key="your-e2b-api-key")

# 执行代码
result = interpreter.code_interpreter({
    "action": {
        "type": "executeCode",
        "code": "print('你好，E2B！')",
        "language": "python"
    }
})
```

#### 2. Strands Agent 集成

```python
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_sandbox import E2BCodeInterpreter

# 创建 E2B 解释器
e2b_interpreter = E2BCodeInterpreter(api_key="your-e2b-api-key")

# 创建模型
model = OpenAIModel(
    client_args={
        "api_key": "your-openai-api-key",
        "base_url": "https://api.together.xyz/v1"
    },
    model_id="openai/gpt-oss-120b",
    params={"max_tokens": 4000, "temperature": 0.3}
)

# 创建带有代码解释器工具的 Agent
agent = Agent(
    name="CodeExecutor",
    system_prompt="你是一个代码执行助手。",
    tools=[e2b_interpreter.code_interpreter],
    model=model
)

# 使用 Agent
response = agent("使用 Python 计算 1 到 10 的平方和")
print(response.message['content'][0]['text'])
```

### 项目结构

```
strands-sandbox/
├── src/strands_sandbox/       # 核心实现
│   ├── __init__.py            # 包导出
│   ├── code_interpreter.py    # 抽象基类
│   ├── models.py              # 数据模型（6种语言）
│   └── e2bcodeinterpreter.py  # E2B 实现
└── poc/                       # 概念验证测试
    ├── poc_e2b_fulltest.py        # E2B 完整测试（11个测试）
    ├── poc_strands_e2b_test.py    # Strands Agent 集成测试（6个测试）
    └── README.md                  # POC 文档
```

### 测试

```bash
# E2B 完整测试
python poc/poc_e2b_fulltest.py

# Strands Agent 集成测试
python poc/poc_strands_e2b_test.py
```

### 环境配置

在 `poc/` 目录下创建 `.env` 文件：

```bash
# E2B API Key
E2B_API_KEY=your-e2b-api-key

# Strands Agent 配置（用于 Together AI）
OPENAI_API_KEY=your-together-ai-key
OPENAI_BASE_URL=https://api.together.xyz/v1
MODEL_NAME=openai/gpt-oss-120b
TEMPERATURE=0.3
MAX_TOKENS=4000
```

### 测试结果

✅ 所有测试通过！

- E2B 完整测试：11/11 通过
- Strands Agent 集成：6/6 通过

### 许可证

MIT License
