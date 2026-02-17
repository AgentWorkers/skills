---
name: soul-pack
description: 导出和导入 OpenClaw 代理的 SOUL 包。这些操作适用于创建可重用的角色包（包括 SOUL.md、preview.md 和 manifest.json 文件），将 SOUL 包安装到新的或现有的代理工作空间中，或者批量列出本地 SOUL 包以供 Soul 市场平台使用。
---
# Soul Pack

使用捆绑的脚本来实现确定性的行为。

## 导出 Soul 包

```bash
bash /Users/feifei/projects/soul-pack-skill/scripts/export-soul.sh \
  --workspace /Users/feifei/.openclaw/workspace \
  --out /Users/feifei/projects/soul-packages \
  --name edith-soul
```

## 导入 Soul 包并创建代理

```bash
bash /Users/feifei/projects/soul-pack-skill/scripts/import-soul.sh \
  --package /Users/feifei/projects/soul-packages/edith-soul.tar.gz \
  --agent my-soul \
  --workspace /Users/feifei/projects/agents/my-soul
```

## 列出本地的 Soul 包

```bash
bash /Users/feifei/projects/soul-pack-skill/scripts/list-souls.sh \
  --dir /Users/feifei/projects/soul-packages
```

## 注意：
- `manifest.json` 会根据 `schema/manifest.schema.v0.1.json` 进行验证。
- 除非提供了 `--force` 选项，否则导入操作不会覆盖现有的 SOUL.md 文件。
- 代理的注册使用 `openclaw agents add` 命令（或重用现有的代理 ID）。