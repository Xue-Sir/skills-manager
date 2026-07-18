# Operations / 操作详情

All config files are in `config/` directory. Project-level files are in the current working directory.

**Important:** Only operate on types where `manage_xxx` is `true` in `config/settings.json`.

---

## switch — 切换分类

**Usage:** `switch <category-name>`

### Phase 1: Sync Check
See `references/sync-check.md`.

### Phase 2: Apply Category

1. Read `config/categories.json` → get target category
2. Apply to project:

**Skills (if `manage_skills` is true) → `.claude/settings.local.json`:**
- Read existing file (create `{}` if missing)
- For each skill in skills-registry:
  - If in category's skills list → `skillOverrides[name] = "on"`
  - If not in list → `skillOverrides[name] = "off"`
- Only modify `skillOverrides`, preserve everything else

**Plugins (if `manage_plugins` is true) → `.claude/settings.local.json`:**
- For each plugin in plugins-registry:
  - If in category's plugins list → `enabledPlugins[name] = true`
  - If not in list → `enabledPlugins[name] = false`
- Only modify `enabledPlugins`, preserve everything else

**MCPs (if `manage_mcps` is true) → `.mcp.json` (project root):**
- Read existing file (create `{"mcpServers": {}}` if missing)
- For each MCP in category's mcps list:
  - If already exists in project with same config → skip
  - If already exists with different config → skip, note in report
  - If doesn't exist → add from mcp-config
- Do NOT delete MCPs in project but not in category

### Report
```
分类已切换到: research / Switched to: research
Skill: skill-a ✅ on, skill-b ❌ off
Plugin: plugin-p ✅ on, plugin-q ❌ off
MCP: mcp-x ✅ added, mcp-y ⏭️ already exists
```

---

## add-category — 添加分类

**Usage:** `add-category <name>`

1. Check `name` doesn't exist and isn't `All` or `None`
2. Create entry with empty lists
3. Optionally prompt user to add items
4. Write to categories.json

---

## delete-category — 删除分类

**Usage:** `delete-category <name>`

1. Reject if `name` is `All` or `None`
2. Confirm with user
3. Remove from categories.json

---

## edit-category — 编辑分类

**Usage:** `edit-category <name>` or natural language

Supports adding/removing skills, MCPs, plugins to/from a category.

**When adding:** Verify item exists in registry/config first.

---

## list — 列出分类

**Usage:** `list`

Display all categories with their contents, grouped by type.

---

## scan — 扫描校验

**Usage:** `scan`

Only scan types where `manage_xxx` is `true`.

1. Check each skill in skills-registry exists in `~/.claude/skills/`
2. Check each plugin in plugins-registry exists in `~/.claude/plugins/installed_plugins.json` (scope: user)
3. Verify `All` category lists match registries
4. Report issues with repair suggestions

---

## update — 更新

**Usage:** `update <target>`

- `update skills`: Execute `update_command` for each skill (skip if null)
- `update plugins`: Run `claude plugin update` for each plugin
- `update all`: Both
- `update <name>`: Update specific item

---

## delete-mcp — 删除 MCP

**Usage:** `delete-mcp <name> --allow-delete-mcp`

1. Reject if `--allow-delete-mcp` flag missing
2. Check MCP exists in mcp-config
3. Confirm with user
4. Remove from mcp-config
5. Update `All` category
6. Write back

---

## manage — 管理类型开关

**Usage:** `manage skills on/off`, `manage mcp on/off`, `manage plugins on/off`

Toggle whether SSM manages a specific type. Updates `config/settings.json`.

---

## backup — 备份管理

**Usage:** `backup list` or `backup clean [days]`

- `backup list`: List all files in `backups/`
- `backup clean`: Delete files older than `backup_retention_days`
- `backup clean <days>`: Delete files older than specified days

---

## set-backup-retention — 设置备份保留天数

**Usage:** `设置备份保留天数为 <days>` or `set backup retention <days>`

Update `backup_retention_days` in `config/settings.json`.

---

## 首次使用 / First Use

If config files don't exist or registries are empty:

1. Create all config files with defaults
2. If `manage_skills` is true: scan `~/.claude/skills/` → populate skills-registry → update `All` category
3. If `manage_plugins` is true: read `~/.claude/plugins/installed_plugins.json`, filter `scope: "user"` → populate plugins-registry → update `All` category
4. If `manage_mcps` is true: read `~/.claude.json` → ask user if MCPs should be migrated
5. Report initialization results
