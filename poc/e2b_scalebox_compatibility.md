# E2B 与 ScaleBox 兼容性测试报告

## 测试环境

### Python 依赖

```
e2b==2.7.0
e2b-code-interpreter==2.3.0
python-dotenv==1.2.1
httpx==0.28.1
attrs==25.4.0
```

安装命令:
```bash
pip install e2b-code-interpreter==2.3.0 python-dotenv==1.2.1
```

### 测试配置

- **E2B SDK 版本**: 
  - 主要测试: `e2b==2.7.0`, `e2b-code-interpreter==2.3.0`
  - 旧版本测试: `e2b==1.2.0b5`, `e2b-code-interpreter==1.2.0b5`

- **ScaleBox API**: `https://api.scalebox.dev/v1`
- **Python 版本**: 3.13
- **测试日期**: 2025-11-21

## API 端点对比

### E2B 官方 API

- **基础 URL**: `https://api.e2b.dev`
- **创建沙箱**: `POST /sandboxes` (无版本前缀)
- **认证方式**: `X-API-KEY` 请求头

### ScaleBox API

- **基础 URL**: `https://api.scalebox.dev`
- **创建沙箱**: `POST /v1/sandboxes` (有 `/v1/` 版本前缀)
- **认证方式**: `X-API-KEY` 请求头

## 兼容性测试结果

### 1. API 端点路径

**差异**: E2B SDK 默认访问 `/sandboxes`，ScaleBox 使用 `/v1/sandboxes`

**测试方法**:

使用新版 SDK (2.7.0) 配置 `E2B_API_URL`:
```python
from e2b_code_interpreter import code_interpreter_sync

sandbox = code_interpreter_sync.Sandbox.create(
    api_key='sk-your-key',
    api_url='https://api.scalebox.dev/v1'
)
```

**结果**: ✅ 请求成功到达 ScaleBox API

### 2. 认证方式

**测试命令**:
```bash
curl -X POST https://api.scalebox.dev/v1/sandboxes \
  -H "X-API-KEY: sk-your-key" \
  -H "Content-Type: application/json" \
  -d '{"template_id":"base","timeout":300}'
```

**结果**: ✅ 认证成功，ScaleBox 接受 `X-API-KEY` 请求头

### 3. 响应格式

**E2B 官方 API 响应格式**

根据 E2B SDK 源码 (`e2b/api/client/models/sandbox.py`)，创建沙箱的响应格式：

**必需字段**:
- `clientID` (string): 客户端标识符
- `envdVersion` (string): 沙箱中运行的 envd 版本
- `sandboxID` (string): 沙箱标识符
- `templateID` (string): 模板标识符

**可选字段**:
- `alias` (string): 模板别名
- `domain` (string | null): 沙箱流量访问的基础域名
- `envdAccessToken` (string): envd 通信访问令牌
- `trafficAccessToken` (string | null): 通过代理访问沙箱所需的令牌

**E2B 实际响应示例**:
```json
{
  "clientID": "6532622b",
  "envdVersion": "0.4.2",
  "sandboxID": "ie3u9aqnzy8gmzamakcb4",
  "templateID": "rki5dems9wqfm4r03t7g",
  "alias": "base",
  "domain": null,
  "trafficAccessToken": null
}
```

**ScaleBox 实际响应**:
```json
{
  "success": true,
  "data": {
    "sandbox_id": "sbx-x86bli4tvxegry1nn",
    "sandbox_domain": "sbx-x86bli4tvxegry1nn.x6rfrvvjiau6per75.scalebox.dev",
    "envd_access_token": "envd-6EihG92wWv5DISQTD9asaH2YlxD5u7BRvhf",
    "status": "running",
    "template_id": "tpl-8m3lr002xe6tjjqi1",
    "timeout": 300,
    "created_at": "2025-11-21T07:20:32.326214Z"
  }
}
```

**差异分析**:

| E2B 字段 | ScaleBox 字段 | 状态 |
|----------|---------------|------|
| `clientID` | ❌ 不存在 | 缺失 |
| `envdVersion` | ❌ 不存在 | 缺失 |
| `sandboxID` | `data.sandbox_id` | 字段名和结构不同 |
| `templateID` | `data.template_id` | 字段名和结构不同 |
| `envdAccessToken` | `data.envd_access_token` | 字段名和结构不同 |
| `domain` | `data.sandbox_domain` | 字段名不同 |
| - | `data.success` | ScaleBox 额外字段 |
| - | `data.status` | ScaleBox 额外字段 |

**SDK 错误信息**:
```
KeyError: 'clientID'
File: e2b/api/client/models/sandbox.py, line 85
```

**结果**: ❌ 响应格式不兼容，SDK 无法解析

## 兼容性总结

| 特性 | E2B | ScaleBox | 兼容性 |
|------|-----|----------|--------|
| API 端点路径 | `/sandboxes` | `/v1/sandboxes` | ⚠️ 可通过配置解决 |
| 认证方式 | `X-API-KEY` | `X-API-KEY` | ✅ 完全兼容 |
| 请求格式 | JSON | JSON | ✅ 兼容 |
| 响应结构 | 扁平 JSON | 嵌套 `{success, data}` | ❌ 不兼容 |
| 字段命名 | 驼峰 (camelCase) | 下划线 (snake_case) | ❌ 不兼容 |
| 必需字段 | `clientID`, `envdVersion` | 缺失 | ❌ 不兼容 |

## 问题说明

### 响应格式不兼容的具体问题

1. **结构差异**: 
   - E2B: 扁平 JSON 对象
   - ScaleBox: 嵌套在 `{success: true, data: {...}}` 结构中

2. **字段命名差异**:
   - E2B: 使用驼峰命名 (`sandboxID`, `templateID`)
   - ScaleBox: 使用下划线命名 (`sandbox_id`, `template_id`)

3. **缺失必需字段**:
   - `clientID`: E2B SDK 必需，ScaleBox 未提供
   - `envdVersion`: E2B SDK 必需，ScaleBox 未提供

## E2B API 规范来源

E2B 没有公开的 OpenAPI/Swagger 规范文档，API 响应格式定义在 SDK 源码中：

- **响应模型定义**: `e2b/api/client/models/sandbox.py`
- **字段验证**: SDK 使用 `attrs` 库进行严格的字段验证
- **命名约定**: 驼峰命名（camelCase）

这些定义是 E2B SDK 的事实标准，任何声称兼容 E2B 的服务都需要遵循这些规范。

## 测试文件

本次测试的相关文件：

- POC 测试脚本: `poc/poc_e2b_test.py`
- 环境配置: `poc/.env`
- 虚拟环境: `e2bvenv/`

## 参考资料

- E2B 官方文档: https://e2b.dev/docs
- E2B SDK GitHub: https://github.com/e2b-dev/e2b
- E2B SDK 响应模型: `e2b/api/client/models/sandbox.py`
