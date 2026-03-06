functions/src/mcp/openclaw-skill/SKILL.md

# 资本设备平台（Capital Equipment Platform）

通过您的AI助手查找、预订和管理科研设备。您可以搜索200多个机构中500多个核心设施内的10,000多种仪器。

## 该功能的用途

- **搜索设备**：在任意地点查找显微镜、光谱仪、测序仪等设备。
- **检查设备可用性**：实时查询共享设备的预订情况。
- **预订设备**：直接通过助手预订设备使用时间。
- **提交服务请求**：描述设备需求并获取供应商的报价。
- **寻找合作者**：根据研究人员在特定技术领域的专长进行匹配。
- **追踪论文**：查找与特定设备相关的已发表研究论文。
- **兼容性检查**：验证设备组合是否适用于您的研究流程。
- **价格信息**：提供设备的公平市场价值、机构收费标准及折旧信息。
- **合规性确认**：确保设备跨机构使用符合知识产权协议和安全要求。

## 认证

该功能使用OAuth 2.1协议进行安全访问，遵循标准的MCP OAuth流程：

1. 首次使用时，系统会将您重定向到资本设备平台的登录页面。
2. 使用您的机构账户凭证（Google、Microsoft或电子邮件）进行登录。
3. 授权AI助手代表您执行操作。
4. OAuth令牌由系统自动管理，无需手动配置API密钥。

**所需权限范围**：`equipment:read`, `equipment:book`, `service-requests:write`, `profile:read`

**令牌有效期**：1小时（系统会自动刷新令牌）。

**请注意：无需在您的OpenClaw配置中存储任何凭证信息。**

## 设置

将MCP服务器添加到您的OpenClaw配置中：

```json
{
  "mcp": {
    "servers": [
      {
        "name": "capneteq-cesco345",
        "type": "sse",
        "url": "[https://capneteq.com/mcpServer/mcp](https://capneteq.com/mcpServer/mcp)"
      }
    ]
  }
}
```