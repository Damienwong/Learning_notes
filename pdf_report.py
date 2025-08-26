#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: haibo.wang
@Date: 2025/8/23
@Description: 
"""


from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, NextPageTemplate, Frame, PageTemplate,
    ListFlowable, ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # 用于注册TTF字体
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from typing import List, Dict, Union, Tuple, Optional
import os
import time
from PIL import Image as PILImage


class PDFReportGenerator:
    def __init__(self, filename: str, title: str = "测试报告", page_size: str = "A4"):
        """
        初始化PDF报告生成器

        Args:
            filename: 输出文件名
            title: 报告标题
            page_size: 页面大小，可选"A4"或"letter"
        """

        # ===== 注册中文字体 =====
        font_paths = {
            "SimSun": "C:/Windows/Fonts/simsun.ttc",  # 宋体
            "SimHei": "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "KaiTi": "C:/Windows/Fonts/simkai.ttf",  # 楷体
            "MicrosoftYaHei": "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
        }

        # 注册字体（如果字体文件存在）
        for font_name, font_path in font_paths.items():
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    print(f'成功注册字体: {font_name}')
                except:
                    print(f'注册字体失败: {font_name}')

        # 设置默认中文字体（优先使用微软雅黑，其次是黑体）
        if "MicrosoftYaHei" in pdfmetrics.getRegisteredFontNames():
            self.DEFAULT_CHINESE_FONT = "MicrosoftYaHei"
        elif "SimHei" in pdfmetrics.getRegisteredFontNames():
            self.DEFAULT_CHINESE_FONT = "SimHei"
        elif "SimSun" in pdfmetrics.getRegisteredFontNames():
            self.DEFAULT_CHINESE_FONT = "SimSun"
        else:
            self.DEFAULT_CHINESE_FONT = "Helvetica"  # 回退到英文字体（可能无法显示中文）
            print("警告: 未找到中文字体，中文显示可能不正常")

        self.filename = filename
        self.title = title

        page_size_map = {
            "A4": A4,
            "letter": letter,
            "PPT_STANDARD": (10 * inch, 7.5 * inch),  # 标准4:3
            "PPT_WIDESCREEN": (13.333 * inch, 7.5 * inch),  # 宽屏16:9
            "PPT_WIDESCREEN_16_10": (13.333 * inch, 8.333 * inch)  # 宽屏16:10
        }
        self.page_size = page_size_map.get(page_size, A4)

        self.doc = SimpleDocTemplate(
            filename,
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # 获取样式表
        self.styles = getSampleStyleSheet()

        # 自定义样式
        self._define_custom_styles()

        # 目录条目收集
        self.toc_entries = []

        # 故事流（内容容器）
        self.story = []

        # 页面标记 - 用于标识特定页面的开始
        self.page_markers = {}

        # 当前章节级别
        self.current_chapter_level = 0

    def _define_custom_styles(self):
        """定义自定义样式"""
        # 报告标题样式
        self.styles.add(ParagraphStyle(
            name='Heading_0',
            fontName=self.DEFAULT_CHINESE_FONT,
            alignment=TA_CENTER,
            fontSize=42,
            spaceAfter=56,
        ))
        # 标题样式
        self.styles.add(ParagraphStyle(
            name='Heading_1',
            fontName=self.DEFAULT_CHINESE_FONT,  # 使用中文字体
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        ))

        self.styles.add(ParagraphStyle(
            name='Heading_2',
            fontName=self.DEFAULT_CHINESE_FONT,  # 使用中文字体
            fontSize=14,
            spaceAfter=10,
            textColor=colors.navy
        ))

        self.styles.add(ParagraphStyle(
            name='Heading_3',
            fontName=self.DEFAULT_CHINESE_FONT,  # 使用中文字体
            fontSize=12,
            spaceAfter=8,
            textColor=colors.darkblue
        ))

        # 正文样式
        self.styles.add(ParagraphStyle(
            name='BodyText_1',
            fontName=self.DEFAULT_CHINESE_FONT,  # 使用中文字体
            fontSize=10,
            spaceAfter=6
        ))

        # 页眉页脚样式
        self.styles.add(ParagraphStyle(
            name='HeaderFooter_1',
            fontName=self.DEFAULT_CHINESE_FONT,  # 使用中文字体
            fontSize=8,
            textColor=colors.gray
        ))

        # 目录样式
        self.styles.add(ParagraphStyle(
            name='TOC_1',
            fontName=self.DEFAULT_CHINESE_FONT,  # 使用中文字体
            fontSize=10,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=6,
            spaceAfter=6
        ))

    def _header_footer_canvas(self, canvas: canvas.Canvas, doc):
        """创建页眉页脚"""
        # 保存当前状态
        canvas.saveState()

        # 页眉 - 使用中文字体
        header_text = f"{self.title} - 测试报告"
        canvas.setFont(self.DEFAULT_CHINESE_FONT, 8)
        canvas.drawString(doc.leftMargin, doc.pagesize[1] - 0.5 * inch, header_text)

        # 页脚 - 页码
        # page_num = canvas.getPageNumber()
        # footer_text = f"第 {page_num} 页"
        # canvas.setFont(self.DEFAULT_CHINESE_FONT, 8)
        # canvas.drawCentredString(doc.pagesize[0] / 2, 0.5 * inch, footer_text)

        # 页脚 - 日期
        date_text = time.strftime("%Y-%m-%d %H:%M:%S")
        canvas.drawString(doc.pagesize[0] - doc.rightMargin - 100, 0.5 * inch, date_text)

        # 恢复状态
        canvas.restoreState()

    def add_report_name(self, text: str, level: int = 0):
        """
        添加报告标题
        :param text:
        :param level:
        :return:
        """
        style_name = f'Heading_{level}'
        self.current_chapter_level = level
        title = Paragraph(text, self.styles[style_name])
        self.story.append(title)
        self.story.append(Spacer(1, 12))

    def add_title(self, text: str, level: int = 1):
        """
        添加标题

        Args:
            text: 标题文本
            level: 标题级别 (1, 2, 3)
        """
        style_name = f"Heading_{level}"
        self.current_chapter_level = level

        # 添加到目录
        self.toc_entries.append((level, text, len(self.story)))

        # 添加到内容
        title = Paragraph(text, self.styles[style_name])
        self.story.append(title)
        self.story.append(Spacer(1, 12))

        return self

    def add_text(self, text: str, style: str = "BodyText_1"):
        """
        添加文本段落

        Args:
            text: 文本内容
            style: 样式名称
        """
        paragraph = Paragraph(text, self.styles[style])
        self.story.append(paragraph)
        self.story.append(Spacer(1, 6))

        return self

    def add_table(self, data: List[List[str]],
                  col_widths: Optional[List[float]] = None,
                  style: TableStyle = None):
        """
        添加表格

        Args:
            data: 表格数据
            col_widths: 列宽列表
            style: 表格样式
        """
        if not data:
            return self

        # 默认列宽
        if col_widths is None:
            col_widths = [self.doc.width / len(data[0]) for _ in data[0]]

        # 创建表格
        table = Table(data, colWidths=col_widths)

        # 默认表格样式 - 使用中文字体
        if style is None:
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), self.DEFAULT_CHINESE_FONT),  # 使用中文字体
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), self.DEFAULT_CHINESE_FONT),  # 使用中文字体
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

        table.setStyle(style)
        self.story.append(table)
        self.story.append(Spacer(1, 12))

        return self

    def add_image(self, image_path: str, width: float):
        """
        添加图片

        Args:
            image_path: 图片路径
            width: 图片宽度
            height: 图片高度
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        with PILImage.open(image_path) as img:
            orig_width, orig_height = img.size
            aspect_ratio = orig_height / orig_width
        height = int(width * aspect_ratio)

        img = Image(image_path, width=width, height=height)
        self.story.append(img)
        self.story.append(Spacer(1, 12))

        return self

    def add_page_break(self):
        """添加分页符"""
        self.story.append(PageBreak())
        return self

    def add_empty_page(self, page_id: str=None):
        """
        添加一个空页面
        :param page_id:
        :return:
        """
        # 添加分页符
        self.story.append(PageBreak())
        # 记录页面标记
        if page_id:
            self.page_markers[page_id] = len(self.story) - 1
        return self

    def add_content_to_marked_page(self, page_id: str, content):
        """
        向标记的页面添加内容
        :param page_id: 页面标识符
        :param content: 要添加的内容
        :return:
        """
        if page_id not in self.page_markers:
            raise ValueError(f"未找到页面标记: {page_id}")
        # 获取页面标记的位置
        marker_index = self.page_markers[page_id]
        # 在标记位置后插入内容
        self.story.insert(marker_index + 1, content)
        # 更新后续页面标记的位置
        for pid, idx in self.page_markers.items():
            if idx > marker_index:
                self.page_markers[pid] = idx + 1
        return self

    def _create_toc(self):
        """创建目录"""
        if not self.toc_entries:
            return

        # 添加目录标题
        self.story.append(Paragraph("目录", self.styles["Heading_1"]))
        self.story.append(Spacer(1, 12))

        # 创建目录条目
        for level, text, page_num in self.toc_entries:
            # 根据级别添加缩进
            indent = (level - 1) * 20
            # 创建带有点前导符的目录项
            # item_text = f'<para leftIndent="{indent}">{text} <dotleader/><color name="black">第 {page_num + 1} 页</color></para>'
            item_text = f'<para leftIndent="{indent}">{text} <dotleader/><color name="black"></color></para>'
            self.story.append(Paragraph(item_text, self.styles["TOC_1"]))
            self.story.append(Spacer(1, 6))

        # 目录后分页
        self.story.append(PageBreak())

    def generate(self):
        """生成PDF文档"""
        # 设置页眉页脚
        frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width,
            self.doc.height,
            id='normal'
        )

        template = PageTemplate(
            id='test_report',
            frames=frame,
            onPage=self._header_footer_canvas
        )

        self.doc.addPageTemplates([template])

        # 保存当前故事流
        original_story = self.story.copy()
        self.story = []

        # 添加第一页内容（封面）
        # 找到第一个分页符的位置（如果有）
        first_page_break_index = -1
        for i, item in enumerate(original_story):
            if isinstance(item, PageBreak):
                first_page_break_index = i
                break

        # 如果有分页符，将第一页内容提取出来
        if first_page_break_index >= 0:
            first_page_content = original_story[:first_page_break_index + 1]
            remaining_content = original_story[first_page_break_index + 1:]
        else:
            # 如果没有分页符，假设所有内容都在第一页
            first_page_content = original_story
            remaining_content = []

        # 添加第一页内容
        self.story.extend(first_page_content)

        # 在内容开始前插入目录（现在会在第二页）
        if self.toc_entries:
            # 创建目录
            self._create_toc()

        # 添加剩余内容
        self.story.extend(remaining_content)

        # 构建PDF
        self.doc.build(self.story)

        print(f"PDF报告已生成: {self.filename}")


