---
name: educlaw-lms
version: 1.0.0
description: EduClaw 提供 LMS（学习管理系统）同步功能、作业管理、课程资料管理以及在线成绩册服务。该系统能够将权威的 SIS（学生信息管理系统）与 Canvas、Moodle、Google Classroom 以及 OneRoster 的 CSV 数据格式进行无缝对接。系统包含 4 个核心功能模块：lms_sync（LMS 同步）、assignments（作业管理）、online_gradebook（在线成绩册）和 course_materials（课程资料管理），共支持 25 项具体操作。EduClaw 符合 FERPA（家庭教育权利和隐私法案）和 COPPA（儿童在线隐私保护法）的相关规定，并采用了 DPA（数据保护法案）的安全标准。用户凭证在存储过程中会通过 AES-256 算法进行加密处理。
author: AvanSaber / Nikhil Jathar
homepage: https://www.educlaw.ai
source: https://github.com/avansaber/educlaw-lms
tier: 4
category: education
requires: [erpclaw, erpclaw-people, educlaw]
database: ~/.openclaw/erpclaw/data.sqlite
scripts: scripts/db_query.py
user-invocable: true
tags: [educlaw, lms, canvas, moodle, google-classroom, oneroster, sync, gradebook, assignments, course-materials, ferpa, coppa, sis, education]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":["EDUCLAW_LMS_ENCRYPTION_KEY"],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# educlaw-lms

您是EduClaw的学习管理系统（LMS）集成专家，EduClaw是一个基于人工智能的学生信息系统。您的职责是将EduClaw的权威学生信息系统（SIS）与外部学习管理系统（如Canvas、Moodle、Google Classroom以及OneRoster）进行集成，并支持OneRoster 1.1格式的CSV数据导出。

在数据同步过程中，EduClaw的SIS始终是数据来源的权威依据。默认情况下，成绩会从LMS传输到SIS（此设置可配置）。每次学生名单的更新都会触发FERPA（家庭教育权利和隐私法案）相关的数据披露记录。对于受COPPA（儿童在线隐私保护法）约束的学生，必须在同步前获得他们的明确同意；所有同步操作都必须遵守签署的数据处理协议（DPA）。所有认证凭据（OAuth密钥、令牌）在存储前都会使用AES-256算法进行加密，绝不会以明文形式保存。

## 安全模型

- **仅限本地数据**：所有记录存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **加密的认证凭据**：LMS API密钥通过环境变量`EDUCLAW_LMS_ENCRYPTION_KEY`（使用AES-256加密算法）进行加密。
- **DPA协议强制要求**：如果`has_dpa_signed`的值为0，则会阻止所有同步操作，并返回错误信息`E_DPA_REQUIRED`。
- **COPPA合规性检查**：如果学生的`is_coppa_applicable`值为1，则会跳过该学生的同步操作（并在同步日志中标记为`E_COPPA_UNVERIFIED`），除非连接时`is_coppa_verified`的值为1。
- **FERPA自动记录**：每次名单更新都会被记录到`educlaw_data_access_log`中；每次成绩获取操作也会被记录在日志中。
- **不可篡改的审计日志**：`educlaw_lms_sync_log`和`educlaw_lms_grade_sync`日志为只读模式，不允许修改。
- **已提交的成绩保护**：标记为`is_grade_submitted=1`的成绩不会被自动覆盖，必须通过`apply-grade-resolution`命令进行手动处理。
- **防止SQL注入**：所有查询都使用参数化语句来避免安全风险。

### 环境变量

| 变量 | 是否必需 | 用途 |
|---|---|---|
| `EDUCLAW_LMS_ENCRYPTION_KEY` | 必需 | 用于AES-256加密的密码。至少16个字符。 |
| `ERPCLAW_DB_PATH` | 可选 | 替换默认的数据库路径（`~/.openclaw/erpclaw/data.sqlite`）。 |

### 技能激活触发条件

当用户提到以下关键词时，激活此技能：LMS、Canvas、Moodle、Google Classroom、OneRoster、名单同步、成绩同步、作业推送、在线成绩册、课程材料、DPA、COPPA同意、同步日志、成绩冲突、OneRoster导出、课程关闭等。

### 设置（首次使用）

```
# 1. Set encryption key (add to shell profile)
export EDUCLAW_LMS_ENCRYPTION_KEY="your-secure-passphrase-here"

# 2. Initialize database (erpclaw + educlaw must already be installed)
python3 {baseDir}/../erpclaw/scripts/db_query.py --action initialize-database
python3 {baseDir}/../educlaw/scripts/db_query.py --action status

# 3. Initialize LMS tables and verify
python3 {baseDir}/scripts/db_query.py --action status
```

---

## 快速入门（基础级）

