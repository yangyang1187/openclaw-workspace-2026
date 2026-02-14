# Errors

Command failures, exceptions, and unexpected behavior logged during development.

**Statuses**: pending | in_progress | resolved | wont_fix
**Priorities**: critical | high | medium | low

---

## [ERR-20260214-001] context-manager

**Logged**: 2026-02-14T16:46:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
context-manager 技能 summarize 命令执行失败

### Error
```
Process exited with code 1
(无具体错误输出)
```

### Context
- **Command**: `./compress.sh summarize agent:main:main --replace`
- **Session**: agent:main:main (token: ~47k)
- **Environment**: macOS, OpenClaw running, zsh

### Root Cause
AI 生成摘要需要阅读整个会话历史，当 token 过多时响应时间超出脚本预期。

### Suggested Fix
1. 增加脚本超时时间
2. 在会话早期执行压缩
3. 使用分段压缩策略

### Metadata
- Reproducible: yes (在长会话中)
- Related Files: skills/context-manager/compress.sh
- See Also: LRN-20260214-001

---
