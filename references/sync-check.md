# Sync Check Logic / 同步检查逻辑

Phase 1 of the `switch` operation. Compares current global state with SSM config, resolves differences.

**Important:** Only check types where `manage_xxx` is `true` in `config/settings.json`. Skip disabled types entirely.

---

## Step 1: Scan Global State

### Skills (only if `manage_skills` is true)
- Scan `~/.claude/skills/` directory
- List all subdirectories (each is a skill)
- Exclude `skills-manager` itself

### Plugins (only if `manage_plugins` is true)
- Read `~/.claude/plugins/installed_plugins.json`
- Filter entries where `"scope": "user"` (user-level installed plugins)
- Extract plugin names from the `plugins` object keys

### MCPs (only if `manage_mcps` is true)
- Read `~/.claude.json` → `mcpServers`
- Get list of all MCP names and their configs

---

## Step 2: Compare with SSM Config

### Skills Comparison

| Situation | Detection | Action |
|-----------|-----------|--------|
| Global has, registry doesn't | `skill ∈ global AND skill ∉ skills-registry` | **Auto-add** to skills-registry with null commands. Update `All` category. Note at end. |
| Registry has, global doesn't | `skill ∈ skills-registry AND skill ∉ global` | **Prompt user**: remove from registry or ignore? |

### Plugins Comparison

| Situation | Detection | Action |
|-----------|-----------|--------|
| Global has, registry doesn't | `plugin ∈ global AND plugin ∉ plugins-registry` | **Auto-add** to plugins-registry. Update `All` category. Note at end. |
| Registry has, global doesn't | `plugin ∈ plugins-registry AND plugin ∉ global` | **Prompt user**: remove from registry or ignore? |

### MCPs Comparison

| Situation | Detection | Action |
|-----------|-----------|--------|
| Global has new, config doesn't | `mcp ∈ global AND mcp ∉ mcp-config` | **Auto-move**: copy to mcp-config, remove from global (backup first). Update `All` category. Note at end. |
| Global has duplicate (identical) | `mcp ∈ both AND configs identical` | **Auto-remove** from global (backup first). Note at end. |
| Global has same name, different config | `mcp ∈ both AND configs differ` | **Prompt user**: which version to keep? |

---

## Step 3: Handle Prompts and Notes

### Prompts (require user decision)
- Missing skills/plugins → remove from registry or ignore?
- Conflicting MCP configs → which version to keep?

**Flow:**
1. Collect ALL prompts
2. Present to user in one batch
3. Wait for user decisions
4. Execute decisions
5. Proceed to Phase 2

### Notes (auto-processed, report after Phase 2)
- New skills/plugins added to registry
- MCPs moved from global to config
- Duplicate MCPs removed
- `All` category updated

---

## Step 4: Backup (if needed)

Before any `~/.claude.json` modification:
1. Read current `~/.claude.json`
2. Write to `backups/claude.json.backup.<timestamp>` (at skill root)
3. Clean up backups older than `backup_retention_days`
4. Then modify `~/.claude.json`

---

## Report Format

### Prompts (before Phase 2)
```
⚠️ 需要确认 / Confirmation needed:
- Skill `old-skill` 在配置中但全局不存在。从配置中移除？[移除/忽略]
- MCP `conflict-mcp` 在全局和配置中内容不同。使用哪个版本？[全局/配置]
```

### Notes (after Phase 2)
```
📝 自动处理说明 / Auto-processed:
- Skill `new-skill` 已自动纳入管理
- Plugin `new-plugin` 已自动纳入管理
- MCP `mcp-x` 已从全局移入配置（已备份）
```
