# OmicVerse 文档

## 一站式转录组全域分析流程

![omicverse-abstract](https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/background_light.png)

**OmicVerse v2** 是一个面向现代转录组学与多组学分析的统一 Python 框架。
它将 **bulk RNA-seq**、**单细胞**、**空间转录组学**、**可视化**、
**基于模型的分析** 以及 **AI 辅助工作流** 集于一体。

如果 OmicVerse 对您的研究有所帮助，请考虑引用
[OmicVerse 论文](https://www.nature.com/articles/s41467-024-50194-3)。

::::{grid} 1 2 3 3
:gutter: 2

:::{grid-item-card} 安装 {octicon}`plug;1em;`
:link: Installation_guild
:link-type: doc

初次使用 _omicverse_？通过 conda、pip 或 Docker 搭建您的环境。
:::

:::{grid-item-card} 教程 {octicon}`play;1em;`
:link: tutorials/index
:link-type: doc

涵盖 bulk、单细胞、空间转录组学及 AI 辅助工作流的分步教程。
:::

:::{grid-item-card} API 参考 {octicon}`book;1em;`
:link: api/index
:link-type: doc

OmicVerse 中每个公开函数和类的详细说明。
:::

:::{grid-item-card} OmicClaw {octicon}`cpu;1em;`
:link: omicclaw/index
:link-type: doc

通过 Telegram、飞书、MCP 等平台将 OmicVerse 部署为对话式 AI 智能体。
:::

:::{grid-item-card} 讨论 {octicon}`megaphone;1em;`
:link: https://github.com/Starlitnightly/omicverse/discussions

需要帮助？欢迎在我们的 GitHub Discussions 论坛提问。
:::

:::{grid-item-card} GitHub {octicon}`mark-github;1em;`
:link: https://github.com/Starlitnightly/omicverse

发现了 bug？想参与贡献？请访问我们的 GitHub。
:::
::::

```{toctree}
:hidden: true
:maxdepth: 3
:titlesonly: true

Installation_guild
Feature_coverage
tutorials/index
omicclaw/index
api/index
Release_notes
Developer_guild
GPU_supported_registry_functions
Discussion <https://github.com/Starlitnightly/omicverse/discussions>
GitHub <https://github.com/Starlitnightly/omicverse>
```
