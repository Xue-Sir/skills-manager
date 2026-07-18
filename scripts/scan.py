#!/usr/bin/env python3
"""
skills-manager scan script
Usage: python scan.py <command>
Commands:
  scan     - Compare global state with SSM config, report differences
  migrate  - Move MCPs from global ~/.claude.json to SSM config
  sync     - Update registries and All category based on global state
  check    - Quick check if registries match global state (no changes)
"""

import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Paths
HOME = Path.home()
SSM_ROOT = HOME / ".claude" / "skills" / "skills-manager"
CONFIG_DIR = SSM_ROOT / "config"
BACKUP_DIR = SSM_ROOT / "backups"
SKILLS_DIR = HOME / ".claude" / "skills"
PLUGINS_FILE = HOME / ".claude" / "plugins" / "installed_plugins.json"
GLOBAL_CLAUDE_JSON = HOME / ".claude.json"

def load_json(path):
    """Load JSON file, return None if not exists."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(path, data):
    """Save JSON file with consistent formatting."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_global_skills():
    """Get list of skills from ~/.claude/skills/ (excluding skills-manager)."""
    skills = []
    if SKILLS_DIR.exists():
        for d in SKILLS_DIR.iterdir():
            if d.is_dir() and d.name != "skills-manager":
                skills.append(d.name)
    return sorted(skills)

def get_global_plugins():
    """Get list of all installed plugins from installed_plugins.json.

    installed_plugins.json is the authoritative installation registry
    maintained by Claude Code. We include all scopes (user/local/remote),
    not just "user" — the original bug was filtering only scope=="user"
    when most plugins are installed with scope=="local".

    We do NOT scan cache .in_use markers — those are deployment artifacts
    that do not represent user-initiated installations. A plugin that
    only exists in cache with .in_use but is not in installed_plugins.json
    is an uninstall residual or auto-deployed dependency, not an
    intentionally installed plugin.

    Returns deduplicated sorted list of "name@marketplace" strings.
    """
    plugins = set()
    data = load_json(PLUGINS_FILE)
    if data and "plugins" in data:
        for name in data["plugins"]:
            plugins.add(name)
    return sorted(plugins)

def get_global_mcps():
    """Get MCPs from ~/.claude.json."""
    data = load_json(GLOBAL_CLAUDE_JSON)
    if data and "mcpServers" in data:
        return data["mcpServers"]
    return {}

def backup_claude_json():
    """Backup ~/.claude.json to backups/ directory."""
    if not GLOBAL_CLAUDE_JSON.exists():
        return None
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    backup_path = BACKUP_DIR / f"claude.json.backup.{timestamp}"
    shutil.copy2(GLOBAL_CLAUDE_JSON, backup_path)
    return backup_path

def clean_old_backups(retention_days=30):
    """Delete backups older than retention_days."""
    if not BACKUP_DIR.exists():
        return 0
    cutoff = datetime.now().timestamp() - (retention_days * 86400)
    count = 0
    for f in BACKUP_DIR.glob("claude.json.backup.*"):
        if f.stat().st_mtime < cutoff:
            f.unlink()
            count += 1
    return count

