# todo-cli
A minimal command-line todo manager in Python.


````markdown
# todo-cli

一个极简的命令行待办事项管理器，使用 Python 编写。

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 简介

`todo-cli` 是一个轻量级的命令行工具，帮助你在终端中快速管理待办事项。数据以 JSON 格式保存在本地，无需数据库，无需网络。

## 功能

- 添加待办事项
- 列出所有待办
- 标记待办为已完成
- 删除单个待办
- 清空所有待办
- 数据持久化到本地 JSON 文件

## 安装

### 从源码安装

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/todo-cli.git
cd todo-cli

# 2. 创建并激活虚拟环境
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\activate

# 3. 安装
pip install -e .
```

安装完成后，验证：

```bash
todo --help
```

如果看到帮助信息，说明安装成功。

## 使用

### 添加待办

```bash
todo add "买牛奶"
todo add "写周报"
todo add "背 50 个单词"
```

> 包含空格的文字需要用引号包裹。

### 查看所有待办

```bash
todo list
```

输出示例：

```text
[ ] 1. 买牛奶
[ ] 2. 写周报
[ ] 3. 背 50 个单词

3 pending, 0 done.
```

`[ ]` 表示未完成，`[x]` 表示已完成。前面的数字是 ID，后续操作需要用到。

### 完成某个待办

```bash
todo done 1
```

再次查看：

```bash
todo list
```

输出：

```text
[x] 1. 买牛奶
[ ] 2. 写周报
[ ] 3. 背 50 个单词

2 pending, 1 done.
```

### 删除某个待办

```bash
todo remove 2
```

### 清空所有待办

```bash
todo clear
```

> 此操作会删除所有待办，请谨慎使用。

## 数据存储

默认情况下，待办数据保存在用户主目录下的 `.todo.json` 文件中：

- macOS / Linux: `~/.todo.json`
- Windows: `C:\Users\你的用户名\.todo.json`

文件内容示例：

```json
[
  {
    "id": 1,
    "text": "买牛奶",
    "done": false
  },
  {
    "id": 2,
    "text": "写周报",
    "done": true
  }
]
```

你可以通过 `--file` 参数指定其他数据文件。注意：`--file` 必须放在子命令之前。

```bash
todo --file ./my-todos.json list
todo --file ./my-todos.json add "测试"
```

## 开发

### 环境准备

```bash
# 安装开发依赖（包含 pytest）
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 项目结构

```text
todo-cli/
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py      # Todo 数据类
│       ├── storage.py     # JSON 持久化层
│       └── cli.py         # 命令行接口
└── tests/
    ├── test_storage.py
    └── test_cli.py
```

### 不使用安装直接运行

```bash
python -m todo_cli list
```

## 卸载

```bash
pip uninstall todo-cli
```

## 许可证

本项目采用 [MIT](LICENSE) 许可证。
````
