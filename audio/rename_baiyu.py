# -*- coding: utf-8 -*-
"""
白语录音批量重命名脚本
------------------------
用法：
  1. 把这个脚本文件放到 baiyu 文件夹【外面】，跟 baiyu 文件夹同级
     （或者直接把下面 FOLDER 改成 baiyu 文件夹的完整路径）。
  2. 确保 baiyu 文件夹里现在的 100 个录音文件名里带有数字编号
     （比如 1.m4a / 录音01.m4a / rec_1.m4a 都可以，只要数字能看出顺序）。
  3. 用命令行运行：  python rename_baiyu.py
     第一次运行会先"预览"改名结果，不会真的改，确认没问题后
     再按提示输入 y 真正执行。

⚠️ 重要：脚本是按"文件名里的数字大小"排序后，依次对应到
   Excel 表里第 1～100 个词条（我、你、我们、这、那……）。
   如果您实际录音的顺序跟 Excel 表词序不一致，改出来的名字
   会对不上，请务必先看预览结果里"原文件名 -> 新文件名"是否
   和您录的内容一致，不对的话手动调整文件名里的数字顺序后
   再运行。
"""

import re
import sys
from pathlib import Path

# ↓↓↓ 如果脚本没有和 baiyu 文件夹放在一起，把这里改成文件夹的完整路径 ↓↓↓
FOLDER = Path(__file__).parent / "baiyu"

# 按 Excel 表格顺序排列的 100 个词条（不要改动这个列表）
WORDS = [
    '我',
    '你',
    '我们',
    '这',
    '那',
    '谁',
    '什么',
    '不',
    '所有',
    '许多',
    '一',
    '二',
    '大',
    '长',
    '小',
    '女',
    '男',
    '人',
    '鱼',
    '鸟',
    '狗',
    '虱',
    '树',
    '种子',
    '树叶',
    '根',
    '树皮',
    '皮肤',
    '肉',
    '血',
    '骨',
    '脂肪',
    '蛋',
    '角',
    '尾',
    '羽毛',
    '头发',
    '头',
    '耳朵',
    '眼睛',
    '鼻子',
    '口',
    '牙齿',
    '舌头',
    '爪子',
    '脚',
    '膝盖',
    '手',
    '腹部',
    '脖子',
    '胸部',
    '心',
    '肝',
    '喝',
    '吃',
    '咬',
    '看',
    '听',
    '知道',
    '睡觉',
    '死',
    '杀',
    '游泳',
    '飞',
    '走',
    '来',
    '躺',
    '坐',
    '站立',
    '给',
    '说',
    '太阳',
    '月亮',
    '星星',
    '水',
    '雨',
    '石头',
    '沙',
    '土壤',
    '云',
    '烟',
    '火',
    '烟灰',
    '烧',
    '小路',
    '山脉',
    '红色',
    '绿色',
    '黄色',
    '白色',
    '黑色',
    '夜',
    '热',
    '冷',
    '满',
    '新',
    '好',
    '圆',
    '干燥',
    '名'
]

def natural_key(path: Path):
    """从文件名中提取数字用于排序，没有数字的排最后。"""
    m = re.search(r"\d+", path.stem)
    return (0, int(m.group())) if m else (1, path.name)

def main():
    if not FOLDER.exists():
        print(f"找不到文件夹：{FOLDER}\n请检查 FOLDER 路径是否正确。")
        sys.exit(1)

    files = [p for p in FOLDER.iterdir() if p.is_file() and not p.name.startswith(".")]
    files.sort(key=natural_key)

    if len(files) != len(WORDS):
        print(f"⚠️ 警告：文件夹里有 {len(files)} 个文件，但词表有 {len(WORDS)} 条，数量不一致！")
        print("请检查是否有多余/缺失的文件，确认无误后再继续。\n")

    plan = []
    for i, f in enumerate(files):
        if i >= len(WORDS):
            break
        new_name = f"{i+1:04d}{WORDS[i]}{f.suffix}"
        plan.append((f, FOLDER / new_name))

    print("预览重命名结果（原文件名 -> 新文件名）：\n")
    for old, new in plan:
        print(f"  {old.name:20s} -> {new.name}")

    print(f"\n共 {len(plan)} 个文件将被重命名。")
    answer = input("确认按以上顺序重命名吗？输入 y 执行，其他任意键取消：")
    if answer.strip().lower() != "y":
        print("已取消，没有改动任何文件。")
        return

    for old, new in plan:
        if new.exists() and new != old:
            print(f"  ⚠️ 目标文件名已存在，跳过：{new.name}")
            continue
        old.rename(new)
    print("重命名完成。")

if __name__ == "__main__":
    main()
