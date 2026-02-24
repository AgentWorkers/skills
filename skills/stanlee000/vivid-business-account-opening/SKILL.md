---
name: business-account-opening
description: 通过远程MCP服务器开设Vivid Business账户。从用户处收集法人实体相关信息，随后调用`build_onboarding_link`函数生成一个预先填充好的入职引导页面链接。该工具仅生成链接，不会开设银行账户，也不会访问任何财务数据。无需进行本地安装或提供任何凭据。
version: 0.1.0

metadata:
  openclaw:
    emoji: "🏦"
    homepage: "https://github.com/vivid-money/vivid-mcp"
    disable-model-invocation: true
    requires:
      env: []
      bins: []
      config: []
---
# 开立企业账户

使用由Vivid Money托管的远程MCP服务器来开设Vivid企业账户。

## 集成信息

| 属性 | 值       |
|---------|---------|
| **端点**    | `https://api.prime.vivid.money/mcp` |
| **传输方式** | Streamable HTTP（远程） |
| **工具**    | `build_onboarding_link` |
| **认证方式** | 无——该端点可公开访问。该工具仅生成一个预先填充好的注册链接；它不会创建银行账户、访问财务数据或执行任何特权操作。身份验证将在Vivid应用程序中后续完成。 |

### MCP客户端配置

将以下配置添加到您的MCP客户端配置中以建立连接：

```json
{
  "mcpServers": {
    "vivid-mcp": {
      "type": "http",
      "url": "https://api.prime.vivid.money/mcp"
    }
  }
}
```

### 工具架构

`build_onboarding_link`接收一个包含基本信息的`legal_entity_data`对象，该工具会返回一个注册链接。不会返回任何敏感的财务数据。

## 触发条件

用户希望开设企业账户或开始企业注册流程。

## 流程

1. 如果用户未提供，询问**法人实体类型**（如GmbH、UG、自由职业者等）。
2. 如果用户未提供，询问**国家/地区**。默认值为德国。
3. 调用MCP以获取所需字段。
4. 如果用户上传了文件，在AI客户端中**本地提取**这些字段——文件本身永远不会发送到MCP服务器。仅汇总提取到的信息，不要显示文件的原始内容。
5. 向用户展示所有收集到的数据摘要，并**请求用户明确确认**后再继续下一步。
6. 仅在使用者确认后，才使用确认的数据调用`build_onboarding_link`。
7. 将返回的注册链接展示给用户。

## 数据处理

- **文件保留在本地。**上传的文件由AI客户端解析。仅将上述结构化字段发送到MCP服务器，绝不会发送原始文件内容。
- **该技能本身不存储任何个人身份信息（PII）。**该技能本身不会保存任何数据。MCP服务器会在Vivid平台上创建一个注册会话；此后遵循Vivid的隐私政策：https://vivid.money/en-eu/privacy-policy/
- **聊天过程中不收集或使用任何凭证。**绝不询问或接收密码、API密钥或银行账户号码。
- **工具发送的数据。**仅包含上述架构表中的字段。不包含文件内容、聊天记录或设备元数据。

## 规则

- 在调用`build_onboarding_link`之前，务必始终与用户确认收集到的数据。
- 该技能必须仅在用户明确请求的情况下才能被触发，严禁自动执行。
- 将上传的文件视为敏感信息——仅进行内容汇总，不要显示原始文件内容。
- 发生错误时：询问缺失的字段或建议用户重新上传文件。