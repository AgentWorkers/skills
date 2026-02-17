---
name: clawdhub
description: 使用 ClawdHub CLI 来搜索、安装、更新以及发布来自 clawdhub.com 的代理技能（agent skills）。当您需要即时获取新技能、将已安装的技能同步到最新版本或特定版本，或者使用 npm 安装的 ClawdHub CLI 来发布新的/更新的技能文件夹时，可以使用该工具。
metadata: {"clawdbot":{"requires":{"bins":["clawdhub"]},"install":[{"id":"node","kind":"node","package":"clawdhub","bins":["clawdhub"],"label":"Install ClawdHub CLI (npm)"}]}}
---

# ClawdHub CLI

**安装**  
```bash
npm i -g clawdhub
```

**身份验证（发布操作）**  
```bash
clawdhub login
clawdhub whoami
```

**搜索**  
```bash
clawdhub search "postgres backups"
```

**安装**  
```bash
clawdhub install my-skill
clawdhub install my-skill --version 1.2.3
```

**更新**  
（基于哈希值的匹配与升级）  
```bash
clawdhub update my-skill
clawdhub update my-skill --version 1.2.3
clawdhub update --all
clawdhub update my-skill --force
clawdhub update --all --no-input --force
```

**列表显示**  
```bash
clawdhub list
```

**发布**  
```bash
clawdhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

**注意事项**  
- 默认注册中心：https://clawdhub.com  
  （可通过 `CLAWDHUB_REGISTRY` 或 `--registry` 参数进行覆盖）  
- 默认工作目录：当前目录（`cwd`）；安装目录：`./skills`  
  （可通过 `--workdir` 或 `--dir` 参数进行覆盖）  
- `update` 命令会更新本地文件，匹配到相应版本后进行升级，除非指定了 `--version` 参数。