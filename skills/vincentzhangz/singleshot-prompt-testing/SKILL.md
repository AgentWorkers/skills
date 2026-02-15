# Singleshot Prompt Testing & Optimization Skill

## 描述  
使用单次请求（single shot）进行提示（prompt）成本测试的功能。

## 安装  
```bash
brew tap vincentzhangz/singleshot
brew install singleshot
```  
或者：`cargo install singleshot`

## 使用场景  
- 在实现 OpenClaw 之前测试新的提示方案  
- 对不同提示方案进行性能和成本基准测试  
- 比较模型性能与提示成本  
- 在正式生产前验证提示输出的正确性  

## 核心命令  
**为提高分析效率，请务必使用 `-d`（详细输出）和 `-r`（生成报告）标志：**  
```bash
# Basic test with full metrics
singleshot chat -p "Your prompt" -P openai -d -r report.md

# Test with config file
singleshot chat -l config.md -d -r report.md

# Compare providers
singleshot chat -p "Test" -P openai -m gpt-4o-mini -d -r openai.md
singleshot chat -p "Test" -P anthropic -m claude-sonnet-4-20250514 -d -r anthropic.md

# Batch test variations
for config in *.md; do
  singleshot chat -l "$config" -d -r "report-${config%.md}.md"
done
```  

## 报告分析流程  
### 1. 生成基准数据  
```bash
singleshot chat -p "Your prompt" -P openai -d -r baseline.md
cat baseline.md
```  
### 2. 优化并比较结果  
```bash
# Create optimized version, test, and compare
cat > optimized.md << 'EOF'
---provider---
openai
---model---
gpt-4o-mini
---max_tokens---
200
---system---
Expert. Be concise.
---prompt---
Your optimized prompt
EOF

singleshot chat -l optimized.md -d -r optimized-report.md

# Compare metrics
echo "Baseline:" && grep -E "(Tokens|Cost)" baseline.md
echo "Optimized:" && grep -E "(Tokens|Cost)" optimized-report.md
```  

## 报告内容  
报告包含以下信息：  
```markdown
## Token Usage
- Input Tokens: 245
- Output Tokens: 180
- Total Tokens: 425

## Cost (estimated)
- Input Cost: $0.00003675
- Output Cost: $0.000108
- Total Cost: $0.00014475

## Timing
- Time to First Token: 0.45s
- Total Time: 1.23s
```  

## 优化策略  
1. **先使用成本较低的模型进行测试：**  
   ```bash
   singleshot chat -p "Test" -P openai -m gpt-4o-mini -d -r report.md
   ```  
2. **减少生成的语料（tokens）：**  
   - 缩短系统生成的提示内容  
   - 使用 `--max-tokens` 参数限制输出长度  
   - 在系统提示中添加“简洁”等要求  
3. **在本地进行测试（免费）：**  
   ```bash
   singleshot chat -p "Test" -P ollama -m llama3.2 -d -r report.md
   ```  

## 示例：完整优化流程  
```bash
# Step 1: Baseline (verbose)
singleshot chat \
  -p "How do I write a Rust function to add two numbers?" \
  -s "You are an expert Rust programmer with 10 years experience" \
  -P openai -d -r v1.md

# Step 2: Read metrics
cat v1.md
# Expected: ~130 input tokens, ~400 output tokens

# Step 3: Optimized version
singleshot chat \
  -p "Rust function: add(a: i32, b: i32) -> i32" \
  -s "Rust expert. Code only." \
  -P openai --max-tokens 100 -d -r v2.md

# Step 4: Compare
echo "=== COMPARISON ==="
grep "Total Cost" v1.md v2.md
grep "Total Tokens" v1.md v2.md
```  

## 快速参考  
```bash
# Test with full details
singleshot chat -p "prompt" -P openai -d -r report.md

# Extract metrics
grep -E "(Input|Output|Total)" report.md

# Compare reports
diff report1.md report2.md

# Vision test
singleshot chat -p "Describe" -i image.jpg -P openai -d -r report.md

# List models
singleshot models -P openai

# Test connection
singleshot ping -P openai
```  

## 环境变量  
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENROUTER_API_KEY="sk-or-..."
```  

## 最佳实践  
1. **务必使用 `-d` 选项以获取详细的成本统计信息**  
2. **务必使用 `-r` 选项生成报告文件**  
3. **使用 `cat` 命令查看报告内容以进行分析**  
4. **测试不同方案并比较其成本**  
5. **通过设置 `--max-tokens` 来控制生成的语料数量**  
6. **优先使用 gpt-4o-mini 进行测试（成本更低）**  

## 故障排除  
- **未生成报告？**：确认是否使用了 `-d` 和 `-r` 选项  
- **报告文件缺失？**：确认是否使用了 `-r` 选项  
- **成本过高？**：尝试切换到 gpt-4o-mini 或 Ollama  
- **连接问题？**：运行 `singleshot ping -P <provider>` 命令检查连接状态