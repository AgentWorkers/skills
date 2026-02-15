---
name: github-star-manager
description: 使用基于人工智能的分类和清理功能来管理 GitHub 的星标（stars）。当用户希望将他们收藏的仓库整理到 GitHub 列表中、清理过时/已弃用的星标、导出星标数据以供分析，或获取关于自己 GitHub 星标的统计信息时，可以使用该工具。该工具支持通过大型语言模型（LLM）进行语义分类，并支持批量操作（取消星标、添加到列表中）。
metadata:
  {
    "openclaw":
      {
        "emoji": "⭐",
        "requires": { "bins": ["gh", "jq"] },
        "notes": "Requires `gh auth login` (authenticated GitHub CLI). For Lists operations (create/add), the token needs `user` scope — use a Classic token. The skill uses the existing `gh` auth session; no separate env var is needed.",
        "install":
          [
            {
              "id": "brew-gh",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
            {
              "id": "apt-gh",
              "kind": "apt",
              "package": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (apt)",
            },
            {
              "id": "brew-jq",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
            {
              "id": "apt-jq",
              "kind": "apt",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (apt)",
            },
          ],
      },
  }
---

# GitHub Star Manager

该工具需要 `gh`（已认证的GitHub客户端）和 `jq` 命令工具。对于列表操作，需要使用具有 `user` 权限范围的令牌（推荐使用经典令牌）。

## 认证

该工具会使用 `gh` CLI 的现有认证会话。使用前，请执行以下操作：

1. 如果尚未认证，请运行 `gh auth login`。
2. 对于只读操作（如导出星标信息、查看统计数据），默认的令牌权限范围即可。
3. 对于列表操作（如创建列表、向列表中添加仓库），需要使用具有 `user` 权限范围的令牌。请运行 `gh auth refresh -s user`，或使用具有 `user` 权限范围的 [经典令牌](https://github.com/settings/tokens)。

无需单独的API密钥或环境变量。

## 导出星标信息

```bash
gh api user/starred --paginate --jq '.[] | {
  full_name, description, url: .html_url, language,
  topics, stars: .stargazers_count, forks: .forks_count,
  archived, updated_at, pushed_at
}' | jq -s '.' > stars.json
```

当仓库的星标数量超过1000个时，导出操作会较慢（大约每1000个星标需要1分钟）。快速统计星标数量的方法是：`gh api user/starred --paginate --jq '. | length' | jq -s 'add'`。

## 查看现有列表

```bash
gh api graphql -f query='{
  viewer {
    lists(first: 100) {
      nodes { id name description isPrivate items { totalCount } }
    }
  }
}' --jq '.data.viewer.lists.nodes'
```

## 创建列表

```bash
gh api graphql -f query='
mutation($name: String!, $desc: String) {
  createUserList(input: {name: $name, description: $desc, isPrivate: false}) {
    list { id name }
  }
}' -f name="LIST_NAME" -f desc="LIST_DESCRIPTION" --jq '.data.createUserList.list'
```

请保存返回的列表ID，以便后续添加仓库到列表中。

## 将仓库添加到列表中

```bash
REPO_ID=$(gh api repos/OWNER/REPO --jq '.node_id')

# Note: listIds is a JSON array, use --input to pass variables correctly
echo '{"query":"mutation($itemId:ID!,$listIds:[ID!]!){updateUserListsForItem(input:{itemId:$itemId,listIds:$listIds}){user{login}}}","variables":{"itemId":"'$REPO_ID'","listIds":["LIST_ID"]}}' \
  | gh api graphql --input -
```

为避免触发API调用速率限制，请在每次调用之间等待约300毫秒。

## 取消星标

```bash
gh api -X DELETE user/starred/OWNER/REPO
```

在取消星标之前，请务必先获得用户的确认。

## 工作流程组织：

1. 将星标信息导出为JSON格式。
2. 分析JSON数据，根据仓库的语言、主题、用途和领域对其进行分类。
3. 将分类结果展示给用户进行审核。
4. 在用户确认后，创建相应的列表并将仓库添加到列表中。
5. 在执行批量操作时，请在每次API调用之间设置适当的延迟。

## 清理工作流程：

1. 将星标信息导出为JSON格式。
2. 使用 `jq` 命令筛选出已归档的仓库、长时间未更新的仓库（超过2年未推送更新）、星标数量较少的仓库或已被弃用的仓库。
3. 将符合条件的仓库列表展示给用户，确认后再取消它们的星标状态。