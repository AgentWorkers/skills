---
name: clawhub
description: 使用 ClawHub CLI 来搜索、安装、更新以及发布来自 clawhub.com 的代理技能（agent skills）。当您需要即时获取新技能、将已安装的技能同步到最新版本或特定版本，或者使用 npm 安装的 ClawHub CLI 发布新的/更新的技能文件夹时，请使用该工具。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "Install ClawHub CLI (npm)",
            },
          ],
      },
  }
---
# ClawHub CLI

## 安装  
```bash
npm i -g clawhub
```

## 认证（发布）  
```bash
clawhub login
clawhub whoami
```

## 搜索  
```bash
clawhub search "postgres backups"
```

## 安装  
```bash
clawhub install my-skill
clawhub install my-skill --version 1.2.3
```

## 更新（基于哈希值的匹配与升级）  
```bash
clawhub update my-skill
clawhub update my-skill --version 1.2.3
clawhub update --all
clawhub update my-skill --force
clawhub update --all --no-input --force
```

## 列出  
```bash
clawhub list
```

## 发布  
```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

## 注意事项：  
- 默认注册地址：https://clawhub.com（可通过 `CLAWHUB_REGISTRY` 或 `--registry` 参数进行覆盖）  
- 默认工作目录：当前目录（`cwd`）；安装目录：`./skills`（可通过 `--workdir` 或 `--dir` 或 `CLAWHUB_WORKDIR` 参数进行覆盖）  
- `update` 命令会更新本地文件，匹配到相应版本后进行升级，除非指定了 `--version` 参数。