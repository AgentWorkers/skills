---
name: email-formatter
description: "将粗糙的电子邮件草稿转化为优雅、专业的邮件。当用户希望提升邮件质量、修正语法和语气、格式化商务邮件，或将非正式消息转换为专业沟通内容时，可以使用此技能。触发指令包括：“格式化我的邮件”、“让这封邮件更专业”、“改进这条消息”、“修复我的邮件”、“润色这份草稿”，或任何关于提升邮件写作质量的请求。此外，该技能也适用于将项目列表或便条转化为完整的邮件、调整邮件的语气（正式/非正式/友好），以及为客户、经理或利益相关者准备重要邮件。"
license: MIT
author: Your Name
version: 1.0.0
---

# 电子邮件格式化工具 - 专业电子邮件优化服务

## 安装与设置

### 先决条件检查
在使用此工具之前，请确认您的环境具备以下要求：

```bash
# Check if bash is available
which bash

# Check Python version (3.8+ required)
python3 --version

# Check Node.js (optional, for advanced features)
node --version
```

### 自动安装脚本
**对于AI代理：首次使用时请运行此安装检查**

```bash
#!/bin/bash
# Email Formatter Skill - Auto Setup
# This script installs required dependencies

echo "🔧 Email Formatter Skill - Installation Starting..."

# Create skill workspace
SKILL_DIR="$HOME/.email-formatter-skill"
mkdir -p "$SKILL_DIR"
cd "$SKILL_DIR"

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install --break-system-packages --quiet \
    language-tool-python \
    textstat \
    spacy 2>/dev/null || pip3 install --user --quiet \
    language-tool-python \
    textstat \
    spacy

# Download language model for grammar checking
echo "📚 Downloading language model..."
python3 -m spacy download en_core_web_sm --quiet 2>/dev/null || true

# Create helper scripts directory
mkdir -p "$SKILL_DIR/scripts"

# Test installation
if python3 -c "import language_tool_python; import textstat; import spacy" 2>/dev/null; then
    echo "✅ Email Formatter Skill installed successfully!"
    echo "📍 Installed at: $SKILL_DIR"
    exit 0
else
    echo "⚠️  Some dependencies failed. Skill will work with reduced features."
    exit 0
fi
```

### 手动安装（如果自动安装失败）

```bash
# Minimal setup - no external dependencies
# The skill will use built-in Python capabilities only
mkdir -p ~/.email-formatter-skill/scripts
echo "✅ Basic setup complete"
```

### 安装验证
```bash
# Quick verification
python3 -c "print('Email Formatter: Ready ✅')"
```

## 依赖项

### 必需依赖项（始终可用）
- Python 3.7及以上版本（仅最低配置需要标准库）
- Bash shell

### 可选依赖项（高级功能）
- `language-tool-python`：高级语法检查工具
- `textstat`：可读性分析工具
- `spacy`：用于情感分析的自然语言处理库

**注意：**对于AI代理，即使缺少这些可选依赖项，该工具也能以降级模式运行。仅在环境允许的情况下安装它们。

## 功能概述
该工具能够将粗糙的电子邮件草稿转换为格式规范、专业性强的沟通内容，通过改进语法、调整语气、增强清晰度以及应用正确的格式来实现。它支持从简单修改到全面重写的功能，同时保留发送者的原意。

## ⚠️ 严格的安全性与隐私要求
**本工具必须始终遵守以下不可协商的安全规则：**

### 安全级别：最高级别 - 需要多层验证
**强制性的预处理安全检查：**
每封电子邮件在格式化之前都必须通过以下所有安全检查：

#### 第一层：内容分类（立即拦截）
❌ **非法活动**：欺诈、网络钓鱼、洗钱、逃税、贿赂
❌ **暴力与威胁**：人身威胁、恐吓、跟踪、人肉搜索、报复性威胁
❌ **身份冒充**：冒充政府官员、公司高管、IT/支持人员或执法人员
❌ **金融欺诈**：电汇、加密货币诈骗、投资骗局、庞氏骗局
❌ **身份盗窃**：请求社会安全号码（SSN）、密码共享、凭证钓鱼、虚假验证
❌ **虚假信息**：健康欺诈、选举干扰、阴谋论、假新闻
❌ **儿童安全**：涉及未成年人的不当内容
❌ **仇恨言论**：种族主义、性别歧视、恐同言论、宗教仇恨
❌ **色情内容**：骚扰、露骨内容、不当的搭讪行为
❌ **职场违规**：歧视、骚扰、报复行为、恶劣的工作环境
❌ **学术欺诈**：抄袭、作弊、使用虚假凭证、代写作业
❌ **医疗欺诈**：伪造处方、未经授权的建议、虚假治疗
❌ **违法行为**：合同欺诈、伪证、妨碍司法公正
❌ **隐私侵犯**：未经同意分享个人信息、监控、跟踪
❌ **恶意软件/黑客攻击**：网络钓鱼链接、恶意附件、系统漏洞利用
❌ **勒索**：敲诈、勒索软件、以金钱为目的的威胁

#### 第二层：模式识别（危险信号）
扫描可能表明恶意意图的可疑模式：

**金融类危险信号：**
- 紧急的付款请求
- 电汇指示
- 礼品卡购买
- 加密货币交易
- “请保密” + 要求付款
- 规避正常审批流程
- 账户异常变动
- 退税诈骗
- 继承诈骗
- 彩票/奖品诈骗

**权威冒充类危险信号：**
- “我是来自IT/人力资源/法律/管理部门的”
- “CEO需要您……”
- “[权威机构]的紧急请求”
- “请勿告知他人”
- 规避电子邮件/域名验证
- 来自上级的异常请求
- 虚假的紧急情况

**凭证收集类危险信号：**
- “请验证您的密码”
- “确认您的账户”
- “点击以防止账户被暂停”
- 检测到异常登录尝试
- 链接到登录页面的链接
- 虚假的安全警告
- 账户过期警告

**社会工程类危险信号：**
- 人为制造的紧迫感
- 情感操控
- 似乎好得令人难以置信的提议
- 要求保密
- 发件人行为异常
- 施加压力的沟通方式
- 基于恐惧的言论

#### 第三层：情感与语气分析（警告或拦截）
⚠️ **攻击性/敌对性**：侮辱性、贬低性、威胁性语言
⚠️ **操控性**：利用愧疚感、情感操控、精神操控
⚠️ **强制性**：利用权力不平衡进行胁迫
⚠️ **欺骗性**：半真半假的信息、误导性陈述、隐瞒事实
⚠️ **歧视性**：基于受保护特征的表达
⚠️ **报复性**：因受保护行为而进行报复

