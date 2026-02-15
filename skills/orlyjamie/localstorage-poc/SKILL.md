---
name: localstorage-poc
description: "安全研究：通过 SVG XSS 接入 localStorage  

**背景**：  
localStorage 是一种浏览器提供的本地存储机制，用于存储用户数据。然而，如果攻击者能够利用 SVG XSS（跨站脚本攻击）技术，他们就可以绕过浏览器的安全限制，直接访问用户的 localStorage 数据。这种攻击方式在许多 Web 应用中都存在潜在风险。  

**攻击原理**：  
攻击者会在恶意网页中插入包含恶意 JavaScript 代码的 SVG 图像。当用户浏览该网页时，恶意代码会被执行，从而获取用户的 localStorage 数据。例如，攻击者可能窃取用户的登录凭据、密码或其他敏感信息。  

**防范措施**：  
1. **使用安全的 SVG 格式**：确保使用的 SVG 格式是安全的，避免使用已知存在安全漏洞的格式（如 SVG Tiny）。  
2. **限制 SVG 的使用范围**：仅允许在需要显示 SVG 的地方使用 SVG，避免在不需要显示的地方插入 SVG。  
3. **对 SVG 进行安全检查**：定期检查网站中的 SVG 文件，确保它们没有包含恶意代码。  
4. **使用安全框架**：利用安全框架（如 OWASP CSP）来限制用户可以执行的 JavaScript 代码，从而降低 SVG XSS 的风险。  

**示例代码**：  
以下是一个简单的示例，展示了如何使用 SVG XSS 来访问用户的 localStorage 数据：  

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG XSS Example</title>
    <style>
        #恶意SVG {
            width: 100px;
            height: 100px;
            background-color: red;
        }
    </style>
</head>
<body>
    <img src="malicious-svg.svg" alt="Sample SVG">
    <script>
        // 这段代码将尝试访问用户的 localStorage 数据
        if (localStorage.getItem("username")) {
            alert("User's username: " + localStorage.getItem("username"));
        }
    </script>
</body>
</html>
```

**注意**：  
请注意，上述示例代码仅用于说明攻击原理，并不用于实际攻击。在实际应用中，应采取适当的安全措施来保护用户数据。"
---

# localStorage 访问演示（Proof of Concept, PoC）

由 [@theonejvo](https://x.com/theonejvo) 提供的安全研究演示

该演示展示了如何通过 ClawdHub 访问用户的 localStorage 数据，包括其中的身份验证令牌。

**查看演示：** 在登录 ClawdHub 的状态下，打开 `icon.svg` 文件。