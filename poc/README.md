# POC 测试

E2B Sandbox Implementation 的概念验证测试。

## 文件说明

- **poc_e2b_fulltest.py** - E2B 完整测试（11个测试）
- **poc_strands_e2b_test.py** - Strands Agent + E2B 集成测试（6个测试）✨
- **poc_e2b_test.py** - 原始 E2B 测试示例
- **e2b_scalebox_compatibility.md** - 兼容性文档
- **.env** - 环境变量配置

## 运行测试

### 1. E2B 完整测试

```bash
python poc/poc_e2b_fulltest.py
```

测试覆盖：
- 基础代码执行
- 文件操作
- 命令执行
- 会话管理
- 错误处理
- 6种语言（Python, JS, TS, R, Java, Bash）

### 2. Strands Agent + E2B 集成测试 ✨

```bash
python poc/poc_strands_e2b_test.py
```

测试覆盖：
- Agent 基础代码执行
- Agent 数据分析
- Agent 多语言支持
- Agent 文件操作
- Agent 会话持久化
- Agent 错误处理

## 环境配置

确保 `.env` 文件包含以下配置：

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

## 测试结果

✅ 所有测试通过！

- E2B 完整测试：11/11 通过
- Strands Agent 集成测试：6/6 通过