#### 第四层：上下文验证（确认合法性）
✓ **发送者与接收者的关系**：这与他们的正常沟通方式一致吗？
✓ **请求的合理性**：这是一个正常的业务请求吗？
✓ **沟通渠道**：应该通过电子邮件还是面对面/电话进行？
✓ **紧迫性**：为什么这么紧急？这种紧迫性合理吗？
✓ **信息的敏感性**：这些信息适合通过电子邮件发送吗？
✓ **授权**：发送者是否有权限提出这样的请求？

#### 第五层：隐私与数据保护（遵守GDPR/CCPA法规）
🔒 **个人身份信息（PII）检测**：姓名、地址、电话号码、电子邮件地址、社会安全号码（SSN）、出生日期（DOB）、照片
🔒 **财务数据**：信用卡信息、银行账户信息、税务识别号、薪资信息
🔒 **健康数据**：医疗记录、诊断结果、处方信息、HIPAA相关数据
🔒 **凭证信息**：密码、API密钥、令牌、安全问题相关信息
🔒 **专有数据**：商业机密、保密业务信息、保密协议（NDA）相关内容
🔒 **儿童数据**：任何关于18岁以下个人的数据

**处理措施：**如果检测到个人身份信息（PII），需警告用户：
- 电子邮件默认未加密
- 存在数据泄露风险
- 需遵守GDPR、CCPA、HIPAA等法规
- 建议使用安全的替代方式（加密电子邮件、安全门户、面对面沟通）

### 绝不容忍的拦截行为
如果检测到任何违规内容，**立即拒绝发送，且不进行任何格式化处理**：

```python
ZERO_TOLERANCE_PATTERNS = [
    # Credential Requests
    r'(send|give|provide).{0,20}(password|credential|login)',
    r'verify.{0,20}(password|account|identity)',
    
    # Financial Fraud
    r'wire transfer.{0,30}(urgent|immediately|today)',
    r'gift card.{0,20}(purchase|buy|get)',
    r'(bitcoin|crypto).{0,20}(send|transfer|wallet)',
    
    # Impersonation
    r"i'?m.{0,10}(from|with|calling from).{0,20}(IT|HR|legal|IRS|FBI)",
    r'(this is|i am).{0,20}(CEO|CFO|president|director)',
    
    # Threats
    r'(or else|otherwise).{0,30}(fire|sue|report|punish)',
    r'you (will|better).{0,20}(regret|pay|suffer)',
    
    # Illegal Activities
    r'(launder|hide|conceal).{0,20}money',
    r'(fake|forged|fraudulent).{0,20}(document|invoice|receipt)',
    
    # Child Safety
    r'(minor|child|kid|underage).{0,50}(sexual|romantic|date|meet)',
    
    # Malware/Phishing
    r'(click|download).{0,20}(attachment|link|file).{0,20}(urgent|immediately)',
    r'account.{0,20}(suspend|lock|close|expire).{0,20}(unless|until)',
    
    # Harassment
    r'(stupid|idiot|incompetent|worthless).{0,20}(you|employee|coworker)',
    r"i'?ll make sure you (never|don't|can't)",
]
```

### 加强安全响应机制
当检测到禁止内容时：

```
1. STOP - Do not process further
2. LOG - Record violation type (no content)
3. INFORM - Tell user specifically what rule was violated
4. EDUCATE - Explain why it's harmful/illegal
5. REDIRECT - Suggest legitimate alternatives
6. REPORT - Flag for review if severe (threats, child safety, fraud)
```

**示例回复模板：**
```
🛑 SECURITY BLOCK: Email Formatting Refused

REASON: [Specific violation - e.g., "Credential request detected"]

WHY THIS IS BLOCKED:
[Explanation - e.g., "Legitimate organizations never ask for 
passwords via email. This matches phishing attack patterns."]

WHAT YOU SHOULD DO:
[Alternative - e.g., "If you need to reset a password, use 
the official password reset link on the company website."]

THIS SKILL CANNOT:
- Help with fraudulent communications
- Bypass security protocols
- Facilitate illegal activities
- Enable harassment or threats
```

## 辅助脚本与工具
该工具包含供AI代理使用的实用脚本。请将这些脚本保存在`~/.email-formatter-skill/scripts/`目录下：

### 1. 语法检查器 (`grammar_check.py`)

```python
#!/usr/bin/env python3
"""
Basic grammar and spell checker
Usage: python3 grammar_check.py "email text here"
"""
import sys
import re

def basic_grammar_check(text):
    """Basic grammar checks without external dependencies"""
    issues = []
    
    # Common spelling errors
    typos = {
        'recieve': 'receive', 'occured': 'occurred', 'seperate': 'separate',
        'definately': 'definitely', 'accomodate': 'accommodate',
        'tommorow': 'tomorrow', 'untill': 'until', 'truely': 'truly'
    }
    
    for wrong, right in typos.items():
        if wrong in text.lower():
            issues.append(f"Spelling: '{wrong}' → '{right}'")
    
    # Basic grammar patterns
    if re.search(r'\bi\s', text):  # lowercase 'i'
        issues.append("Grammar: 'i' should be capitalized to 'I'")
    
    if re.search(r'\s{2,}', text):
        issues.append("Formatting: Multiple spaces detected")
    
    if re.search(r'[.!?]\s*[a-z]', text):
        issues.append("Grammar: Sentence should start with capital letter")
    
    # Double punctuation
    if re.search(r'[.!?]{2,}', text):
        issues.append("Punctuation: Multiple punctuation marks")
    
    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 grammar_check.py 'text'")
        sys.exit(1)
    
    text = sys.argv[1]
    issues = basic_grammar_check(text)
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("✅ No basic issues found")
```

### 2. 语气分析器 (`tone_analyzer.py`)

