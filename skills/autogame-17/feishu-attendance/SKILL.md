---
name: feishu-attendance
description: 监控飞书（Lark）的考勤记录，检查是否有员工迟到、早退或缺勤的情况，并向管理员报告。
tags: [feishu, lark, attendance, monitor, report]
---

# Feishu考勤系统

该系统用于监控员工的每日出勤情况，及时通知异常情况，并向管理员报告考勤汇总数据。

## 主要功能
- **智能检测**：能够自动识别员工迟到、早退或缺席的情况。
- **节假日识别**：通过 `timor.tech` API 自动识别节假日和周末。
- **安全模式**：在节假日 API 发生故障时，系统会关闭用户通知功能（防止垃圾信息发送）。
- **缓存机制**：为了提升系统性能，系统会缓存用户列表（缓存有效期为24小时）和节假日信息。
- **报表生成**：能够向管理员发送格式丰富的交互式报表。

## 使用方法

```bash
# Check today's attendance (Default)
node index.js check

# Check specific date
node index.js check --date 2023-10-27

# Dry Run (Test mode, no messages sent)
node index.js check --dry-run
```

## 所需权限
- `attendance:report:readonly`：仅用于读取考勤报告数据。
- `contact:user.employee:readonly`：仅用于读取员工联系方式信息。
- `im:message:send_as_bot`：仅用于以机器人身份发送消息。