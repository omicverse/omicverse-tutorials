---
orphan: true
---

# AI and Foundation Model Tutorials

This page is a markdown overview for the AI-related tutorials currently exposed in `mkdocs.yml`.

## Foundation Models (`ov.llm.ModelFactory`)

Single-cell foundation models are created with
`ov.llm.ModelFactory.create_model(model_type, model_path, device)` and used
through the returned model object (`get_embeddings`, `predict`, `fine_tune`,
`integrate`, ...). See the [overview](t_fm_guide.md) and the
[overview notebook](t_fm.ipynb).

Integrated models with an executed tutorial:

- [scGPT](t_scgpt.ipynb)
- [Geneformer](t_geneformer.ipynb)
- [scFoundation](t_scfoundation.ipynb)
- [UCE](t_uce.ipynb)
- [CellPLM](t_cellplm.ipynb)

Integrated without an executed tutorial: [scMulan](t_fm_scmulan_guide.md).

The other 16 registered model types (scBERT, GeneCompass, Nicheformer, tGPT,
CellFM, scCello, scPRINT, AIDO.Cell, PULSAR, Tabula, ATACformer, scPlantLLM,
LangCell, Cell2Sentence, GenePT, ChatCell) are placeholders that are **not
integrated yet**; each guide page says what exists and what is missing.

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