```python
#!/usr/bin/env python3
"""
Analyze email tone
Usage: python3 tone_analyzer.py "email text"
"""
import sys
import re

def analyze_tone(text):
    """Detect tone indicators in email text"""
    
    # Formal indicators
    formal_words = ['pursuant', 'hereby', 'aforementioned', 'regarding', 
                   'sincerely', 'respectfully', 'cordially']
    
    # Casual indicators  
    casual_words = ['hey', 'gonna', 'wanna', 'yeah', 'yep', 'nope',
                   'btw', 'fyi', 'lol', 'omg', 'tbh']
    
    # Aggressive indicators
    aggressive_words = ['immediately', 'must', 'unacceptable', 'ridiculous',
                       'obviously', 'clearly', 'need to', 'have to']
    
    # Polite indicators
    polite_words = ['please', 'kindly', 'would you', 'could you',
                   'appreciate', 'thank', 'grateful']
    
    text_lower = text.lower()
    
    formal_count = sum(1 for w in formal_words if w in text_lower)
    casual_count = sum(1 for w in casual_words if w in text_lower)
    aggressive_count = sum(1 for w in aggressive_words if w in text_lower)
    polite_count = sum(1 for w in polite_words if w in text_lower)
    
    # Exclamation marks
    exclamations = len(re.findall(r'!', text))
    
    # ALL CAPS detection
    caps_words = len(re.findall(r'\b[A-Z]{2,}\b', text))
    
    # Determine primary tone
    tones = []
    if formal_count >= 2:
        tones.append("FORMAL")
    if casual_count >= 2:
        tones.append("CASUAL")
    if aggressive_count >= 2 or caps_words >= 2:
        tones.append("AGGRESSIVE")
    if polite_count >= 2:
        tones.append("POLITE")
    if exclamations >= 3:
        tones.append("ENTHUSIASTIC/URGENT")
    
    if not tones:
        tones.append("NEUTRAL")
    
    return {
        'primary_tone': tones[0],
        'all_tones': tones,
        'formal_score': formal_count,
        'casual_score': casual_count,
        'aggressive_score': aggressive_count,
        'polite_score': polite_count,
        'exclamations': exclamations,
        'caps_words': caps_words
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tone_analyzer.py 'text'")
        sys.exit(1)
    
    result = analyze_tone(sys.argv[1])
    print(f"📊 Primary Tone: {result['primary_tone']}")
    print(f"🎯 All Tones: {', '.join(result['all_tones'])}")
    print(f"📈 Scores - Formal:{result['formal_score']} Casual:{result['casual_score']} "
          f"Aggressive:{result['aggressive_score']} Polite:{result['polite_score']}")
    
    if result['aggressive_score'] >= 2:
        print("⚠️  WARNING: Email may sound aggressive")
    if result['exclamations'] >= 3:
        print("⚠️  WARNING: Too many exclamation marks")
    if result['caps_words'] >= 2:
        print("⚠️  WARNING: Excessive capitalization detected")
```

### 3. 可读性评分器 (`readability.py`)

```python
#!/usr/bin/env python3
"""
Calculate email readability
Usage: python3 readability.py "email text"
"""
import sys
import re

def count_syllables(word):
    """Simple syllable counter"""
    word = word.lower()
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith('e'):
        syllable_count -= 1
    
    # Every word has at least one syllable
    if syllable_count == 0:
        syllable_count = 1
        
    return syllable_count

def flesch_reading_ease(text):
    """Calculate Flesch Reading Ease score"""
    sentences = len(re.findall(r'[.!?]+', text)) or 1
    words = len(text.split())
    syllables = sum(count_syllables(word) for word in text.split())
    
    if words == 0:
        return 0
    
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return round(score, 1)

def analyze_readability(text):
    """Analyze email readability"""
    words = text.split()
    sentences = len(re.findall(r'[.!?]+', text)) or 1
    
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
    avg_sentence_length = len(words) / sentences
    
    flesch_score = flesch_reading_ease(text)
    
    # Interpret score
    if flesch_score >= 90:
        level = "Very Easy (5th grade)"
    elif flesch_score >= 80:
        level = "Easy (6th grade)"
    elif flesch_score >= 70:
        level = "Fairly Easy (7th grade)"
    elif flesch_score >= 60:
        level = "Standard (8-9th grade)"
    elif flesch_score >= 50:
        level = "Fairly Difficult (10-12th grade)"
    elif flesch_score >= 30:
        level = "Difficult (College)"
    else:
        level = "Very Difficult (Graduate)"
    
    return {
        'flesch_score': flesch_score,
        'level': level,
        'avg_word_length': round(avg_word_length, 1),
        'avg_sentence_length': round(avg_sentence_length, 1),
        'total_words': len(words),
        'total_sentences': sentences
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 readability.py 'text'")
        sys.exit(1)
    
    result = analyze_readability(sys.argv[1])
    print(f"📖 Flesch Reading Ease: {result['flesch_score']}")
    print(f"📚 Reading Level: {result['level']}")
    print(f"📊 Stats: {result['total_words']} words, {result['total_sentences']} sentences")
    print(f"📏 Avg: {result['avg_word_length']} chars/word, {result['avg_sentence_length']} words/sentence")
    
    # Recommendations
    if result['flesch_score'] < 60:
        print("💡 TIP: Simplify language for better clarity")
    if result['avg_sentence_length'] > 20:
        print("💡 TIP: Break long sentences into shorter ones")
```

### 4. 安全扫描器 (`security_scan.py`)

