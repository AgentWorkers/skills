---
name: rose-container-tools
version: 0.1.0
description: 使用部署在 Docker 容器中的 ROSE 工具来构建和运行 ROSE 编译器工具。这些工具适用于开发源到源翻译器、调用图分析器、抽象语法树（AST）处理器，或任何需要链接到 librose.so 的工具。相关命令包括：“ROSE tool”、“callgraph”、“AST traversal”、“source-to-source”、“build with ROSE”以及“librose”。
---

# ROSE容器工具

使用安装在容器中的ROSE来构建和运行基于ROSE的源代码分析工具。

## ⚠️ 必须使用Makefile

**切勿使用自定义脚本或命令行进行ROSE工具的编译。**

- 所有构建操作都应使用`Makefile`；
- 支持使用`make -j`进行并行编译；
- 确保编译参数的一致性；
- 支持使用`make check`进行测试。

## 为什么使用容器？

ROSE需要GCC 7-10版本以及特定的Boost版本，而大多数现代主机并不具备这些环境。容器提供了以下优势：
- 容器中预先安装了ROSE（位于`/rose/install`目录）；
- 配置了正确的编译工具链；
- 所有依赖项都已预先配置好。

## 快速入门

### 1. 启动容器

```bash
# If container exists
docker start rose-tools-dev
docker exec -it rose-tools-dev bash

# Or create new container
docker run -it --name rose-tools-dev \
  -v /home/liao/rose-install:/rose/install:ro \
  -v $(pwd):/work \
  -w /work \
  rose-dev:latest bash
```

### 2. 使用Makefile进行构建

**构建ROSE工具时必须使用Makefile，切勿使用自定义脚本。**

```bash
# Inside container
make        # Build all tools
make check  # Build and test
```

### 3. 运行工具

```bash
./build/my_tool -c input.c
```

## Makefile（必备）

为你的工具创建一个`Makefile`文件：

```makefile
ROSE_INSTALL = /rose/install

CXX      = g++
CXXFLAGS = -std=c++14 -Wall -g -I$(ROSE_INSTALL)/include/rose
LDFLAGS  = -L$(ROSE_INSTALL)/lib -Wl,-rpath,$(ROSE_INSTALL)/lib
LIBS     = -lrose

BUILDDIR = build
SOURCES  = $(wildcard tools/*.cpp)
TOOLS    = $(patsubst tools/%.cpp,$(BUILDDIR)/%,$(SOURCES))

.PHONY: all clean check

all: $(TOOLS)

$(BUILDDIR)/%: tools/%.cpp
	@mkdir -p $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS) $(LIBS)

check: all
	@for tool in $(TOOLS); do \
		echo "Testing $$tool..."; \
		LD_LIBRARY_PATH=$(ROSE_INSTALL)/lib $$tool -c tests/hello.c; \
	done

clean:
	rm -rf $(BUILDDIR)
```

## 示例：身份转换器（Identity Translator）

这是一个简单的ROSE工具，用于解析和反解析代码：

```cpp
// tools/identity.cpp
#include "rose.h"

int main(int argc, char* argv[]) {
    SgProject* project = frontend(argc, argv);
    if (!project) return 1;
    
    AstTests::runAllTests(project);
    return backend(project);
}
```

构建并运行该工具：
```bash
make
./build/identity -c tests/hello.c
# Output: rose_hello.c (unparsed)
```

## 示例：调用图生成器（Call Graph Generator）

```cpp
// tools/callgraph.cpp
#include "rose.h"
#include <CallGraph.h>

int main(int argc, char* argv[]) {
    ROSE_INITIALIZE;
    SgProject* project = new SgProject(argc, argv);
    
    CallGraphBuilder builder(project);
    builder.buildCallGraph();
    
    AstDOTGeneration dotgen;
    dotgen.writeIncidenceGraphToDOTFile(
        builder.getGraph(), "callgraph.dot");
    
    return 0;
}
```

## 示例：AST节点计数器（AST Node Counter）

```cpp
// tools/ast_stats.cpp
#include "rose.h"
#include <map>

class NodeCounter : public AstSimpleProcessing {
public:
    std::map<std::string, int> counts;
    
    void visit(SgNode* node) override {
        if (node) counts[node->class_name()]++;
    }
};

int main(int argc, char* argv[]) {
    SgProject* project = frontend(argc, argv);
    
    NodeCounter counter;
    counter.traverseInputFiles(project, preorder);
    
    for (auto& [name, count] : counter.counts)
        std::cout << name << ": " << count << "\n";
    
    return 0;
}
```

## 常用的ROSE头文件

| 头文件 | 用途 |
|--------|---------|
| `rose.h` | 主要头文件（包含大部分功能） |
| `CallGraph.h` | 用于生成调用图 |
| `AstDOTGeneration.h` | 用于生成AST图的DOT格式输出 |
| `sageInterface.h` | 用于操作AST的实用函数 |

## AST遍历模式

### 简单遍历（先序/后序）
```cpp
class MyTraversal : public AstSimpleProcessing {
    void visit(SgNode* node) override {
        // Process each node
    }
};

MyTraversal t;
t.traverseInputFiles(project, preorder);
```

### 自上而下的遍历（包含继承属性）
```cpp
class MyTraversal : public AstTopDownProcessing<int> {
    int evaluateInheritedAttribute(SgNode* node, int depth) override {
        return depth + 1;  // Pass to children
    }
};
```

### 自下而上的遍历（包含合成属性）
```cpp
class MyTraversal : public AstBottomUpProcessing<int> {
    int evaluateSynthesizedAttribute(SgNode* node, 
        SynthesizedAttributesList childAttrs) override {
        int sum = 0;
        for (auto& attr : childAttrs) sum += attr;
        return sum + 1;  // Return to parent
    }
};
```

## 在容器中进行测试

```bash
# Run from host
docker exec -w /work rose-tools-dev make check

# Or interactively
docker exec -it rose-tools-dev bash
cd /work
make && make check
```

## 故障排除

### “找不到rose.h”
```bash
# Check include path
echo $ROSE/include/rose
ls $ROSE/include/rose/rose.h
```

### “无法找到-lrose”
```bash
# Check library path
ls $ROSE/lib/librose.so
```

### 运行时错误：“找不到librose.so”
```bash
# Set library path
export LD_LIBRARY_PATH=$ROSE/lib:$LD_LIBRARY_PATH
```

### 处理大文件时出现段错误（Segment Fault）
```bash
# Increase stack size
ulimit -s unlimited
```

## 容器目录结构

| 目录 | 内容 |
|------|----------|
| `/rose/install` | ROSE的安装目录（头文件、库文件、可执行文件） |
| `/rose/install/include/rose` | 头文件目录 |
| `/rose/install/lib` | librose.so及依赖库文件 |
| `/rose/install/bin` | ROSE工具（如identityTranslator等） |
| `/work` | 挂载的工作区（用于存放你的代码） |