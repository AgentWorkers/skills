# debug-pro

系统化的调试方法论及特定语言的调试命令。

## 七步调试流程

1. **重现问题** — 确保问题能够一致性地发生。记录问题的具体步骤、输入参数以及运行环境。
2. **隔离问题** — 缩小问题的影响范围。通过注释掉相关代码、使用二分查找法（`git bisect`）来定位问题所在。
3. **提出假设** — 对问题的根本原因形成一个具体且可验证的猜测。
4. **添加调试工具** — 添加针对性的日志记录、断点或断言语句。
5. **验证假设** — 确认问题的根本原因。如果假设错误，返回步骤3。
6. **修复问题** — 仅应用最必要的修复措施。在调试过程中避免进行重构。
7. **回归测试** — 编写测试用例来检测该问题是否仍然存在，并确保测试通过。

## 特定语言的调试方法

### JavaScript / TypeScript
```bash
# Node.js debugger
node --inspect-brk app.js
# Chrome DevTools: chrome://inspect

# Console debugging
console.log(JSON.stringify(obj, null, 2))
console.trace('Call stack here')
console.time('perf'); /* code */ console.timeEnd('perf')

# Memory leaks
node --expose-gc --max-old-space-size=4096 app.js
```

### Python
```bash
# Built-in debugger
python -m pdb script.py

# Breakpoint in code
breakpoint()  # Python 3.7+

# Verbose tracing
python -X tracemalloc script.py

# Profile
python -m cProfile -s cumulative script.py
```

### Swift
```bash
# LLDB debugging
lldb ./MyApp
(lldb) breakpoint set --name main
(lldb) run
(lldb) po myVariable

# Xcode: Product → Profile (Instruments)
```

### CSS / 布局
```css
/* Outline all elements */
* { outline: 1px solid red !important; }

/* Debug specific element */
.debug { background: rgba(255,0,0,0.1) !important; }
```

### 网络相关问题
```bash
# HTTP debugging
curl -v https://api.example.com/endpoint
curl -w "@curl-format.txt" -o /dev/null -s https://example.com

# DNS
dig example.com
nslookup example.com

# Ports
lsof -i :3000
netstat -tlnp
```

### Git Bisect
```bash
git bisect start
git bisect bad              # Current commit is broken
git bisect good abc1234     # Known good commit
# Git checks out middle commit — test it, then:
git bisect good  # or  git bisect bad
# Repeat until root cause commit is found
git bisect reset
```

## 常见错误类型及解决方法

| 错误类型 | 可能原因 | 解决方案 |
|---------|-------------|---------|
| `Cannot read property of undefined` | 未进行空值检查或数据格式错误 | 使用可选链操作符（`?.`）或验证数据格式 |
| `ENOENT` | 文件/目录不存在 | 检查路径，创建目录（使用`existsSync`函数） |
| `CORS error` | 后端未设置正确的CORS头信息 | 添加包含正确源地址的CORS中间件 |
| `Module not found` | 依赖项未安装或导入路径错误 | 使用`npm install`命令安装依赖项，检查`tsconfig`文件中的路径设置 |
| `Hydration mismatch`（React） | 服务器和客户端渲染的HTML不一致 | 确保渲染结果一致，对于仅客户端渲染的部分使用`useEffect`生命周期钩子 |
| `Segmentation fault` | 内存损坏或空指针异常 | 检查数组边界和指针的有效性 |
| `Connection refused` | 服务未在指定端口上运行 | 检查服务是否启动，验证端口和主机地址 |
| `Permission denied` | 文件/网络权限问题 | 检查文件权限设置、防火墙配置或使用`sudo`命令 |

## 快速诊断命令
```bash
# What's using this port?
lsof -i :PORT

# What's this process doing?
ps aux | grep PROCESS

# Watch file changes
fswatch -r ./src

# Disk space
df -h

# System resource usage
top -l 1 | head -10
```