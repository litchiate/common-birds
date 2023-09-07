
from PIL import Image, ImageDraw, ImageFont
import os

def merge_images(folder_path, output_path, spacing, title="常见鸟类鉴识图鉴", images_per_row=4):
    # 获取文件夹下的所有图片文件
    image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    if not image_files:
        print("文件夹中没有图片文件。")
        return

    # 加载第一张图片作为基准大小
    base_image = Image.open(os.path.join(folder_path, image_files[0]))
    image_width, image_height = base_image.size

    # 计算合成图片的宽度和高度
    num_images = len(image_files)
    num_rows = (num_images - 1) // images_per_row + 1
    merged_width = image_width * images_per_row + spacing * (images_per_row - 1) + spacing * 2
    merged_height = image_height * num_rows + spacing * (num_rows) + spacing * 2

    print("merged_width %d, merged_height %d" % (merged_width, merged_height))

    # 创建空白合成图片
    merged_image = Image.new('RGB', (merged_width, merged_height), color='white')
    draw = ImageDraw.Draw(merged_image)

    # 加载字体
    font = ImageFont.truetype("msyh.ttc", 48)  # 分类字体大小

    # 设置标题位置和样式
    title_x = merged_width // 2
    title_y = 10
    title_font = ImageFont.truetype("msyh.ttc", 56)  # 标题字体大小

    # 绘制标题
    title_width, title_height = draw.textsize(title, font=title_font)
    draw.text((title_x - title_width // 2, title_y), title, fill='black', font=title_font)

    # 逐个处理每张图片
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(folder_path, image_file)

        # 打开图片文件
        image = Image.open(image_path)

        # 图片缩放
        image = image.resize((image_width, image_height))

        # 计算当前图片所在行和列
        row = i // images_per_row
        col = i % images_per_row

        # 计算图片位置
        image_x = (image_width + spacing) * col + spacing
        image_y = title_height + spacing + (image_height + spacing) * row

        # 将图片粘贴到合成图片上
        merged_image.paste(image, (image_x, image_y))

        # 添加文件名
        file_name = os.path.splitext(image_file)[0]
        text_width, text_height = draw.textsize(file_name, font=font)
        text_x = image_x + (image_width - text_width) // 2
        text_y = image_y + image_height
        draw.text((text_x, text_y), file_name[2:], fill='black', font=font)  # 去除文件名之前的序号
        # print("%d, %d"%(text_x,text_y))

    # 保存合成图片
    merged_image.save(output_path)

    print("图片合成完成。")

# 指定文件夹路径、输出路径和间距
folder_path = r"C:\Users\Leon\PycharmProjects\common birds\img\source"
output_path = r"C:\Users\Leon\PycharmProjects\common birds\img\output_image.jpg"
spacing = 70

# 调用合成图片函数
merge_images(folder_path, output_path, spacing, images_per_row=4)
