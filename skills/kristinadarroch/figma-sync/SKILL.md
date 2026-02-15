---
name: figma-sync
description: |
  Read Figma files, extract design tokens, generate React Native Expo TS or Web React + Tailwind code,
  write back to Figma, and diff local models against Figma for minimal patches.
  Triggers: "pull figma", "sync figma", "figma to code", "push to figma", "diff figma",
  "extract design tokens", "generate from figma", "preview figma changes"
---

# figma-sync

一种支持 Figma 与代码双向同步的工具。

## 设置

```bash
export FIGMA_TOKEN="your-personal-access-token"
```

请在 [https://www.figma.com/developers/api#access-tokens](https://www.figma.com/developers/api#access-tokens) 获取访问令牌。

## 命令

### Pull（读取数据并生成代码）

```bash
python3 scripts/figma_pull.py --file-key <KEY> --platform rn-expo --output-dir ./out
python3 scripts/figma_pull.py --file-key <KEY> --node-ids 1:2,3:4 --platform web-react --output-dir ./out
```

输出：`designModel.json`、`tokens.json`、`codePlan.json` 以及生成的组件文件。

### Push（将更改写入 Figma）

```bash
python3 scripts/figma_push.py --file-key <KEY> --patch-spec patch.json
python3 scripts/figma_push.py --file-key <KEY> --patch-spec patch.json --execute  # actually apply
```

默认情况下会进行模拟执行（dry-run）；若需实际应用更改，请使用 `--execute` 参数。

### Diff（比较差异）

```bash
python3 scripts/figma_diff.py --file-key <KEY> --local-model designModel.json
```

输出差异内容及用于同步的补丁文件（patchSpec）。

### Preview（预览更改）

```bash
python3 scripts/figma_preview.py --file-key <KEY> --operations ops.json
```

在不进行任何操作的情况下，显示将会发生的更改。

## 支持的平台

- **rn-expo**：React Native + Expo + TypeScript（主要支持平台）
- **web-react**：React + Tailwind CSS（次要支持平台）

## 速率限制

该工具采用指数退避算法（exponential backoff）来控制请求频率，并利用 ETag 缓存机制；同时遵循 Figma 的速率限制（约 30 次请求/分钟）。缓存文件存储在 `.figma-cache/` 目录中。

## 参考资料

- [DesignSpec Schema](references/design-spec-schema.json)
- [API Guide](references/api-guide.md)