# 使用示例
if __name__ == "__main__":
    # 创建报告实例 - 使用PPT宽屏尺寸
    report = PDFReportGenerator("测试报告示例.pdf", "激光雷达点云性能测试报告", page_size="PPT_WIDESCREEN")

    # --------------------------------添加报告标题-------------------------------------
    # report.add_empty_page("custom_page_0")
    # 添加报告标题
    report.add_report_name('Robin E1X动态测试报告', 0)
    # 添加测试信息
    test_info = [
        ['雷达型号', 'E1X'],
        ['软固件版本', '123.0.1'],
        ['测试人员', '王海波'],
        ['测试结果', 'PASS']
    ]
    report.add_table(test_info, col_widths=[2 * inch, 2 * inch])

    # --------------------------------添加每页内容-------------------------------------
    # 添加内容
    report.add_empty_page("custom_page_1")
    report.add_title("1.概述", 1)
    report.add_text("这是自动化测试报告的概述部分。")

    report.add_title("2.测试环境", 1)
    report.add_text("测试环境配置如下：")
    # 添加表格
    env_data = [
        ["环境项", "配置"],
        ["操作系统", "Windows 10"],
        ["浏览器", "Chrome 90"],
        ["测试框架", "pytest"],
        ["编程语言", "Python 3.8"]
    ]
    report.add_table(env_data)

    # 添加一个空页面并标记它
    report.add_empty_page("custom_page_2")

    # 添加另一个表格
    result_data = [
        ["测试用例", "状态", "执行时间"],
        ["登录测试", "通过", "2.3s"],
        ["搜索测试", "通过", "1.8s"],
        ["下单测试", "失败", "3.1s"],
        ["支付测试", "通过", "2.9s"]
    ]

    # 自定义表格样式 - 使用中文字体
    custom_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), report.DEFAULT_CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('FONTNAME', (0, 1), (-1, -1), report.DEFAULT_CHINESE_FONT),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('TEXTCOLOR', (2, 3), (2, 3), colors.red),  # 失败用例标红
    ])

    # 向标记的页面添加内容
    custom_table = Table(result_data)
    custom_table.setStyle(custom_style)
    # report.add_table(result_data)
    report.add_content_to_marked_page("custom_page_2", custom_table)

    # 添加标题和文本到标记的页面
    custom_title = Paragraph("自定义页面内容", report.styles["Heading_2"])
    report.add_content_to_marked_page("custom_page_2", custom_title)

    custom_text = Paragraph("这是在自定义页面上添加的内容。", report.styles["BodyText_1"])
    report.add_content_to_marked_page("custom_page_2", custom_text)

    # 添加另一个空页面
    report.add_empty_page("custom_page_3")

    # 向第二个标记页面添加内容
    custom_title2 = Paragraph("第二个自定义页面", report.styles["Heading_2"])
    report.add_content_to_marked_page("custom_page_3", custom_title2)

    custom_text2 = Paragraph("这是第二个自定义页面的内容。", report.styles["BodyText_1"])
    report.add_content_to_marked_page("custom_page_3", custom_text2)

    # 添加图片（如果有）
    report.add_image("hollow_knight.jpg", width=200)

    report.add_empty_page("custom_page_4")
    report.add_title("总结", 1)
    report.add_text("本次测试共执行了20个测试用例，通过19个，失败1个，通过率为95%。")

    # 生成PDF
    report.generate()