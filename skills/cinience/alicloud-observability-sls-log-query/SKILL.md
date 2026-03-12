---
name: alicloud-observability-sls-log-query
description: 使用 `query|analysis` 语法以及 Python SDK，在 Alibaba Cloud Log Service (SLS) 中查询和排查日志问题。该功能适用于基于时间范围的日志搜索、错误排查以及根本原因分析等工作流程。
version: 1.0.0
---
## 分类：服务  
### SLS 日志查询与故障排除  

使用 SLS 的查询/分析语法以及 Python SDK 进行日志搜索、过滤和数据分析。  

### 先决条件  
- 安装 SDK（建议使用虚拟环境以避免 PEP 668 的限制）：  
   ```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U aliyun-log-python-sdk
```  
- 配置环境变量：  
  - `ALIBABA_CLOUD_ACCESS_KEY_ID`  
  - `ALIBABA_CLOUD_ACCESS_KEY_SECRET`  
  - `SLS_ENDPOINT`（例如：`cn-hangzhou.log.aliyuncs.com`）  
  - `SLS_PROJECT`  
  - `SLS_LOGSTORE`（支持单个值或逗号分隔的值）  

### 查询组成  
- **查询子句**：用于过滤日志（例如：`status:500`）。  
- **分析子句**：用于统计聚合，格式为 `query|analysis`。  
- **示例**：`* | SELECT status, count(*) AS pv GROUP BY status`  

详细的语法请参阅 `references/query-syntax.md`。  

### 快速入门（Python SDK）  
```python
import os
import time
from aliyun.log import LogClient, GetLogsRequest

client = LogClient(
    os.environ["SLS_ENDPOINT"],
    os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
    os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
)

project = os.environ["SLS_PROJECT"]
logstore = os.environ["SLS_LOGSTORE"]

query = "status:500"
start_time = int(time.time()) - 15 * 60
end_time = int(time.time())

request = GetLogsRequest(project, logstore, start_time, end_time, query=query)
response = client.get_logs(request)
for log in response.get_logs():
    print(log.contents)
```  

### 脚本快速入门  
```bash
python skills/observability/sls/alicloud-observability-sls-log-query/scripts/query_logs.py \
  --query "status:500" \
  --last-minutes 15
```  

**可选参数**：`--project`、`--logstore`（可重复使用或以逗号分隔的值）、`--endpoint`、`--start`、`--end`、`--last-minutes`、`--limit`、`--parallel`。  

### 故障排除脚本  
```bash
python skills/observability/sls/alicloud-observability-sls-log-query/scripts/troubleshoot.py \
  --group-field status \
  --last-minutes 30 \
  --limit 20
```  

**可选参数**：`--error-query`、`--group-field`、`--limit`、`--logstore`（可重复使用或以逗号分隔的值）、`--parallel`，以及上述的时间范围参数。  

### 工作流程  
1. 确保已启用 Logstore 的索引功能（没有索引时，查询/分析操作将失败）。  
2. 编写查询子句，并根据需要添加分析子句。  
3. 使用 SDK 或脚本执行查询并检查结果。  
4. 使用 `limit` 参数控制返回的行数；根据需要缩小时间范围。  

### 验证  
```bash
mkdir -p output/alicloud-observability-sls-log-query
for f in skills/observability/sls/alicloud-observability-sls-log-query/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-observability-sls-log-query/validate.txt
```  
- 如果命令成功执行且 `output/alicloud-observability-sls-log-query/validate.txt` 文件生成，则验证通过。  

### 输出与证据  
- 将输出结果、命令输出以及 API 响应摘要保存在 `output/alicloud-observability-sls-log-query/` 目录下。  
- 在证据文件中包含关键参数（区域/资源 ID/时间范围），以便重现问题。  

### 参考资料  
- 语法与示例：`references/query-syntax.md`  
- Python SDK 的初始化与查询方法：`references/python-sdk.md`  
- 故障排除模板：`references/templates.md`  
- 源代码列表：`references/sources.md`