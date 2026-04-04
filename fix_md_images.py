# 批量修复 Markdown 图片路径中的空格
# 使用方法：把此脚本放到项目根目录运行

import os
import re

def fix_md_images(md_file):
    """修复单个 md 文件的图片路径"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有图片路径
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # 如果路径中有空格，用 %20 替换
        if ' ' in img_path:
            new_path = img_path.replace(' ', '%20')
            print(f"修复: {img_path} -> {new_path}")
            return f'![{alt_text}]({new_path})'
        
        return match.group(0)
    
    new_content = re.sub(pattern, replace_path, content)
    
    # 写回文件
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已修复: {md_file}")

# 遍历所有 md 文件
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.md'):
            md_path = os.path.join(root, file)
            fix_md_images(md_path)

print("\n全部修复完成！")