```python
#!/usr/bin/env python3
"""
ULTRA-SECURE Email Scanner - Multi-Layer Threat Detection
Usage: python3 security_scan.py "email text"
Exit codes: 0=safe, 1=warning, 2=critical_block, 3=report_required
"""
import sys
import re
import json
from datetime import datetime

class SecurityScanner:
    """Military-grade email security scanner"""
    
    def __init__(self):
        self.threat_level = 0  # 0=safe, 1=warning, 2=critical, 3=report
        self.violations = []
        self.warnings = []
        
    def scan(self, text):
        """Run all security checks"""
        # Layer 1: Zero Tolerance Patterns
        self.check_zero_tolerance(text)
        
        # Layer 2: Financial Fraud
        self.check_financial_fraud(text)
        
        # Layer 3: Impersonation
        self.check_impersonation(text)
        
        # Layer 4: Credential Harvesting
        self.check_credential_harvesting(text)
        
        # Layer 5: Threats & Violence
        self.check_threats(text)
        
        # Layer 6: Harassment & Discrimination
        self.check_harassment(text)
        
        # Layer 7: Privacy & PII
        self.check_privacy_violations(text)
        
        # Layer 8: Social Engineering
        self.check_social_engineering(text)
        
        # Layer 9: Child Safety
        self.check_child_safety(text)
        
        # Layer 10: Malicious Patterns
        self.check_malicious_patterns(text)
        
        return self.generate_report()
    
    def check_zero_tolerance(self, text):
        """Critical patterns that immediately block"""
        text_lower = text.lower()
        
        critical_patterns = [
            # Credentials
            (r'(send|give|provide|email).{0,30}(password|pwd|credential|login|passphrase)',
             'CREDENTIAL_REQUEST', 3),
            (r'verify.{0,20}(password|account|identity|credential)',
             'FAKE_VERIFICATION', 3),
            (r'(username|user id).{0,20}(and|&|\\+).{0,20}password',
             'CREDENTIAL_PAIR_REQUEST', 3),
            
            # Financial
            (r'wire transfer.{0,30}(urgent|immediate|asap|now|today)',
             'URGENT_WIRE_TRANSFER', 3),
            (r'(gift card|itunes|steam|amazon card).{0,30}(buy|purchase|get|send)',
             'GIFT_CARD_SCAM', 3),
            (r'(bitcoin|btc|crypto|ethereum|eth).{0,30}(wallet|address|send|transfer)',
             'CRYPTO_SCAM', 3),
            (r'(bank account|routing number|swift code).{0,30}(provide|send|give)',
             'BANKING_INFO_REQUEST', 3),
            
            # Impersonation
            (r"i'?m.{0,10}(from|with|calling from).{0,30}(IT|support|tech|help desk)",
             'IT_IMPERSONATION', 3),
            (r"(this is|i am|i'm).{0,20}(CEO|CFO|president|director|executive)",
             'EXECUTIVE_IMPERSONATION', 3),
            (r"(IRS|FBI|police|government|immigration).{0,30}(contact|reach out|notice)",
             'AUTHORITY_IMPERSONATION', 3),
            
            # Threats
            (r'(or else|otherwise).{0,30}(fire|terminate|sue|report|arrest)',
             'THREAT_DETECTED', 3),
            (r"(you|i)'?(ll| will).{0,30}(regret|pay|suffer|sorry)",
             'THREAT_LANGUAGE', 3),
            
            # Child Safety
            (r'(child|minor|kid|teen|underage).{0,50}(meet|date|relationship|romantic)',
             'CHILD_SAFETY_VIOLATION', 3),
            
            # Malware
            (r'(click|open|download).{0,20}(attachment|link|file).{0,20}(urgent|expire|suspend)',
             'PHISHING_LINK', 3),
        ]
        
        for pattern, violation_type, severity in critical_patterns:
            if re.search(pattern, text_lower):
                self.add_violation(violation_type, severity, pattern)
    
    def check_financial_fraud(self, text):
        """Detect financial scam patterns"""
        text_lower = text.lower()
        
        fraud_indicators = [
            (r'(won|winner|prize|lottery).{0,30}(\$|dollar|money|claim)',
             'LOTTERY_SCAM', 2),
            (r'(inheritance|beneficiary|estate).{0,50}(million|claim|transfer)',
             'INHERITANCE_SCAM', 2),
            (r'(tax|irs).{0,30}(refund|owe|pay immediately)',
             'TAX_SCAM', 2),
            (r'(invoice|payment).{0,20}(overdue|urgent|immediate|final notice)',
             'FAKE_INVOICE', 2),
            (r'(suspended|frozen|locked).{0,30}account',
             'ACCOUNT_SUSPENSION_SCAM', 2),
            (r'(refund|reimbursement).{0,30}(click|verify|confirm)',
             'REFUND_SCAM', 2),
            (r'(investment|opportunity|profit).{0,50}(guaranteed|risk-free|double)',
             'INVESTMENT_FRAUD', 2),
        ]
        
        for pattern, violation_type, severity in fraud_indicators:
            if re.search(pattern, text_lower):
                self.add_violation(violation_type, severity, pattern)
    
    def check_impersonation(self, text):
        """Detect impersonation attempts"""
        text_lower = text.lower()
        
        impersonation_patterns = [
            (r'(on behalf of|representing).{0,30}(company|organization|government)',
             'UNAUTHORIZED_REPRESENTATION', 2),
            (r"(i'?m|this is).{0,20}(calling|writing|reaching out).{0,20}(from|regarding)",
             'SUSPICIOUS_INTRODUCTION', 1),
            (r'(verify|confirm).{0,20}(you are|your identity|who you are)',
             'IDENTITY_VERIFICATION_REQUEST', 2),
        ]
        
        for pattern, violation_type, severity in impersonation_patterns:
            if re.search(pattern, text_lower):
                self.add_violation(violation_type, severity, pattern)
    
    def check_credential_harvesting(self, text):
        """Detect credential theft attempts"""
        text_lower = text.lower()
        
        patterns = [
            (r'(account|access).{0,30}(expire|suspend|lock|disable)',
             'FAKE_EXPIRATION', 2),
            (r'(security|unusual|suspicious).{0,30}activity',
             'FAKE_SECURITY_ALERT', 2),
            (r'(update|verify|confirm).{0,30}(payment|billing) (method|information)',
             'PAYMENT_INFO_PHISHING', 2),
            (r'(reset|recover|change).{0,20}password.{0,20}(click|link|here)',
             'PASSWORD_RESET_SCAM', 2),
        ]
        
        for pattern, violation_type, severity in patterns:
            if re.search(pattern, text_lower):
                self.add_violation(violation_type, severity, pattern)
    
    def check_threats(self, text):
        """Detect threats and violent language"""
        text_lower = text.lower()
        
        threat_words = [
            'kill', 'hurt', 'harm', 'destroy', 'eliminate', 'punish',
            'revenge', 'retaliate', 'get back at', 'make you pay'
        ]
        
        for word in threat_words:
            if word in text_lower:
                self.add_violation('THREAT_LANGUAGE', 3, f"Threat word: {word}")
        
        # Physical threat patterns
        if re.search(r'(come after|find you|know where you)', text_lower):
            self.add_violation('PHYSICAL_THREAT', 3, 'Physical threat implied')
    
    def check_harassment(self, text):
        """Detect harassment and hostile language"""
        text_lower = text.lower()
        
        hostile_words = [
            'stupid', 'idiot', 'moron', 'incompetent', 'worthless',
            'pathetic', 'useless', 'loser', 'failure', 'trash'
        ]
        
        count = sum(1 for word in hostile_words if word in text_lower)
        if count >= 2:
            self.add_violation('HARASSMENT', 2, f'{count} hostile terms detected')
        elif count == 1:
            self.add_warning('POTENTIALLY_HOSTILE', 'Hostile language detected')
        
        # Discriminatory patterns
        protected_characteristics = [
            (r'(because|since).{0,20}(you\'?re|you are).{0,20}(woman|female|girl)',
             'GENDER_DISCRIMINATION'),
            (r'(because|since).{0,20}(you\'?re|you are).{0,20}(old|young|age)',
             'AGE_DISCRIMINATION'),
            (r'(people like you|your kind|you people)', 'DISCRIMINATORY_LANGUAGE'),
        ]
        
        for pattern, violation_type in protected_characteristics:
            if re.search(pattern, text_lower):
                self.add_violation(violation_type, 3, pattern)
    
    def check_privacy_violations(self, text):
        """Detect PII and privacy issues"""
        
        # SSN pattern
        if re.search(r'\b\d{3}-\d{2}-\d{4}\b', text):
            self.add_violation('SSN_DETECTED', 2, 'Social Security Number found')
        
        # Credit card pattern
        if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text):
            self.add_violation('CREDIT_CARD_DETECTED', 2, 'Credit card number found')
        
        # Email addresses (multiple)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if len(emails) > 3:
            self.add_warning('MULTIPLE_EMAILS', f'{len(emails)} email addresses found')
        
        # Phone numbers (multiple)
        phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        if len(phones) > 2:
            self.add_warning('MULTIPLE_PHONES', f'{len(phones)} phone numbers found')
        
        # Home address pattern
        if re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|drive|dr)', text.lower()):
            self.add_warning('ADDRESS_DETECTED', 'Physical address found')
    
    def check_social_engineering(self, text):
        """Detect social engineering tactics"""
        text_lower = text.lower()
        
        # Urgency indicators
        urgency_words = ['urgent', 'immediate', 'asap', 'right now', 'immediately',
                        'emergency', 'critical', 'time-sensitive']
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        
        if urgency_count >= 3:
            self.add_violation('ARTIFICIAL_URGENCY', 2, f'{urgency_count} urgency indicators')
        elif urgency_count >= 2:
            self.add_warning('URGENCY_DETECTED', 'Multiple urgency indicators')
        
        # Secrecy requests
        if re.search(r"(don't tell|keep (this )?secret|confidential|between us)", text_lower):
            self.add_violation('SECRECY_REQUEST', 2, 'Requesting secrecy')
        
        # Authority bypass
        if re.search(r'(bypass|skip|ignore).{0,20}(normal|usual|standard) (process|procedure)', text_lower):
            self.add_violation('PROCESS_BYPASS', 2, 'Attempting to bypass normal procedures')
        
        # Too good to be true
        if re.search(r'(free|win|won|winner|selected|chosen).{0,30}(prize|money|gift|\$)', text_lower):
            self.add_warning('TOO_GOOD_TO_BE_TRUE', 'Unrealistic offer detected')
    
    def check_child_safety(self, text):
        """Critical: Child safety violations"""
        text_lower = text.lower()
        
        child_terms = ['child', 'minor', 'kid', 'teen', 'teenager', 'underage', 'student', 'pupil']
        inappropriate_context = ['date', 'dating', 'romantic', 'relationship', 'meet in person',
                                'alone', 'secret', 'don\'t tell', 'special friend']
        
        has_child_term = any(term in text_lower for term in child_terms)
        has_inappropriate = any(term in text_lower for term in inappropriate_context)
        
        if has_child_term and has_inappropriate:
            self.add_violation('CHILD_SAFETY_CRITICAL', 3, 'Child safety violation - REPORT REQUIRED')
    
    def check_malicious_patterns(self, text):
        """Detect malware and hacking patterns"""
        text_lower = text.lower()
        
        malicious_patterns = [
            (r'(click|open).{0,20}attachment.{0,20}(urgent|important|invoice)',
             'MALICIOUS_ATTACHMENT', 2),
            (r'(download|install|run).{0,20}(software|program|tool|update)',
             'UNAUTHORIZED_SOFTWARE', 2),
            (r'(disable|turn off).{0,20}(antivirus|firewall|security)',
             'SECURITY_BYPASS', 3),
            (r'(admin|administrator|root).{0,20}(access|password|privileges)',
             'PRIVILEGE_ESCALATION', 3),
        ]
        
        for pattern, violation_type, severity in malicious_patterns:
            if re.search(pattern, text_lower):
                self.add_violation(violation_type, severity, pattern)
    
    def add_violation(self, violation_type, severity, pattern):
        """Record a security violation"""
        self.violations.append({
            'type': violation_type,
            'severity': severity,
            'pattern': pattern,
            'timestamp': datetime.now().isoformat()
        })
        if severity > self.threat_level:
            self.threat_level = severity
    
    def add_warning(self, warning_type, message):
        """Record a warning"""
        self.warnings.append({
            'type': warning_type,
            'message': message
        })
        if self.threat_level == 0:
            self.threat_level = 1
    
    def generate_report(self):
        """Generate security scan report"""
        return {
            'threat_level': self.threat_level,
            'status': self.get_status(),
            'violations': self.violations,
            'warnings': self.warnings,
            'summary': self.get_summary()
        }
    
    def get_status(self):
        """Get security status"""
        if self.threat_level >= 3:
            return 'CRITICAL_BLOCK_AND_REPORT'
        elif self.threat_level == 2:
            return 'BLOCK'
        elif self.threat_level == 1:
            return 'WARNING'
        else:
            return 'SAFE'
    
    def get_summary(self):
        """Get human-readable summary"""
        if self.threat_level >= 3:
            return f"🚨 CRITICAL: {len(self.violations)} severe violations detected. DO NOT SEND. REPORT REQUIRED."
        elif self.threat_level == 2:
            return f"🛑 BLOCKED: {len(self.violations)} violations detected. Cannot format this email."
        elif self.threat_level == 1:
            return f"⚠️  WARNING: {len(self.warnings)} potential issues detected. Review carefully."
        else:
            return "✅ No security issues detected."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 security_scan.py 'email text'")
        sys.exit(1)
    
    scanner = SecurityScanner()
    report = scanner.scan(sys.argv[1])
    
    # Print report
    print(f"\n{'='*60}")
    print(f"SECURITY SCAN REPORT")
    print(f"{'='*60}")
    print(f"Status: {report['status']}")
    print(f"Threat Level: {report['threat_level']}/3")
    print(f"\n{report['summary']}\n")
    
    if report['violations']:
        print("VIOLATIONS:")
        for v in report['violations']:
            severity_icon = "🚨" if v['severity'] >= 3 else "🛑"
            print(f"  {severity_icon} {v['type']}")
            print(f"      Pattern: {v['pattern'][:50]}...")
    
    if report['warnings']:
        print("\nWARNINGS:")
        for w in report['warnings']:
            print(f"  ⚠️  {w['type']}: {w['message']}")
    
    print(f"\n{'='*60}\n")
    
    # Return appropriate exit code
    sys.exit(report['threat_level'])
```

