# Coq Platform 安装指南

## 方式一：手动下载安装（推荐）

### 步骤1：下载安装包

直接访问以下链接下载：

**Rocq Platform 2025.08.3 (Windows x86_64)**
- 下载地址：https://github.com/rocq-prover/platform/releases/download/2025.08.3/Rocq-Platform-release-2025.08.3-version.9.0.2025.08-Windows-x86_64-UNSIGNED.exe
- 文件大小：约 505 MB

或者访问Releases页面选择其他版本：
- https://github.com/rocq-prover/platform/releases

### 步骤2：运行安装程序

1. 双击下载的 `.exe` 文件
2. 选择 "Full Installation"（完整安装）
3. 选择安装路径（建议使用默认路径）
4. 等待安装完成（约15-30分钟）

### 步骤3：验证安装

安装完成后，打开命令提示符，输入：

```cmd
coqc --version
```

应该显示类似：
```
Coq 9.0.0 (2025.08)
```

---

## 方式二：使用安装脚本（自动下载）

### 脚本位置

`d:\project\code\maths\黎曼猜想\coq_verification\download_coq.ps1`

### 使用方法

1. 右键点击 `download_coq.ps1`
2. 选择 "使用PowerShell运行"
3. 按照提示操作

### 注意

如果自动下载失败（网络问题），请使用方式一手动下载。

---

## 方式三：在线使用（无需安装）

如果不想安装，可以使用在线Coq平台：

### Coq Playground
- 网址：https://coq.inria.fr/coq-with-a-web-browser
- 优点：无需安装，直接在浏览器中使用
- 缺点：性能可能较慢

### JsCoq
- 网址：https://jscoq.github.io/
- 优点：完全基于Web，无需安装
- 缺点：可能不支持所有Coq库

---

## 安装后配置

### 设置环境变量（如果需要）

1. 右键 "此电脑" → "属性"
2. 点击 "高级系统设置"
3. 点击 "环境变量"
4. 在 "系统变量" 中找到 "Path"
5. 添加Coq安装路径，例如：
   ```
   C:\Program Files\Rocq Platform 9.0.0\bin
   ```

### 打开证明文件

1. 启动 Coq IDE
2. 文件 → 打开
3. 浏览到：`d:\project\code\maths\黎曼猜想\coq_verification\Riemann_Hypothesis.v`
4. 打开文件

### 验证证明

1. 按 `Ctrl+B` 编译整个文件
2. 或使用菜单：验证 → 编译
3. 查看底部 "消息" 窗口查看编译结果

---

## 常见问题

### Q1: 安装后找不到Coq IDE？

**答**：在开始菜单中搜索 "Coq IDE" 或 "Rocq Platform"

### Q2: 编译时提示缺少库？

**答**：确保选择了 "Full Installation" 安装所有组件

### Q3: 编译很慢怎么办？

**答**：这是正常的，首次编译需要较长时间

### Q4: 部分证明失败？

**答**：这是预期的，论文中的部分证明需要进一步补充

---

## 验证流程图

```
┌─────────────────────────────────────────────┐
│  1. 下载 Coq Platform                       │
│     ↓                                       │
│  2. 安装 (选择 Full Installation)           │
│     ↓                                       │
│  3. 启动 Coq IDE                            │
│     ↓                                       │
│  4. 打开 Riemann_Hypothesis.v               │
│     ↓                                       │
│  5. 按 Ctrl+B 编译                          │
│     ↓                                       │
│  6. 查看结果                                │
│     - 绿色 = 成功                           │
│     - 红色 = 有错误                          │
└─────────────────────────────────────────────┘
```

---

## 下一步

完成安装后，你可以：

1. **验证论文中的证明脚本**
   - 打开 `Riemann_Hypothesis.v`
   - 逐个引理验证

2. **学习Coq基础**
   - https://coq.inria.fr/documentation
   - Software Foundations (免费在线书籍)

3. **完善证明**
   - 修复 `Admitted` 部分
   - 添加缺失的引理

---

**祝你验证顺利！**