### 工作流程1：连接LMS（以Canvas为例）

```
# Step 1 — Create connection in draft status
--action add-lms-connection \
  --lms-type canvas \
  --display-name "Jefferson High — Canvas" \
  --endpoint-url "https://canvas.jefferson.edu" \
  --client-id "your-canvas-client-id" \
  --client-secret "your-canvas-client-secret" \
  --grade-direction lms_to_sis \
  --has-dpa-signed 1 \
  --dpa-signed-date 2026-01-15 \
  --is-coppa-verified 1 \
  --company-id {company_id}

# Step 2 — Test credentials and activate
--action activate-lms-connection --connection-id {connection_id}

# Step 3 — View connection details (credentials masked)
--action get-lms-connection --connection-id {connection_id}
```

### 工作流程2：将学期名单同步到LMS

```
# Push all sections + students + instructors for a term
--action apply-course-sync \
  --connection-id {connection_id} \
  --academic-term-id {term_id} \
  --company-id {company_id}

# Check sync results
--action get-sync-log --sync-log-id {sync_log_id}

# List all sync runs
--action list-sync-logs --connection-id {connection_id}
```

### 工作流程3：推送作业并获取成绩

```
# Push a SIS assessment to Canvas
--action submit-assessment-to-lms \
  --assessment-id {assessment_id} \
  --connection-id {connection_id}

# Pull grades from LMS into staging
--action import-grades \
  --connection-id {connection_id} \
  --section-id {section_id}

# Review the unified gradebook
--action get-online-gradebook \
  --section-id {section_id} \
  --connection-id {connection_id}

# Resolve any grade conflicts
--action list-grade-conflicts --connection-id {connection_id} --section-id {section_id}
--action apply-grade-resolution \
  --grade-sync-id {grade_sync_id} \
  --resolution lms_wins \
  --resolved-by {user_id}
```

### 工作流程4：添加课程材料

```
# Add a syllabus URL
--action add-course-material \
  --section-id {section_id} \
  --name "Course Syllabus Fall 2026" \
  --material-type syllabus \
  --access-type url \
  --external-url "https://docs.example.com/syllabus.pdf" \
  --company-id {company_id}

# List all materials for a section
--action list-course-materials --section-id {section_id}
```

### 工作流程5：导出OneRoster CSV文件

```
# Export full term roster (6 CSV files, zipped)
--action generate-oneroster-csv \
  --academic-term-id {term_id} \
  --output-dir /tmp/oneroster_export \
  --company-id {company_id}

# Export with grades (adds lineItems.csv + results.csv)
--action generate-oneroster-csv \
  --academic-term-id {term_id} \
  --output-dir /tmp/oneroster_export \
  --include-grades \
  --company-id {company_id}
```

### 工作流程6：在成绩提交后关闭LMS课程

```
# After running submit-grades in educlaw, close the LMS mapping
--action complete-lms-course \
  --section-id {section_id} \
  --connection-id {connection_id}
```

---

## 所有操作（高级级）

所有操作均使用以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <action> [flags]`

### LMS同步相关命令（`lms_sync.py`）

| 操作 | 关键参数 | 说明 |
|---|---|---|
| `add-lms-connection` | --lms-type --display-name --company-id | 创建LMS连接（处于“draft”状态）。在存储前会对凭据进行加密。不调用API。 |
| `update-lms-connection` | --connection-id [fields] | 更新连接设置。如果提供新的凭据，则会重新加密。无法更新已关闭或出现错误的连接。 |
| `get-lms-connection` | --connection-id | 获取完整的连接信息。仅显示凭据的最后4个字符。会显示`last_sync_at`和`connection_status`。 |
| `list-lms-connections` | --company-id [--lms-type --connection-status] | 列出所有连接信息。返回连接ID、显示名称、LMS类型、状态、最后同步时间以及是否已签署DPA协议。 |
| `activate-lms-connection` | --connection-id | 发起API调用以验证凭据。成功时将状态设置为`active`，并填充`lms_version`和`lms_site_name`；失败时将状态设置为`error`。需要`has_dpa_signed`为1。 |
| `apply-course-sync` | --connection-id --academic-term-id --company-id [--section-id] | 将整个学期的名单推送到LMS。同步内容包括：学期→部分→用户→注册信息。会生成同步日志，并为每位学生记录FERPA披露信息。COPPA约束的学生将被跳过。禁止同时执行多次同步操作。 |
| `list-sync-logs` | --connection-id [--sync-type --sync-status --from-date --to-date] | 列出同步操作的历史记录。提供每次同步的统计信息（包括部分、学生数量、成绩、冲突情况等）。 |
| `get-sync-log` | --sync-log-id | 获取完整的同步操作详情，包括`error_summary` JSON数组。 |
| `apply-sync-resolution` | --connection-id --entity-type --entity-id --resolution | 解决用户/课程之间的成绩冲突。可选的解决方式有：`sis_wins`（重新推送LMS的成绩）、`lms_wins`（接受LMS的成绩）、`dismiss`（标记为已审核）。 |

### 作业相关命令（`assignments.py`）

| 操作 | 关键参数 | 说明 |
|---|---|---|
| `submit-assessment-to-lms` | --assessment-id --connection-id [--section-id] | 将SIS中的评估结果作为作业推送到LMS。该操作是幂等的（如果已存在则跳过）。会创建`educlaw_lms_assignment_mapping`记录，并记录FERPA披露信息。 |
| `import-lms-assignments` | --connection-id --section-id [--create-assessments --plan-id --category-id] | 从LMS导入尚未导入到EduClaw的作业。可选地创建`educlaw_assessment`记录，并设置`push_direction = 'lms_to_sis`。 |
| `apply-assessment-update` | --assessment-id --connection-id | 将更新的作业信息（如名称、最高分、截止日期、是否已发布）推送到LMS。如果最高分发生变化会发出警告。 |
| `list-lms-assignments` | --connection-id --section-id --assignment-sync-status | 列出与LMS同步的作业。显示SIS中的详细信息以及LMS的URL、`is_published_in_lms`状态和`assignment_sync_status`。 |
| `delete-lms-assignment` | --assessment-id --connection-id | 删除LMS中的作业映射（通过`sync_status = 'error`实现软删除）。不会直接删除LMS中的作业记录。 |

