#!/usr/bin/env python3
"""简洁的 Todo CLI 工具"""
import json
import sys
from pathlib import Path

TODO_FILE = Path.home() / ".todo.json"


def load_todos():
    """加载任务"""
    if not TODO_FILE.exists():
        return []
    return json.loads(TODO_FILE.read_text())


def save_todos(todos):
    """保存任务"""
    TODO_FILE.write_text(json.dumps(todos, indent=2, ensure_ascii=False))


def add_todo(title):
    """添加任务"""
    todos = load_todos()
    todo_id = max([t["id"] for t in todos], default=0) + 1
    todos.append({"id": todo_id, "title": title, "completed": False})
    save_todos(todos)
    print(f"✓ 添加任务 #{todo_id}: {title}")


def list_todos():
    """列出所有任务"""
    todos = load_todos()
    if not todos:
        print("暂无任务")
        return
    print("\n待办事项:")
    for t in todos:
        status = "✓" if t["completed"] else " "
        print(f"  [{status}] #{t['id']} {t['title']}")
    print()


def done_todo(todo_id):
    """完成任务"""
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            t["completed"] = True
            save_todos(todos)
            print(f"✓ 完成任务 #{todo_id}: {t['title']}")
            return
    print(f"✗ 未找到任务 #{todo_id}")


def delete_todo(todo_id):
    """删除任务"""
    todos = load_todos()
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            deleted = todos.pop(i)
            save_todos(todos)
            print(f"✓ 删除任务 #{todo_id}: {deleted['title']}")
            return
    print(f"✗ 未找到任务 #{todo_id}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: todo <命令> [参数]")
        print("命令: add <任务> | list | done <ID> | delete <ID>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        if len(sys.argv) < 3:
            print("用法: todo add <任务内容>")
            sys.exit(1)
        add_todo(" ".join(sys.argv[2:]))
    
    elif cmd == "list":
        list_todos()
    
    elif cmd == "done":
        if len(sys.argv) < 3:
            print("用法: todo done <任务ID>")
            sys.exit(1)
        done_todo(int(sys.argv[2]))
    
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("用法: todo delete <任务ID>")
            sys.exit(1)
        delete_todo(int(sys.argv[2]))
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
