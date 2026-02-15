---
name: korea-metropolitan-bus-alerts
description: 使用韩国国土交通部（Korea TAGO）的 OpenAPI 和 Clawdbot 的 cron 任务来创建和管理公交车到站提醒。当用户需要注册工作日/周末的出行计划（例如：“工作日上午 7 点，<公交站名称>，<相关线路>”）时，系统会通过用户配置的 Gateway（仅限私信）自动发送公交车到站信息。
metadata:
  {
    "openclaw": {
      "emoji": "🚌",
      "requires": {
        "env": ["TAGO_SERVICE_KEY"],
        "bins": ["python3", "systemctl"],
        "optionalBins": ["clawdbot"]
      },
      "primaryEnv": "TAGO_SERVICE_KEY"
    }
  }
---

# 首都圈公交车到站通知（Clawdbot cron）

该功能基于**韩国国土交通部TAGO OpenAPI**提供定时公交车到站提醒服务。

本技能专为使用**Clawdbot Gateway + Clawdbot cron**的用户设计。用户可以注册如下规则：
- “工作日早上7点，仁川汉光小学，535路公交车”
- “工作日下午5点30分，高阳香洞小学，730路/503路公交车”

系统会按照预定时间将到站信息发送给**注册用户（通过私信）**。

> 注意（MVP）：公交站点的查询是通过**站点名称搜索**来完成的（格式为`cityCode + 关键词`）。虽然系统也支持基于GPS的附近站点查询，但由于地区或关键词的不同，可能会返回0个结果。

## 先决条件
- Clawdbot Gateway已启动并配置完成（支持Telegram/Slack等通信方式）
- Clawdbot cron功能已启用且可用
- 拥有TAGO API的访问密钥（data.go.kr提供）
- （若使用自动化设置）系统需要支持`systemctl --user`命令（即systemd用户服务）
- （若要通过`rule_wizard`注册规则）需要`clawdbot` CLI工具

## 一次性设置：TAGO API密钥
您需要在环境中设置TAGO服务密钥（切勿将密钥直接写入markdown文件中）。

推荐的环境变量：
- `TAGO_SERVICE_KEY`

### 选项A（最快方式）：在当前shell中一次性测试
适用于快速手动测试；**cron作业不会自动继承此密钥**，除非您在Gateway服务中也设置了该密钥。

```bash
export TAGO_SERVICE_KEY='...'
```

### 选项B（推荐方式）：一键完成设置
这是“设置一次即可永久使用”的方案。

运行以下命令：
```bash
python3 korea-metropolitan-bus-alerts/scripts/setup.py
```

如果网络问题导致无法访问API端点，或者TAGO返回403错误，您仍可完成设置：
```bash
python3 korea-metropolitan-bus-alerts/scripts/setup.py --skip-smoke
```

该流程将：
- 自动检测您的Gateway systemd用户服务（支持自定义服务名称）
- 提示您输入`TAGO_SERVICE_KEY`（该密钥会以隐藏形式输入）
- 将密钥保存到`~/.clawdbot/secrets/tago.env`文件中（并设置权限为600）
- 生成systemd配置文件以加载该环境变量
- 重启Gateway服务
- 运行一次TAGO测试

（高级/手动操作）如果您更喜欢使用shell脚本，`korea-metropolitan-bus-alerts/scripts/set_tago_key.sh`仍然可用，但推荐使用`setup.py`进行设置。

### 安全注意事项
- 严禁将`.env`或`tago.env`文件中的密钥泄露
- 避免分享`docker compose config`等命令的输出内容（这些命令可能会显示环境变量）

## 快速入门

### A）测试TAGO API的连接是否正常
```bash
export TAGO_SERVICE_KEY='...'
python3 korea-metropolitan-bus-alerts/scripts/tago_bus_alert.py nearby-stops --lat 37.5665 --long 126.9780
```

### B）注册公交到站通知规则
您可以向系统发送如下指令：
- “工作日07:00，为仁川汉光小学，535路公交车注册到站通知”

如果站点名称不明确（例如，站点位于道路对面），系统会要求您提供更多信息以确定正确的站点位置。

### C）查看所有已注册的规则
- “显示所有公交到站通知规则”

### D）删除规则
- “删除编号为3的公交到站通知规则”（删除前需要确认）

### E）立即测试规则
- “测试刚刚注册的规则”

## 支持的调度表达式（MVP版本）
- 每天HH:MM
- 工作日HH:MM
- 周末HH:MM

（后续版本将支持更复杂的cron表达式）

## Cron任务实现细节
- 使用独立的cron作业（`sessionTarget: isolated`）并设置`deliver: true`选项
- 通知仅发送给注册用户（通过私信）
- 详情请参考`references/cron_recipe.md`和`scripts/cron_builder.py`文件

### 交互式规则注册助手（服务器端）
对于集成测试或高级用户，可以使用`scripts/rule_wizard.py`工具：
- 该工具会：
  1) 获取用户输入的调度时间、路线信息
  2) 通过GPS查询附近的公交站点（解决站点名称的歧义）
  3) 生成用于注册cron任务的JSON数据
  4）（可选）调用`clawdbot cron add`命令完成规则注册

## 数据来源
目前仅支持一个数据提供者（MVP版本）：
- 公交站点信息查询：BusSttnInfoInqireService（API编号：15098534）
- 公交到站信息查询：ArvlInfoInqireService（API编号：15098530）

## 安全性注意事项
- 绝不要将API密钥或密码写入markdown文件中
- 对于通过浏览器进行的自动化操作，需用户明确确认
- 对于可能具有破坏性的操作（如删除规则），请在执行前再次确认
- 通知仅发送给注册用户（MVP版本），避免向群组或频道广播

## 实现细节
- 建议将相关脚本放在`scripts/`目录下，以确保行为的稳定性
- API字段的详细映射信息请参考`references/api_reference.md`

### 确定性辅助脚本
使用`scripts/tago_bus_alert.py`进行TAGO相关操作：
- `nearby-stops`函数用于根据GPS坐标查找附近的公交站点
- `arrivals`函数用于根据`cityCode`和`nodeId`获取公交车到站信息（支持路线筛选）