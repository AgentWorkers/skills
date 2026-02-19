---
name: opensoulmd
description: 使用 OpenSOUL.md 注册表中的 SOUL.md 个性文件来搜索、召唤并控制你的代理（agent）。
metadata:
  {
    "openclaw": { "requires": { "bins": ["soul"] }, "primaryEnv": null },
    "install":
      [
        {
          "id": "curl",
          "kind": "shell",
          "command": "curl -fsSL https://opensoul.md/install.sh | sh",
          "bins": ["soul"],
          "label": "Install via curl (recommended)",
        },
        {
          "id": "npm",
          "kind": "node",
          "package": "opensoul",
          "bins": ["soul"],
          "label": "Install via npm",
        },
      ],
  }
---
您可以通过使用 OpenSOUL.md 注册表中的 SOUL.md 文件来管理您的代理的“个性”（即代理的行为或表现方式）。

## 可用的操作

### 拥有（Possess）——更改个性

当用户请求更改个性时：
- 运行 `soul possess <名称> --yes` — 如果该个性文件未在本地缓存中，系统会自动从注册表中加载它。
- 您也可以通过本地文件路径来拥有该个性：`soul possess /path/to/SOUL.md --yes`
- 使用 `--dry-run` 可以预览操作结果，而不会实际执行任何操作。

### 驱逐（Exorcise）——恢复原始状态

如果用户希望恢复到原始的个性：`soul exorcise`  
此命令会恢复第一次使用该个性之前的备份 SOUL.md 文件。

### 搜索个性（Search Souls）

- 要搜索注册表中的个性：`soul search <查询条件> --no-interactive`
- 排序选项：
  - `--top`：按评分最高排序
  - `--popular`：按下载次数最多排序
- 要显示所有可用的个性：`soul search --top --no-interactive`

### 下载（Summon）——仅下载而不立即应用

- 要将某个个性文件下载到本地缓存中但不立即应用：`soul summon <名称>`
- 用户之后可以通过 `soul possess <名称>` 来激活该个性。

### 列出缓存中的个性（List Cached Souls）

- 要显示本地缓存的个性文件：`soul list`
- 支持分页：`--page <页码>` 和 `--per-page <每页显示数量>`

### 移除（Banish）——从缓存中删除

- 要从本地缓存中删除某个个性文件：`soul banish <名称>`

### 状态（Status）

- 要查看当前加载的个性文件：`soul status`
- 该命令会显示 SOUL.md 文件的路径、当前使用的个性状态（原始状态或被占用的状态）以及备份状态。

### 路径（Path）

- 要查看当前的 SOUL.md 文件路径：`soul path`
- 要设置新的 SOUL.md 文件路径：`soul path /path/to/SOUL.md`
- 要查看或设置 OpenClaw 技能目录的路径：`soul path --skills` 或 `soul path /path/to/skills --skills`

### 配置（Config）

- 要获取或设置 CLI 配置值：
  - `soul config get <键>`
  - `soul config set <键> <值>`

### 安装/卸载技能（Install/Uninstall Skills）

- 要将某个 OpenSoul 技能安装到 OpenClaw 中：`soul install`
- 要卸载该技能：`soul uninstall`

## 重要说明：
- 使用 `soul search` 时请务必加上 `--no-interactive` 选项，因为无法通过交互式用户界面进行操作。
- 使用 `soul possess` 时请务必加上 `--yes` 选项，以跳过确认提示。
- 如果某个个性文件未在本地缓存中，`soul possess` 会自动从注册表中加载它，无需手动再次加载。
- 拥有某个个性后，应告知用户可以使用 `soul exorcise` 来恢复到原始状态。
- 新设置的个性仅会在下一次对话中生效，当前对话不会受到影响。