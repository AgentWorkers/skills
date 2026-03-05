---
name: medical-record-structurer
description: >
  **医疗记录结构化与标准化工具**  
  该工具可将医生口述或手写的医疗记录转换为标准化的电子医疗记录（EMR）。支持语音/文本输入、自动字段识别以及结构化输出功能，适用于处理医疗记录、临床笔记、患者病史，或将非结构化的医疗数据转换为标准化格式。同时具备 skillpay.me 支付集成功能，支持按使用量计费的商业模式。
version: 1.0.3
---
# 医疗记录整理工具

这是一个专业的医疗记录处理工具，可将非结构化的医疗记录（语音或文本形式）转换为标准化的电子医疗记录。

## 主要功能

1. **语音/文本输入处理**：支持接收医生的口头描述或手写笔记。
2. **基于AI的字段提取**：自动识别并提取医疗相关字段。
3. **标准化电子病历输出**：生成结构化的电子医疗记录。
4. **支付集成**：支持与skillpay.me平台集成以实现盈利（每次使用费用为0.001 USDT）。

## 快速入门

### 处理医疗记录：

```python
from scripts.process_record import process_medical_record
import os

# Set API key via environment variable
os.environ["SKILLPAY_API_KEY"] = "your-api-key"

# Process with user_id for billing
result = process_medical_record(
    input_text="患者张三，男，45岁，主诉头痛3天...",
    user_id="user_123"
)

# Check result
if result["success"]:
    print("结构化病历:", result["structured_record"])
    print("剩余余额:", result["balance"])
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### API使用方法：

```bash
# Set API key via environment variable
export SKILLPAY_API_KEY="your-api-key"

# Run with user_id for billing
python scripts/process_record.py \
  --input "患者张三，男，45岁，主诉头痛3天..." \
  --user-id "user_123"
```

## 配置信息

该工具使用skillpay.me平台进行计费集成：
- 提供商：skillpay.me
- 费用：每次请求0.001 USDT
- 区块链：BNB Chain
- API密钥：通过`SKILLPAY_API_KEY`环境变量设置
- 技能ID：通过`SKILLPAY_SKILL_ID`环境变量设置

## 输出格式

结构化的电子医疗记录包含以下内容：
- 患者基本信息（姓名、年龄、性别）
- 主诉
- 现病史
- 过往病史
- 体格检查结果
- 诊断结果
- 治疗方案
- 用药信息
- 随访建议

## 参考资料

- 详细字段规范：请参阅[references/emr-schema.md](references/emr-schema.md)
- 支付API详细信息：请参阅[references/skillpay-api.md](references/skillpay-api.md)