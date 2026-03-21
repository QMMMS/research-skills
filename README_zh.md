# Codex 科研 Skill 套件

[English README](README.md)

这是一套面向 Codex 的轻量科研写作 skill，覆盖系统综述、文献调研、基于证据的写作与修订。📎

## 概览

这套仓库的目标不是重建一个庞大的 research-agent runtime，而是把真正可复用的科研工作流拆成稳定模块：

- skill 负责工作流、产物约束和审稿式检查
- 脚本负责检索、元数据整理、全文回查、引用清洗等确定性步骤
- 可选工程设施保持可选，而不是默认依赖

因此，它可以在不引入本地向量库、重型 reranker 或多 agent runtime 的前提下直接使用。

## 包含内容

- `research-survey-workflow`
  - 端到端系统综述流程：定题、综述引导、语料构建、提纲、写作、修订。
- `research-literature-curation`
  - 多视角文献收集、筛选、paper folder 组织与证据整理。
- `research-outline-synthesis`
  - 读书笔记聚类、粗提纲生成、子节展开和最终整理。
- `research-grounded-writing`
  - 基于来源、证据映射、全文笔记和 section packet 的按节写作。
- `research-review-and-revise`
  - 语料充分性、覆盖范围、结构、引用与修订检查。
- `research-latex-export`
  - 把 Markdown-first 的科研产物导出成 `.tex`、`.bib` 和可选 `.pdf`。

## 工作流总览

完整流程大致分为：

1. 明确主题边界与交付物
2. 先阅读已有综述、教程或 benchmark overview
3. 构建并筛选候选论文池
4. 为全文阅读论文建立结构化笔记和证据映射
5. 在本地 paper folder 上增加一层轻量全文检索
6. 从聚类后的笔记中生成多层提纲
7. 运行提纲 lint，并初始化 `section_packets`
8. 按小节进行 grounded draft 写作
9. 先做结构一致性与引用白名单检查，再审查 coverage、grounding 与结构
10. 修订并产出差异记录与数值化质量门 ✍️
11. 可选导出成 LaTeX 和 PDF

每一阶段也都可以单独作为 skill 使用。

## 为什么这样拆

这个仓库**不是**为了复刻一个完整科研 agent 平台。

它更强调分层设计：

- skill：认知流程、产物约束、审稿式检查
- script：检索、元数据处理、全文回查、引用清洗、参考文献渲染
- 可选基础设施：本地论文库、reranker、大索引

## 推荐使用方式

如果要跑完整流程，建议把 6 个 skill 一起安装。

如果只需要单个阶段，也可以单独使用：

- 只做文献收集：`research-literature-curation`
- 只做提纲：`research-outline-synthesis`
- 只做正文草拟：`research-grounded-writing`
- 只做审阅与修订：`research-review-and-revise`
- 只做 LaTeX 导出：`research-latex-export`

## 安装方式

把一个或多个 skill 文件夹复制到 Codex 的 skills 目录：

- `$CODEX_HOME/skills`
- 或 `~/.codex/skills`

示例结构：

```text
$CODEX_HOME/skills/
  research-survey-workflow/
  research-literature-curation/
  research-outline-synthesis/
  research-grounded-writing/
  research-review-and-revise/
  research-latex-export/
```

每个 skill 真正必需的只有 `SKILL.md`。仓库里附带的脚本和 references 都是为了提高可执行性和可复用性。

## 平台兼容性

- 已在 Windows 11 上完成测试。
- 尚未完成 Linux 和 macOS 的适配验证，实际使用可能需要路径和命令调整。

## 分阶段输出

### 阶段 1：定题与综述引导

- `topic_scope.md`
- `research_questions.md`
- `existing_surveys.md`

### 阶段 2：语料构建

- `candidate_pool.json`
- `screening_decisions.md`
- `source_inventory.json` 或 `source_inventory.md`
- `papers/<paper-id>/metadata.md`
- `papers/<paper-id>/notes.md`
- `papers/<paper-id>/bib.txt`
- `papers/<paper-id>/links.txt`

### 阶段 3：证据与结构

- `evidence_map.json` 或 `evidence_map.md`
- `rough_outlines.md`
- `merged_outline.md`
- `subsection_outline.md`
- `draft_outline.md`
- `refined_outline.md`
- `outline_lint_report.md`
- `section_evidence_index.md`
- `corpus_queries/<query-id>.md`

### 阶段 4：写作与修订

- `section_packets/<section-id>.md`
- `draft_report_raw.md`
- `draft_report_refined.md`
- `draft_report.md`
- `detailed_report.md`
- `coherence_edits.md`
- `citation_whitelist_report.md`
- `outline_conformance_report.md`
- `review_notes.md`
- `revision_delta.md`
- `revised_report.md`
- `quality_gate.json`

### 阶段 5：出版导出

- `latex/main.tex`
- `latex/references.bib`
- `latex/build.log`
- `latex/compile_error.json`
- `latex/citation_gaps.md`
- `latex/paragraph_citation_gaps.md`
- `latex/main.pdf`

### 运行元数据

- `run_manifest.json`
- `state_manifest.json`
- `artifact_validation_report.md`

这些名称只是建议，不是强制要求。

## 设计原则

这套 skill 默认遵循三个原则：

