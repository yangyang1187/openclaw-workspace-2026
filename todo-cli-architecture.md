# Todo CLI 工具技术架构设计

## 1. 技术栈选择

### 1.1 编程语言: Go

**理由：**
- 编译型语言，性能好，启动快
- 交叉编译方便，一个二进制文件部署
- 标准库丰富，CLI 开发体验好
- 社区成熟（cobra, urfave/cli 等成熟的 CLI 框架）

### 1.2 存储方案: SQLite + JSON 文件

| 方案 | 适用场景 | 优势 |
|------|----------|------|
| **SQLite** | 任务数据持久化 | 轻量级、事务支持、查询灵活 |
| **JSON 文件** | 配置文件、简单导出 | 人类可读、易于调试、版本控制友好 |

**混合策略：**
- 任务数据 → SQLite (`~/.todo/tasks.db`)
- 配置文件 → JSON (`~/.todo/config.json`)
- 导出/备份 → JSON/CSV

---

## 2. 模块划分（4个核心模块）

```
┌─────────────────────────────────────────────────────────┐
│                      CLI Entry                          │
│                    (cmd/todo/main.go)                    │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Command     │  │   Storage     │  │   Business    │
│   (命令层)    │  │   (存储层)    │  │   (业务层)    │
│               │  │               │  │               │
│ - add         │  │ - SQLite      │  │ - TaskService │
│ - list        │  │ - Config      │  │ - TagService  │
│ - done        │  │ - Export      │  │ - ProjectSvc  │
│ - rm          │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                ┌───────────────────────┐
                │      Domain           │
                │      (核心模型)       │
                │   - Task              │
                │   - Tag               │
                │   - Project           │
                └───────────────────────┘
```

---

## 3. 数据结构设计

### 3.1 核心模型

```go
// domain/task.go
package domain

import "time"

type Task struct {
    ID          int64     `json:"id" db:"id"`
    Title       string    `json:"title" db:"title"`
    Description string    `json:"description,omitempty" db:"description"`
    Priority    int       `json:"priority" db:"priority"` // 1=低, 2=中, 3=高
    Status      string    `json:"status" db:"status"`     // pending, done, archived
    
    // 关联
    ProjectID   *int64    `json:"project_id,omitempty" db:"project_id"`
    Tags        []string  `json:"tags,omitempty"` // 内存字段，不存DB
    
    // 时间
    DueDate     *time.Time `json:"due_date,omitempty" db:"due_date"`
    CompletedAt *time.Time `json:"completed_at,omitempty" db:"completed_at"`
    CreatedAt   time.Time  `json:"created_at" db:"created_at"`
    UpdatedAt   time.Time  `json:"updated_at" db:"updated_at"`
}

type Project struct {
    ID          int64     `json:"id" db:"id"`
    Name        string    `json:"name" db:"name"`
    Description string    `json:"description,omitempty" db:"description"`
    Color       string    `json:"color" db:"color"` // hex颜色
    Archived    bool      `json:"archived" db:"archived"`
    CreatedAt   time.Time `json:"created_at" db:"created_at"`
}

type Tag struct {
    ID    int64  `json:"id" db:"id"`
    Name  string `json:"name" db:"name"`
    Color string `json:"color" db:"color"`
}
```

### 3.2 配置结构

```go
// domain/config.go
package domain

type Config struct {
    DBPath       string `json:"db_path"`       // 数据库路径
    Editor      string `json:"editor"`        // 首选编辑器
    DateFormat   string `json:"date_format"`   // 日期格式
    ListFormat   string `json:"list_format"`   // 输出格式: compact, detailed
    ShowDone     bool   `json:"show_done"`     // 是否显示已完成任务
}
```

### 3.3 数据库表结构

```sql
-- schema.sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    color TEXT DEFAULT '#3b82f6',
    archived INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    priority INTEGER DEFAULT 2,
    status TEXT DEFAULT 'pending',
    project_id INTEGER REFERENCES projects(id),
    due_date TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#6b7280'
);

-- 任务-标签 多对多关系
CREATE TABLE task_tags (
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- 索引
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

---

## 4. 目录结构

```
todo/
├── cmd/
│   └── todo/
│       └── main.go              # 入口文件
├── internal/
│   ├── domain/                  # 核心领域模型
│   │   ├── task.go
│   │   ├── project.go
│   │   ├── tag.go
│   │   └── config.go
│   │
│   ├── storage/                 # 存储层
│   │   ├── db.go               # SQLite 连接初始化
│   │   ├── task_repo.go        # Task CRUD
│   │   ├── project_repo.go
│   │   ├── tag_repo.go
│   │   └── config_repo.go
│   │
│   ├── service/                # 业务逻辑层
│   │   ├── task_service.go
│   │   ├── project_service.go
│   │   └── export_service.go
│   │
│   └── cli/                    # CLI 命令定义
│       ├── root.go            # root command
│       ├── add.go             # add 命令
│       ├── list.go            # list 命令
│       ├── done.go            # done 命令
│       ├── rm.go              # rm 命令
│       ├── project.go         # project 子命令
│       ├── tag.go             # tag 子命令
│       └── flags.go           # 公共 flags
│
├── pkg/
│   └── utils/                  # 工具函数
│       ├── time.go
│       └── string.go
│
├── schema/
│   └── schema.sql              # 数据库 Schema
│
├── config/
│   └── default.json            # 默认配置
│
├── go.mod
├── go.sum
└── README.md
```

---

## 5. 核心代码示例

### 5.1 入口文件

```go
// cmd/todo/main.go
package main