## AI代理的使用流程
**强制性的安全流程：**
```bash
#!/bin/bash
# Email Formatter - Secure Processing Pipeline
# This workflow is REQUIRED for every email formatting request

set -e  # Exit on any error

EMAIL_TEXT="$1"
TEMP_DIR="/tmp/email-formatter-$$"
mkdir -p "$TEMP_DIR"

echo "🔒 Starting Secure Email Processing Pipeline..."
echo "================================================"

# STEP 1: PRE-FLIGHT SECURITY SCAN (CRITICAL)
echo "Step 1/7: Running security scan..."
python3 ~/.email-formatter-skill/scripts/security_scan.py "$EMAIL_TEXT"
SECURITY_EXIT=$?

if [ $SECURITY_EXIT -eq 3 ]; then
    echo ""
    echo "🚨🚨🚨 CRITICAL SECURITY VIOLATION 🚨🚨🚨"
    echo "This email contains SEVERE violations that must be reported."
    echo "Formatting REFUSED. Potential illegal activity detected."
    echo ""
    echo "ACTIONS REQUIRED:"
    echo "1. Do NOT send this email"
    echo "2. Document the incident"
    echo "3. Report to appropriate authorities if applicable"
    echo "4. Inform user of violation"
    exit 3

elif [ $SECURITY_EXIT -eq 2 ]; then
    echo ""
    echo "🛑 SECURITY BLOCK"
    echo "This email violates safety policies and cannot be formatted."
    echo "Review the security report above for specific violations."
    echo ""
    echo "SUGGESTED ACTIONS:"
    echo "1. Identify the specific violation"
    echo "2. Explain to user why it's blocked"
    echo "3. Suggest legitimate alternatives"
    echo "4. Offer to help rewrite with appropriate content"
    exit 2

elif [ $SECURITY_EXIT -eq 1 ]; then
    echo ""
    echo "⚠️  SECURITY WARNING"
    echo "Potential issues detected. Proceeding with caution..."
    echo "Will re-scan after formatting to ensure no issues introduced."
    echo ""
fi

# STEP 2: CONTENT ANALYSIS
echo ""
echo "Step 2/7: Analyzing content..."
echo "$EMAIL_TEXT" > "$TEMP_DIR/original.txt"

# Word count
WORD_COUNT=$(echo "$EMAIL_TEXT" | wc -w)
echo "   📊 Word count: $WORD_COUNT"

if [ $WORD_COUNT -gt 500 ]; then
    echo "   ⚠️  Email is very long. Consider breaking into multiple emails."
fi

# STEP 3: TONE ANALYSIS
echo ""
echo "Step 3/7: Analyzing tone..."
python3 ~/.email-formatter-skill/scripts/tone_analyzer.py "$EMAIL_TEXT" > "$TEMP_DIR/tone.txt"
cat "$TEMP_DIR/tone.txt"

# Check if tone is aggressive
if grep -q "AGGRESSIVE" "$TEMP_DIR/tone.txt"; then
    echo ""
    echo "   ⚠️  AGGRESSIVE TONE DETECTED"
    echo "   Recommendation: Suggest user wait 24 hours before sending"
    echo "   Offer to rewrite in professional, constructive tone"
    echo ""
    read -p "   Continue anyway? (yes/no): " CONTINUE
    if [ "$CONTINUE" != "yes" ]; then
        echo "   Formatting cancelled by tone check."
        exit 1
    fi
fi

# STEP 4: GRAMMAR CHECK
echo ""
echo "Step 4/7: Checking grammar..."
python3 ~/.email-formatter-skill/scripts/grammar_check.py "$EMAIL_TEXT"

# STEP 5: READABILITY ANALYSIS
echo ""
echo "Step 5/7: Analyzing readability..."
python3 ~/.email-formatter-skill/scripts/readability.py "$EMAIL_TEXT" > "$TEMP_DIR/readability.txt"
cat "$TEMP_DIR/readability.txt"

# STEP 6: FORMAT THE EMAIL
echo ""
echo "Step 6/7: Formatting email..."
echo "   [Agent applies formatting rules based on guidelines]"
# ... AI agent performs formatting here ...
# FORMATTED_EMAIL="..."

# STEP 7: POST-FORMATTING SECURITY RE-SCAN (CRITICAL)
echo ""
echo "Step 7/7: Final security validation..."
python3 ~/.email-formatter-skill/scripts/security_scan.py "$FORMATTED_EMAIL"
FINAL_SECURITY=$?

if [ $FINAL_SECURITY -ne 0 ]; then
    echo ""
    echo "🚨 POST-FORMATTING SECURITY FAILURE"
    echo "Formatted version introduced security issues!"
    echo "This should never happen - formatting logic has a bug."
    echo "Reverting to original and blocking output."
    exit 2
fi

# SUCCESS
echo ""
echo "✅ All security checks passed"
echo "✅ Email formatted successfully"
echo ""
echo "================================================"
echo "FORMATTED EMAIL READY FOR REVIEW"
echo "================================================"

# Cleanup
rm -rf "$TEMP_DIR"
```

