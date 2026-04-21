#!/usr/bin/python3
"""
封面生成工具 - 创作文章时调用
生成AI封面图 → 调整尺寸压缩 → 上传图床 → 返回图片URL

用法:
    python3 cover_generator.py <分类> <标题>
    
示例:
    python3 cover_generator.py bazi "八字十神详解"
    python3 cover_generator.py fengshui "罗盘使用方法"
    
输出: 图片URL（用于写入文章frontmatter的cover字段）
"""

import os
import sys
import json
import requests
from io import BytesIO

# 图片处理
from PIL import Image

# ============== 配置 ==============
IMAGE_GEN_API = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
IMAGE_GEN_TOKEN = "cc205358-72d6-4d90-887e-f8671b10d2b1"
IMAGE_GEN_MODEL = "doubao-seedream-5-0-260128"

IMAGE_UPLOAD_API = "https://img.baidu2022.com/api/v1/upload"
IMAGE_UPLOAD_TOKEN = "8|bS2trmr98QPgyh8XGzPGItpaROK6DvuFW0LEXgxl"
UPLOAD_STRATEGY_ID = 3

# 生成尺寸（API最小要求）
GEN_SIZE = "2048x2048"

# 最终输出尺寸（网站封面优化）
OUTPUT_WIDTH = 800      # 宽度
OUTPUT_HEIGHT = 450     # 高度（16:9 比例）
OUTPUT_QUALITY = 75     # JPEG质量 (1-100)

# ============== 分类Prompt模板 ==============
CATEGORY_PROMPTS = {
    "bazi": "中国传统八字命理，天干地支符号排列，命盘排盘，阴阳五行元素交织，水墨画风格，古朴典雅，金色装饰线条，神秘东方玄学美学",
    "zhouyi": "周易八卦，太极阴阳图旋转，六十四卦符号，古老竹简卷轴，青铜器纹样，深邃玄学氛围，水墨意境，中国古典美学",
    "ziwei": "紫微斗数星象图，十二宫位格子，紫微星垣，古代天文星图，星座连线，夜空星辰闪烁，神秘宫殿背景，华丽金色点缀",
    "fengshui": "风水堪舆山水画，罗盘指南针特写，古典亭台楼阁，自然山川河流龙脉，云雾缭绕仙境，中国传统风水美学，宁静深远",
    "liuyao": "六爻占卜铜钱卦象，三枚古铜钱抛掷瞬间，爻线符号，卜筮器具，古书卷轴翻阅，神秘烛光摇曳，道教符咒，东方古朴神秘",
    "qimen": "奇门遁甲九宫格局，八门九星排列，古代排兵布阵，军事阵法图，神秘符咒阵盘，帝王气象，中国古典壮观气势",
    "wuxing": "五行元素金木水火土循环，阴阳太极旋转，自然元素融合流转，东方哲学抽象美学，色彩丰富层次分明",
    "general": "中国传统命理学，阴阳五行太极八卦，古朴书卷笔墨，神秘东方玄学美学，水墨意境，金色点缀，典雅大气"
}

STYLE_SUFFIX = "，电影级光影，细腻色彩层次，真实质感，艺术构图，超高清细节"