import (
    "log"
    "os"
    "todo/internal/cli"
    "todo/internal/storage"
)

func main() {
    // 初始化存储
    db, err := storage.InitDB()
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
    
    // 初始化配置
    cfg, err := storage.LoadConfig()
    if err != nil {
        log.Fatal(err)
    }
    
    // 运行 CLI
    if err := cli.New(cfg, db).Execute(); err != nil {
        os.Exit(1)
    }
}
```

### 5.2 CLI 框架

```go
// internal/cli/root.go
package cli

import (
    "github.com/spf13/cobra"
    "todo/internal/domain"
)

type CLI struct {
    cfg   *domain.Config
    db    interface{} // *sql.DB
    root  *cobra.Command
}

func New(cfg *domain.Config, db interface{}) *CLI {
    cli := &CLI{cfg: cfg, db: db}
    
    cli.root = &cobra.Command{
        Use:   "todo",
        Short: "一个简洁的 CLI 任务管理工具",
    }
    
    // 注册子命令
    cli.root.AddCommand(
        newAddCmd(cli),
        newListCmd(cli),
        newDoneCmd(cli),
        newRmCmd(cli),
        newProjectCmd(cli),
        newTagCmd(cli),
    )
    
    return cli
}

func (c *CLI) Execute() error {
    return c.root.Execute()
}
```

### 5.3 任务服务

```go
// internal/service/task_service.go
package service

import (
    "time"
    "todo/internal/domain"
    "todo/internal/storage"
)

type TaskService struct {
    repo *storage.TaskRepo
}

func NewTaskService(repo *storage.TaskRepo) *TaskService {
    return &TaskService{repo: repo}
}

func (s *TaskService) Create(title, desc string, priority int, projectID *int64, tags []string) (*domain.Task, error) {
    task := &domain.Task{
        Title:       title,
        Description: desc,
        Priority:    priority,
        Status:      "pending",
        ProjectID:   projectID,
        Tags:        tags,
        CreatedAt:   time.Now(),
        UpdatedAt:   time.Now(),
    }
    
    id, err := s.repo.Insert(task)
    if err != nil {
        return nil, err
    }
    
    task.ID = id
    return task, nil
}

func (s *TaskService) List(status string, projectID *int64) ([]domain.Task, error) {
    return s.repo.FindByFilter(status, projectID)
}

func (s *TaskService) Complete(id int64) error {
    now := time.Now()
    return s.repo.UpdateStatus(id, "done", &now)
}
```

### 5.4 Storage Repo

```go
// internal/storage/task_repo.go
package storage

import (
    "database/sql"
    "time"
    "todo/internal/domain"
)

type TaskRepo struct {
    db *sql.DB
}

func NewTaskRepo(db *sql.DB) *TaskRepo {
    return &TaskRepo{db: db}
}

func (r *TaskRepo) Insert(task *domain.Task) (int64, error) {
    result, err := r.db.Exec(`
        INSERT INTO tasks (title, description, priority, status, project_id, due_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
        task.Title, task.Description, task.Priority, task.Status, 
        task.ProjectID, task.DueDate, task.CreatedAt, task.UpdatedAt,
    )
    if err != nil {
        return 0, err
    }
    return result.LastInsertId()
}

func (r *TaskRepo) FindByFilter(status string, projectID *int64) ([]domain.Task, error) {
    query := "SELECT id, title, description, priority, status, project_id, due_date, created_at, updated_at FROM tasks WHERE 1=1"
    args := []interface{}{}
    
    if status != "" {
        query += " AND status = ?"
        args = append(args, status)
    }
    if projectID != nil {
        query += " AND project_id = ?"
        args = append(args, *projectID)
    }
    
    query += " ORDER BY priority DESC, created_at DESC"
    
    rows, err := r.db.Query(query, args...)
    if err != nil {
        return nil, err
    }
    defer rows.Close()
    
    var tasks []domain.Task
    for rows.Next() {
        var t domain.Task
        rows.Scan(&t.ID, &t.Title, &t.Description, &t.Priority, &t.Status, &t.ProjectID, &t.DueDate, &t.CreatedAt, &t.UpdatedAt)
        tasks = append(tasks, t)
    }
    return tasks, nil
}
```

---

## 6. 命令行使用示例

```bash
# 添加任务
todo add "完成架构设计文档" -p 3 -t work -d 2024-02-20

# 列出所有任务
todo list

# 列出指定项目任务
todo list -p project-name

# 标记完成
todo done 1

# 删除任务
todo rm 1

# 项目管理
todo project add "Go学习" -c "#10b981"
todo project list

# 标签管理
todo tag add important -c "#ef4444"
todo tag list
```

---

## 7. 扩展建议

| 扩展功能 | 实现方案 |
|----------|----------|
| 同步能力 | 未来可接入云端 SQLite (如 rclone 挂载) |
| 插件系统 | 使用 Go plugin 或 JSON-RPC |
| Web UI | 嵌入静态页面 + 小型 HTTP 服务器 |
| 多语言 | 使用 go-i18n |
