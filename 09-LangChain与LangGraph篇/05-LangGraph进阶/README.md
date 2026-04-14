# 第 09.05 章 - LangGraph 进阶

本章介绍 LangGraph 的进阶功能：记忆管理、中断审核、持久化。

## 学习目标

- 理解记忆系统（短期/长期）
- 实现 Human-in-the-loop
- 掌握状态持久化

## 章节内容

| 序号 | 标题 | 内容 |
|------|------|------|
| 01 | 记忆管理 | State、Store、memory 类型 |
| 02 | 中断与审核 | interrupt、Command(resume) |
| 03 | 持久化 | Checkpointer、thread_id |

## 示例项目

`langgraph_advanced/` - Human-in-the-loop 审批流程