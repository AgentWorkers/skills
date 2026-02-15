# 个人基因组分析技能 v4.2.0

提供全面的本地DNA分析服务，涵盖**30个类别**中的**1600多个基因标记**。专为AI代理设计的、以隐私保护为核心的基因分析工具。

## 快速入门

```bash
python comprehensive_analysis.py /path/to/dna_file.txt
```

## 触发条件

当用户提及以下内容时，激活此技能：
- DNA分析、基因分析、基因组分析
- 23andMe、AncestryDNA、MyHeritage的检测结果
- 药物基因组学、药物-基因相互作用
- 药物相互作用、药物安全性
- 基因风险、疾病风险、健康风险
- 携带者状态、携带者检测
- VCF文件分析
- APOE、MTHFR、CYP2D6、BRCA等基因名称
- 多基因风险评分
- 单倍群、母系血统、父系血统
- 祖先构成、种族
- 遗传性癌症、林奇综合征
- 自身免疫遗传学、HLA、乳糜泻
- 疼痛敏感性、阿片类药物反应
- 睡眠优化、生物钟类型、咖啡因代谢
- 饮食遗传学、乳糖不耐受、乳糜泻
- 运动遗传学、运动表现
- 紫外线敏感性、皮肤类型、黑色素瘤风险
- 端粒长度、长寿遗传学

## 支持的文件格式

- 23andMe、AncestryDNA、MyHeritage、FTDNA的检测结果文件
- VCF文件（全基因组/外显子组，格式为.vcf或.vcf.gz）
- 任何以制表符分隔的rsid格式文件

## 输出路径

`~/dna-analysis/reports/`

- `agent_summary.json` - 为AI代理优化处理后的数据，按优先级排序
- `full_analysis.json` - 完整分析数据
- `report.txt` - 人类可读的文本文件
- `genetic_report.pdf` - 专业的PDF报告

## v4.0的新功能

### 单倍群分析
- 线粒体DNA（mtDNA） - 母系血统
- Y染色体 - 父系血统（仅限男性）
- 迁移历史信息
- 遵循PhyloTree/ISOGG标准进行解析

### 祖先构成分析
- 人群比较（欧洲人、非洲人、东亚人、南亚人、美洲原住民）
- 混合血统检测
- 提供有关祖先的信息的基因标记

### 遗传性癌症检测
- BRCA1/BRCA2基因的全面检测
- 林奇综合征（MLH1、MSH2、MSH6、PMS2）
- 其他相关基因（APC、TP53、CHEK2、PALB2、ATM）
- 按ACMG标准进行分类

### 自身免疫相关HLA检测
- 乳糜泻（DQ2/DQ8） - 阴性结果可排除相关风险
- 1型糖尿病
- 强直性脊柱炎（HLA-B27）
- 类风湿性关节炎、狼疮、多发性硬化症

### 疼痛敏感性分析
- COMT Val158Met基因变异
- OPRM1阿片受体基因
- SCN9A基因与疼痛感知的关系
- TRPV1基因与辣椒素敏感性的关系
- 偏头痛易感性分析

### PDF报告
- 专业格式，可供医生分享
- 包含执行摘要和详细分析结果
- 报告中包含免责声明

## v4.1.0的新功能

### 药物相互作用检测
```python
from markers.medication_interactions import check_medication_interactions

result = check_medication_interactions(
    medications=["warfarin", "clopidogrel", "omeprazole"],
    genotypes=user_genotypes
)
# Returns critical/serious/moderate interactions with alternatives
```
- 支持品牌名或通用名
- 集成了CPIC（临床药物相互作用委员会）的指导原则
- 报告中包含PubMed文献引用
- 显示FDA警告信息

### 睡眠优化分析
```python
from markers.sleep_optimization import generate_sleep_profile

profile = generate_sleep_profile(genotypes)
# Returns ideal wake/sleep times, coffee cutoff, etc.
```
- 生物钟类型（早起型/晚睡型）
- 咖啡因代谢速度
- 个性化的时间管理建议

