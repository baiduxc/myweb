#!/usr/bin/env python3
"""
每日命理文章自动创作脚本
根据当前文章分布，自动选择分类创作新文章
"""
import os
import re
import random
from datetime import datetime
from pathlib import Path

# 项目路径
PROJECT_DIR = Path("/root/myweb")
BLOG_DIR = PROJECT_DIR / "src/content/blog"

# 8个分类
CATEGORIES = ["zhouyi", "bazi", "ziwei", "fengshui", "qimen", "liuyao", "wuxing", "general"]

# 分类中文名称
CAT_NAMES = {
    "zhouyi": "周易",
    "bazi": "八字",
    "ziwei": "紫微斗数",
    "fengshui": "风水",
    "qimen": "奇门遁甲",
    "liuyao": "六爻",
    "wuxing": "五行",
    "general": "命理综合"
}

# 每个分类的文章主题库（可扩展）
TOPICS = {
    "zhouyi": [
        ("六十四卦详解系列", "详解各卦象含义与应用"),
        ("周易与人生智慧", "从周易角度解读人生"),
        ("易学入门基础", "周易基础知识系列"),
        ("卦象实战解析", "实际占卜案例分析"),
    ],
    "bazi": [
        ("十神详解系列", "深入解析各十神含义"),
        ("格局论命", "各种格局的判断方法"),
        ("用神取法", "如何选取用神"),
        ("八字实战案例", "名人八字分析"),
        ("神煞详解", "各种神煞的含义与应用"),
    ],
    "ziwei": [
        ("十四主星详解", "紫微斗数主星系列"),
        ("辅星系列", "左辅右弼文昌文曲等"),
        ("宫位解读", "十二宫位的含义"),
        ("四化应用", "化禄化权化科化忌"),
        ("格局分析", "紫微斗数经典格局"),
    ],
    "fengshui": [
        ("阳宅风水", "居家风水布局"),
        ("阴宅风水", "墓地风水知识"),
        ("玄空飞星", "玄空风水理论"),
        ("形峦理气", "风水两派要义"),
        ("择日学", "风水择日方法"),
    ],
    "qimen": [
        ("奇门排盘", "奇门遁甲排盘方法"),
        ("九星八门", "奇门核心元素"),
        ("格局吉凶", "奇门格局分析"),
        ("实战应用", "奇门预测案例"),
    ],
    "liuyao": [
        ("六爻基础", "六爻预测入门"),
        ("用神取法", "六爻用神详解"),
        ("六亲含义", "六爻六亲解读"),
        ("断卦技巧", "实战断卦方法"),
    ],
    "wuxing": [
        ("五行基础", "五行生克制化"),
        ("天干地支", "干支详解系列"),
        ("旺衰理论", "五行旺衰判断"),
        ("纳音五行", "六十甲子纳音"),
    ],
    "general": [
        ("命理学习心得", "学习方法与经验"),
        ("命理发展史", "命理学发展脉络"),
        ("古籍解读", "经典命理著作解析"),
        ("综合应用", "多种术数综合运用"),
    ],
}

def get_existing_counts():
    """统计现有文章各分类数量"""
    counts = {cat: 0 for cat in CATEGORIES}
    
    for mdx_file in BLOG_DIR.glob("*.mdx"):
        try:
            content = mdx_file.read_text(encoding='utf-8')
            match = re.search(r"category: '(\w+)'", content)
            if match:
                cat = match.group(1)
                if cat in counts:
                    counts[cat] += 1
        except:
            continue
    
    return counts

def select_categories(counts, num_articles=12):
    """选择今天要创作的分类（优先补充薄弱分类）"""
    # 按数量排序，少的优先
    sorted_cats = sorted(counts.items(), key=lambda x: x[1])
    
    selected = []
    for cat, count in sorted_cats:
        if len(selected) >= num_articles:
            break
        # 薄弱分类多创作几篇
        if count < 3:
            selected.extend([cat] * min(3, num_articles - len(selected)))
        elif count < 5:
            selected.extend([cat] * min(2, num_articles - len(selected)))
        else:
            selected.append(cat)
    
    # 如果还不够，从所有分类中随机选
    while len(selected) < num_articles:
        selected.append(random.choice(CATEGORIES))
    
    random.shuffle(selected)
    return selected[:num_articles]

def generate_article(category, index):
    """生成一篇文章（这里用占位符，实际需要LLM生成）"""
    topics = TOPICS.get(category, TOPICS["general"])
    topic_idx = index % len(topics)
    main_topic, topic_desc = topics[topic_idx]
    
    cat_name = CAT_NAMES[category]
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 生成唯一slug
    slug = f"{category}-{today.replace('-', '')}-{index}"
    
    # 这里是简化版，实际应该调用LLM生成完整内容
    title = f"{cat_name}{main_topic}（{today}）"
    description = f"本文讲解{cat_name}领域的{topic_desc}相关知识。"
    
    content = f"""---
title: '{title}'
description: '{description}'
date: {today}
category: '{category}'
tags: ['{cat_name}', '{main_topic}', '每日创作']
---

# {title}

> 本文由每日自动创作任务生成，待进一步完善。

## 引言

{topic_desc}是{cat_name}学习中的重要内容，本文将从基础概念讲起，逐步深入。

## 基础概念

（此处应有详细内容）

## 核心要点

（此处应有详细内容）

## 实战应用

（此处应有详细内容）

## 注意事项

（此处应有详细内容）

---

> **学习要点**：本文为自动生成，后续将进行内容完善和优化。
"""
    
    return slug, content

def main():
    """主函数"""
    print(f"=== 每日文章创作任务 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    
    # 统计现有文章
    counts = get_existing_counts()
    print("\n现有文章统计：")
    total = 0
    for cat, count in sorted(counts.items(), key=lambda x: x[1]):
        print(f"  {CAT_NAMES[cat]}: {count}篇")
        total += count
    print(f"  总计: {total}篇")
    
    # 选择今天要创作的分类
    num_to_create = random.randint(10, 15)
    categories = select_categories(counts, num_to_create)
    
    print(f"\n今日创作计划: {num_to_create}篇文章")
    cat_plan = {}
    for cat in categories:
        cat_plan[cat] = cat_plan.get(cat, 0) + 1
    for cat, count in sorted(cat_plan.items()):
        print(f"  {CAT_NAMES[cat]}: {count}篇")
    
    # 生成文章（实际项目中这里应该调用LLM）
    # 这里只做占位，真正的内容生成需要在Hermes中执行
    print("\n⚠️  注意：此脚本仅统计和规划，实际内容创作需要Hermes执行")
    print("建议通过Hermes的cronjob任务来调用完整的创作流程")
    
    return counts, categories

if __name__ == "__main__":
    main()