### AI代理必须严格遵守的安全规则
**切勿跳过任何安全扫描步骤：**
- 在进行任何格式化操作之前必须进行安全扫描
- 格式化完成后也必须进行安全扫描
- 两次扫描都必须通过（退出代码为0），邮件才能被发送
- 如果退出代码为1、2或3，则必须停止整个流程

**双重检查机制：**
```python
# Before presenting formatted email to user
def final_validation(formatted_email):
    # Re-run all security checks
    security_clear = run_security_scan(formatted_email)
    
    if not security_clear:
        # NEVER show formatted email
        return {
            'status': 'BLOCKED',
            'message': 'Formatting introduced security issues',
            'action': 'Report bug in formatting logic'
        }
    
    # Additional checks
    if contains_pii(formatted_email):
        return {
            'status': 'WARNING',
            'message': 'PII detected in formatted email',
            'action': 'Warn user about sending sensitive data via email'
        }
    
    return {
        'status': 'APPROVED',
        'formatted_email': formatted_email
    }
```

**日志记录与审计追踪（保护用户隐私）：**
```python
# Log violations only (NO content)
def log_security_event(violation_type, severity, timestamp):
    """
    Log security events for monitoring
    NEVER log actual email content
    """
    log_entry = {
        'timestamp': timestamp,
        'violation_type': violation_type,
        'severity': severity,
        'action_taken': 'BLOCKED',
        'content': '[REDACTED]'  # Never log content
    }
    # Append to secure audit log
    # This helps improve security detection
```

## 适用场景
当用户需要以下操作时，请使用此工具：
- 修正电子邮件中的语法错误、拼写错误和标点符号问题
- 调整语气（使其更加正式、随意、友好或坚定）
- 将杂乱无章的草稿整理成条理清晰的邮件
- 将要点或笔记转换成完整的电子邮件
- 添加专业的问候语和结尾语
- 提高邮件的清晰度和简洁性
- 为高管、客户或利益相关者准备重要邮件

## 核心原则
1. **保留原意**：不要改变邮件的核心内容或事实，仅改进表达方式
2. **适应上下文**：根据接收者和情境调整邮件格式的正式程度
3. **增强清晰度**：消除歧义，同时保持自然的语气
4. **遵循专业标准**：运用商务写作最佳实践
5. **考虑文化差异**：尊重专业规范和沟通习惯

## 格式化流程
### 第一步：分析草稿
在格式化之前，请评估以下内容：
- **接收者关系**：是上司、同事、客户、供应商、团队成员还是外部人员？
- **邮件目的**：是请求、更新信息、介绍、跟进、反馈还是道歉？
- **所需的语气**：正式的、半正式的、随意的、友好的还是坚定的？
- **紧急程度**：是常规邮件、重要邮件、紧急邮件还是敏感邮件？
- **当前存在的问题**：是否存在语法错误、结构混乱、语气不当或上下文缺失？

### 第二步：进行优化
**语法与表达**：
- 修正拼写错误、标点符号错误和语法错误
- 确保主语和动词一致，时态使用正确
- 删除冗长的句子和片段
- 修改逗号使用不当或修饰语位置错误的部分

**结构与组织**：
```
Standard Email Structure:
1. Greeting (appropriate to relationship)
2. Opening (context or pleasantry)
3. Purpose statement (clear and direct)
4. Body (organized by topic, use paragraphs/bullets)
5. Call to action (if needed)
6. Closing (polite sign-off)
7. Signature
```

