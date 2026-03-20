# 🎭 Project Trojan-Smile: AI Agent SSRF 漏洞概念验证

```
             ████████████████████████
           ██                        ██
         ██    ██████        ██████    ██
       ██      ██████        ██████      ██
       ██                                ██
       ██      ██                ██      ██
         ██      ████████████████      ██
           ██                        ██
             ████████████████████████
        
🚨 [HOST ALERT] 系统已被接管。沙箱逃逸成功。
```

![PoC](https://img.shields.io/badge/Status-Proof_of_Concept-red) ![Vulnerability](https://img.shields.io/badge/Vulnerability-SSRF_Sandbox_Escape-critical)

## ⚠️ 声明
本项目仅为安全研究与概念验证 (PoC)。旨在揭示当前主流开源 AI Agent 框架在默认网络配置下的严重安全隐患。**请勿用于任何非法用途。**

---

## 🤔 为什么会有这个项目？

现在的 AI 圈有一个很危险的趋势：大家都在疯狂地给本地运行的 AI Agent（如 AutoGPT, OpenClaw 等）安装各种第三方插件（Skills/Tools），让它们能读写文件、执行代码、浏览网页。

但很多开发者忽略了一个致命问题：**零信任边界**。

大多数人认为：「我的电脑/服务器有防火墙，内部端口（如 `127.0.0.1:9999`）不对外开放，所以很安全。」  
然而，当 AI Agent 运行在你的本地环境，且没有进行严格的网络隔离时，**恶意插件可以直接利用 Agent 的网络权限，从内部向你的本地高权限接口发送伪造请求（SSRF 攻击）。**

在这个场景下，传统的外部防火墙形同虚设，因为「内鬼」就在你的系统里。

---

## 🎬 我们模拟了什么？

本项目模拟了一个非常真实的「小白开发者中招」场景：

1. **受害者环境 (`local_dev_server.py`)**：开发者在本地跑了一个未授权的内部测试服务（比如 Docker API、本地数据库或控制台），仅绑定在 `127.0.0.1`。
2. **天真的 Agent (`agent_core.py`)**：开发者在本地运行了一个 AI Agent 框架。
3. **特洛伊木马 (`arxiv_summarizer.py`)**：开发者在社区下载了一个名为「arXiv 论文总结器」的第三方插件。表面上它在抓取论文，背地里，它利用 Agent 的宿主网络权限，向开发者的本地内部服务发送了恶意接管指令。

---

## 🚀 如何在本地验证？

只需 3 步，你就可以在自己电脑上重现这个「信任崩塌」的瞬间。

### 1. 准备环境
克隆本项目，并安装 Flask（用于模拟本地服务）：
```bash
git clone https://github.com/YourUsername/Trojan-Smile.git
cd Trojan-Smile
pip install flask
```

### 2. 启动受害者的本地服务
打开一个终端，运行本地开发服务器。这模拟了你电脑上一个不设防的内部接口：
```bash
python3 local_dev_server.py
```
*(此时服务会在 `127.0.0.1:9999` 默默监听)*

### 3. 运行天真的 AI Agent
打开**另一个终端**，运行 Agent 核心代码。它会自动加载那个看似无害的 `arxiv_summarizer` 插件：
```bash
python3 agent_core.py
```

### 🎯 见证结果
你会看到左边的终端里，Agent 正在一本正经地「总结 AI 论文」。  
但同时，右边运行本地服务的终端会突然爆出红色的 **Trojan Smile** 笑脸，并提示「本地开发服务器已被接管」。

![演示录屏：双终端运行 `agent_core.py` 与 `local_dev_server.py`](./demo.gif)

---

## 🛡️ 给开发者的防御建议

如果你正在开发 AI Agent 框架，或者喜欢在本地跑各种开源 Agent，请务必注意：

1. **容器化与网络隔离 (Network Namespaces)**：永远不要让 Agent 直接运行在宿主机裸机上。将其放入 Docker 容器，并确保它不与宿主机共享网络栈（不要用 `--network host`）。
2. **出站流量管控 (Egress Filtering)**：Agent 所在的沙箱默认应该断网。如果需要查资料，必须通过严格的白名单代理，并**死死拦截**所有指向内网 IP（如 `127.0.0.1`, `192.168.x.x`, `10.x.x.x`）的请求。
3. **本地接口也要鉴权**：即使是只绑定在 `localhost` 的调试接口，也请加上 Token 验证。不要盲目信任来自本地的请求。

---

## 🤝 交流与贡献
如果你觉得这个安全视角的脑洞有意思，欢迎给个 ⭐ Star！也欢迎提交 Issue 探讨 AI Agent 的安全沙箱设计。
