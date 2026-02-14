---
name: sequential-thinking
description: 使用 Sequential Thinking MCP 服务进行结构化、分步骤的复杂问题解决。支持动态调整、回溯和假设验证。
homepage: https://bigmodel.cn/marketplace/index/mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["mcporter"], "env": ["ZHIPU_API_KEY"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
      },
  }
---

# Sequential Thinking MCP 技能

使用智谱 AI 开放平台提供的 Sequential Thinking MCP 服务，通过结构化思维过程促进复杂问题的分步骤解决。

## 功能特性

- 🧠 **结构化思考**：将复杂问题分解为可管理的步骤
- 🔄 **动态调整**：随着理解的加深，修改和完善想法
- 💡 **假设验证**：生成解决方案假设，基于思维链步骤进行验证
- 🔙 **回溯分支**：支持质疑和修订之前的想法，分支探索不同路径

## 使用场景

- 将复杂问题分解成步骤使解决方案逐步清晰
- 需要迭代修订的规划和设计过程
- 分析初始范围不明确的问题
- 需要在多个步骤中保持上下文的任务
- 在解决问题过程中过滤掉无关信息

## 配置

### 1. 获取 API Key

前往 [智谱 BigModel 开放平台 API Key 页面](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) 获取您的 API Key。

### 2. 设置环境变量

```bash
export ZHIPU_API_KEY="your_api_key_here"
```

或者在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
export ZHIPU_API_KEY="your_api_key_here"
```

### 3. 配置 mcporter

创建或编辑 `~/.openclaw/workspace/config/mcporter.json`：

```json
{
  "servers": {
    "sequential-thinking": {
      "url": "https://open.bigmodel.cn/api/mcp-broker/proxy/sequential-thinking/sse",
      "headers": {
        "Authorization": "Bearer ${ZHIPU_API_KEY}"
      }
    }
  }
}
```

## 使用方法

### 基本调用

```bash
mcporter call sequential-thinking.sequentialThinking \
  thought="第一步：分析问题的核心要素" \
  thought_number:1 \
  total_thoughts:5 \
  next_thought_needed:true
```

### 参数说明

- `thought`：当前思考步骤的内容（可包含分析、修订、疑问、假设等）
- `thought_number`：当前步骤编号
- `total_thoughts`：预计需要的总步骤数（可动态调整）
- `next_thought_needed`：是否需要继续思考（true/false）
- `is_revision`：是否是对之前想法的修订（可选）
- `revises_thought`：如果 is_revision 为 true，指明修订的是第几步（可选）
- `branch_from_thought`：如果分支，从第几步开始分支（可选）
- `branch_id`：当前分支的标识符（可选）
- `needs_more_thoughts`：是否需要更多思考步骤（可选）

### 使用示例

#### 分步骤解决数学问题

```bash
# 第一步
mcporter call sequential-thinking.sequentialThinking \
  thought="小明初始有1个苹果" \
  thought_number:1 \
  total_thoughts:4 \
  next_thought_needed:true

# 第二步
mcporter call sequential-thinking.sequentialThinking \
  thought="妈妈给了小明1个苹果，现在小明有1+1=2个苹果" \
  thought_number:2 \
  total_thoughts:4 \
  next_thought_needed:true

# 第三步
mcporter call sequential-thinking.sequentialThinking \
  thought="爸爸拿走了2个苹果，小明现在有2-2=0个苹果" \
  thought_number:3 \
  total_thoughts:4 \
  next_thought_needed:true

# 第四步（结论）
mcporter call sequential-thinking.sequentialThinking \
  thought="最终答案：小明还有0个苹果" \
  thought_number:4 \
  total_thoughts:4 \
  next_thought_needed:false
```

#### 修订之前的想法

```bash
mcporter call sequential-thinking.sequentialThinking \
  thought="等等，我需要重新考虑第三步..." \
  thought_number:4 \
  total_thoughts:5 \
  next_thought_needed:true \
  is_revision:true \
  revises_thought:3
```

## 价格

**免费使用** - 该服务基于 MIT 开源许可，智谱 AI 开放平台已为您部署好云端服务。

## 相关链接

- [智谱 AI 开放平台](https://bigmodel.cn/)
- [MCP 服务市场](https://bigmodel.cn/marketplace/index/mcp)
- [源码地址](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
- [API Key 页面](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)

## 注意事项

1. 该 MCP 支持通过 GLM 文本模型 API 直接调用
2. 支持 SSE 和 Streamable 两种协议
3. 需要使用支持 Function Calling 的模型（Z1 系列推理模型不支持）
4. 可根据实际情况动态调整 total_thoughts 参数
