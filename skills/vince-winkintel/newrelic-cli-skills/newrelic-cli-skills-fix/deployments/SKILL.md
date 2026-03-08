# 部署标记（Deployment Markers）

在新Relic中记录部署事件，以便将发布版本与性能变化关联起来。

---

## 记录部署（Record a Deployment）

```bash
newrelic apm deployment create \
  --applicationId <APP_ID> \
  --revision "v1.2.3" \
  --description "Brief description of what changed" \
  --user "deploy-bot"
```

### 必需参数（Required Parameters）  
- `--applicationId` — APM应用程序的ID（数字形式）  
- `--revision` — 版本字符串（例如：git SHA、semver或MR编号）  

### 可选参数（Optional Parameters）  
- `--description` — 发生的变化（会在New Relic的用户界面中以图表形式显示）  
- `--user` — 负责部署的人员或系统  
- `--changelog` — 详细的变更说明  

---

## 获取应用程序ID（Get Application ID）

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, applicationId}'
```

---

## 列出最近的部署（List Recent Deployments）

```bash
newrelic apm deployment list --applicationId <APP_ID>
```

---

## GitLab/GitHub持续集成（CI）集成（GitLab/GitHub CI Integration）

在部署成功后，将此脚本添加到您的持续集成流程中：

```bash
#!/bin/bash
# deploy-marker.sh
APP_ID="${NEW_RELIC_APP_ID}"
REVISION="${CI_COMMIT_SHORT_SHA:-$(git rev-parse --short HEAD)}"
DESCRIPTION="${CI_COMMIT_TITLE:-Deployment}"
USER="${GITLAB_USER_LOGIN:-ci-bot}"

newrelic apm deployment create \
  --applicationId "$APP_ID" \
  --revision "$REVISION" \
  --description "$DESCRIPTION" \
  --user "$USER"
```

---

## 部署标记的重要性（Why Deployment Markers Matter）

记录部署事件后，New Relic的用户界面会在所有APM图表上在该时间戳处显示一条垂直线。这有助于立即识别以下情况：  
- 部署后响应时间是否增加  
- 发布后错误率是否急剧上升  
- 吞吐量是否意外下降  

您还可以通过NRQL查询这些数据：

```nrql
SELECT *
FROM Deployment
WHERE appId = <APP_ID>
SINCE 1 week ago
```

---

## 自动化：在每次合并时进行标记（Automation: Mark on Every Merge）

可以在合并后的Webhook或CI步骤中调用以下脚本：

```bash
#!/bin/bash
# Usage: ./deployment-marker.sh <app_id> <revision> <description>
set -euo pipefail

APP_ID="${1:?app_id required}"
REVISION="${2:?revision required}"
DESCRIPTION="${3:-Automated deployment}"

newrelic apm deployment create \
  --applicationId "$APP_ID" \
  --revision "$REVISION" \
  --description "$DESCRIPTION" \
  --user "steven-openclaw"

echo "Deployment marker recorded: $REVISION → app $APP_ID"
```