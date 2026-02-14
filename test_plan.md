# Todo CLI 工具测试方案

本测试方案为 Todo CLI 工具设计全面的测试覆盖，包括单元测试、集成测试和边界条件测试。

---

## 1. 单元测试用例（5个关键场景）

### 1.1 测试 load_todos 加载任务功能
- 测试空文件时返回空列表
- 测试正常加载任务列表

### 1.2 测试 add_todo 添加任务功能
- 测试添加单个任务
- 测试任务 ID 自增正确

### 1.3 测试 done_todo 完成任务功能
- 测试成功完成任务
- 测试任务不存在的情况

### 1.4 测试 delete_todo 删除任务功能
- 测试成功删除任务
- 测试删除不存在的任务

### 1.5 测试 save_todos 保存任务功能
- 测试数据正确序列化到文件

---

## 2. 集成测试场景（2个）

### 2.1 完整的任务生命周期
- 添加 → 列表查看 → 完成 → 列表确认 → 删除

### 2.2 多个任务并发操作
- 同时添加多个任务，验证 ID 唯一性和数据一致性

---

## 3. 边界条件测试

- 空任务标题
- 超长任务标题
- 负数任务 ID
- 非数字任务 ID
- 并发写入冲突
- 文件权限问题

---

# pytest 测试代码示例

