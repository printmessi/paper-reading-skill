# 单篇论文完整工作流

## 0. 入库

在 Zotero：

1. 论文加入对应研究主题 Collection；
2. 附上 PDF；
3. 设置 `状态/待读`；
4. Better BibTeX 生成 citekey。

## 1. 筛选论文

对 Codex 说：

> 筛选论文 <citekey 或标题>

Codex 应：

1. 从 Zotero 找到条目；
2. 确认 PDF 存在；
3. 复制 PDF 到工作区；
4. 自动识别论文类型；
5. 输出 5–10 分钟导读；
6. 给出四档推荐；
7. 标出阅读重点与章节/页码；
8. 给出“只花 20 分钟怎么读”。

如果 No：

- 保存简短 No 记录到工作区；
- 建议 Zotero `状态/No`；
- 不进入 Obsidian。

## 2. 精读论文

对 Codex 说：

> 精读论文 <citekey>

Codex 应：

1. 使用主论文 PDF；
2. 教学式解释前置知识、方法、公式、图表；
3. 科研式分析实验、创新、局限、可复现性；
4. 默认少量外部横向对比；
5. 生成 active recall；
6. 输出 `deep-reading.md` 到工作区；
7. 建议 Zotero `状态/整理`。

## 3. 你自己补知识点

在 Obsidian 当前研究主题内写自己的理解、概念节点、问题和灵感。

AI 不代替这一步。

## 4. 整理知识库

对 Codex 说：

> 整理知识库 <citekey>

Codex 应：

1. 读取精读稿；
2. 只扫描指定主题目录；
3. 读取可选 Zotero 注释；
4. 先串联已有材料；
5. 针对你的理解缺口，少量逐个提问；
6. 询问是否启用 YAML/Properties；
7. 生成 `knowledge-update-proposal.md`；
8. 等待确认。

## 5. 完成论文笔记

你确认提案后：

> 完成论文笔记

Codex 才能：

- 创建/更新最终论文主笔记；
- 创建必要知识节点；
- 更新 MOC；
- 保留更新记录；
- 建议 Git diff；
- 建议 Zotero `状态/已读`。

## 6. 更新 Zotero

只有你明确说：

> 更新 Zotero 状态为 已读

才允许执行真实写入。
