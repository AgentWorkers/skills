---
name: linear
description: "通过 Linear GraphQL API 查询和管理问题（issues）、项目（projects）、开发周期（cycles）以及团队（teams）。当您需要列出或创建问题、检查开发周期的状态、管理项目，或在工作空间内进行搜索时，可以使用该 API。该 API 直接调用 `api.linear.app`，无需通过任何第三方代理。"
metadata:
  openclaw:
    requires:
      env:
        - LINEAR_API_KEY
      bins:
        - python3
    primaryEnv: LINEAR_API_KEY
    files:
      - "scripts/*"
---
# Linear

您可以通过 Linear 的 GraphQL API (`api.linear.appgraphql`) 直接与其交互。

## 设置（只需完成一次）

1. 登录 Linear，进入“设置”（Settings）→“账户”（Account）→“安全与访问”（Security & Access）→“API 密钥”（API Keys）。
2. 创建一个新的 API 密钥。
3. 设置环境变量：
   ```
   LINEAR_API_KEY=lin_api_...
   ```

## 使用方法

### 列出您的团队
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py teams
```

### 列出分配给您的任务
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py my-issues
python3 /mnt/skills/user/linear/scripts/linear_query.py my-issues --state "In Progress"
```

### 列出某个团队的任务
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py issues --team "Engineering"
python3 /mnt/skills/user/linear/scripts/linear_query.py issues --team "Engineering" --state "Todo" --limit 20
```

### 获取特定任务
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py issue ENG-123
```

### 搜索任务
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py search "authentication bug"
```

### 创建任务
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py create --team "Engineering" --title "Fix login bug" --description "Users can't log in on Safari"
python3 /mnt/skills/user/linear/scripts/linear_query.py create --team "Engineering" --title "Add dark mode" --priority 2
```

### 更新任务
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py update ENG-123 --state "Done"
python3 /mnt/skills/user/linear/scripts/linear_query.py update ENG-123 --priority 1 --title "New title"
```

### 列出项目
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py projects
python3 /mnt/skills/user/linear/scripts/linear_query.py projects --team "Engineering"
```

### 列出冲刺（sprints）
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py cycles --team "Engineering"
```

### 查看某个团队的工作流程状态
```bash
python3 /mnt/skills/user/linear/scripts/linear_query.py states --team "Engineering"
```

## 优先级级别
- 0 = 无优先级
- 1 = 紧急
- 2 = 高
- 3 = 一般
- 4 = 低