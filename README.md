# LangChain 学习实验室

这是根据《尚硅谷大模型技术之 LangChain》整理的中文学习项目，目标是让初学者从 Model I/O 一直走到 RAG、Agent 和 MCP。

## 快速开始

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
$env:PYTHONPATH="src"
python app.py model "什么是 LangChain？"
python app.py rag "RAG 的流程是什么？"
python app.py agent "计算 12 * (3 + 2)"
python tests/run_all.py
```

详细学习顺序、LangChain 真实 API、Ollama/OpenAI 配置、向量库和 MCP 说明见 [`docs/学习教程.md`](docs/学习教程.md)。

## 项目结构

- `src/lab/model_io.py`：提示词、结构化输出和 LCEL 顺序链。
- `src/lab/rag.py`：文档切分、离线检索和引用。
- `src/lab/agent.py`：工具调用、计算器、天气和 thread 记忆。
- `src/lab/mcp_server.py`：MCP Stdio 服务端工具。
- `examples/`：按章节拆开的示例。
- `tests/`：pytest 测试和无 pytest 依赖的 `run_all.py`。

默认实现是教学用离线版本。安装 `.[langchain]`、`.[mcp]` 后，可以逐步替换为真实模型、Chroma/Milvus 和 MCP 服务。
