---
name: telnyx-seti-go
description: >-
  Access SETI (Space Exploration Telecommunications Infrastructure) APIs. This
  skill provides Go SDK examples.
metadata:
  author: telnyx
  product: seti
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Seti - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取黑盒测试结果

返回各种黑盒测试的结果

`GET /seti/black_box_test_results`

```go
	response, err := client.Seti.GetBlackBoxTestResults(context.TODO(), telnyx.SetiGetBlackBoxTestResultsParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```
```