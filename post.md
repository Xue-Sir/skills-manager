# skills-manager: 一键切换你的 Claude Code 工具集

> 你是否也有这样的烦恼：装了一堆 skills、MCPs、plugins，不同项目需要不同的工具组合，每次都要手动开关？

## 问题

作为 Claude Code 用户，我装了很多工具：
- 研究用的 skills
- 编程用的 MCPs
- 各种 plugins

但问题是：
- 研究项目不需要编程工具
- 编程项目不需要研究工具
- 手动管理太麻烦

## 解决方案

我做了一个 Claude Code skill：**skills-manager**

它可以把工具组织成「分类」（categories），然后一键切换：

```
/skills-manager switch research    # 只有研究工具
/skills-manager switch coding      # 只有编程工具
/skills-manager switch All         # 全部开启
```

## 特色功能

### 1. 自然语言支持

不用记命令，直接说人话：

```
# 中文
"切换到research模式"
"把skill-a加入research"
"列出所有分类"

# 英文
"switch to research"
"add skill-a to research"
"list categories"
```

### 2. 自动 MCP 迁移

Claude Code 的 MCP 配置有个「全局泄漏」问题：任何在 `~/.claude.json` 中的 MCP 都会对所有项目生效。

skills-manager 会自动把这些 MCP 迁移到项目级控制：

```bash
/skills-manager scan
# 自动检测并迁移，还会备份
```

### 3. Skill-MCP 绑定

如果你的 skill 需要特定的 MCP，可以绑定：

```
/skills-manager bind codebase-memory --mcp codebase-memory-mcp
```

这样切换分类时，skill和 MCP 会一起切换。

### 4. 安全备份

修改 `~/.claude.json` 前总是会自动备份：

```
/skills-manager backup list    # 查看备份
```

## 与其他方案的对比

| 特性 | skills-manager | 桌面应用 | 其他 skills |
|------|---------------|----------|-------------|
| 在 Claude Code 中运行 | ✅ | ❌ | ✅ |
| 无需安装 | ✅ | ❌ | ✅ |
| 自然语言 | ✅ 中英文 | ❌ | ⚠️ 英文 |
| 自动 MCP 迁移 | ✅ | ❌ | ❌ |
| Skill-MCP 绑定 | ✅ | ❌ | ❌ |

## 如何使用

### 安装

```bash
git clone https://github.com/Xue-Sir/skills-manager.git ~/.claude/skills/skills-manager
```

### 首次使用

```
/skills-manager scan
```

### 创建分类

```
/skills-manager add-category research
/skills-manager add skill-a to research
/skills-manager add mcp-x to research
/skills-manager switch research
```

## 适合谁？

- Claude Code 用户
- 装了很多 skills/MCPs/plugins 的用户
- 需要在不同项目间切换工具的用户
- 喜欢用自然语言操作的用户

## 链接

- GitHub: https://github.com/Xue-Sir/skills-manager
- 有问题或建议？欢迎提 Issue！

---

*如果你觉得有用，欢迎 ⭐ Star 支持！*
