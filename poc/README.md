# POC Tests

Proof of concept tests for E2B Sandbox Implementation.

## File Descriptions

- **poc_e2b_fulltest.py** - E2B full test suite (11 tests)
- **poc_strands_e2b_test.py** - Strands Agent + E2B integration tests (6 tests) ✨
- **poc_e2b_test.py** - Original E2B test examples
- **e2b_scalebox_compatibility.md** - Compatibility documentation
- **.env** - Environment variable configuration

## Running Tests

### 1. E2B Full Test Suite

```bash
python poc/poc_e2b_fulltest.py
```

Test coverage:
- Basic code execution
- File operations
- Command execution
- Session management
- Error handling
- 6 languages (Python, JS, TS, R, Java, Bash)

### 2. Strands Agent + E2B Integration Tests ✨

```bash
python poc/poc_strands_e2b_test.py
```

Test coverage:
- Agent basic code execution
- Agent data analysis
- Agent multi-language support
- Agent file operations
- Agent session persistence
- Agent error handling

## Environment Configuration

Ensure your `.env` file contains the following configuration:

```bash
# E2B API Key
E2B_API_KEY=your-e2b-api-key

# Strands Agent Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4
TEMPERATURE=0.3
MAX_TOKENS=4000
```

## Test Results

✅ All tests passed!

- E2B full test suite: 11/11 passed
- Strands Agent integration tests: 6/6 passed