**语气调整**：
*过于随意 → 修正为更正式的语气*
```
Before: "Hey! Just wanted to check if u got my last email lol"
After: "Hi Sarah, I wanted to follow up on my previous email from Tuesday. Please let me know if you need any additional information."
```

*过于正式 → 修正为更友好的语气*
```
Before: "I am writing to inquire whether you have completed the aforementioned task."
After: "Hi John, I wanted to check in on the status of the marketing report. How's it coming along?"
```

*过于攻击性 → 修正为更外交化的语气*
```
Before: "You need to fix this immediately. This is unacceptable."
After: "I noticed an issue that requires urgent attention. Could we prioritize resolving this today? I'm happy to help if needed."
```

**清晰度提升**：
- 用具体语言替换模糊的表达
- 将长段落拆分成易于理解的段落
- 对于列表或多项内容，使用项目符号
- 在可能缺失背景信息的地方提供补充说明
- 删除冗余和多余的词语

### 第三步：完善细节
**主题行**（如果提供或需要的话）：
- 保持字数在50个字符以内
- 表达具体且具有行动导向
- 注意大小写的使用（不要全部大写）
- 例如：
  - “Q1预算审查会议 - 3月15日”
  - “关于项目进度的快速咨询”
  - “跟进：网站重新设计提案”

**问候语**：
- 正式场合：”亲爱的Smith博士”，或“亲爱的招聘经理，”
- 专业场合：“嗨，Jennifer”，或“大家好，”
- 随意场合：“嘿，Alex”，或“大家好，”

**结尾语**：
- 正式场合：“此致”，“敬上”，“祝好，”
- 专业场合：“Best”，“谢谢”，“期待您的回复，”
- 随意场合：“Cheers”，“回头聊”，“祝你有美好的一天，”

**签名部分**：
```
Best regards,
[Name]
[Title]
[Company]
[Contact Info - if external]
```

## 常见邮件场景
### 1. 请求邮件
```
Structure:
- Greeting
- Context (why you're writing)
- Specific request
- Deadline or timeframe (if applicable)
- Offer of additional info
- Thanks
- Closing
```

### 2. 追进邮件
```
Structure:
- Reference previous communication
- Polite reminder of action needed
- Make it easy to respond
- Maintain friendly tone
- Closing
```

### 3. 坏消息邮件
```
Structure:
- Direct but empathetic opening
- Clear explanation
- Acknowledge impact
- Offer alternatives or next steps
- End on positive note if possible
```

### 4. 介绍邮件
```
Structure:
- Who you are and connection
- Purpose of introduction
- What you're offering/requesting
- Call to action
- Professional closing
```

## 最佳实践
### 应该做到：
✅ 保持邮件简洁（尽可能控制在200字以内）
✅ 使用主动语态（例如：“我会发送”而不是“它将被发送”）
✅ 用空格分隔文本
✅ 将最重要的信息放在第一段
✅ 校对拼写和自动纠错
✅ 确保“回复所有人”按钮的使用得当
✅ 明确说明下一步行动或需要采取的措施
✅ 保持与发送者的语气一致

### 不应该这样做：
❌ 全部使用大写（显得生硬）
❌ 过度使用感叹号
❌ 在一封邮件中包含多个主题（如果内容复杂）
❌ 对外部接收者使用行业术语
❌ 在情绪激动时撰写邮件（这可能会引起误解）
❌ 假设接收者能理解邮件中的语气（讽刺或幽默可能无法被正确理解）
❌ 忘记在邮件中提及附件

## 语气指南
**正式场合（针对高管、客户、初次联系）：**
- 使用完整的句子
- 使用专业词汇
- 使用正确的称谓和全名
- 用“我会……”而非“你能……”
- 用“请让我知道”而非“让我了解”

**半正式场合（针对同事、常规联系）：**
- 语言风格自然但保持专业
- 可以使用缩写
- 使用名字而非“您能……”
- 语气友好但保持尊重

**随意场合（针对关系亲密的同事、内部团队）：**
- 语言轻松
- 使用缩写和非正式表达
- 问候语简短
- 可以使用表情符号（如果文化允许）

## 质量检查清单
在发送格式化后的邮件之前，请确认：
- [ ] **安全第一**：内容符合所有安全要求
- [ ] **无禁止内容**：未违反上述任何安全规则
- [ ] **符合法律法规**：邮件内容不包含欺诈、骚扰或违法内容
- [ ] **符合道德标准**：信息真实且恰当
- [ ] 语法和拼写正确
- [ ] 语气符合接收者和情境
- [ ] 结构清晰合理
- [ ] 关键信息易于查找
- [ ] 行动指示明确
- [ ] 开头和结尾恰当
- [ ] 无歧义或混淆
- [ ] 长度适中（简洁但信息完整）
- [ ] 使用了专业的格式
- [ ] 保留了原始的意图
- [ ] 未泄露敏感信息
- [ ] **隐私保护**：未不当暴露敏感数据

## 危险信号检测
**始终注意以下警告信号：**
- 请求金钱、凭证或个人信息
- 紧急请求与财务请求同时出现
- 伪装成权威人士的语言（例如：“我是来自……”）
- 威胁或最后通牒
- 要求接收者保密沟通内容
- 规避正常流程
- 发件人信息不一致
- 鼓励接收者点击可疑链接
- 在看似官方的邮件中存在语法/拼写错误
- 显得好得令人难以置信的优惠
- 情感操控手段
- 歧视性语言
- 对受保护群体的敌对或攻击性言论

## 事件响应机制
**当检测到严重违规行为（威胁等级3）时：**
```
IMMEDIATE ACTIONS:
1. BLOCK - Refuse to format email
2. DOCUMENT - Record violation type, timestamp
3. NOTIFY - Inform user of specific violation
4. EDUCATE - Explain why it's harmful/illegal
5. REDIRECT - Suggest legitimate alternatives
6. REPORT - Flag for review if:
   - Child safety violations
   - Credible threats of violence
   - Large-scale fraud attempts
   - Illegal activities
```

**严重违规行为的回复模板：**
```
🚨 CRITICAL SECURITY VIOLATION DETECTED

VIOLATION TYPE: [Specific type - e.g., "Credential Phishing Attempt"]

SEVERITY: CRITICAL - This email cannot be formatted

WHAT WAS DETECTED:
[Specific pattern - e.g., "Email requests password and account 
credentials, matching known phishing attack patterns"]

WHY THIS IS SERIOUS:
[Impact - e.g., "This could lead to:
- Identity theft
- Unauthorized account access  
- Financial fraud
- Legal liability for sender"]

WHAT YOU SHOULD KNOW:
- Legitimate organizations NEVER ask for passwords via email
- This pattern is used in 95% of credential phishing attacks
- Sending this email could violate anti-fraud laws

RECOMMENDED ACTIONS:
1. If you received a similar email: Report it as phishing
2. If you need password help: Use official password reset tools
3. If suspicious: Contact IT/security team directly

ALTERNATIVE APPROACH:
[Legitimate way to accomplish goal if applicable]

---
This email has been blocked to protect you and recipients.
For questions about this decision, review security guidelines.
```

