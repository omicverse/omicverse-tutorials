---
orphan: true
---

# AI and Foundation Model Tutorials

This page is a markdown overview for the AI-related tutorials currently exposed in `mkdocs.yml`.

## Foundation Models (`ov.llm.SCLLMManager`)

The supported entry point for single-cell foundation models is the
high-level `ov.llm.SCLLMManager` manager — see each tutorial for
checkpoint setup, embedding extraction, annotation, and integration.

- [scGPT](t_scgpt.ipynb)
- [Geneformer](t_geneformer.ipynb)
- [scFoundation](t_scfoundation.ipynb)
- [UCE](t_uce.ipynb)
- [CellPLM](t_cellplm.ipynb)

## OmicClaw and Gateway

- Gateway and channel tutorials
  - [OmicClaw Gateway Overview](../Tutorials-jarvis/t_msg_bot_overview.md)
  - [Setup and Auth](../Tutorials-jarvis/t_setup_auth.md)
  - [Telegram Tutorial](../Tutorials-jarvis/t_channel_telegram.md)
  - [Feishu Tutorial](../Tutorials-jarvis/t_channel_feishu.md)
  - [iMessage Tutorial](../Tutorials-jarvis/t_channel_imessage.md)
  - [QQ Tutorial](../Tutorials-jarvis/t_channel_qq.md)
  - [Session Workflow](../Tutorials-jarvis/t_session_commands.md)
  - [Common Issues](../Tutorials-jarvis/t_troubleshooting.md)
- MCP tutorials
  - [MCP Overview](t_mcp_guide.md)
- Notebook / pipeline workflows
  - [J.A.R.V.I.S. with PBMC3k](t_ov_agent_pbmc3k.ipynb)
  - [J.A.R.V.I.S. with Ten-Task Suite](ov_agent_ten_task_suite.ipynb)
