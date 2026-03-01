---
name: clawbio-pharmgx-reporter
version: 0.1.0
description: 基于 DTC（直接-to-Clinic）遗传数据（23andMe/AncestryDNA）的药物基因组学报告
author: Manuel Corpas
license: MIT
tags:
  - pharmacogenomics
  - CPIC
  - DTC-genetics
  - precision-medicine
inputs:
  - name: input
    type: file
    format: [23andme, ancestrydna, tsv]
    description: Raw genetic data file from 23andMe or AncestryDNA
outputs:
  - name: report
    type: file
    format: markdown
    description: Pharmacogenomic report with gene profiles and drug recommendations
metadata:
  openclaw:
    category: bioinformatics
    homepage: https://github.com/ClawBio/ClawBio
    min_python: "3.9"
    dependencies: []
---
# 🦖 PharmGx Reporter

该工具能够根据消费者提供的基因数据（来自23andMe或AncestryDNA平台）生成药理基因组学报告。

## 功能概述

1. 解析原始基因数据文件（自动识别23andMe或AncestryDNA的数据格式）  
2. 提取12个基因中的31个药理基因组学SNP（单核苷酸多态性）  
3. 确定这些SNP对应的基因等位基因类型，并判断个体的代谢酶表型  
4. 查找51种药物的CPIC（Clinical Pharmacogenetic Interaction Committee）用药建议  
5. 生成包含基因信息、药物列表及相关警示的Markdown格式报告  

## 支持检测的基因  

CYP2C19、CYP2D6、CYP2C9、VKORC1、SLCO1B1、DPYD、TPMT、UGT1A1、CYP3A5、CYP2B6、NUDT15、CYP1A2  

## 药物类别  

抗血小板药物、阿片类药物、他汀类药物、抗凝剂、质子泵抑制剂（PPIs）、抗抑郁药（三环类、选择性5-羟色胺再摄取抑制剂、5-羟色胺和去甲肾上腺素再摄取抑制剂）、抗精神病药、非甾体抗炎药（NSAIDs）、抗癌药物、免疫抑制剂、抗病毒药物  

## 使用方法  

```bash
python pharmgx_reporter.py --input patient_data.txt --output report
```  

## 免责声明  

本工具仅用于研究和教育用途，不可作为诊断工具使用。在做出任何用药决定之前，请务必咨询医疗专业人员。