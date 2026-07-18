# skills-manager

[English](#installation) | [中文](#安装)

Claude Code skill for managing skills, MCPs, and plugins by categories. Switch modes to configure project tools per project.

---

## Installation

### Method 1: Clone from GitHub

```bash
git clone https://github.com/YOUR_USERNAME/skills-manager.git ~/.claude/skills/skills-manager
```

### Method 2: Manual Download

1. Download the repository as ZIP
2. Extract to `~/.claude/skills/skills-manager/`

---

## Quick Start

### 1. First Use

After installation, start Claude Code and run:
```
/skills-manager scan
```

This will:
- Scan your existing skills, MCPs, and plugins
- Register them in skills-manager
- Migrate any MCPs from global `~/.claude.json` to skills-manager (with backup)

### 2. Basic Commands

| Command | Description |
|---------|-------------|
| `/skills-manager scan` | Scan and sync all tools |
| `/skills-manager list` | List all categories |
| `/skills-manager switch All` | Enable all tools |
| `/skills-manager switch None` | Disable all tools |

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

## Important Notes

### ⚠️ MCP Migration

When you run `scan`, skills-manager will:
1. Detect any MCPs in your global `~/.claude.json`
2. Move them to skills-manager's config
3. Clear the global `mcpServers` to `{}`

**Why?** Any MCP in `~/.claude.json` is a "global leak" — it's available to EVERY project, bypassing skills-manager's per-project control.

**Backup:** Before modifying `~/.claude.json`, a backup is created in `backups/` directory.

### 📁 Files Read by skills-manager

| File | Purpose |
|------|---------|
| `~/.claude/skills/` | List of installed skills |
| `~/.claude/plugins/installed_plugins.json` | List of installed plugins |
| `~/.claude.json` → `mcpServers` | Global MCP configurations |
| `<project>/.claude/settings.local.json` | Project-level skill/plugin switches |
| `<project>/.mcp.json` | Project-level MCP configurations |

### 🔧 Configuration Files

All config files are in `config/` directory:
- `settings.json` — skills-manager settings
- `categories.json` — category definitions
- `skills-registry.json` — skill registry
- `mcp-config.json` — MCP configurations
- `plugins-registry.json` — plugin registry
- `bindings.json` — skill→MCP/plugin bindings

**Note:** Config files are managed by AI based on your environment. You can also edit them manually.

---

## Detailed Usage

### Category Management

| Command | Description |
|---------|-------------|
| `/skills-manager add-category <name>` | Create a new category |
| `/skills-manager delete-category <name>` | Delete a category |
| `/skills-manager edit-category <name>` | Edit category contents |
| `/skills-manager 把 <item> 加入 <category>` | Add item to category |
| `/skills-manager 把 <item> 从 <category> 去掉` | Remove item from category |

### Tool Type Toggle

Each tool type can be toggled independently:
```
/skills-manager manage skills off    # Disable skill management
/skills-manager manage mcp on        # Enable MCP management
/skills-manager manage plugins off   # Disable plugin management
```

When disabled, skills-manager ignores that type completely.

### Backup Management

```
/skills-manager backup list          # List backups
/skills-manager backup clean         # Clean old backups
/skills-manager 设置备份保留天数为 60  # Set retention days
```

### Natural Language Support

You can use natural language (Chinese or English):
- "切换到research模式" / "switch to research mode"
- "把skill-a加入research" / "add skill-a to research"
- "列出所有分类" / "list all categories"
- "分析这个项目应该用什么分类" / "analyze this project and recommend category"

---

## How It Works

### Architecture

```
~/.claude/skills/skills-manager/
├── SKILL.md                ← Skill entry point
├── README.md               ← This file
├── scripts/
│   └── scan.py             ← Scan and sync script
├── config/                 ← Configuration files
│   ├── settings.json
│   ├── categories.json
│   ├── skills-registry.json
│   ├── mcp-config.json
│   ├── plugins-registry.json
│   └── bindings.json
├── references/             ← Detailed documentation
│   ├── config-formats.md
│   ├── sync-check.md
│   └── operations.md
└── backups/                ← Automatic backups
```

### Workflow

1. **Scan**: Detect all installed skills, MCPs, plugins
2. **Sync**: Register new tools, update All category
3. **Migrate**: Move global MCPs to skills-manager (with backup)
4. **Switch**: Apply category to current project

### Safety

- Only modifies `skillOverrides` and `enabledPlugins` in settings.local.json
- Only modifies `mcpServers` in ~/.claude.json
- Always backs up before modifying ~/.claude.json
- Never overwrites existing files (read → modify → write)

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

## 安装

### 方法一：从 GitHub 克隆

```bash
git clone https://github.com/YOUR_USERNAME/skills-manager.git ~/.claude/skills/skills-manager
```

### 方法二：手动下载

1. 下载仓库 ZIP 文件
2. 解压到 `~/.claude/skills/skills-manager/`

---

## 快速开始

### 1. 首次使用

安装后，启动 Claude Code 并运行：
```
/skills-manager scan
```

这将：
- 扫描你现有的 skills、MCPs 和 plugins
- 将它们注册到 skills-manager
- 迁移全局 `~/.claude.json` 中的 MCPs 到 skills-manager（自动备份）

### 2. 基本命令

| 命令 | 说明 |
|------|------|
| `/skills-manager scan` | 扫描并同步所有工具 |
| `/skills-manager list` | 列出所有分类 |
| `/skills-manager switch All` | 开启所有工具 |
| `/skills-manager switch None` | 关闭所有工具 |

### 3. 创建自己的分类

```
/skills-manager add-category research
/skills-manager 把 skill-a 加入 research
/skills-manager 把 mcp-x 加入 research
/skills-manager switch research
```

---

## 重要说明

### ⚠️ MCP 迁移

运行 `scan` 时，skills-manager 会：
1. 检测全局 `~/.claude.json` 中的 MCPs
2. 将它们移到 skills-manager 的配置中
3. 清空全局 `mcpServers` 为 `{}`

**为什么？** 任何留在 `~/.claude.json` 中的 MCP 都是"全局泄漏"——它对所有项目可用，绕过了 skills-manager 的项目级控制。

**备份：** 修改 `~/.claude.json` 前，会自动备份到 `backups/` 目录。

### 📁 skills-manager 读取的文件

| 文件 | 用途 |
|------|------|
| `~/.claude/skills/` | 已安装的 skills 列表 |
| `~/.claude/plugins/installed_plugins.json` | 已安装的 plugins 列表 |
| `~/.claude.json` → `mcpServers` | 全局 MCP 配置 |
| `<项目>/.claude/settings.local.json` | 项目级 skill/plugin 开关 |
| `<项目>/.mcp.json` | 项目级 MCP 配置 |

### 🔧 配置文件

所有配置文件在 `config/` 目录下：
- `settings.json` — skills-manager 设置
- `categories.json` — 分类定义
- `skills-registry.json` — Skill 注册表
- `mcp-config.json` — MCP 配置
- `plugins-registry.json` — Plugin 注册表
- `bindings.json` — skill→MCP/plugin 绑定

**注意：** 配置文件由 AI 根据你的环境自动管理，你也可以手动编辑。

---

## 详细用法

### 分类管理

| 命令 | 说明 |
|------|------|
| `/skills-manager add-category <名称>` | 创建新分类 |
| `/skills-manager delete-category <名称>` | 删除分类 |
| `/skills-manager edit-category <名称>` | 编辑分类内容 |
| `/skills-manager 把 <项目> 加入 <分类>` | 将项目加入分类 |
| `/skills-manager 把 <项目> 从 <分类> 去掉` | 将项目从分类移除 |

### 工具类型开关

每种工具类型可独立开关：
```
/skills-manager manage skills off    # 关闭 skill 管理
/skills-manager manage mcp on        # 开启 MCP 管理
/skills-manager manage plugins off   # 关闭 plugin 管理
```

关闭后，skills-manager 完全忽略该类型。

### 备份管理

```
/skills-manager backup list          # 列出备份
/skills-manager backup clean         # 清理旧备份
/skills-manager 设置备份保留天数为 60  # 设置保留天数
```

### 自然语言支持

你可以使用自然语言（中文或英文）：
- "切换到research模式" / "switch to research mode"
- "把skill-a加入research" / "add skill-a to research"
- "列出所有分类" / "list all categories"
- "分析这个项目应该用什么分类" / "analyze this project and recommend category"

---

## 工作原理

### 架构

```
~/.claude/skills/skills-manager/
├── SKILL.md                ← Skill 入口
├── README.md               ← 本文件
├── scripts/
│   └── scan.py             ← 扫描和同步脚本
├── config/                 ← 配置文件
│   ├── settings.json
│   ├── categories.json
│   ├── skills-registry.json
│   ├── mcp-config.json
│   ├── plugins-registry.json
│   └── bindings.json
├── references/             ← 详细文档
│   ├── config-formats.md
│   ├── sync-check.md
│   └── operations.md
└── backups/                ← 自动备份
```

### 工作流程

1. **扫描**：检测所有已安装的 skills、MCPs、plugins
2. **同步**：注册新工具，更新 All 分类
3. **迁移**：将全局 MCPs 移到 skills-manager（自动备份）
4. **切换**：将分类应用到当前项目

### 安全性

- 只修改 settings.local.json 中的 `skillOverrides` 和 `enabledPlugins`
- 只修改 ~/.claude.json 中的 `mcpServers`
- 修改 ~/.claude.json 前总是备份
- 从不覆盖现有文件（读取→修改→写入）

---

## 许可证

MIT 许可证 - 见 [LICENSE](LICENSE) 文件。
