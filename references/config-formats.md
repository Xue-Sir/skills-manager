# Config File Formats / 配置文件格式

All config files are in `config/` directory, relative to this skill's root.

---

## settings.json — SSM 自身设置

Controls which types SSM manages. When a type is `false`, SSM ignores it completely.

```json
{
  "manage_skills": true,
  "manage_mcps": true,
  "manage_plugins": true,
  "backup_retention_days": 30
}
```

**Fields:**
- `manage_skills`: Whether SSM manages skills. `false` = ignore all skill operations.
- `manage_mcps`: Whether SSM manages MCPs. `false` = ignore all MCP operations.
- `manage_plugins`: Whether SSM manages plugins. `false` = ignore all plugin operations.
- `backup_retention_days`: Days to keep backups in `backups/` directory.

---

## categories.json — 分类定义

Each category specifies which skills, MCPs, and plugins are enabled.

```json
{
  "categories": {
    "All": {
      "description": "所有都开启 / All enabled",
      "skills": ["skill-a", "skill-b"],
      "mcps": ["mcp-x", "mcp-y"],
      "plugins": ["plugin-p", "plugin-q"]
    },
    "None": {
      "description": "所有都关闭 / All disabled",
      "skills": [],
      "mcps": [],
      "plugins": []
    }
  },
  "default_category": "None"
}
```

**Rules:**
- `All` and `None` are protected categories, cannot be deleted.
- `All` category's lists must stay in sync with registries.
- `None` category's lists are always empty.
- Custom categories only list the items they need.

---

## skills-registry.json — Skill 注册表

Tracks all managed skills. Install/update commands are user-provided.

```json
{
  "skills": {
    "skill-a": {
      "install_command": null,
      "update_command": null
    },
    "skill-b": {
      "install_command": "git clone <url> ~/.claude/skills/skill-b",
      "update_command": "cd ~/.claude/skills/skill-b && git pull"
    }
  }
}
```

**Sync with All:** When adding/removing from registry, update `All` category's skills list.

---

## mcp-config.json — MCP 配置

Stores all managed MCP configurations in standard `.mcp.json` format.

```json
{
  "mcpServers": {
    "mcp-x": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "env": {}
    },
    "mcp-y": {
      "command": "npx",
      "args": ["-y", "some-mcp-server"],
      "env": {}
    }
  }
}
```

**Sync with All:** When adding/removing from config, update `All` category's mcps list.

---

## plugins-registry.json — Plugin 注册表

Tracks all managed plugins.

```json
{
  "plugins": {
    "plugin-name@marketplace": {},
    "another-plugin@marketplace": {}
  }
}
```

**Sync with All:** When adding/removing from registry, update `All` category's plugins list.

**Source:** Installed plugins are read from `~/.claude/plugins/installed_plugins.json`. Only entries with `"scope": "user"` are considered user-level plugins.

---

## Project-level files (modified by SSM)

### `.claude/settings.local.json`

SSM modifies ONLY these fields, preserves everything else.

```json
{
  "skillOverrides": {
    "skill-a": "on",
    "skill-b": "off"
  },
  "enabledPlugins": {
    "plugin-name@marketplace": true,
    "another-plugin@marketplace": false
  }
}
```

- `skillOverrides`: `"on"` = enabled, `"off"` = disabled
- `enabledPlugins`: `true` = enabled, `false` = disabled

### `.mcp.json` (project root)

SSM adds MCPs from mcp-config.json. Does NOT delete existing entries.

```json
{
  "mcpServers": {
    "mcp-x": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "env": {}
    }
  }
}
```

---

## Backups

Location: `backups/` (at skill root, not in config/)

Naming: `claude.json.backup.YYYY-MM-DDTHH-MM-SS`

Created only when modifying `~/.claude.json` (MCP removal operations).