def cmd_check():
    """Quick check: compare global state with SSM config, report only."""
    settings = load_json(CONFIG_DIR / "settings.json") or {}
    skills_reg = load_json(CONFIG_DIR / "skills-registry.json") or {"skills": {}}
    plugins_reg = load_json(CONFIG_DIR / "plugins-registry.json") or {"plugins": {}}
    mcp_config = load_json(CONFIG_DIR / "mcp-config.json") or {"mcpServers": {}}
    categories = load_json(CONFIG_DIR / "categories.json") or {"categories": {}}

    report = {"skills": [], "plugins": [], "mcps": [], "all_sync": []}

    # Check skills
    if settings.get("manage_skills", True):
        global_skills = get_global_skills()
        reg_skills = list(skills_reg.get("skills", {}).keys())
        for s in global_skills:
            if s not in reg_skills:
                report["skills"].append(f"NEW: {s} (on disk, not in registry)")
        for s in reg_skills:
            if s not in global_skills:
                report["skills"].append(f"MISSING: {s} (in registry, not on disk)")

    # Check plugins
    if settings.get("manage_plugins", True):
        global_plugins = get_global_plugins()
        reg_plugins = list(plugins_reg.get("plugins", {}).keys())
        for p in global_plugins:
            if p not in reg_plugins:
                report["plugins"].append(f"NEW: {p} (installed, not in registry)")
        for p in reg_plugins:
            if p not in global_plugins:
                report["plugins"].append(f"MISSING: {p} (in registry, not installed)")

    # Check MCPs
    if settings.get("manage_mcps", True):
        global_mcps = get_global_mcps()
        config_mcps = mcp_config.get("mcpServers", {})
        for name, config in global_mcps.items():
            if name not in config_mcps:
                report["mcps"].append(f"LEAK: {name} (in global ~/.claude.json but not managed by skills-manager — leaks to ALL projects)")
            elif config_mcps[name] != config:
                report["mcps"].append(f"DRIFT: {name} (config differs between global and SSM — run migrate to sync)")
            else:
                report["mcps"].append(f"LEAK: {name} (in both global and SSM — run migrate to remove from global)")

    # Check All category sync
    all_cat = categories.get("categories", {}).get("All", {})
    if all_cat:
        reg_skills = set(skills_reg.get("skills", {}).keys())
        all_skills = set(all_cat.get("skills", []))
        if reg_skills != all_skills:
            report["all_sync"].append(f"Skills mismatch: registry={sorted(reg_skills)}, All={sorted(all_skills)}")

        reg_plugins = set(plugins_reg.get("plugins", {}).keys())
        all_plugins = set(all_cat.get("plugins", []))
        if reg_plugins != all_plugins:
            report["all_sync"].append(f"Plugins mismatch: registry={sorted(reg_plugins)}, All={sorted(all_plugins)}")

        reg_mcps = set(mcp_config.get("mcpServers", {}).keys())
        all_mcps = set(all_cat.get("mcps", []))
        if reg_mcps != all_mcps:
            report["all_sync"].append(f"MCPs mismatch: registry={sorted(reg_mcps)}, All={sorted(all_mcps)}")

    return report

def cmd_sync():
    """Update registries and All category based on global state."""
    settings = load_json(CONFIG_DIR / "settings.json") or {}
    skills_reg = load_json(CONFIG_DIR / "skills-registry.json") or {"skills": {}}
    plugins_reg = load_json(CONFIG_DIR / "plugins-registry.json") or {"plugins": {}}
    mcp_config = load_json(CONFIG_DIR / "mcp-config.json") or {"mcpServers": {}}
    categories = load_json(CONFIG_DIR / "categories.json") or {"categories": {}}

    changes = {"skills_added": [], "plugins_added": [], "all_updated": False}

    # Sync skills
    if settings.get("manage_skills", True):
        global_skills = get_global_skills()
        for s in global_skills:
            if s not in skills_reg["skills"]:
                skills_reg["skills"][s] = {"install_command": None, "update_command": None}
                changes["skills_added"].append(s)
        save_json(CONFIG_DIR / "skills-registry.json", skills_reg)

    # Sync plugins
    if settings.get("manage_plugins", True):
        global_plugins = get_global_plugins()
        for p in global_plugins:
            if p not in plugins_reg["plugins"]:
                plugins_reg["plugins"][p] = {}
                changes["plugins_added"].append(p)
        save_json(CONFIG_DIR / "plugins-registry.json", plugins_reg)

    # Update All category
    all_cat = categories.get("categories", {}).get("All", {})
    if all_cat:
        all_cat["skills"] = sorted(skills_reg.get("skills", {}).keys())
        all_cat["plugins"] = sorted(plugins_reg.get("plugins", {}).keys())
        all_cat["mcps"] = sorted(mcp_config.get("mcpServers", {}).keys())
        categories["categories"]["All"] = all_cat
        save_json(CONFIG_DIR / "categories.json", categories)
        changes["all_updated"] = True

    # Clean old backups
    retention = settings.get("backup_retention_days", 30)
    cleaned = clean_old_backups(retention)

    return changes

def cmd_migrate():
    """Move MCPs from global ~/.claude.json to SSM config."""
    global_mcps = get_global_mcps()
    if not global_mcps:
        return {"status": "no_mcps", "message": "No MCPs found in ~/.claude.json"}

    mcp_config = load_json(CONFIG_DIR / "mcp-config.json") or {"mcpServers": {}}
    categories = load_json(CONFIG_DIR / "categories.json") or {"categories": {}}

    # Backup first
    backup_path = backup_claude_json()

    # Move MCPs to SSM config
    mcp_config["mcpServers"].update(global_mcps)
    save_json(CONFIG_DIR / "mcp-config.json", mcp_config)

    # Update All category
    all_cat = categories.get("categories", {}).get("All", {})
    if all_cat:
        all_cat["mcps"] = sorted(mcp_config["mcpServers"].keys())
        categories["categories"]["All"] = all_cat
        save_json(CONFIG_DIR / "categories.json", categories)

    # Clear global MCPs (keep the key, set to {})
    data = load_json(GLOBAL_CLAUDE_JSON) or {}
    data["mcpServers"] = {}
    save_json(GLOBAL_CLAUDE_JSON, data)

    return {
        "status": "migrated",
        "mcp_count": len(global_mcps),
        "mcp_names": sorted(global_mcps.keys()),
        "backup": str(backup_path) if backup_path else None
    }

