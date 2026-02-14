#!/usr/bin/env python3
"""Todo CLI 测试方案"""
import pytest
import json
import tempfile
from pathlib import Path
from todo import load_todos, save_todos, add_todo, list_todos, done_todo, delete_todo


class TestTodoCLI:
    """Todo CLI 单元测试"""
    
    def setup_method(self):
        """每个测试前创建临时文件"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_path = Path(self.temp_file.name)
        self.temp_file.close()
    
    def teardown_method(self):
        """每个测试后清理"""
        if self.temp_path.exists():
            self.temp_path.unlink()
    
    # ========== 1. 单元测试用例 ==========
    
    def test_add_todo(self):
        """测试添加任务"""
        save_todos([])
        add_todo("测试任务1")
        todos = load_todos()
        
        assert len(todos) == 1
        assert todos[0]["title"] == "测试任务1"
        assert todos[0]["completed"] is False
        assert todos[0]["id"] == 1
    
    def test_add_multiple_todos(self):
        """测试添加多个任务，ID自增"""
        save_todos([])
        add_todo("任务1")
        add_todo("任务2")
        add_todo("任务3")
        todos = load_todos()
        
        assert len(todos) == 3
        assert todos[0]["id"] == 1
        assert todos[1]["id"] == 2
        assert todos[2]["id"] == 3
    
    def test_list_todos_empty(self, capsys):
        """测试列出空任务列表"""
        save_todos([])
        list_todos()
        captured = capsys.readouterr()
        
        assert "暂无任务" in captured.out
    
    def test_list_todos_with_data(self, capsys):
        """测试列出有任务的列表"""
        save_todos([
            {"id": 1, "title": "任务A", "completed": False},
            {"id": 2, "title": "任务B", "completed": True}
        ])
        list_todos()
        captured = capsys.readouterr()
        
        assert "任务A" in captured.out
        assert "任务B" in captured.out
    
    def test_done_todo(self):
        """测试完成任务"""
        save_todos([
            {"id": 1, "title": "待完成任务", "completed": False}
        ])
        done_todo(1)
        todos = load_todos()
        
        assert todos[0]["completed"] is True
    
    def test_done_nonexistent_todo(self, capsys):
        """测试完成不存在的任务"""
        save_todos([])
        done_todo(999)
        captured = capsys.readouterr()
        
        assert "未找到任务" in captured.out
    
    def test_delete_todo(self):
        """测试删除任务"""
        save_todos([
            {"id": 1, "title": "待删除任务", "completed": False}
        ])
        delete_todo(1)
        todos = load_todos()
        
        assert len(todos) == 0
    
    def test_delete_nonexistent_todo(self, capsys):
        """测试删除不存在的任务"""
        save_todos([])
        delete_todo(999)
        captured = capsys.readouterr()
        
        assert "未找到任务" in captured.out
    
    # ========== 2. 集成测试场景 ==========
    
    def test_full_workflow(self):
        """集成测试：完整工作流"""
        # 清空
        save_todos([])
        
        # 添加3个任务
        add_todo("任务A")
        add_todo("任务B")
        add_todo("任务C")
        
        # 完成1个
        done_todo(1)
        
        # 删除1个
        delete_todo(2)
        
        # 验证最终状态
        todos = load_todos()
        assert len(todos) == 2
        assert todos[0]["completed"] is True  # 任务A
        assert todos[1]["completed"] is False  # 任务C
    
    def test_persistence(self):
        """集成测试：数据持久化"""
        # 添加任务
        save_todos([])
        add_todo("持久化测试")
        
        # 重新加载，验证数据仍然存在
        todos = load_todos()
        assert len(todos) == 1
        assert todos[0]["title"] == "持久化测试"
    
    # ========== 3. 边界条件测试 ==========
    
    def test_empty_title(self):
        """边界测试：空任务标题"""
        # 当前实现允许空标题，这是一个潜在的改进点
        save_todos([])
        add_todo("")
        todos = load_todos()
        
        assert len(todos) == 1
        assert todos[0]["title"] == ""
    
    def test_long_title(self):
        """边界测试：超长任务标题"""
        save_todos([])
        long_title = "这是一个非常长的任务标题" * 100
        add_todo(long_title)
        todos = load_todos()
        
        assert todos[0]["title"] == long_title
    
    def test_special_characters(self):
        """边界测试：特殊字符"""
        save_todos([])
        special_title = "任务 <script> & 'quote' \"double\" 中文 🎉"
        add_todo(special_title)
        todos = load_todos()
        
        assert todos[0]["title"] == special_title
    
    def test_large_dataset(self):
        """边界测试：大量任务"""
        save_todos([])
        for i in range(1000):
            add_todo(f"任务{i}")
        
        todos = load_todos()
        assert len(todos) == 1000
    
    def test_duplicate_ids(self):
        """边界测试：ID不重复（删除后重新添加）"""
        save_todos([])
        add_todo("任务1")
        add_todo("任务2")
        delete_todo(1)
        add_todo("任务3")
        
        todos = load_todos()
        ids = [t["id"] for t in todos]
        
        # ID应该唯一
        assert len(ids) == len(set(ids))


# 运行测试: pytest test_todo.py -v
