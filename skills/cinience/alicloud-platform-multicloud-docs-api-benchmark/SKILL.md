---
name: alicloud-platform-multicloud-docs-api-benchmark
description: 对比分析阿里巴巴云（Alibaba Cloud）、亚马逊网络服务（AWS）、微软Azure、谷歌云平台（GCP）、腾讯云（Tencent Cloud）、Volcano Engine以及华为云（Huawei Cloud）上类似产品的文档和API文档。根据给定的产品关键词，自动检索最新的官方文档和API链接，持续评估文档的质量，并输出详细的、按优先级排序的改进建议。
version: 1.0.0
---
# 多云产品文档/API基准测试

当用户需要对类似产品的跨云文档/API进行比较时，请使用此技能。

## 支持的云服务

- 阿里云（Alibaba Cloud）
- AWS
- Azure
- GCP
- 腾讯云（Tencent Cloud）
- Volcano Engine
- 华为云（Huawei Cloud）

## 数据来源策略

- `L0`（最高级别）：用户指定的官方链接（通过 `--<provider>-links` 参数提供）
- `L1`：机器可读取的官方元数据/来源
  - GCP：Discovery API
  - AWS：API Models 仓库
  - Azure：REST API Specs 仓库
- `L2`：基于官方域名的网页发现方式（作为备用方案）
- `L3`：发现信息不足（置信度较低）

## 工作流程

运行基准测试脚本：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "<product keyword>"
```

示例：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "serverless"
```

LLM平台基准测试示例（Bailian/Bedrock/Azure OpenAI/Vertex AI/Hunyuan/Ark/Pangu）：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "Bailian" --preset "llm-platform"
```

如果省略了 `--preset` 参数，脚本会尝试根据关键词自动匹配预设配置。

评分权重可以通过配置文件（`references/scoring.json`）进行更改：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py --product "Bailian" --preset "llm-platform" --scoring-profile "llm-platform"
```

## 可选：手动指定权威链接

自动发现可能会遗漏某些页面。为了进行更严格的比较，可以手动提供官方链接：

```bash
python skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/benchmark_multicloud_docs_api.py \
  --product "object storage" \
  --aws-links "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html" \
  --azure-links "https://learn.microsoft.com/azure/storage/blobs/"
```

可使用的手动参数：

- `--alicloud-links`  
- `--aws-links`  
- `--azure-links`  
- `--gcp-links`  
- `--tencent-links`  
- `--volcengine-links`  
- `--huawei-links`  

每个参数接受以逗号分隔的URL列表。

## 输出策略

所有测试结果文件应保存在以下目录中：

`output/alicloud-platform-multicloud-docs-api-benchmark/`

每次运行测试后，会生成以下文件：

- `benchmark_evidence.json`  
- `benchmark_report.md`

## 报告指南

在向用户提供报告时，请：

1) 显示所有云服务的评分排名。
2) 突出主要的差距（P0/P1/P2）以及具体的改进措施。
3) 如果发现信息的置信度较低，请让用户提供官方链接并重新运行测试。

## 验证

```bash
mkdir -p output/alicloud-platform-multicloud-docs-api-benchmark
for f in skills/platform/docs/alicloud-platform-multicloud-docs-api-benchmark/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-platform-multicloud-docs-api-benchmark/validate.txt
```

验证条件：脚本执行成功（退出代码为0），并且会生成 `output/alicloud-platform-multicloud-docs-api-benchmark/validate.txt` 文件。

## 输出结果与证据

- 将所有测试结果文件、命令输出以及API响应摘要保存在 `output/alicloud-platform-multicloud-docs-api-benchmark/` 目录下。
- 在证据文件中包含关键参数（区域、资源ID、时间范围），以便后续复现测试。

## 先决条件

- 在执行测试前，请配置具有最小权限的阿里云访问凭据。
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。
- 如果区域信息不明确，请在运行测试前询问用户。

## 参考资料

- 评估标准：`references/review-rubric.md`