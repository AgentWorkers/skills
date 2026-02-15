---
name: telnyx-seti-python
description: >-
  Access SETI (Space Exploration Telecommunications Infrastructure) APIs. This
  skill provides Python SDK examples.
metadata:
  author: telnyx
  product: seti
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Seti - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取黑盒测试结果

返回各种黑盒测试的结果

`GET /seti/black_box_test_results`

```python
response = client.seti.retrieve_black_box_test_results()
print(response.data)
```
```