---
name: placed-job-tracker
description: 当用户希望“跟踪工作申请”、“添加工作申请”、“更新申请状态”、“查看我的工作流程”或使用 Placed 职业平台（placed.exidian.tech）管理自己的求职活动时，应使用此技能。
version: 1.0.0
metadata: {"openclaw":{"emoji":"📋","homepage":"https://placed.exidian.tech","requires":{"env":["PLACED_API_KEY"]},"primaryEnv":"PLACED_API_KEY"}}
---
# Placed Job Tracker

通过 Placed 平台，利用人工智能驱动的流程分析功能来跟踪和管理您的求职申请。

## 先决条件

需要安装 Placed MCP 服务器。安装方法如下：
```json
{
  "mcpServers": {
    "placed": {
      "command": "npx",
      "args": ["-y", "@exidian/placed-mcp"],
      "env": {
        "PLACED_API_KEY": "your-api-key",
        "PLACED_BASE_URL": "https://placed.exidian.tech"
      }
    }
  }
}
```
请在 https://placed.exidian.tech/settings/api 获取您的 API 密钥。

## 可用工具

- `add_job_application` — 添加新的求职申请
- `list_job_applications` — 查看您的申请流程
- `update_job_status` — 更新申请状态（已申请、电话面试、面试中、收到录用通知、被拒绝）
- `get_application_analytics` — 获取申请流程分析数据及转化率
- `match_job` — 评估您的简历与职位的匹配程度（0-100 分）
- `analyze_resume_gaps` — 识别特定职位所需的关键词和技能缺失项

## 使用方法

**添加求职申请：**
调用 `add_job_application年公司="Stripe", 职位="Senior Engineer", 状态="Applied", url="https://stripe.com/jobs/123", 备注="由 John 推荐")`

**查看申请流程：**
调用 `list_job_applications(status="all")` 查看所有申请
调用 `list_job_applications(status="Interview")` 按阶段筛选申请

**更新申请状态：**
调用 `update_job_status(申请ID="...", 状态="Phone Screen", 备注="安排在下周二进行电话面试")`

**获取申请流程分析数据：**
调用 `get_application_analytics(时间范围="30d")`
返回：各阶段的转化率、回复率、到收到录用通知所需时间、热门招聘公司信息

**在申请前评估简历匹配度：**
调用 `match_job(简历ID="...", 职位描述="...")`
返回：匹配分数（0-100 分）、缺失的关键词、个人优势

## 申请状态

- `Saved` — 申请已保存，待后续处理
- `Applied` — 申请已提交
- `Phone Screen` — 初步电话面试或招聘人员面试
- `Interview` — 技术面试或现场面试
- `Offer` — 收到录用通知
- `Accepted` — 接受录用通知
- `Rejected` — 申请被拒绝
- `Withdrawn` — 申请已撤回

## 求职技巧

1. 每周申请 5-10 个职位以获得最佳效果
2. 使用 `optimize_resume_for_job` 功能为每个申请定制简历
3. 记录所有申请情况（包括非正式申请）
4. 如果 1-2 周内没有回复，请及时跟进
5. 通过分析数据找出需要改进的环节
6. 力求电话面试通过率达到 20% 以上；如果低于此比例，请优化简历内容