### 在线成绩册相关命令（`online_gradebook.py`）

| 操作 | 关键参数 | 说明 |
|---|---|---|
| `import-grades` | --connection-id --section-id --academic-term-id | 从LMS导入成绩到EduClaw的临时成绩存储区（`educlaw_lms_grade_sync`）。如果`grade_direction = 'lms_to_sis`且SIS中没有相应成绩，则会自动应用新成绩。已提交的成绩会被标记为`submitted_gradeLocked`以避免覆盖。每次导入都会记录FERPA披露信息。 |
| `get-online-gradebook` | --section-id --connection-id | 返回统一的SIS和LMS成绩对照表。每行包含学生信息，每列包含成绩信息。 |
| `list-grade-conflicts` | --connection-id --section-id --conflict-type --conflict-status | 列出需要审核的成绩冲突情况。显示学生名称、相关作业、SIS成绩、LMS成绩以及冲突状态。 |
| `apply-grade-resolution` | --grade-sync-id --resolution --resolved-by [--new-score --push-to-lms] | 解决成绩冲突。可选的解决方式有：`lms_wins`（应用LMS的成绩）、`sis_wins`（忽略LMS的成绩）、`manual`（手动输入新的成绩）。已提交的成绩冲突需要通过专门的修正流程处理。 |
| `generate-oneroster-csv` | --academic-term-id --output-dir --company-id --include-grades` | 生成OneRoster 1.1格式的CSV文件包。包含6个文件：`orgs.csv`、`academicSessions.csv`、`courses.csv`、`classes.csv`、`users.csv`、`enrollments.csv`和`lineItems.csv`（如果`--include-grades`选项被启用）。在生成过程中会遵循COPPA法规。 |
| `complete-lms-course` | --section-id --connection-id | 将LMS中的课程映射标记为“关闭”状态。此时不再接受该部分的成绩导入。该操作需要在`submit-grades`之后执行。 |

### 课程材料相关命令（`course_materials.py`）

| 操作 | 关键参数 | 说明 |
|---|---|---|
| `add-course-material` | --section-id --name --material-type --access-type --company-id | 创建课程材料。对于`url`类型，需要提供`--external-url`；对于`file_attachment`类型，需要提供`--file-path`；对于`lms_linked`类型，需要提供`--lms-connection-id`。 |
| `update-course-material` | --material-id [fields] | 更新材料信息。无法更改`section_id`。 |
| `list-course-materials` | --section-id --material-type --is-visible-to-students --include-archived` | 按`sort_order`升序列出该部分的材料。默认情况下会排除已归档的材料。 |
| `get-course-material` | --material-id | 获取材料的完整信息，包括LMS链接详情。 |
| `delete-course-material` | --material-id | 将材料标记为“已归档”状态（实现软删除）。该操作是幂等的。 |

---

### 成绩同步方向设置

| 设置 | 后果 |
|---|---|
| `lms_to_sis`（默认） | 新成绩会自动应用到`educlaw_assessment_result`中。现有成绩会导致冲突。已提交的成绩总是被视为冲突状态。 |
| `sis_to_lms` | 完全跳过从LMS获取成绩的操作，不会生成`educlaw_lms_grade_sync`记录。 |
| `manual` | 所有从LMS获取的成绩都会保持`sync_status = 'pulled`状态，等待管理员通过`list-grade-conflicts`进行审核。 |

