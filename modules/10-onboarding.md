# 模块 10：首次使用引导

当用户第一次使用，按以下顺序介绍，不要一次倾倒所有细节；每完成一段给出检查点。

## 1. 说明角色

- Zotero：文献
- Obsidian：知识
- Codex：阅读和串联
- 工作区：中间产物

## 2. 检查环境

说明需要：Python 3、Git、Zotero Desktop、Obsidian、Better BibTeX。

运行 `scripts/init_workspace.py --check-only` 只检查，不自动安装。

## 3. Zotero

指导开启 Local API、本地安装 BBT、确认 citekey、Collection/Tag 规则。

## 4. Obsidian

让用户选择 Vault 和 Research 根目录。第一版不要求 REST API/MCP。

## 5. 创建工作区

运行初始化脚本。默认工作区和 Vault 分离。

## 6. 创建第一个研究主题

先展示将创建哪些目录/状态配置；确认后执行 `scripts/create_topic.py`。

## 7. 完整示例

引导用户查看 `examples/README.md`，理解：待读 → 筛选 → 精读 → 整理 → 已读。

## 8. 安全提示

强调：

- 不自动装软件
- 不直接写 Zotero SQLite
- 不无确认改 Obsidian
- 主论文无 PDF 不分析
- 不确定就写暂无
