# Paper Reading Skill for Codex

一套面向工科研究生的**单篇论文阅读 → 深度精读 → Obsidian 知识沉淀**工作流。

核心设计：

- Zotero 管文献；
- Obsidian 管知识；
- Codex Skill 负责阅读、科研判断与串联；
- 脚本只做文件/数据层机械工作；
- 主论文必须由你提供 PDF；
- 所有关键判断尽量可追溯；
- Obsidian/Zotero 修改必须先提案、后确认；
- 本地优先、最小权限、可回退、可审计。

## 适合谁

特别适合刚开始系统论文阅读的工科研究生，也能覆盖算法、信号处理、图像、通信、控制、硬件、材料、器件、光学、实验测量等常见工科论文。

## 三阶段

1. **筛选论文**：5–10 分钟导读，判断是否值得精读，并给出重点章节/页码。
2. **精读论文**：生成工作区 Markdown 精读稿；前半教学，后半科研分析。
3. **整理知识库**：结合你的 Obsidian 知识点，把论文重构为“问题—方法—证据—结论”，先提案，确认后写入。

## 推荐目录

```text
paper-reading-skill/          # Skill 工程本身
research-workspace/           # 运行时工作区（建议单独 Git）
  topics/
  papers/
  deep-reading/
  drafts/
  state/
  cache/
  no-records/
ObsidianVault/                # 独立于工作区
  Research/
    <主题>/
      Papers/
      Concepts/
      Methods/
      MOC.md
```

## 快速开始（Windows 11）

1. 安装 Python 3、Git、Zotero Desktop、Obsidian。
2. 在 Zotero 安装 Better BibTeX。
3. 在 Zotero 设置中开启本机应用访问（用于 Local API）。
4. 复制 `config.example.yaml` 为你的运行配置参考。
5. 在 Codex 中加载本 Skill 后说：`初始化论文阅读工作区`。
6. 再说：`创建研究主题`。
7. 把论文保存到 Zotero 并附 PDF，之后说：`筛选论文 <citekey 或标题>`。

详细步骤见：

- `docs/SETUP_WINDOWS.md`
- `docs/ZOTERO_SETUP.md`
- `docs/OBSIDIAN_SETUP.md`
- `docs/WORKFLOW.md`
- `docs/COMMANDS.md`

## 安全边界

- 不直接写 `zotero.sqlite`。
- Zotero 原 PDF 永不修改，只复制到工作区分析。
- Obsidian 正式写入前必须生成修改提案并得到用户确认。
- 主论文没有 PDF 时不进行内容分析，也不自行上网搜索全文。
- 不能核验的数据或结论必须写“暂无 / 无法确认 / 待核验”。

## 技术参考

- OpenAI Skills：`https://openai.com/academy/skills/`
- Zotero Local API：`https://www.zotero.org/support/dev/web_api/v3/local_api`
- Better BibTeX：`https://retorque.re/zotero-better-bibtex/`
- Better BibTeX JSON-RPC：`https://retorque.re/zotero-better-bibtex/exporting/json-rpc/`
- Obsidian Help：`https://help.obsidian.md/`

## 迁移到 macOS

核心 Skill 和 Python 脚本按跨平台路径设计。迁移时主要修改配置中的工作区、Vault 和 Zotero 路径。见 `docs/MACOS_MIGRATION.md`。
