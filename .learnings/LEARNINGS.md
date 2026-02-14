# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---

## [LRN-20260214-001] best_practice

**Logged**: 2026-02-14T16:45:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
Context Manager 技能的 summarize 命令在长会话中可能超时失败

### Details
在安装和测试 ClawHub 的 context-manager 技能时发现：
- `list` 和 `status` 命令正常工作
- `summarize` 命令调用 `openclaw agent --session-id` 让 AI 生成摘要
- 当会话 token 较多（>40k）时，AI 处理时间过长导致命令失败
- 脚本没有设置足够的超时时间

### Suggested Action
1. 在会话早期（token < 30k）使用 summarize
2. 或者等待 OpenClaw 内置的自动压缩功能
3. 可以只用 list/status 监控会话使用情况

### Metadata
- Source: user_feedback
- Related Files: skills/context-manager/compress.sh
- Tags: context-manager, timeout, session-compression

---

