---
name: gitea
description: "使用 `tea` CLI 与 Gitea 进行交互。可以通过 `tea issue`、`tea pr`、`tea actions` 和 `tea api` 来处理问题（issues）、拉取请求（PRs）、执行操作（Actions）以及进行高级查询。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🍵",
        "requires": { "bins": ["tea"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "tea",
              "bins": ["tea"],
              "label": "Install Tea CLI (brew)",
            },
            {
              "id": "go",
              "kind": "go",
              "module": "code.gitea.io/tea@latest",
              "bins": ["tea"],
              "label": "Install Tea CLI (go)",
            },
          ],
      },
  }
---

# Gitea 技能

使用 `tea` 命令行工具（CLI）与 Gitea 实例进行交互。`tea` 是 Gitea 的官方命令行工具。

## 提交请求（Pull Requests）

- 列出所有未解决的提交请求（Pull Requests）：
  ```bash
tea pulls --repo owner/repo
```

- 查看某个提交请求的详细信息：
  ```bash
tea pr 55 --repo owner/repo
```

## 问题（Issues）

- 列出所有未解决的问题（Issues）：
  ```bash
tea issues --repo owner/repo
```

- 查看某个问题的详细信息：
  ```bash
tea issue 123 --repo owner/repo
```

## 操作（CI/CD）

- 列出仓库的秘密信息（Repository Secrets）：
  ```bash
tea actions secrets list --repo owner/repo
```

- 列出仓库的变量（Repository Variables）：
  ```bash
tea actions variables list --repo owner/repo
```

## 高级查询 API

`tea api` 命令可用于获取其他子命令无法提供的数据。

- 获取包含特定字段的提交请求（需要使用 `jq` 进行过滤）：
  ```bash
tea api repos/owner/repo/pulls/55 | jq '.title, .state, .user.login'
```

## 登录

要使用 `tea` 命令与特定的 Gitea 实例进行交互，首先需要登录：
  ```bash
tea login add --name my-gitea --url https://gitea.example.com --token <your-token>
```

之后，你可以在命令中添加 `--login my-gitea` 选项来指定登录信息：
  ```bash
tea pulls --repo owner/repo --login my-gitea
```

- 列出所有已配置的登录信息：
  ```bash
tea logins
```