def cmd_scan():
    """Full scan: check, sync, and auto-migrate MCPs from global config.

    Always performs three steps:
    1. check — detect all issues
    2. sync — register any new skills/plugins discovered on disk
    3. migrate — move any MCPs still in ~/.claude.json to SSM config
       (not just on first use — global MCPs leak to every project)

    Returns a dict with initial_check, sync, migrate (if performed),
    and final_check (if migrate was performed).
    """
    initial_check = cmd_check()
    sync_result = cmd_sync()

    # ALWAYS migrate stray MCPs from global config.
    # Any MCP left in ~/.claude.json's mcpServers leaks to every project,
    # bypassing skills-manager's per-project MCP control.
    settings = load_json(CONFIG_DIR / "settings.json") or {}
    global_mcps = get_global_mcps()
    migrate_result = None
    final_check = None
    if global_mcps and settings.get("manage_mcps", True):
        migrate_result = cmd_migrate()
        final_check = cmd_check()

    return {
        "type": "scan",
        "initial_check": initial_check,
        "sync": sync_result,
        "migrate": migrate_result,
        "final_check": final_check
    }

def cmd_set_skill_info(skill_name, install_command=None, update_command=None):
    """Set install/update commands for a skill in the registry."""
    skills_reg = load_json(CONFIG_DIR / "skills-registry.json") or {"skills": {}}

    if skill_name not in skills_reg["skills"]:
        return {"status": "error", "message": f"Skill '{skill_name}' not found in registry"}

    if install_command:
        skills_reg["skills"][skill_name]["install_command"] = install_command
    if update_command:
        skills_reg["skills"][skill_name]["update_command"] = update_command

    save_json(CONFIG_DIR / "skills-registry.json", skills_reg)

    return {
        "status": "updated",
        "skill": skill_name,
        "install_command": skills_reg["skills"][skill_name].get("install_command"),
        "update_command": skills_reg["skills"][skill_name].get("update_command")
    }

def cmd_update_marketplace(marketplace_name=None):
    """Update plugins from marketplace by pulling from git."""
    marketplaces = load_json(CONFIG_DIR / "marketplaces.json") or {"marketplaces": {}}
    results = []

    targets = {}
    if marketplace_name:
        if marketplace_name in marketplaces.get("marketplaces", {}):
            targets[marketplace_name] = marketplaces["marketplaces"][marketplace_name]
        else:
            return {"status": "error", "message": f"Marketplace '{marketplace_name}' not found"}
    else:
        targets = marketplaces.get("marketplaces", {})

    for name, config in targets.items():
        path = Path(config["path"].replace("~", str(HOME)))
        for plugin in config.get("plugins", []):
            plugin_path = path / plugin
            if plugin_path.exists() and (plugin_path / ".git").exists():
                # Git pull
                import subprocess
                try:
                    result = subprocess.run(
                        ["git", "pull"],
                        cwd=str(plugin_path),
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    git_status = "updated" if "Already up to date" not in result.stdout else "up-to-date"
                except Exception as e:
                    git_status = f"error: {e}"

                results.append({
                    "marketplace": name,
                    "plugin": plugin,
                    "git": git_status
                })

    return {"status": "done", "updates": results}

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "check":
        result = cmd_check()
    elif command == "sync":
        result = cmd_sync()
    elif command == "migrate":
        result = cmd_migrate()
    elif command == "scan":
        result = cmd_scan()
    elif command == "set-skill-info":
        if len(sys.argv) < 3:
            print("Usage: scan.py set-skill-info <skill_name> [--install <cmd>] [--update <cmd>]")
            sys.exit(1)
        skill_name = sys.argv[2]
        install_cmd = None
        update_cmd = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--install" and i + 1 < len(sys.argv):
                install_cmd = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--update" and i + 1 < len(sys.argv):
                update_cmd = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        result = cmd_set_skill_info(skill_name, install_cmd, update_cmd)
    elif command == "update-marketplace":
        marketplace_name = sys.argv[2] if len(sys.argv) > 2 else None
        result = cmd_update_marketplace(marketplace_name)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
