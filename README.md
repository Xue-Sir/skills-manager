# skills-manager

[![GitHub stars](https://img.shields.io/github/stars/Xue-Sir/skills-manager?style=social)](https://github.com/Xue-Sir/skills-manager/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)

[English](#installation) | [中文](#安装)

> Stop manually switching skills and MCPs per project. Let skills-manager organize them into categories and switch with one command.

A [Claude Code](https://claude.ai/code) skill that manages your skills, MCPs, and plugins by categories. Define once, switch anywhere.

**⚠️ For Claude Code users only.** This skill relies on Claude Code's directory structure (`~/.claude/skills/`, `skillOverrides`, `enabledPlugins`, etc.) and will not work with other AI coding tools.

> Tested on Claude Code CLI. Should work with Desktop/Web/IDE versions since they share the same directory structure, but not yet verified.

---

## Why skills-manager?

**The problem:** You have multiple skills, MCPs, and plugins. Different projects need different tools. Managing them manually is tedious and error-prone.

**The solution:** Organize tools into categories (modes). Switch to a category, and only those tools are active for your current project.

```
/skills-manager switch research    # Only research tools active
/skills-manager switch coding      # Only coding tools active
/skills-manager switch All         # Everything on
```

### What makes it different?

| Feature | skills-manager | Desktop apps | Other skills |
|---------|---------------|--------------|--------------|
| **Runs inside Claude Code** | ✅ Native skill | ❌ Separate app | ✅ |
| **No installation needed** | ✅ Just clone | ❌ Need to install | ✅ |
| **Natural language** | ✅ Chinese + English | ❌ GUI only | ⚠️ English only |
| **Auto MCP migration** | ✅ Fixes global leaks | ❌ Manual | ❌ |
| **Skill-MCP binding** | ✅ Auto-associate | ❌ Manual | ❌ |
| **Safe backup** | ✅ Always backup | ⚠️ Varies | ❌ |
| **Lightweight** | ✅ Pure CLI | ❌ Heavy | ✅ |

---

## Installation

### Method 1: Clone from GitHub

```bash
git clone https://github.com/Xue-Sir/skills-manager.git ~/.claude/skills/skills-manager
```

### Method 2: Manual Download

1. Download the repository as ZIP
2. Extract to `~/.claude/skills/skills-manager/`

---

## Requirements

- **Python 3.6+** (uses only standard library, no extra packages)
- **Claude Code** installed
- **Windows 10/11, Linux, macOS** — all supported

The `scan.py` script uses only Python standard library modules (json, os, sys, shutil, pathlib, subprocess). No `pip install` needed.

---

## Quick Start

### 1. First Use

After installation, start Claude Code and run:
```
/skills-manager scan
```

This scans your existing tools, registers them, and migrates any global MCPs (with automatic backup).

### 2. Try It

```
/skills-manager list              # See all categories
/skills-manager switch All        # Enable everything
/skills-manager switch None       # Disable everything
```

### 3. Create Your Own Category

```
/skills-manager add-category research
/skills-manager 把 skill-a 加入 research
/skills-manager 把 mcp-x 加入 research
/skills-manager switch research
```

Or in English:
```
/skills-manager add-category research
/skills-manager add skill-a to research
/skills-manager add mcp-x to research
/skills-manager switch research
```

---

## Key Features

- **Category-based management** — Group tools by project type, workflow, or any criteria
- **One-command switch** — Change your entire tool set instantly
- **Auto scan & sync** — Detects new tools automatically
- **MCP migration** — Moves global MCPs to per-project control (with backup)
- **Skill-MCP binding** — Associate skills with their required MCPs/plugins
- **Natural language** — Use Chinese or English, whatever feels natural
- **Safe by design** — Always backs up before modifying, never overwrites

---

## Commands

| Command | Description |
|---------|-------------|
| `/skills-manager scan` | Scan and sync all tools |
| `/skills-manager list` | List all categories |
| `/skills-manager switch <category>` | Switch to a category |
| `/skills-manager add-category <name>` | Create new category |
| `/skills-manager delete-category <name>` | Delete category |
| `/skills-manager 把 <item> 加入 <category>` | Add item to category |
| `/skills-manager manage <type> on/off` | Toggle tool type |
| `/skills-manager backup list` | List backups |

---

## Natural Language

You can use natural language (Chinese or English):

| Say this | Do this |
|----------|---------|
| "切换到research模式" / "switch to research" | Switch category |
| "把skill-a加入research" / "add skill-a to research" | Add to category |
| "列出所有分类" / "list categories" | Show categories |
| "分析这个项目" / "analyze this project" | Get recommendation |

---

## Important Notes

### MCP Migration

When you run `scan`, any MCPs in your global `~/.claude.json` are moved to skills-manager. This prevents "global leaks" where an MCP is available to ALL projects regardless of category.

A backup is always created before modifying `~/.claude.json`.

### Files Read

| File | Purpose |
|------|---------|
| `~/.claude/skills/` | Installed skills |
| `~/.claude/plugins/installed_plugins.json` | Installed plugins |
| `~/.claude.json` → `mcpServers` | Global MCP configs |

### Configuration

Config files are in `config/` directory. They're managed by AI based on your environment, but you can edit them manually too.

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

---

# skills-manager

> 别再手动切换每个项目的 skills 和 MCPs 了。让 skills-manager 把它们组织成分类，一键切换。

一个 [Claude Code](https://claude.ai/code) 的 skill，用于管理 skills、MCPs 和 plugins 的分类。定义一次，随处切换。

**⚠️ 仅适用于 Claude Code 用户。** 此 skill 依赖 Claude Code 的目录结构（`~/.claude/skills/`、`skillOverrides`、`enabledPlugins` 等），不支持其他 AI 编程工具。

> 已在 Claude Code CLI 上测试。理论上适用于桌面端/Web/IDE版本（共享相同目录结构），但尚未验证。

---

## 为什么用 skills-manager？

**问题：** 你有多个 skills、MCPs、plugins。不同项目需要不同工具。手动管理很麻烦。

**解决：** 把工具组织成分类（模式）。切换到一个分类，只有那些工具在当前项目中激活。

```
/skills-manager switch research    # 只有研究工具
/skills-manager switch coding      # 只有编程工具
/skills-manager switch All         # 全部开启
```

### 有什么不同？

| 特性 | skills-manager | 桌面应用 | 其他 skills |
|------|---------------|----------|-------------|
| **在 Claude Code 中运行** | ✅ 原生 skill | ❌ 需要单独应用 | ✅ |
| **无需安装** | ✅ 只需克隆 | ❌ 需要安装 | ✅ |
| **自然语言** | ✅ 中英文 | ❌ 只有 GUI | ⚠️ 仅英文 |
| **自动 MCP 迁移** | ✅ 解决全局泄漏 | ❌ 手动 | ❌ |
| **Skill-MCP 绑定** | ✅ 自动关联 | ❌ 手动 | ❌ |
| **安全备份** | ✅ 总是备份 | ⚠️ 不一定 | ❌ |
| **轻量级** | ✅ 纯 CLI | ❌ 笨重 | ✅ |

---

## 安装

### 方法一：从 GitHub 克隆

```bash
git clone https://github.com/Xue-Sir/skills-manager.git ~/.claude/skills/skills-manager
```

### 方法二：手动下载

1. 下载仓库 ZIP 文件
2. 解压到 `~/.claude/skills/skills-manager/`

---

## 环境要求

- **Python 3.6+**（仅使用标准库，无需额外安装包）
- **Claude Code** 已安装
- **Windows 10/11、Linux、macOS** — 全部支持

`scan.py` 脚本仅使用 Python 标准库模块（json、os、sys、shutil、pathlib、subprocess）。无需 `pip install`。

---

## 快速开始

### 1. 首次使用

安装后，启动 Claude Code 并运行：
```
/skills-manager scan
```

这会扫描你现有的工具，注册它们，并迁移全局 MCPs（自动备份）。

### 2. 试试看

```
/skills-manager list              # 查看所有分类
/skills-manager switch All        # 开启所有工具
/skills-manager switch None       # 关闭所有工具
```

### 3. 创建自己的分类

```
/skills-manager add-category research
/skills-manager 把 skill-a 加入 research
/skills-manager 把 mcp-x 加入 research
/skills-manager switch research
```

---

## 核心功能

- **分类管理** — 按项目类型、工作流或任何标准分组工具
- **一键切换** — 立即切换整套工具
- **自动扫描同步** — 自动检测新工具
- **MCP 迁移** — 将全局 MCPs 移到项目级控制（自动备份）
- **Skill-MCP 绑定** — 自动关联 skill和对应的 MCP/plugin
- **自然语言** — 中英文都行，怎么顺口怎么说
- **安全设计** — 修改前总是备份，从不覆盖

---

## 命令

| 命令 | 说明 |
|------|------|
| `/skills-manager scan` | 扫描并同步所有工具 |
| `/skills-manager list` | 列出所有分类 |
| `/skills-manager switch <分类>` | 切换到指定分类 |
| `/skills-manager add-category <名称>` | 创建新分类 |
| `/skills-manager delete-category <名称>` | 删除分类 |
| `/skills-manager 把 <项目> 加入 <分类>` | 将项目加入分类 |
| `/skills-manager manage <类型> on/off` | 切换工具类型 |
| `/skills-manager backup list` | 列出备份 |

---

## 自然语言

你可以用自然语言（中文或英文）：

| 这样说 | 这样做 |
|--------|--------|
| "切换到research模式" / "switch to research" | 切换分类 |
| "把skill-a加入research" / "add skill-a to research" | 加入分类 |
| "列出所有分类" / "list categories" | 显示分类 |
| "分析这个项目" / "analyze this project" | 获取推荐 |

---

## 重要说明

### MCP 迁移

运行 `scan` 时，全局 `~/.claude.json` 中的 MCPs 会被移到 skills-manager。这防止了"全局泄漏"——MCP 对所有项目可用，不管分类是什么。

修改 `~/.claude.json` 前总是会创建备份。

### 读取的文件

| 文件 | 用途 |
|------|------|
| `~/.claude/skills/` | 已安装的 skills |
| `~/.claude/plugins/installed_plugins.json` | 已安装的 plugins |
| `~/.claude.json` → `mcpServers` | 全局 MCP 配置 |

### 配置

配置文件在 `config/` 目录下。由 AI 根据你的环境管理，你也可以手动编辑。

---

## 许可证

MIT 许可证 - 见 [LICENSE](LICENSE) 文件。
