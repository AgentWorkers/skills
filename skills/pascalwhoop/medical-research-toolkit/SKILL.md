---
name: medical-research-toolkit
description: 查询14个以上的生物医学数据库，以获取药物再利用、靶点发现、临床试验和文献研究的相关信息。通过统一的MCP接口，可以访问ChEMBL、PubMed、ClinicalTrials.gov、OpenTargets、OpenFDA、OMIM、Reactome、KEGG、UniProt等数据库。该工具适用于研究疾病靶点、查找已批准或正在研究的药物、搜索临床证据、发现基因关联以及分析化合物的生物活性数据。
---
# 医学研究工具包

通过一个统一的MCP接口，可以查询14个以上的生物医学数据库，以获取药物再利用、靶点发现、临床证据和文献研究的相关信息。

## ⚡ 30秒快速入门

```bash
# Find drugs for myasthenia gravis
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_find_drugs_by_indication","arguments":{"indication":"myasthenia gravis","max_results":10}},"id":1}'
```

**就这样！** 现在你已经获取到了针对该疾病的已批准药物和正在研究中的药物信息了。

---

## 快速操作指南

### 查找适用于某种疾病的药物

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_find_drugs_by_indication","arguments":{"indication":"myasthenia gravis","max_results":20}},"id":1}'
```

返回：已批准的药物以及处于研究阶段的药物（达到最高研究阶段的药物）。

### 查找疾病靶点

```bash
# First: Find disease ID
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"opentargets_search","arguments":{"query":"myasthenia gravis","entity_type":"disease"}},"id":1}'

# Returns: disease ID (e.g., EFO_0004991)
# Then: Get targets
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"opentargets_get_associations","arguments":{"disease_id":"EFO_0004991","size":20}},"id":2}'
```

返回：根据证据强度（0-1分）排序的顶级疾病靶点。

### 搜索文献

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"pubmed_search_articles","arguments":{"diseases":["myasthenia gravis"],"keywords":["immunotherapy"],"max_results":20}},"id":1}'
```

返回：关于重症肌无力的免疫疗法的PubMed文章。

### 查找正在进行的临床试验

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ctg_search_studies","arguments":{"condition":"myasthenia gravis","recruitment_status":"RECRUITING","max_results":20}},"id":1}'
```

返回：针对该疾病的正在招募参与者的临床试验。

### 检查药物安全性

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"openfda_search_adverse_events","arguments":{"drug_name":"eculizumab","limit":50}},"id":1}'
```

返回：FDA的不良事件报告——检查是否有严重后果、死亡或住院情况。

---

## 你将获得什么

**14个以上的集成数据库**

| 数据库 | 包含内容 | 用途 |
|----------|---------------|---------|
| **ChEMBL** | 200万种药物及其生物活性数据 | 查找已批准或正在研究中的药物 |
| **OpenTargets** | 疾病与靶点的关联信息及证据 | 识别治疗靶点 |
| **PubMed** | 3500多万篇论文及预印本 | 文献检索与验证 |
| **ClinicalTrials.gov** | 40多万项正在进行的临床试验 | 查找正在进行的研究 |
| **OpenFDA** | 药物不良事件信息及标签 | 安全性评估 |
| **OMIM** | 遗传疾病信息及基因与表型的关联 | 了解疾病遗传机制 |
| **Reactome** | 通路信息及蛋白质相互作用 | 理解生物学机制 |
| **UniProt** | 蛋白质序列及注释 | 蛋白质特性 |
| **KEGG** | 代谢途径及疾病相关通路 | 系统级视图 |
| **GWAS Catalog** | 基因与疾病之间的关联 | 变异体发现 |
| **Pathway Commons** | 集成通路数据 | 网络分析 |
| **MyGene.info** | 基因注释 | 基因标识 |
| **MyVariant.info** | 变异体效应 | 变异体解读 |
| + 更多 | | |

---

## 使用场景

### 🧬 药物再利用
为罕见/复杂疾病寻找非标准治疗药物：
1. 查找疾病靶点（OpenTargets）
2. 搜索针对这些基因的药物（ChEMBL）
3. 查看正在进行的临床试验（ClinicalTrials）
4. 验证药物安全性（OpenFDA, PubMed）

### 🔬 靶点发现
识别新的治疗靶点：
1. 查找疾病与基因的关联（OpenTargets, GWAS）
2. 了解通路背景（Reactome, KEGG）
3. 查阅文献（PubMed）
4. 查看蛋白质特性（UniProt）

### 📋 临床证据整理
为假设收集证据：
1. 搜索临床试验（ClinicalTrials.gov）
2. 查找相关文献（PubMed）
3. 查看FDA数据（OpenFDA）

### 📊 文献挖掘
系统地搜索生物医学研究：
1. PubMed：可按基因、疾病、药物或化学物质进行搜索
2. 预印本：bioRxiv, medRxiv
3. 通过关键词、日期或研究类型进行筛选