### 饮食相互作用分析
```python
from markers.dietary_interactions import analyze_dietary_interactions

diet = analyze_dietary_interactions(genotypes)
# Returns food-specific guidance
```
- 咖啡因、酒精、饱和脂肪、乳糖、麸质的相互作用
- 根据APOE基因类型提供饮食建议
- 对苦味的感知能力

### 运动表现分析
```python
from markers.athletic_profile import calculate_athletic_profile

profile = calculate_athletic_profile(genotypes)
# Returns power/endurance type, recovery profile, injury risk
```
- 评估运动适应性
- 提供训练建议
- 提供预防受伤的指导

### 紫外线敏感性分析
```python
from markers.uv_sensitivity import generate_uv_sensitivity_report

uv = generate_uv_sensitivity_report(genotypes)
# Returns skin type, SPF recommendation, melanoma risk
```
- 估算Fitzpatrick皮肤类型
- 评估维生素D合成能力
- 分析黑色素瘤风险因素

### 自然语言解释
```python
from markers.explanations import generate_plain_english_explanation

explanation = generate_plain_english_explanation(
    rsid="rs3892097", gene="CYP2D6", genotype="GA",
    trait="Drug metabolism", finding="Poor metabolizer carrier"
)
```
- 用通俗易懂的语言解释分析结果
- 标注研究中的关键变异
- 提供PubMed文献链接

### 端粒与长寿分析
```python
from markers.advanced_genetics import estimate_telomere_length

telomere = estimate_telomere_length(genotypes)
# Returns relative estimate with appropriate caveats
```
- TERT、TERC、OBFC1基因变异与长寿的关系
- FOXO3、APOE基因与长寿的关系

### 数据质量控制
- 分析数据的质量和准确性
- 提供置信度评分
- 对数据质量存在问题的情况发出警告

### 数据导出格式
- 可导出用于遗传咨询的格式
- 兼容Apple Health应用
- 提供API接口（JSON格式）
- 支持与其他系统集成

## 基因标记类别（共21个）

1. **药物基因组学**（159个标记） - 药物代谢相关
2. **多基因风险评分**（277个标记） - 疾病风险相关
3. **携带者状态**（181个标记） - 识别隐性携带者
4. **健康风险**（233个标记） - 疾病易感性相关
5. **表型特征**（163个标记） - 与身体/行为相关的特征
6. **单倍群**（44个标记） - 血统相关
7. **祖先信息**（124个标记） - 与祖先相关的信息
8. **遗传性癌症**（41个标记） - 如BRCA、林奇综合征等
9. **自身免疫相关HLA**（31个标记） - 与自身免疫相关的HLA基因
10. **疼痛敏感性**（20个标记） - 与疼痛和阿片类药物反应相关的基因
11. **罕见疾病**（29个标记） - 罕见遗传病相关
12. **心理健康**（25个标记） - 与精神健康相关的基因
13. **皮肤科相关**（37个标记） - 与皮肤和头发相关的基因
14. **视觉与听觉**（33个标记） - 与感官相关的基因
15. **生育能力**（31个标记） - 与生殖健康相关的基因
16. **营养学**（34个标记） - 与营养相关的基因
17. **健康与健身**（30个标记） - 与运动表现相关的基因
18. **神经遗传学**（28个标记） - 与认知和行为相关的基因
19. **长寿**（30个标记） - 与衰老相关的基因
20. **免疫系统**（43个标记） - 与免疫系统相关的基因
21. **祖先信息**（24个标记） - 与种族混合相关的基因

## 代理集成

`agent_summary.json`文件包含以下信息：