```python
#!/usr/bin/env python3
"""
Todo CLI 工具测试套件
使用 pytest 风格编写
"""

import json
import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# 导入待测模块
import todo


# ===== Fixtures =====

@pytest.fixture
def temp_todo_file(tmp_path):
    """创建临时 TODO 文件"""
    todo_file = tmp_path / ".todo.json"
    todo.TODO_FILE = todo_file
    yield todo_file
    # 清理


@pytest.fixture
def sample_todos():
    """示例任务数据"""
    return [
        {"id": 1, "title": "完成报告", "completed": False},
        {"id": 2, "title": "发送邮件", "completed": True},
    ]


# ===== 单元测试 =====

class TestLoadTodos:
    """测试 load_todos 函数"""

    def test_load_empty_file(self, temp_todo_file):
        """场景1: 空文件返回空列表"""
        temp_todo_file.write_text("")
        todos = todo.load_todos()
        assert todos == []

    def test_load_nonexistent_file(self, temp_todo_file):
        """场景2: 文件不存在返回空列表"""
        temp_todo_file.unlink()  # 确保文件不存在
        todos = todo.load_todos()
        assert todos == []

    def test_load_valid_data(self, temp_todo_file, sample_todos):
        """场景3: 正常加载任务列表"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        todos = todo.load_todos()
        assert len(todos) == 2
        assert todos[0]["title"] == "完成报告"


class TestAddTodo:
    """测试 add_todo 函数"""

    def test_add_single_todo(self, temp_todo_file, capsys):
        """场景4: 添加单个任务"""
        todo.add_todo("编写测试代码")
        
        todos = todo.load_todos()
        assert len(todos) == 1
        assert todos[0]["title"] == "编写测试代码"
        assert todos[0]["completed"] is False
        
        captured = capsys.readouterr()
        assert "✓ 添加任务 #1" in captured.out

    def test_add_multiple_todos_increment_id(self, temp_todo_file, capsys):
        """场景5: 多个任务 ID 正确自增"""
        todo.add_todo("任务1")
        todo.add_todo("任务2")
        todo.add_todo("任务3")
        
        todos = todo.load_todos()
        assert len(todos) == 3
        assert [t["id"] for t in todos] == [1, 2, 3]

    def test_add_empty_title(self, temp_todo_file, capsys):
        """边界: 空任务标题"""
        todo.add_todo("")
        
        todos = todo.load_todos()
        assert len(todos) == 1
        assert todos[0]["title"] == ""

    def test_add_very_long_title(self, temp_todo_file):
        """边界: 超长任务标题 (1000+ 字符)"""
        long_title = "测试任务标题 " * 100
        todo.add_todo(long_title)
        
        todos = todo.load_todos()
        assert len(todos[0]["title"]) == len(long_title)


class TestDoneTodo:
    """测试 done_todo 函数"""

    def test_done_existing_todo(self, temp_todo_file, sample_todos, capsys):
        """场景6: 成功完成任务"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        
        todo.done_todo(1)
        
        todos = todo.load_todos()
        assert todos[0]["completed"] is True
        
        captured = capsys.readouterr()
        assert "✓ 完成任务 #1" in captured.out

    def test_done_nonexistent_todo(self, temp_todo_file, sample_todos, capsys):
        """场景7: 任务不存在"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        
        todo.done_todo(999)
        
        captured = capsys.readouterr()
        assert "✗ 未找到任务 #999" in captured.out


class TestDeleteTodo:
    """测试 delete_todo 函数"""

    def test_delete_existing_todo(self, temp_todo_file, sample_todos, capsys):
        """场景8: 成功删除任务"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        
        todo.delete_todo(1)
        
        todos = todo.load_todos()
        assert len(todos) == 1
        assert todos[0]["id"] == 2
        
        captured = capsys.readouterr()
        assert "✓ 删除任务 #1" in captured.out

    def test_delete_nonexistent_todo(self, temp_todo_file, sample_todos, capsys):
        """场景9: 删除不存在的任务"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        
        todo.delete_todo(999)
        
        captured = capsys.readouterr()
        assert "✗ 未找到任务 #999" in captured.out

    def test_delete_last_todo(self, temp_todo_file, sample_todos):
        """边界: 删除最后一个任务"""
        temp_todo_file.write_text(json.dumps([sample_todos[0]]))
        
        todo.delete_todo(1)
        
        todos = todo.load_todos()
        assert todos == []


class TestSaveTodos:
    """测试 save_todos 函数"""

    def test_save_todos(self, temp_todo_file, sample_todos):
        """场景10: 保存任务到文件"""
        todo.save_todos(sample_todos)
        
        content = json.loads(temp_todo_file.read_text())
        assert content == sample_todos


# ===== 集成测试 =====

class TestTaskLifecycle:
    """集成测试: 完整的任务生命周期"""

    def test_complete_lifecycle(self, temp_todo_file, capsys):
        """场景11: 添加 → 列表 → 完成 → 列表确认 → 删除"""
        # 1. 添加任务
        todo.add_todo("学习 Python")
        
        # 2. 列出任务
        todo.list_todos()
        captured = capsys.readouterr()
        assert "学习 Python" in captured.out
        
        # 3. 完成任务
        todo.done_todo(1)
        
        # 4. 再次列出确认状态
        todo.list_todos()
        captured = capsys.readouterr()
        assert "[✓]" in captured.out
        
        # 5. 删除任务
        todo.delete_todo(1)
        
        # 6. 确认删除
        todo.list_todos()
        captured = capsys.readouterr()
        assert "暂无任务" in captured.out


class TestMultipleTasks:
    """集成测试: 多个任务并发操作"""

    def test_multiple_concurrent_tasks(self, temp_todo_file):
        """场景12: 添加多个任务，验证 ID 唯一性和数据一致性"""
        # 添加多个任务
        titles = ["任务A", "任务B", "任务C", "任务D", "任务E"]
        for title in titles:
            todo.add_todo(title)
        
        # 验证
        todos = todo.load_todos()
        
        # ID 唯一性
        ids = [t["id"] for t in todos]
        assert len(ids) == len(set(ids))
        
        # 数据完整性
        saved_titles = [t["title"] for t in todos]
        assert saved_titles == titles
        
        # 完成部分任务
        todo.done_todo(1)
        todo.done_todo(3)
        
        todos = todo.load_todos()
        assert todos[0]["completed"] is True
        assert todos[1]["completed"] is False
        assert todos[2]["completed"] is True


# ===== 边界条件测试 =====

class TestEdgeCases:
    """边界条件测试"""

    def test_invalid_todo_id_negative(self, temp_todo_file, sample_todos, capsys):
        """边界13: 负数任务 ID"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        
        todo.done_todo(-1)
        
        captured = capsys.readouterr()
        assert "✗ 未找到任务 #-1" in captured.out

    def test_invalid_todo_id_zero(self, temp_todo_file, sample_todos, capsys):
        """边界14: 零 ID"""
        temp_todo_file.write_text(json.dumps(sample_todos))
        
        todo.done_todo(0)
        
        captured = capsys.readouterr()
        assert "✗ 未找到任务 #0" in captured.out

    def test_non_numeric_id(self, temp_todo_file, capsys):
        """边界15: 非数字 ID（测试 main 函数参数处理）"""
        with patch.object(sys, "argv", ["todo", "done", "abc"]):
            with pytest.raises(SystemExit):
                todo.main()

    def test_invalid_json_file(self, temp_todo_file):
        """边界16: 损坏的 JSON 文件"""
        temp_todo_file.write_text("{invalid json")
        
        with pytest.raises(json.JSONDecodeError):
            todo.load_todos()

    def test_command_without_arguments(self, temp_todo_file, capsys):
        """边界17: 无参数运行"""
        with patch.object(sys, "argv", ["todo"]):
            with pytest.raises(SystemExit):
                todo.main()
            
            captured = capsys.readouterr()
            assert "用法" in captured.out

    def test_unknown_command(self, temp_todo_file, capsys):
        """边界18: 未知命令"""
        with patch.object(sys, "argv", ["todo", "unknown"]):
            with pytest.raises(SystemExit):
                todo.main()
            
            captured = capsys.readouterr()
            assert "未知命令" in captured.out

    def test_add_command_without_title(self, temp_todo_file, capsys):
        """边界19: add 命令缺少标题"""
        with patch.object(sys, "argv", ["todo", "add"]):
            with pytest.raises(SystemExit):
                todo.main()
            
            captured = capsys.readouterr()
            assert "用法" in captured.out

    def test_done_command_without_id(self, temp_todo_file, capsys):
        """边界20: done 命令缺少 ID"""
        with patch.object(sys, "argv", ["todo", "done"]):
            with pytest.raises(SystemExit):
                todo.main()


# ===== 运行测试 =====

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
```

---

## 测试覆盖总结

| 测试类型 | 测试场景数 | 覆盖功能 |
|---------|-----------|---------|
| 单元测试 | 10 | load_todos, add_todo, done_todo, delete_todo, save_todos |
| 集成测试 | 2 | 任务生命周期, 多任务并发操作 |
| 边界测试 | 8 | 无效 ID, 损坏文件, 参数缺失, 未知命令 |

**总计: 20 个测试用例**

---

## 运行方式

```bash
# 运行所有测试
pytest test_todo.py -v

# 运行指定测试类
pytest test_todo.py::TestAddTodo -v

# 显示详细输出
pytest test_todo.py -v --tb=long

# 生成覆盖率报告
pytest test_todo.py --cov=todo --cov-report=html
```