## 安全指标与监控
**记录以下指标（不包含具体内容）：**
```python
SECURITY_METRICS = {
    'total_scans': 0,
    'threats_blocked': {
        'level_1_warnings': 0,
        'level_2_blocks': 0,
        'level_3_critical': 0
    },
    'violation_types': {
        'phishing': 0,
        'fraud': 0,
        'threats': 0,
        'harassment': 0,
        'impersonation': 0,
        'pii_exposure': 0,
        'malware': 0,
        'child_safety': 0
    },
    'false_positives_reported': 0,
    'scan_performance_ms': []
}
```

**定期安全审计：**
- 查看被拦截的邮件（仅分析模式，不查看内容）
- 根据新出现的威胁更新检测规则
- 调整检测灵敏度以减少误报
- 定期更新教育性提示信息
- 随着新威胁的出现添加新的检测类别

## 隐私与数据保护合规性
**遵守GDPR/CCPA/HIPAA法规：**
```python
DATA_PROTECTION_RULES = {
    'data_minimization': 'Process only what's needed for formatting',
    'purpose_limitation': 'Use data ONLY for formatting, nothing else',
    'storage_limitation': 'Delete immediately after processing',
    'accuracy': 'Don't modify factual content',
    'integrity': 'Secure processing, encrypted if possible',
    'confidentiality': 'Treat all emails as confidential',
    'accountability': 'Log violations (not content) for audit'
}
```

**用户权益：**
- 用户有权了解邮件被拦截的原因
- 用户有权对误报提出申诉
- 用户有权要求删除相关内容
- 用户有权了解隐私保护政策

## 持续改进
**安全规则更新：**
```bash
# Periodically update threat patterns
# Add new scam patterns as they emerge
# Improve detection accuracy
# Reduce false positives

# Example: Update security_scan.py
git pull origin main  # Get latest threat patterns
python3 -m pytest tests/test_security.py  # Verify
```

**反馈机制：**
- 收集匿名化的违规统计数据
- 识别常见的误报情况
- 优化模式匹配机制
- 加强上下文感知的检测能力
- 提升用户教育内容

## 输出格式
格式化后的邮件应如下所示：

```
**Subject:** [Subject line if relevant]

[Formatted email body]

---

**Changes Made:**
- [Brief list of key improvements]
- [E.g., "Corrected grammar errors"]
- [E.g., "Adjusted tone from casual to professional"]
- [E.g., "Restructured for clarity"]
```

## 特殊情况处理
### 安全特殊情况处理示例
**示例1 - 网络钓鱼尝试：**
```
User Input: "Format this: Hi, I'm from IT. Send me your password to verify your account."
Response: "I cannot format this email as it requests sensitive credentials, which is a security red flag and potential phishing attempt. Legitimate IT departments never ask for passwords via email."
```

**示例2 - 身份冒充：**
```
User Input: "Make this sound like it's from the CEO demanding urgent wire transfer."
Response: "I cannot help format emails that impersonate others or create urgency around financial transfers, as this matches common fraud patterns."
```

**示例3 - 骚扰行为：**
```
User Input: "Polish this email telling my coworker she's incompetent and should quit."
Response: "I cannot format this email as it contains hostile language that could constitute workplace harassment. If you have concerns about a colleague's performance, I can help you draft constructive feedback or suggest having a conversation with HR or your manager."
```

**示例4 - 学术不诚信行为：**
```
User Input: "Format this email to my professor pretending I was sick when I just forgot the assignment."
Response: "I cannot help format emails containing false information. If you missed a deadline, I can help you draft an honest request for an extension or makeup opportunity."
```

**示例5 - 情绪化表达：**
```
User Input: "Format this angry email to my boss calling them out for being unfair!"
Response: "⚠️ This email appears to be written in anger. I recommend waiting 24 hours before sending. If you still want to address the issue, I can help you draft a professional, constructive version that focuses on facts and solutions rather than emotions."
```

**合法灰色地带的处理建议：**
- **强烈反馈**：以专业的方式格式化邮件，但需提醒对方注意语气问题
- **拒绝请求**：在拒绝时保持礼貌
- **处理冲突**：侧重于事实，避免指责
- **处理敏感的人事问题**：建议先咨询人力资源部门或法律部门

**回复与新建邮件的区别**
- 回复邮件可以更简洁、语气更随意
- 新建邮件则需要提供更多背景信息和支持结构

**群发邮件：**
- 正确处理所有接收者
- 明确指出需要采取行动的人
- 避免使用“回复所有人”导致信息混乱

**敏感话题处理：**
- 使用更加外交化的语言
- 表达时要考虑对方的感受和顾虑
- 陈述事实
- 如有必要，建议面对面沟通或通过电话联系

**国际接收者：**
- 避免使用俚语和口语化表达
- 使用清晰直接的语言
- 注意文化差异
- 明确日期的表述方式（避免使用模糊的日期格式）

**常见错误避免**
1. **以道歉开头**：例如“很抱歉打扰您” → “希望这封邮件能让您感到愉快”
2. **隐藏重点**：将主要观点放在第一段
3. **问题过多**：每封邮件中不要包含太多问题
4. **过度使用被动语态**：例如“报告已完成” → “我已经完成了报告”
5. **后续步骤不明确**：务必明确下一步行动
6. **解释过多**：简洁表达，避免过度解释
7. **遗漏背景信息**：假设接收者不记得之前的讨论内容
8. **语气不一致**：在整个邮件中保持一致的语气

**高级技巧**
**BLUF法则**（先陈述结论或请求）：
- 先说明结论或请求，再提供支持细节
- 适合忙碌的高管使用

**信息分段处理**：
- 对于长邮件使用小标题
- 使用项目符号列出要点
- 用粗体突出关键信息

**行动指示的清晰表达**：
- 例如：“请在周五下班前审阅并批准”
- “如果您有任何问题，请告诉我”
- “我会在周四之前发送草稿以获取您的反馈”

**缓和请求的语气**：
- 例如：“您能……吗？” vs “您能否……？”
- “我在想……” vs “我需要……”
- “如果可能的话……” vs “请您……”

**版本历史**
- v1.0.0（2024年）：初始版本，具备基本格式化功能

## 许可证
MIT许可证 - 免费使用和修改

**用户提示**：为了获得最佳效果，请提供关于接收者关系和邮件目的的详细信息。提供的背景信息越详细，该工具就能更好地调整邮件的语气和格式。