---

## API接口

**生产环境（无需设置）：**
```
https://mcp.cloud.curiloo.com/tools/unified/mcp
```

所有14个以上的数据库都通过一个统一的接口提供数据。

**本地运行：**
```bash
pip install medical-mcps
medical-mcps
# Available at: http://localhost:8000/tools/unified/mcp
```

---

## 完整参考资料

每个数据库的详细使用指南请参阅以下链接：

- **[PubMed使用指南](./references/pubmed.md)** — 文献搜索（基因、疾病、关键词）
- **[ClinicalTrials使用指南](./references/clinical-trials.md)** — 查找正在进行的临床试验
- **[ChEMBL使用指南](./references/chembl.md)** — 药物-靶点数据及生物活性信息
- **[OpenTargets使用指南](./references/opentargets.md)** — 疾病-靶点关联信息
- **[OpenFDA使用指南](./references/openfda.md)** — 药物安全性及不良事件信息
- **[OMIM使用指南](./references/omim.md)** — 遗传疾病信息（需要API密钥）
- **[其他API使用指南](./references/other-apis.md)** — Reactome, UniProt, KEGG等

---

## 工作流程示例

**完整的药物再利用流程：**

请参阅 [drug-repurposing-workflow.md](./scripts/drug-repurposing-workflow.md)，其中包含详细的8个步骤及对应的curl命令示例。

---

## API密钥

大多数API是**免费的，无需密钥**。部分API提供更高的请求速率限制，需要密钥：

| 数据库 | 是否需要密钥 | 原因 | 获取方式 |
|----------|------|-----|---------|
| ChEMBL | 不需要 | 公共数据 | （无需密钥） |
| OpenTargets | 不需要 | 公共数据 | （无需密钥） |
| PubMed | 不需要 | 公共数据 | （无需密钥） |
| ClinicalTrials | 不需要 | 公共数据 | （无需密钥） |
| **OMIM** | 需要 | 专有数据 | https://omim.org/api |
| OpenFDA | 可选 | 提供更高请求速率限制 | https://open.fda.gov |
| NCI Clinical Trials | 可选 | 提供更高请求速率限制 | https://clinicaltrialsapi.cancer.gov |

---

## 请求速率限制与缓存

- **生产环境接口**无需身份验证（公开访问）
- **请求速率限制**：每个数据库每天约1000次以上请求
- **缓存**：自动30天HTTP缓存（遵循RFC 9111标准）
- **费用**：所有数据库均为免费或仅限研究人员使用

---

## 常见问题

### 批量查询循环

```bash
# Search multiple targets
for gene in CHRNE RAPSN LRP4; do
  curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"chembl_find_drugs_by_target\",\"arguments\":{\"target_name\":\"$gene\",\"max_results\":10}},\"id\":1}"
  sleep 1  # Be nice to the API
done
```

### ID转换

需要在不同数据库之间转换ID吗？

```bash
curl -X POST https://mcp.cloud.curiloo.com/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"nodenorm_get_normalized_nodes","arguments":{"curie":"HGNC:11998"}},"id":1}'
```

返回：NCBI Gene、Uniprot、Ensembl、MyGene等数据库中的等效ID。

---

## 故障排除

**没有结果？**
- 尝试使用其他术语（如基因符号或蛋白质名称）
- 检查拼写是否正确
- 使用标准化的ID格式（如基因符号、疾病名称）
- 部分API使用特定的ID格式（如EFO或MONDO等）

**结果过多？**
- 添加筛选条件（如max_results、phase、recruitment_status）
- 使用`limit`或`size`参数来限制结果数量
- 结合使用多个数据库以缩小搜索范围

**API密钥错误？**
- OMIM需要API密钥——请从https://omim.org/api获取
- 其他数据库通常不需要密钥——但在达到请求速率限制时可能需要申请密钥

---

## 下一步

1. **选择一种使用场景**（如药物再利用、靶点发现等）
2. **阅读相关数据库的使用指南**
3. **复制上述快速操作指南中的示例代码**
4. **根据你的疾病/基因/药物需求自定义参数**
5. **逐步构建完整的研发工作流程**

---

## 资源

- **源代码**：https://github.com/pascalwhoop/medical-mcps
- **作者**：Pascal Brockmeyer (@pascalwhoop)
- **组织**：Every Cure (https://www.everycure.org)
- **许可证**：MIT许可

---

## 帮助资源

- 如果数据库无法使用，请参阅 [故障排除指南](#troubleshooting)
- 需要详细指南？请参阅 [完整参考资料](#complete-references)
- 需要工作流程示例？请参阅 [drug-repurposing-workflow.md](./scripts/drug-repurposing-workflow.md)
- 有关OpenClaw的使用说明，请参阅 [OPENCLAW-USAGE.md](./OPENCLAW-USAGE.md)