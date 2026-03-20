# Codex 科研 Skill 套件

[English README](README.md)

这是一个面向 Codex 的轻量科研 skill 套件，主要覆盖以下任务：🔎

- 文献调研
- 综述写作
- 基于证据的草稿生成
- 审阅与修订

## 概览

这套 skill 的核心思路是把科研写作流程拆成稳定的几个阶段，并把不同类型的工作分层处理：

- skill 负责工作流、产物合同和审稿式检查
- 脚本负责检索、元数据处理、引用清洗等确定性工作
- 可选基础设施保持为可选，而不是默认依赖

因此，这套 skill 可以在不引入本地论文库、复杂 reranker 服务或多 agent runtime 的情况下直接使用。

## 仓库包含什么

- `research-survey-workflow`
  - 端到端主流程：定题、调研、提纲、写作、修订。
- `research-literature-curation`
  - 多视角文献收集与证据整理。
- `research-outline-synthesis`
  - 粗提纲生成、合并、子节展开和最终整理。
- `research-grounded-writing`
  - 按 section 写作，并绑定来源与证据。
- `research-review-and-revise`
  - coverage、结构、引用和修订检查。

## 工作流总览

完整流程大致分为：

1. 明确主题边界与交付形式
2. 收集来源并整理证据
3. 生成并修订提纲
4. 按 section 写基于来源的正文
5. 审查 coverage、grounding 与结构
6. 修订并在需要时清洗引用 ✍️

每一步也都可以单独使用。

## 为什么这样拆

这个仓库**不是**为了复刻一个完整 research-agent runtime。

它更强调分层设计：

- skill：认知流程、产物合同、审稿式检查
- script：检索、元数据处理、引用清洗、参考文献渲染
- 可选基础设施：本地论文库、reranker、大索引

## 推荐使用方式

完整工作流建议五个 skill 一起安装。

如果只需要某个阶段，也可以单独使用：

- 只做文献收集：`research-literature-curation`
- 只做提纲：`research-outline-synthesis`
- 只做正文草稿：`research-grounded-writing`
- 只做审阅修订：`research-review-and-revise`

## 安装方式

把一个或多个 skill 文件夹复制到 Codex 的 skills 目录：

- `$CODEX_HOME/skills`
- 或者 `~/.codex/skills`

示例：

```text
$CODEX_HOME/skills/
  research-survey-workflow/
  research-literature-curation/
  research-outline-synthesis/
  research-grounded-writing/
  research-review-and-revise/
```

每个 skill 最核心的文件只有一个：`SKILL.md`。

## 建议的中间产物

这套 skill 围绕以下中间产物组织工作：

- `topic_scope.md`
- `research_questions.md`
- `source_inventory.json`
- `evidence_map.json`
- `draft_outline.md`
- `refined_outline.md`
- `draft_report.md`
- `review_notes.md`
- `revised_report.md`

这些只是建议命名，不是强制要求。

## 设计原则

这套 skill 默认遵循三个原则：

1. 优先选择简单流程，而不是大而全 runtime。
2. 优先选择小脚本，而不是重工程服务。
3. 人类审阅必须保留为显式阶段。

因此，核心工作流不依赖：

- 本地论文向量库
- cross-encoder reranker 服务
- 自定义训练流程
- 多 agent 编排 runtime

## 附带的小脚本

- `research-literature-curation/scripts/search_arxiv.py`
  - 简单的 arXiv 检索脚本。
- `research-grounded-writing/scripts/normalize_citations.py`
  - 把 `[@source-id]` 这种引用占位替换成数字引用。
- `research-grounded-writing/scripts/render_references.py`
  - 从 JSON 元数据生成 Markdown 参考文献列表。

这些脚本都尽量保持轻量、易替换。

## 仓库结构

```text
research-skills/
  README.md
  README_zh.md
  research-survey-workflow/
  research-literature-curation/
  research-outline-synthesis/
  research-grounded-writing/
  research-review-and-revise/
```

## 最小使用示例

一种实用的使用方式如下：

1. 先用 `research-literature-curation` 收集来源并建立 evidence map。
2. 再用 `research-outline-synthesis` 生成 draft outline 和 refined outline。
3. 使用 `research-grounded-writing` 按 section 写带来源占位的草稿。
4. 使用 `research-review-and-revise` 检查 unsupported claims、结构重复和 coverage 缺口。
5. 如有需要，再用附带脚本清洗引用并生成参考文献列表。

## 致谢

这套 skill 的方法设计参考了以下开源项目：

- [STORM](https://github.com/stanford-oval/storm)
- [OpenScholar](https://github.com/AkariAsai/OpenScholar)
- [AutoSurvey](https://github.com/AutoSurveys/AutoSurvey)
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)

这里的目标不是重新打包这些项目，而是提炼其中适合 Codex skill 的可复用工作流。

## 许可证

[MIT](LICENSE)
