---
name: pscale-org
description: 列出、显示以及切换 PlanetScale 组织。此功能适用于管理多个组织、在多个账户之间切换、查看组织详情或排查组织访问权限问题。相关操作会触发 `org`, `organization`, `switch org`, `list orgs` 等相关事件。
---

# pscale org

用于列出、显示以及切换组织。

## 常用命令

```bash
# List all organizations
pscale org list

# Show current organization
pscale org show

# Switch organization
pscale org switch <org-name>
```

## 工作流程

### 在不同组织之间切换

```bash
# View current org
pscale org show

# List available orgs
pscale org list

# Switch to different org
pscale org switch my-other-org

# Verify switch
pscale database list --org my-other-org
```

## 故障排除

### 无法查看预期的数据库

**解决方案：** 检查当前所属的组织

```bash
pscale org show
pscale org switch <correct-org>
```

## 相关技能

- **pscale-auth** - 身份验证和账户管理
- **pscale-database** - 组织范围内的数据库操作

## 参考资料

请参阅 `references/commands.md` 以获取完整的命令参考信息。