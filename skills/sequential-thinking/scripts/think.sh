#!/bin/bash
# Sequential Thinking MCP 调用脚本
# 用法: ./think.sh "思考内容" 步骤编号 总步骤数 是否继续 是否修订

THOUGHT="$1"
THOUGHT_NUMBER="${2:-1}"
TOTAL_THOUGHTS="${3:-5}"
NEXT_THOUGHT="${4:-true}"
IS_REVISION="${5:-false}"
REVISIONS_THOUGHT="${6:-0}"
BRANCH_FROM="${7:-0}"
BRANCH_ID="${8:-}"
NEEDS_MORE="${9:-false}"

export ZHIPU_API_KEY="5767413d4c9c4b4bbcf37fe71987a246.q8c587g9VUgjOxBN"

mcporter call sequential-thinking.sequentialThinking \
  thought="$THOUGHT" \
  thoughtNumber:$THOUGHT_NUMBER \
  totalThoughts:$TOTAL_THOUGHTS \
  nextThoughtNeeded:$NEXT_THOUGHT \
  isRevision:$IS_REVISION \
  revisesThought:$REVISIONS_THOUGHT \
  branchFromThought:$BRANCH_FROM \
  branchId:"$BRANCH_ID" \
  needsMoreThoughts:$NEEDS_MORE \
  --output json
