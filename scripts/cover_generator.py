#!/usr/bin/python3
"""
封面生成工具 v2
生成简洁风格背景 + 标题文字叠加

用法:
    python3 cover_generator.py <分类> <标题>
"""

import os
import sys
import json
import requests
import textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ============== 配置 ==============
IMAGE_GEN_API = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
IMAGE_GEN_TOKEN = "cc205358-72d6-4d90-887e-f8671b10d2b1"
IMAGE_GEN_MODEL = "doubao-seedream-5-0-260128"

IMAGE_UPLOAD_API = "https://img.baidu2022.com/api/v1/upload"
IMAGE_UPLOAD_TOKEN = "8|bS2trmr98QPgyh8XGzPGItpaROK6DvuFW0LEXgxl"
UPLOAD_STRATEGY_ID = 3

# 输出尺寸
OUTPUT_WIDTH = 800
OUTPUT_HEIGHT = 450
OUTPUT_QUALITY = 85

# 中文字体
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# ============== 分类背景风格 ==============
CATEGORY_BACKGROUNDS = {
    "bazi": "中国传统水墨画背景，淡雅米黄色宣纸纹理，淡淡的金色祥云纹样，极简留白，优雅宁静",
    "zhouyi": "古老竹简卷轴纹理背景，深褐色木质纹理，淡淡八卦符号水印，古朴厚重",
    "ziwei": "深邃夜空背景，星光点点，紫蓝色渐变，神秘星象氛围，高贵典雅",
    "fengshui": "山水水墨画背景，远山淡影，云雾缭绕，青灰色调，意境深远",
    "liuyao": "古铜钱纹理背景，暗红色调，神秘烛光氛围，古旧质感",
    "qimen": "九宫格纹样背景，暗金色边框，神秘符咒淡影，帝王气质",
    "wuxing": "五行元素抽象背景，金木水火土符号流动，柔和渐变色彩",
    "general": "传统书房背景，淡淡书卷气息，米白色调，文雅素净"
}

# 文字颜色配置（根据分类）
CATEGORY_TEXT_COLORS = {
    "bazi": "#2c1810",       # 深褐色
    "zhouyi": "#1a1a1a",     # 黑色
    "ziwei": "#ffffff",      # 白色（深色背景）
    "fengshui": "#1e3a2f",   # 深绿色
    "liuyao": "#3d1515",     # 深红色
    "qimen": "#2d1f0f",      # 深棕
    "wuxing": "#1a1a2e",     # 深蓝紫
    "general": "#2c1810"     # 深褐
}


def generate_background(prompt: str) -> str:
    """生成背景图，返回临时URL"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IMAGE_GEN_TOKEN}"
    }
    data = {
        "model": IMAGE_GEN_MODEL,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "2048x2048",
        "stream": False,
        "watermark": False
    }

    print(f"🎨 生成背景中...", file=sys.stderr)
    
    resp = requests.post(IMAGE_GEN_API, headers=headers, json=data, timeout=120)
    resp.raise_for_status()
    result = resp.json()

    if "data" in result and len(result["data"]) > 0:
        url = result["data"][0].get("url")
        if url:
            print(f"✅ 背景生成完成", file=sys.stderr)
            return url

    print(f"❌ 生成失败: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
    sys.exit(1)


def download_image(image_url: str) -> Image.Image:
    """下载图片，返回PIL Image对象"""
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))


def add_title_to_image(img: Image.Image, title: str, category: str) -> Image.Image:
    """在图片上添加标题文字"""
    # 调整尺寸
    img = img.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), Image.Resampling.LANCZOS)
    
    # 转换为RGB
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # 创建绘图对象
    draw = ImageDraw.Draw(img)
    
    # 获取文字颜色
    text_color = CATEGORY_TEXT_COLORS.get(category, "#2c1810")
    
    # 计算字体大小（根据标题长度自适应）
    title_len = len(title)
    if title_len <= 10:
        font_size = 52
    elif title_len <= 15:
        font_size = 44
    elif title_len <= 20:
        font_size = 38
    else:
        font_size = 32
    
    # 加载字体
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
        font_small = ImageFont.truetype(FONT_PATH, font_size // 3)
    except:
        print(f"⚠️ 字体加载失败，使用默认", file=sys.stderr)
        font = ImageFont.load_default()
        font_small = font
    
    # 文字换行处理
    max_chars = int(OUTPUT_WIDTH / (font_size * 0.8))
    lines = textwrap.wrap(title, width=max_chars)
    
    # 计算文字总高度
    line_height = font_size * 1.3
    total_height = len(lines) * line_height
    
    # 计算起始Y位置（垂直居中）
    y = (OUTPUT_HEIGHT - total_height) / 2
    
    # 绘制文字阴影（增加可读性）
    shadow_color = (255, 255, 255, 180) if text_color.startswith("#fff") else (0, 0, 0, 100)
    
    for line in lines:
        # 计算X位置（水平居中）
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (OUTPUT_WIDTH - (bbox[2] - bbox[0])) / 2
        
        # 绘制阴影
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, 80))
        
        # 绘制主文字
        # 转换颜色
        r = int(text_color[1:3], 16)
        g = int(text_color[3:5], 16)
        b = int(text_color[5:7], 16)
        draw.text((x, y), line, font=font, fill=(r, g, b))
        
        y += line_height
    
    return img


def upload_image(img: Image.Image) -> str:
    """上传图片到图床"""
    output = BytesIO()
    img.save(output, format='JPEG', quality=OUTPUT_QUALITY, optimize=True)
    output.seek(0)
    
    headers = {
        "Authorization": f"Bearer {IMAGE_UPLOAD_TOKEN}",
        "Accept": "application/json"
    }

    print(f"📤 上传中...", file=sys.stderr)
    
    resp = requests.post(
        IMAGE_UPLOAD_API,
        headers=headers,
        files={"file": ("cover.jpg", output, "image/jpeg")},
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


def main():
    if len(sys.argv) < 3:
        print("用法: python3 cover_generator.py <分类> <标题>", file=sys.stderr)
        print(f"分类: {', '.join(CATEGORY_BACKGROUNDS.keys())}", file=sys.stderr)
        sys.exit(1)

    category = sys.argv[1]
    title = sys.argv[2]

    # 1. 生成背景prompt
    bg_style = CATEGORY_BACKGROUNDS.get(category, CATEGORY_BACKGROUNDS["general"])
    prompt = f"{bg_style}，简洁干净，没有文字，适合作为背景图"
    
    print(f"📝 标题: {title}", file=sys.stderr)

    # 2. 生成背景图
    bg_url = generate_background(prompt)

    # 3. 下载背景图
    print(f"📥 下载背景...", file=sys.stderr)
    bg_img = download_image(bg_url)

    # 4. 添加标题文字
    print(f"✍️ 添加标题...", file=sys.stderr)
    final_img = add_title_to_image(bg_img, title, category)

    # 5. 上传
    final_url = upload_image(final_img)
    print(f"✅ 完成", file=sys.stderr)

    # 输出URL
    print(final_url)


if __name__ == "__main__":
    main()