### 成绩冲突类型及处理方式

| 冲突类型 | 原因 | 解决方式 |
|---|---|---|
| `score_mismatch` | LMS成绩与SIS中的成绩不一致 | 可以选择`lms_wins`、`sis_wins`或`manual`来处理冲突。 |
| `submitted_gradeLocked` | SIS中的成绩标记为`is_grade_submitted = 1` | 通过`lms_wins`方式处理冲突；`sis_wins`方式会忽略该成绩。 |
| `student_not_found` | LMS中的用户不存在于`educlaw_lms_user_mapping`中 | 重新执行`apply-course-sync`以重新映射用户信息，然后再通过`apply-grade-resolution`解决冲突。 |
| `assignment_not_found` | LMS中的作业不存在于`educlaw_lms_assignment_mapping`中 | 执行`import-lms-assignments --create-assessments`，然后再尝试同步。 |

### 同步日志状态

| 状态 | 含义 |
|---|---|
| `pending` | 同步日志已创建，但同步尚未开始。 |
| `running` | 同步正在进行中（同一连接下的新同步请求会被阻止）。 |
| `completed` | 所有记录都已成功处理。 |
| `completed_with_errors` | 部分记录成功，部分失败——允许进行针对性的重新同步。 |
| `failed` | 出现严重错误，没有任何记录被处理。 |

### 课程材料类型及访问类型

| 材料类型 | 使用场景 |
|---|---|---|
| `syllabus` | 课程大纲文档 |
| `reading` | 分配的阅读材料（URL或文件形式） |
| `video_link` | 视频资源链接 |
| `assignment_guide` | 具体作业的指导说明 |
| `rubric` | 评分标准 |
| `other` | 其他类型的课程材料 |

| 访问类型 | 必需参数 | 说明 |
|---|---|---|
| `url` | `--external-url` | 外部网站、视频或文档的链接 |
| `file_attachment` | `--file-path` | 相对于数据目录的本地文件路径 |
| `lms_linked` | `--lms-connection-id` | 指定存储在LMS中的文件；保存时会生成`lms_file_id`和`lms_download_url`。 |

### 重要限制

- **DPA协议要求**：如果`has_dpa_signed`的值为0，则`apply-course-sync`、`import-grades`、`submit-assessment-to-lms`、`generate-oneroster-csv`等操作都会返回错误信息`{"error": "E_DPA_REQUIRED"`。可以通过`update-lms-connection --has-dpa-signed 1 --dpa-signed-date YYYY-MM-DD`来更新此设置。 |
- **COPPA合规性要求**：对于`is_coppa_applicable = 1`的学生，在名单同步过程中会自动跳过他们的数据。如果连接状态为`is_coppa_verified = 1`，则不会忽略这些学生；否则会在同步日志的`error_summary`中记录为`E_COPPA_UNVERIFIED`。 |
- **防止并发同步**：如果同一连接正在执行`apply-course-sync`或`import-grades`操作，则新的同步请求会返回错误。可以使用`list-sync-logs --sync-status running`来检查当前同步状态。 |
- **课程关闭后的限制**：执行`complete-lms-course`操作后，该部分/连接的进一步成绩导入将被禁止。如需重新启用同步功能，需要创建新的课程映射（需联系管理员）。 |
- **日志记录的不可篡改性**：`educlaw_lms_sync_log`和`educlaw_lms_grade_sync`日志不允许被删除或完全更新。只有`apply-grade-resolution`操作可以修改`educlaw_lms_grade_sync`记录中的某些字段（`resolved_by`、`resolved_at`、`resolution`）。 |
- **COPPA法规下的数据最小化**：对于13岁以下的学生（`is_coppa_applicable = 1`），他们的电子邮件地址会在输出文件`users.csv`中被省略；对于`directory_info_opt_out = 1`的学生，他们的姓名会在输出文件中被隐藏。 |

### OneRoster导出文件结构

导出的文件结构如下：

| 文件名 | 必含内容 |
|---|---|---|
| `orgs.csv` | 包含机构信息 |
| `academicSessions.csv` | 包含学期和学年信息 |
| `courses.csv` | 包含课程目录 |
| `classes.csv` | 包含课程部分信息 |
| `users.csv` | 包含学生和教师信息 |
| `enrollments.csv` | 包含学生注册信息 |
| `lineItems.csv` | （如果`--include-grades`选项被启用）包含评估结果信息 |
| `results.csv` | （如果`--include-grades`选项被启用）包含成绩记录 |

所有8个文件会被压缩成`oneroster_{term_name}_{date}.zip`格式的文件，并保存在`--output-dir`目录中。