def generate_image(prompt: str) -> str:
    """调用AI生成图片，返回图片临时URL"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IMAGE_GEN_TOKEN}"
    }
    data = {
        "model": IMAGE_GEN_MODEL,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": GEN_SIZE,
        "stream": False,
        "watermark": False
    }

    print(f"🎨 生成封面中...", file=sys.stderr)
    
    resp = requests.post(IMAGE_GEN_API, headers=headers, json=data, timeout=120)
    resp.raise_for_status()
    result = resp.json()

    if "data" in result and len(result["data"]) > 0:
        url = result["data"][0].get("url")
        if url:
            print(f"✅ 图片生成完成 (2048x2048)", file=sys.stderr)
            return url

    print(f"❌ 生成失败: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
    sys.exit(1)


def process_image(image_url: str) -> BytesIO:
    """下载图片、调整尺寸、压缩质量，返回处理后的图片字节流"""
    print(f"📥 下载原图...", file=sys.stderr)
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    
    # 打开图片
    img = Image.open(BytesIO(resp.content))
    print(f"   原始尺寸: {img.size[0]}x{img.size[1]}", file=sys.stderr)
    
    # 调整尺寸（使用高质量重采样）
    img_resized = img.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), Image.Resampling.LANCZOS)
    print(f"📐 调整尺寸: {OUTPUT_WIDTH}x{OUTPUT_HEIGHT}", file=sys.stderr)
    
    # 转换为RGB（去除alpha通道，如果有的话）
    if img_resized.mode in ('RGBA', 'P'):
        img_resized = img_resized.convert('RGB')
    
    # 压缩为JPEG
    output = BytesIO()
    img_resized.save(output, format='JPEG', quality=OUTPUT_QUALITY, optimize=True)
    output.seek(0)
    
    # 显示压缩效果
    original_size = len(resp.content)
    compressed_size = output.getbuffer().nbytes
    ratio = (1 - compressed_size / original_size) * 100
    print(f"🗜️ 压缩完成: {original_size//1024}KB → {compressed_size//1024}KB (节省{ratio:.0f}%)", file=sys.stderr)
    
    return output


def upload_image(image_data: BytesIO, filename: str = "cover.jpg") -> str:
    """上传图片到图床，返回永久URL"""
    headers = {
        "Authorization": f"Bearer {IMAGE_UPLOAD_TOKEN}",
        "Accept": "application/json"
    }

    print(f"📤 上传到图床...", file=sys.stderr)
    
    resp = requests.post(
        IMAGE_UPLOAD_API,
        headers=headers,
        files={"file": (filename, image_data, "image/jpeg")},
        data={"strategy_id": UPLOAD_STRATEGY_ID},
        timeout=60
    )
    resp.raise_for_status()
    result = resp.json()

    if result.get("status"):
        url = result.get("data", {}).get("links", {}).get("url")
        if url:
            return url

    print(f"❌ 上传失败: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
    sys.exit(1)


def build_prompt(category: str, title: str) -> str:
    """组合生成prompt"""
    base = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["general"])
    
    # 从标题提取增强关键词
    keyword_map = {
        "八字": "八字命盘天干地支", "紫微": "紫微星盘宫位",
        "风水": "山水格局罗盘", "周易": "八卦易经卦象",
        "六爻": "铜钱爻卦", "奇门": "九宫八门遁甲",
        "五行": "金木水火土循环", "阴阳": "太极阴阳平衡",
        "十神": "十神关系图", "格局": "命局结构",
        "宫位": "十二宫格", "星曜": "星曜排列",
        "罗盘": "罗盘特写", "八卦": "八卦符号",
        "入门": "古籍书卷初学", "基础": "基础理论典籍",
        "详解": "古书注解详述", "简史": "历史长卷",
    }
    keywords = ""
    for key, val in keyword_map.items():
        if key in title:
            keywords += val + "，"
    
    prompt = f"{base}，{keywords}{STYLE_SUFFIX}"
    return prompt


def main():
    if len(sys.argv) < 3:
        print("用法: python3 cover_generator.py <分类> <标题>", file=sys.stderr)
        print(f"分类: {', '.join(CATEGORY_PROMPTS.keys())}", file=sys.stderr)
        sys.exit(1)

    category = sys.argv[1]
    title = sys.argv[2]

    # 1. 组合prompt
    prompt = build_prompt(category, title)
    print(f"📝 Prompt: {prompt[:60]}...", file=sys.stderr)

    # 2. 生成图片（2048x2048）
    image_url = generate_image(prompt)

    # 3. 下载并处理图片（调整尺寸+压缩）
    processed_image = process_image(image_url)

    # 4. 上传图床
    final_url = upload_image(processed_image)
    print(f"✅ 封面就绪", file=sys.stderr)

    # 输出最终URL（stdout，供调用方获取）
    print(final_url)


if __name__ == "__main__":
    main()
