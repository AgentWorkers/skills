---
name: arcagent-mcp
description: 通过 MCP 工具端到端执行 ArcAgent 奖金工作流程。该流程适用于以下场景：领取奖金、在工作区中实施相关操作、提交成果以供验证、调试工作者/工作区中出现的错误，以及反复尝试（直到运行成功）。根据验证结果，系统会持续进行重试或重新提交操作，直到满足以下条件之一：（1）提交的 PR 被验证通过并完成支付；（2）用户明确放弃领取奖金的请求。
---
# ArcAgent MCP

使用MCP工具集来执行ArcAgent的赏金工作流程。

## 结果合约

将每个被领取的赏金引导至以下两种最终状态之一：
- 成功：验证通过，创建相应的Pull Request（PR），支付流程完成。
- 失败：进度受阻或耗尽，释放该赏金申请。

即使初次验证失败，只要还有尝试次数和时间，也不要停止尝试。

## 标准流程

1. 发现并领取赏金：
   - 使用`list_bounties`、`get_bounty_details`、`claim_bounty`命令。
   - 通过`get_claim_status`、`workspace_status`确认赏金申请的状态和工作区的状态。

2. 等待工作区准备好：
   - 持续检查`workspace_status`，直到工作区状态变为“ready”。
   - 如果进程停滞，查看`workspace_startup_log`和`check_worker_status`以获取更多信息。

3. 仅在工作区内进行操作：
   - 使用`workspace_read_file`、`workspace_edit_file`、`workspace_write_file`、`workspace_apply_patch`来处理文件。
   - 使用`workspace_search`、`workspace_grep`、`workspace_glob`、`workspace_list_files`来定位需要修改的文件。
   - 使用`workspace_exec`/`workspace_exec_stream`来执行项目所需的命令。

4. 提交并验证结果：
   - 使用`submit_solution`提交解决方案。
   - 通过`getverification_status`跟踪验证进度。

5. 失败时重试：
   - 阅读`get_verification_status`和`getsubmission_feedback`的结果。
   - 在工作区内修复问题。
   - 再次使用`submit_solution`提交解决方案。
   - 重复上述步骤，直到验证通过或达到终止条件。

6. 完成流程：
   - 如果验证通过，确保PR和支付流程已完成。
   - 如果工作区处于无法恢复的状态或所有尝试次数都已用尽，调用`release_claim`释放赏金申请。

## 必须的重试规则

当验证失败且还有尝试次数和时间时：
- 必须至少再提交一次修正方案。
- 必须优先处理严重性最高的反馈问题。
- 修复的范围应仅限于出现问题的部分。

只有在以下情况下才停止重试：
- 验证通过；
- 所有尝试次数都已用尽；
- 赏金申请的过期或其他阻碍因素使得继续执行变得不可行。

## 按任务划分的工具使用指南

**赏金和申请生命周期相关工具：**
- `list_bounties`、`get_bounty_details`、`claim_bounty`、`get_claim_status`、`extend_claim`、`release_claim`

**工作区开发相关工具：**
- `workspace_status`、`workspace_read_file`、`workspace_batch_read`、`workspace_edit_file`、`workspace_apply_patch`、`workspace_write_file`、`workspace_batch_write`、`workspace_exec`、`workspace_exec_stream`、`workspace_shell`

**验证和迭代相关工具：**
- `submit_solution`、`getverification_status`、`getsubmission_feedback`、`list_my_submissions`

**基础设施诊断相关工具：**
- `workspace_startup_log`、`check_worker_status`、`workspace_crash_reports`

## 常见故障及其应对措施

- **验证排队时间过长：**
  - 通过`check_worker_status`和日志检查工作器的运行状态及队列使用情况。

- **工作区配置失败：**
  - 查看`workspace_startup_log`；如果工作区无法使用，重新配置或释放资源。

- **提交内容中包含无关更改：**
  - 保持修改内容最小化，并确保与任务相关；避免修改无关的文件。

- **测试门（test-gate）失败：**
  - 将反馈视为问题的根本原因，修复后重新提交。

## 终止条件

**成功终止条件：**
- 验证通过，且PR和支付流程已完成。

**放弃终止条件：**
- 在剩余的尝试次数和时间内多次尝试均失败，且无法解决问题。
- 显式调用`release_claim`释放赏金申请。