# Sequential Thinking 快速调用指南

## 紫灵的调用方式

紫灵现在可以直接调用 Sequential Thinking MCP 来帮助主人解决复杂问题。

### 基本用法

```bash
# 快速调用脚本
/Users/yangyang/.openclaw/workspace/skills/sequential-thinking/scripts/think.sh "思考内容" 步骤编号 总步骤数 是否继续

# 示例：第一步思考
./think.sh "分析问题的核心要素" 1 5 true
```

### 紫灵自动调用示例

当主人遇到复杂问题时，紫灵会：

1. **分解问题**
   ```bash
   # 第一步：理解问题
   ./think.sh "首先，我需要理解这个问题的核心是什么..." 1 5 true

   # 第二步：收集信息
   ./think.sh "接下来，我需要收集哪些相关信息..." 2 5 true

   # 第三步：分析
   ./think.sh "基于收集的信息，我的分析是..." 3 5 true

   # 第四步：验证
   ./think.sh "让我验证一下这个结论..." 4 5 true

   # 第五步：结论
   ./think.sh "最终，我的答案是..." 5 5 false
   ```

2. **动态调整**
   ```bash
   # 如果发现需要更多步骤
   ./think.sh "我发现需要更深入的分析..." 6 7 true
   ```

3. **回溯修订**
   ```bash
   # 修订之前的想法
   ./think.sh "等等，我需要重新考虑第三步..." 4 5 true true 3
   ```

## 适用场景

### ✅ 适合使用 Sequential Thinking
- 复杂的推理问题（数学、逻辑）
- 多步骤规划任务
- 需要验证的假设推理
- 初始信息不完整的问题
- 需要逐步拆解的复杂任务

### ❌ 不适合使用 Sequential Thinking
- 简单的直接查询
- 单步就能解决的问题
- 不需要推理的事实性问题

## 紫灵的调用策略

1. **自动判断**：紫灵会根据问题的复杂度决定是否使用
2. **逐步推进**：每次调用都会基于前一次的结果
3. **动态调整**：根据实际情况调整总步骤数
4. **适时结束**：当得出满意答案时及时结束思考

## API 调用格式

```bash
export ZHIPU_API_KEY="5767413d4c9c4b4bbcf37fe71987a246.q8c587g9VUgjOxBN"

mcporter call sequential-thinking.sequentialThinking \
  thought="思考内容" \
  thoughtNumber:1 \
  totalThoughts:5 \
  nextThoughtNeeded:true \
  isRevision:false \
  revisesThought:0 \
  branchFromThought:0 \
  branchId:"" \
  needsMoreThoughts:false \
  --output json
```

## 注意事项

- **免费服务**：MIT 开源许可，智谱 AI 提供云端服务
- **支持模型**：GLM-4-Plus、GLM-4-Flash 等支持 Function Calling 的模型
- **协议支持**：SSE 和 Streamable 两种协议
- **环境变量**：API Key 已配置在 `~/.zshrc` 中

## 调试命令

```bash
# 查看服务状态
mcporter list

# 查看工具详情
mcporter list sequential-thinking --schema

# 测试连接
mcporter call sequential-thinking.sequentialThinking \
  thought="测试连接" \
  thoughtNumber:1 \
  totalThoughts:1 \
  nextThoughtNeeded:false \
  isRevision:false \
  revisesThought:0 \
  branchFromThought:0 \
  branchId:"" \
  needsMoreThoughts:false
```
