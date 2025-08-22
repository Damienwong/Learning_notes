from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, PageTemplate, Frame
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # 用于注册TTF字体
import os

# ===== 注册中文字体 =====
font_paths = {
    "SimSun": "C:/Windows/Fonts/SimsunExtG.ttf",          # 宋体
    "SimHei": "C:/Windows/Fonts/simhei.ttf",          # 黑体
    "KaiTi": "C:/Windows/Fonts/simkai.ttf",           # 楷体
    "MicrosoftYaHei": "C:/Windows/Fonts/msyh.ttc"     # 微软雅黑
}

# 注册字体（如果字体文件存在）
for font_name, font_path in font_paths.items():
    if os.path.exists(font_path):
        print('注册字体==============')
        pdfmetrics.registerFont(TTFont(font_name, font_path))

# 设置默认中文字体（优先使用微软雅黑，其次是黑体）
if "MicrosoftYaHei" in pdfmetrics.getRegisteredFontNames():
    DEFAULT_CHINESE_FONT = "MicrosoftYaHei"
elif "SimHei" in pdfmetrics.getRegisteredFontNames():
    DEFAULT_CHINESE_FONT = "SimHei"
else:
    DEFAULT_CHINESE_FONT = "Helvetica"  # 回退到英文字体（可能无法显示中文）
print(DEFAULT_CHINESE_FONT)

# ===== 创建PDF文档 =====
doc = SimpleDocTemplate(
    "中文报告.pdf",
    pagesize=A4,
    topMargin=1 * cm,
    bottomMargin=1.5 * cm
)

# ===== 自定义中文样式 =====
styles = getSampleStyleSheet()

# 删除可能冲突的样式
for style_name in ["ReportTitle", "ReportHeading1", "ReportFooter"]:
    if style_name in styles:
        del styles[style_name]

# 创建支持中文的样式
styles.add(ParagraphStyle(
    name="ReportTitle",
    fontName=DEFAULT_CHINESE_FONT,  # 使用中文字体
    fontSize=24,
    alignment=TA_CENTER,
    spaceAfter=20,
    leading=30  # 行高
))

styles.add(ParagraphStyle(
    name="ReportHeading1",
    fontName=DEFAULT_CHINESE_FONT,
    fontSize=16,
    textColor=colors.darkblue,
    spaceBefore=12,
    spaceAfter=6
))

# 正文样式 - 使用中文字体
styles.add(ParagraphStyle(
    name="ChineseBody",
    fontName=DEFAULT_CHINESE_FONT,
    fontSize=10,
    leading=14,  # 行高
    spaceAfter=6,
    wordWrap='CJK'  # 针对中日韩文本的换行
))

styles.add(ParagraphStyle(
    name="ReportFooter",
    fontName=DEFAULT_CHINESE_FONT,
    fontSize=8,
    textColor=colors.grey
))


# ===== 页眉/页脚绘制函数 =====
def add_header_footer(canvas, doc):
    page_num = canvas.getPageNumber()

    # 页眉 - 使用中文
    canvas.saveState()
    canvas.setFont(DEFAULT_CHINESE_FONT, 9)
    canvas.drawString(2 * cm, A4[1] - 1 * cm, "月度业务分析报告")
    canvas.line(1.5 * cm, A4[1] - 1.2 * cm, A4[0] - 1.5 * cm, A4[1] - 1.2 * cm)
    canvas.restoreState()

    # 页脚 - 使用中文
    canvas.saveState()
    canvas.setFont(DEFAULT_CHINESE_FONT, 8)
    canvas.drawString(2 * cm, 1 * cm, "生成时间: 2023-11-15")

    # 居中页码 (中文格式)
    page_text = f"第 {page_num} 页"
    canvas.drawCentredString(A4[0] / 2, 1 * cm, page_text)

    canvas.drawRightString(A4[0] - 2 * cm, 1 * cm, "机密文件")
    canvas.restoreState()


# ===== 创建页面模板 =====
frame = Frame(
    doc.leftMargin, doc.bottomMargin,
    doc.width, doc.height,
    id='normal'
)
template = PageTemplate(
    id='AllPages',
    frames=frame,
    onPage=add_header_footer
)
doc.addPageTemplates([template])

# ===== 报告内容构建 =====
story = []

# === 首页标题页 ===
story.append(Spacer(1, 2 * cm))
story.append(Paragraph("2023年度业务分析报告", styles["ReportTitle"]))
story.append(Spacer(1, 0.5 * cm))
story.append(Image("hollow_knight.jpg", width=3 * cm, height=2 * cm))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("生成部门: 数据分析中心", styles["ChineseBody"]))
story.append(Paragraph("生成日期: 2023年11月15日", styles["ChineseBody"]))
story.append(PageBreak())

# === 目录页 ===
story.append(Paragraph("目录", styles["ReportHeading1"]))
story.append(Spacer(1, 0.3 * cm))

# 中文目录条目
toc_items = [
    "1. 销售数据概览 ...................... 3",
    "2. 区域业绩分析 ...................... 5",
    "3. 产品表现统计 ...................... 8"
]

for item in toc_items:
    story.append(Paragraph(item, styles["ChineseBody"]))

story.append(PageBreak())

# === 正文内容 ===
# 章节1：销售数据概览
story.append(Paragraph("1. 销售数据概览", styles["ReportHeading1"]))
story.append(
    Paragraph("本季度总销售额达到¥1,200,000，同比增长18%。主要增长来自电子产品线，同比增长28%。", styles["ChineseBody"]))

# 插入图表（中文标题）
story.append(Spacer(1, 0.2 * cm))
story.append(Image("hollow_knight.jpg", width=10 * cm, height=6 * cm))
story.append(Paragraph("<b>图1:</b> 2023年各季度销售额对比", styles["ChineseBody"]))
story.append(Spacer(1, 0.3 * cm))

# 创建表格数据（中文表头）
table_data = [
    ["产品线", "第一季度", "第二季度", "第三季度", "同比增长"],
    ["电子产品", "¥320,000", "¥380,000", "¥410,000", "+28%"],
    ["家居用品", "¥180,000", "¥210,000", "¥240,000", "+15%"],
    ["服装", "¥150,000", "¥140,000", "¥170,000", "+8%"],
    ["食品", "¥90,000", "¥110,000", "¥130,000", "+22%"]
]

# 创建表格
sales_table = Table(
    table_data,
    colWidths=[3 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm],
    repeatRows=1
)

# 表格样式（支持中文）
table_style = TableStyle([
    ('FONT', (0, 0), (-1, 0), DEFAULT_CHINESE_FONT),  # 表头使用中文字体
    ('FONT', (0, 1), (-1, -1), DEFAULT_CHINESE_FONT),  # 数据行使用中文字体
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
])
sales_table.setStyle(table_style)
story.append(sales_table)

# 添加更多中文段落
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("关键发现：", styles["ChineseBody"]))
story.append(Paragraph("- 电子产品线表现突出，主要得益于新推出的智能家居系列", styles["ChineseBody"]))
story.append(Paragraph("- 食品类别增长显著，线上渠道销售额同比增长45%", styles["ChineseBody"]))
story.append(Paragraph("- 华北地区销售额最高，占总销售额的35%", styles["ChineseBody"]))

# === 后续内容 ===
story.append(PageBreak())
story.append(Paragraph("2. 区域业绩分析", styles["ReportHeading1"]))
story.append(Paragraph("按区域划分的销售业绩如下表所示：", styles["ChineseBody"]))

# ===== 生成PDF文件 =====
doc.build(story)

print("中文PDF报告生成完成！文件已保存为 '中文报告.pdf'")