1. 优先简单工作流，而不是大而全 runtime。
2. 优先小脚本，而不是重型服务。
3. 把人工审阅保留为显式检查点。

因此，核心工作流默认不依赖：

- 本地论文向量库
- cross-encoder reranker 服务
- 自定义训练流水线
- 多 agent 编排 runtime

## 语料规模经验值

如果目标是较正式的综述，一个实用的经验值是：

- 初检索候选：`80-150`
- 标题与摘要筛选后：`40-60`
- 全文结构化笔记：`30-40+`

这是工作流上的经验值，不是出版规则。如果主题本身非常窄，应记录原因，而不是假装文献规模足够大。

## 提纲深度经验值

如果目标是较正式的综述：

- refined outline 不应只是平铺的一层 section
- 当全文笔记达到 `20+` 篇时，通常应至少出现 `1.1` 级子节，很多情况下还应出现 `1.1.1`
- 子节边界应来自读书笔记聚类和 evidence map，而不只是套一个通用模板
- 每个子节都应有明确的比较目的、论证目的或证据簇

## 写作经验值

如果目标是较正式的 detailed report：

- 重要小节在写作前先建立 `section_packets/<section-id>.md`
- 不只看 `notes.md`，还要回查 `papers/<paper-id>/src/` 中的全文语料
- 当全文检索对小节写作有实质影响时，留下 `corpus_queries/<query-id>.md`
- 对过薄的小节，先做一轮有界补检索，再决定扩写还是合并

## 附带脚本

- `research-literature-curation/scripts/search_arxiv.py`
  - 简单的 arXiv 检索脚本。
- `research-literature-curation/scripts/export_arxiv_candidates.ps1`
  - Windows 下从多组查询导出去重后的 arXiv 候选论文池。
- `research-literature-curation/scripts/materialize_paper_folders.ps1`
  - 根据选中的候选论文批量生成 paper folder、BibTeX 和链接文件。
- `research-literature-curation/scripts/fetch_arxiv_sources.ps1`
  - 为每个 paper folder 下载并解压 arXiv source。
- `research-literature-curation/scripts/search_corpus.ps1`
  - 在 `papers/` 下对 `notes.md`、`metadata.md` 和 `src/` 全文文件做轻量检索。
- `research-grounded-writing/scripts/normalize_citations.py`
  - 把 `[@source-id]` 这类引用占位替换成数字引用。
- `research-grounded-writing/scripts/render_references.py`
  - 从 JSON 元数据生成 Markdown 参考文献列表。
- `research-outline-synthesis/scripts/lint_outline.py`
  - 对 refined outline 做重复标题、空小节和重叠风险检查。
- `research-grounded-writing/scripts/init_section_packets.py`
  - 从 `refined_outline.md` 批量初始化 section packet 模板与检索预算字段。
- `research-grounded-writing/scripts/check_outline_conformance.py`
  - 检查 `refined_outline.md` 与报告标题层级的一致性。
- `research-grounded-writing/scripts/check_citation_whitelist.py`
  - 检查每个小节是否只引用本小节 packet 白名单中的来源。
- `research-review-and-revise/scripts/quality_gate_scorecard.py`
  - 生成 coverage/structure/relevance/citation 的数值化质量门。
- `research-survey-workflow/scripts/validate_artifacts.py`
  - 校验分阶段产物并生成 `state_manifest.json`。
- `research-latex-export/scripts/export_markdown_to_latex.py`
  - 把 Markdown 研究报告转换成 LaTeX 正文。
- `research-latex-export/scripts/collect_bibtex.py`
  - 把 paper folder 里的 BibTeX 汇总成 `references.bib`。
- `research-latex-export/scripts/compile_latex_project.py`
  - 用 `latexmk` 或 `pdflatex` 编译 LaTeX 项目，并输出 `compile_error.json`。
- `research-latex-export/scripts/audit_paragraph_citations.py`
  - 标出较长但不含任何引用命令的 LaTeX 段落。

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
  research-latex-export/
```

## 最小使用示例

一个实用的模式是：

1. 用 `research-literature-curation` 先读已有综述、收集候选池、建立 paper folder 和 evidence map。
2. 用 `search_corpus.ps1` 针对某个小节的概念词，在本地全文语料中做回查。
3. 用 `research-outline-synthesis` 把笔记聚类成多层 outline。
4. 为重要小节建立 `section_packets/<section-id>.md` 证据包。
5. 用 `research-grounded-writing` 写带来源占位的 section 草稿。
6. 用 `research-review-and-revise` 找 unsupported claims、语料薄弱处、结构重叠和 coverage 缺口。
7. 如有需要，再用脚本清洗引用并生成参考文献列表。
8. 用 `research-latex-export` 导出 `latex/main.tex`、`latex/references.bib`，并在环境可用时编译 `latex/main.pdf`。

## 致谢

这套 skill 的方法设计参考了以下开源项目：

- [STORM](https://github.com/stanford-oval/storm)
- [OpenScholar](https://github.com/AkariAsai/OpenScholar)
- [AutoSurvey](https://github.com/AutoSurveys/AutoSurvey)
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)

这里的目标不是重新打包这些项目，而是提炼其中适合 Codex skill 的可复用工作流。

## 许可证

[MIT](LICENSE)
