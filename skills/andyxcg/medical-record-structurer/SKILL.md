---
name: medical-record-structurer
description: >
  **医疗记录结构化与标准化工具**  
  该工具可将医生口述或手写的医疗记录转换为标准化的电子医疗记录（EMR）。支持语音/文本输入、自动字段识别以及结构化输出功能，适用于处理医疗记录、临床笔记、患者病历，或将非结构化的医疗数据转换为标准化格式。同时具备与 skillpay.me 的支付集成功能，支持按使用量计费的商业模式。
version: 1.0.4
---
# 医疗记录整理工具

> **版本**: 1.0.4  
> **类别**: 医疗保健  
> **计费方式**: SkillPay（每次调用收费0.001 USDT）  
> **免费试用**: 每位新用户可享受10次免费调用

这是一款专业的医疗记录处理工具，可将非结构化的医疗笔记（语音或文本）转换为标准化的电子医疗记录。

## 主要功能

1. **语音/文本输入处理**：支持医生口述或手写笔记的输入。  
2. **基于AI的字段提取**：自动识别并提取医疗相关字段。  
3. **标准化电子病历输出**：生成结构化的电子病历。  
4. **支付集成**：通过skillpay.me实现计费（每次使用收费0.001 USDT）。  
5. **免费试用**：每位新用户可享受10次免费调用。

## 免费试用

每位用户在开始计费前可享受**10次免费调用**。试用期间：  
- 无需支付费用  
- 可使用所有功能  
- 试用状态会通过API响应返回。  

**免费试用结束后，将开始正常计费。**

## 快速入门

### 处理医疗记录：

（具体操作步骤请参见**```python
{
    "success": True,
    "trial_mode": True,      # Currently in free trial
    "trial_remaining": 5,    # 5 free calls left
    "balance": None,         # No balance needed in trial
    "structured_record": {...}
}
```**）

### API使用方法：

（具体API调用方式请参见**```bash
# Set API key via environment variable (only needed after trial)
export SKILLPAY_API_KEY="your-api-key"

# Run with user_id for billing/trial tracking
python scripts/process_record.py \
  --input "患者张三，男，45岁，主诉头痛3天..." \
  --user-id "user_123"
```**）

## 环境变量

本工具需要以下环境变量：

### 必需环境变量（试用结束后设置）

| 变量 | 说明 | 是否必需 | 示例值 |
|--------|---------|---------|---------|
| `SKILLPAY_API_KEY` | SkillPay的API密钥（用于计费） | 试用结束后设置 | `skp_abc123...` |
| `SKILLPAY_SKILL_ID` | SkillPay仪表板中的技能ID | 试用结束后设置 | `skill_def456...` |

### 可选环境变量

| 变量 | 说明 | 默认值 | |
|--------|---------|---------|---|
| `OCR_API_KEY` | OCR服务的API密钥（用于图像处理） | - | |
| `OCR_PROVIDER` | OCR服务提供商（如google、azure、aws、tesseract） | `google` | |
| `STT_API_KEY` | 语音转文本服务的API密钥 | - | |
| `STT_PROVIDER` | 语音转文本服务提供商（如google、azure、aws、whisper） | `whisper` | |
| `PHI_ENCRYPTION_KEY` | 用于保护患者隐私信息的加密密钥 | - | |
| `DATA_RETENTION_days` | 数据保留天数 | `30` | |
| `AUDIT_LOGGING_ENABLED` | 是否启用审计日志记录 | `true` | |

请参阅`.env.example`文件以获取完整的环境变量列表。

## 配置

本工具使用SkillPay进行计费：  
- 提供商：skillpay.me  
- 计费价格：每次请求0.001 USDT  
- 使用的区块链：BNB Chain  
- 免费试用次数：每位用户10次调用  
- API密钥：通过`SKILLPAY_API_KEY`环境变量设置  
- 技能ID：通过`SKILLPAY_SKILL_ID`环境变量设置  

## 输出格式

结构化的电子病历包含以下内容：  
- 患者基本信息（姓名、年龄、性别）  
- 主诉  
- 现病史  
- 过往病史  
- 体格检查结果  
- 诊断结果  
- 治疗方案  
- 用药信息  
- 随访建议  

### 响应格式

（响应数据结构请参见**```python
{
    "success": True,
    "trial_mode": False,        # True during free trial
    "trial_remaining": 0,       # Remaining free calls
    "balance": 95.5,            # User balance (None during trial)
    "structured_record": {
        "emr_version": "1.0",
        "record_id": "EMR_20240306120000",
        "record_date": "2024-03-06T12:00:00",
        "patient_demographics": {...},
        "clinical_information": {...},
        "assessment_and_plan": {...},
        "metadata": {...}
    }
}
```**）

## 患者隐私保护

本工具处理受保护的医疗信息（PHI），并采取以下安全措施：  

### 数据保护  
- **加密**：所有数据在存储和传输过程中均经过加密。  
- **访问控制**：所有操作均需用户身份验证。  
- **审计日志记录**：所有对患者隐私信息的访问操作都会被记录。  
- **数据最小化**：仅提取和存储必要的字段。  

### 合规性  
- **HIPAA合规性**：遵循HIPAA安全标准设计。  
- **GDPR合规性**：支持数据删除请求。  
- **数据保留政策**：可配置数据保留期限（默认为30天）。  

### 最佳实践  
1. 对敏感配置信息始终使用环境变量进行管理。  
2. 在生产环境中启用审计日志记录。  
3. 实施适当的访问控制机制。  
4. 建议定期进行安全审查。  

## OCR/STT服务支持  

本工具支持外部OCR和STT服务：  

### OCR（光学字符识别）  
- 用于处理手写或扫描的医疗记录：  
  - Google Vision API  
  - Azure Computer Vision  
  - AWS Textract  
  - Tesseract（开源工具）  

### STT（语音转文本）  
- 用于处理语音录制的医疗笔记：  
  - Google Speech-to-Text  
  - Azure Speech Services  
  - AWS Transcribe  
  - OpenAI Whisper（开源工具）  

请在`.env`文件中配置相应的API密钥以启用这些功能。  

## 参考资料  
- 详细字段规范：[references/emr-schema.md](references/emr-schema.md)  
- 计费API详情：[references/skillpay-api.md](references/skillpay-api.md)  
- 完整文档：[README.md](README.md)