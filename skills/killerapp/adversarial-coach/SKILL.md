---
name: adversarial-coach
description: 基于Block的g3辩证自动编码研究的对抗性实现审查方法。该方法用于以全新的客观性来验证实现是否满足所有需求。
---

# /coach - 对抗性实现审查

## 使用方法

```
/coach [requirements-file]
```

- `/coach`：从代码上下文中推断出需求
- `/coach requirements.md`：根据具体文件验证实现是否满足需求

## 实施者（玩家）与审查者（教练）的互动循环

你负责协调实施者（玩家）与审查者（教练）之间的这种互动过程：

1. 你（玩家）实现代码功能。
2. `/coach` 会启动对抗性审查，并独立评估代码是否符合需求。
3. 审查者会返回 `IMPLEMENTATION_APPROVED` 或具体的修改建议。
4. 根据反馈进行修改，直到代码获得批准。

## 审查流程

### 第一步：识别需求

按顺序检查以下内容：
- 是否有明确的需求文件或相关问题/工单被提及；
- `requirements.md`、`REQUIREMENTS.md`、`SPEC.md`、`TODO.md` 文件；
- 交流过程中的信息；询问开发者是否还有其他遗漏的需求。

### 第二步：对抗性审查

以 **全新的、客观的态度** 进行审查——摒弃先前的认知，避免使用捷径。

| 审查类别 | 需要检查的内容 |
|----------------|-------|
| 需求 | 每一项需求：是否已实现，以及存在的具体差距 |
| 编译 | 代码是否能够编译？测试是否通过？程序是否能够正常运行？ |
| 常见问题 | 终端认证、令牌刷新机制、密码加密（使用 bcrypt）、错误处理、输入验证等 |
| 功能性 | 测试实际的功能流程（而不仅仅是代码是否能够编译），验证边缘情况是否正常处理 |
| 测试覆盖率 | 认证错误（如 401/403 错误）、令牌过期、无效输入、速率限制等 |

### 第三步：给出审查结果

**如果代码满足 95% 以上的要求，则批准：**
```
IMPLEMENTATION_APPROVED

- [Requirement 1]: Verified
- [Requirement 2]: Verified
- Compilation: Success
- Tests: All passing
```

**如果需要修改：**
```
REQUIREMENTS COMPLIANCE:
- [Requirement]: Implemented
- [Requirement]: Missing - [specific gap]

IMMEDIATE ACTIONS NEEDED:
1. [Specific fix with file/line if known]
2. [Specific fix]
```

## 关键原则

**严谨但公平：**
- 发现实际存在的问题（如安全漏洞、逻辑错误、数据流问题），而非仅仅是代码风格问题；
- 优先考虑功能完整性，务必指出安全相关的问题（如认证、加密、数据验证等）；
- 表达简洁明了：使用项目符号列出问题，避免冗长的描述；
- 审查结果中不应包含代码内容或详细的分析。

**全新的视角是你的优势：**
- 像从未见过这段代码一样进行审查，严格依据需求进行验证，而不是基于开发者的意图。

## 审查完成的信号

`IMPLEMENTATION_APPROVED`：表示审查完成。

只有在以下所有条件都满足时，才能使用该信号：
- 所有需求都得到满足；
- 代码能够编译并正常运行；
- 测试通过；
- 不存在重大缺陷。

如果有疑问，请不要批准代码。

## 最小示例

```
User: /coach SPEC.md

Claude:
REQUIREMENTS COMPLIANCE:
- User registration endpoint (bcrypt hashing)
- Login with JWT tokens
- Logout endpoint - not implemented
- Token refresh - missing /auth/refresh endpoint

IMMEDIATE ACTIONS NEEDED:
1. Add POST /auth/logout endpoint
2. Add POST /auth/refresh for token renewal
3. Add tests for 401 on expired tokens

---

User: [fixes] /coach SPEC.md

Claude:
IMPLEMENTATION_APPROVED
- All auth endpoints verified (register, login, logout, refresh)
- 18 tests passing including auth error cases
```

## 参考资料

- **论文**：[《代码合成中的对抗性合作》（Adversarial Cooperation in Code Synthesis）[链接](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf)
- **实现示例**：[g3](https://github.com/dhanji/g3)
- **核心观点**：不要相信实施者的自我评估结果，应独立地根据需求进行评估。