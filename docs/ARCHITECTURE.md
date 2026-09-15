# 架构

```text
                    ┌─────────────┐
                    │   Zotero    │
                    │ 文献/PDF/注释 │
                    └──────┬──────┘
                           │ 只读为主
                           v
┌────────────────────────────────────────────┐
│              Research Workspace            │
│ PDF 副本 / state / deep-reading / proposal │
└───────────────┬────────────────────────────┘
                │
                v
        ┌───────────────┐
        │ Codex + Skill │
        │ 科研判断/串联   │
        └───────┬───────┘
                │ 提案 + 用户确认
                v
          ┌───────────┐
          │ Obsidian  │
          │ 正式知识库  │
          └───────────┘
```

## 模块层

- Screening：快速筛选
- Deep Reading：教学 + 科研分析
- Knowledge Integration：知识串联与提案
- Zotero：文献入口与状态
- Obsidian：正式知识库
- Paper Types：论文类型模板
- Evidence：证据与引用边界
- Quality Check：轻量自检
- Onboarding：首次使用

## 脚本边界

脚本处理：路径、目录、编号、状态、Zotero API 读写、Vault 文件扫描。

Skill 处理：创新性、方法价值、实验质量、Research Gap、解释与科研判断。
