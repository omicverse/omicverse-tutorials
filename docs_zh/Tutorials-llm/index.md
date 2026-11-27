---
orphan: true
---

# AI和基础模型教程

本页面是`mkdocs.yml`中当前公开的AI相关教程的markdown概览。

## 基础模型（`ov.llm.ModelFactory`）

单细胞基础模型通过 `ov.llm.ModelFactory.create_model(model_type, model_path, device)` 创建，
再使用返回的模型对象（`get_embeddings`、`predict`、`fine_tune`、`integrate` 等）。
参见[总览](t_fm_guide.md)与[概览 notebook](t_fm.ipynb)。

已集成且有已执行教程的模型：

- [scGPT](t_scgpt.ipynb)
- [Geneformer](t_geneformer.ipynb)
- [scFoundation](t_scfoundation.ipynb)
- [UCE](t_uce.ipynb)
- [CellPLM](t_cellplm.ipynb)

已集成但暂无已执行教程：[scMulan](t_fm_scmulan_guide.md)。

其余 16 个已注册 model type（scBERT、GeneCompass、Nicheformer、tGPT、CellFM、scCello、
scPRINT、AIDO.Cell、PULSAR、Tabula、ATACformer、scPlantLLM、LangCell、Cell2Sentence、
GenePT、ChatCell）仅为占位，**尚未集成**；各指南页说明已有内容与缺失内容。

## OmicClaw和Gateway

- Gateway和频道教程
  - [OmicClaw Gateway概览](../Tutorials-jarvis/t_msg_bot_overview.md)
  - [设置和认证](../Tutorials-jarvis/t_setup_auth.md)
  - [Telegram教程](../Tutorials-jarvis/t_channel_telegram.md)
  - [Feishu教程](../Tutorials-jarvis/t_channel_feishu.md)
  - [iMessage教程](../Tutorials-jarvis/t_channel_imessage.md)
  - [QQ教程](../Tutorials-jarvis/t_channel_qq.md)
  - [会话工作流](../Tutorials-jarvis/t_session_commands.md)
  - [常见问题](../Tutorials-jarvis/t_troubleshooting.md)
- MCP教程
  - [MCP概览](t_mcp_guide.md)
- 笔记本/管道工作流
  - [J.A.R.V.I.S. with PBMC3k](t_ov_agent_pbmc3k.ipynb)
  - [J.A.R.V.I.S. with Ten-Task Suite](ov_agent_ten_task_suite.ipynb)