```json
{
  "critical_alerts": [],
  "high_priority": [],
  "medium_priority": [],
  "pharmacogenomics_alerts": [],
  "apoe_status": {},
  "polygenic_risk_scores": {},
  "haplogroups": {
    "mtDNA": {"haplogroup": "H", "lineage": "maternal"},
    "Y_DNA": {"haplogroup": "R1b", "lineage": "paternal"}
  },
  "ancestry": {
    "composition": {},
    "admixture": {}
  },
  "hereditary_cancer": {},
  "autoimmune_risk": {},
  "pain_sensitivity": {},
  "lifestyle_recommendations": {
    "diet": [],
    "exercise": [],
    "supplements": [],
    "avoid": []
  },
  "drug_interaction_matrix": {},
  "data_quality": {}
}
```

## 重要提示（会自动提醒用户）

### 药物基因组学相关结果
- **DPYD**基因变异 - 与5-FU或卡培他滨的致命毒性风险相关
- **HLA-B*5701** - 与阿巴卡韦过敏反应相关
- **HLA-B*1502** - 与卡马西平引起的严重皮疹（某些人群）
- **MT-RNR1** - 与氨基糖苷类药物引起的耳聋风险相关

### 遗传性癌症相关结果
- **BRCA1/BRCA2**基因突变 - 与乳腺癌/卵巢癌相关
- **林奇综合征**相关基因 - 与结直肠癌/子宫内膜癌相关
- **TP53**基因突变 - 与李-弗劳梅尼综合征（多发性癌症）相关

### 疾病风险相关结果
- **APOE ε4/ε4**基因型 - 阿尔茨海默病风险增加约12倍
- **Factor V Leiden**基因突变 - 增加血栓风险，影响避孕效果
- **HLA-B27**基因 - 与强直性脊柱炎风险相关

### 携带者状态相关结果
- **CFTR**基因突变 - 与囊性纤维化相关（每25个欧洲人中就有1人携带）
- **HBB**基因突变 - 与镰状细胞贫血相关（每12个非裔美国人中就有1人携带）
- **HEXA**基因突变 - 与泰-萨克斯病相关（每30个阿什肯纳兹犹太人中就有1人携带）

## 使用示例

### 基本分析
```python
from comprehensive_analysis import main
main()  # Uses command line args
```

### 单倍群分析
```python
from markers.haplogroups import analyze_haplogroups
result = analyze_haplogroups(genotypes)
print(result["mtDNA"]["haplogroup"])  # e.g., "H"
```

### 祖先分析
```python
from markers.ancestry_composition import get_ancestry_summary
ancestry = get_ancestry_summary(genotypes)
```

### 癌症相关检测
```python
from markers.cancer_panel import analyze_cancer_panel
cancer = analyze_cancer_panel(genotypes)
if cancer["pathogenic_variants"]:
    print("ALERT: Pathogenic variants detected")
```

### 生成PDF报告
```python
from pdf_report import generate_pdf_report
pdf_path = generate_pdf_report(analysis_results)
```

### 导出数据给遗传咨询师
```python
from exports import generate_genetic_counselor_export
clinical = generate_genetic_counselor_export(results, "clinical.json")
```

## 隐私保护

- 所有分析都在本地完成
- 不会发送任何网络请求
- 数据不会离开设备

## 限制因素

- 消费者使用的基因检测芯片可能无法检测到罕见基因变异（约占基因组的0.1%）
- 分析结果为概率性结果，而非确定性结论
- 本工具不能替代医学诊断
- 大多数健康问题受遗传因素影响的比例在50%-80%之间
- 建议用户咨询医疗专业人士以获取医学建议
- 即使检测结果为阴性，也不能完全排除遗传性癌症的风险
- 未经全基因组测序（WGS），单倍群的解析精度有限

## 何时建议寻求遗传咨询

- 发现任何致病性遗传性癌症变异
- 携带APOE ε4/ε4基因型
- 出现多个重要的药物基因组学相关结果
- 携带可能影响生育的遗传基因
- 出现与自身免疫相关的高风险HLA类型且伴有症状
- 分析结果对用户造成严重困扰的情况