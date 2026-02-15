---
name: codeberg
description: "使用 `tea` CLI 与 Codeberg 进行交互。可以通过 `tea issue`、`tea pr`、`tea actions` 和 `tea api` 来处理问题（issues）、 pull 请求（PRs）、自动化任务（Actions）以及执行高级查询。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🏔️",
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

# Codeberg 技能

使用 `tea` 命令行工具（CLI）与 Codeberg 进行交互。Codeberg 是一个 Forgejo 实例，而 `tea` CLI 与之完全兼容。

## 提交请求（Pull Requests）

列出所有未解决的提交请求（Pull Requests）：

```bash
tea pulls --repo owner/repo
```

查看某个提交请求的详细信息：

```bash
tea pr 55 --repo owner/repo
```

## 问题（Issues）

列出所有未解决的问题（Issues）：

```bash
tea issues --repo owner/repo
```

查看某个问题（Issue）的详细信息：

```bash
tea issue 123 --repo owner/repo
```

## 操作（持续集成/持续部署，CI/CD）

列出仓库的秘密信息（repository secrets）：

```bash
tea actions secrets list --repo owner/repo
```

列出仓库的变量（repository variables）：

```bash
tea actions variables list --repo owner/repo
```

## 高级查询 API

`tea api` 命令可用于获取其他子命令无法提供的数据。

获取包含特定字段的提交请求（需要使用 `jq` 进行过滤）：

```bash
tea api repos/owner/repo/pulls/55 | jq '.title, .state, .user.login'
```

## 登录

要使用 `tea` 命令与 Codeberg 交互，首先需要登录：

```bash
tea login add --name codeberg --url https://codeberg.org --token <your-token>
```

之后，你可以在命令中添加 `--login codeberg` 选项来指定登录信息：

```bash
tea pulls --repo owner/repo --login codeberg
```

列出所有已配置的登录账户：

```bash
tea logins
```