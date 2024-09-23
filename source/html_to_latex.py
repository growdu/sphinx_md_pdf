import logging
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from bs4 import BeautifulSoup

class HTMLTableToLaTeX(SphinxDirective):
    has_content = True

    def run(self):
        #logging.info("HTML to LaTeX directive triggered.")
        html_content = "\n".join(self.content)
        #logging.info(f"Received HTML content: {html_content}")

        latex_code = self.convert_html_tables_to_latex(html_content)

        if not latex_code:
            logging.warning("No LaTeX code generated from HTML tables.")

        node = nodes.raw('', latex_code, format='latex')
        return [node]

    def convert_html_tables_to_latex(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')

        if not tables:
            logging.warning("No tables found in HTML content.")
            return ""

        latex_output = ""
        for table in tables:
            latex_output += self.convert_single_table_to_latex(table)
            latex_output += "\n\\bigskip\n"

        return latex_output

    def convert_single_table_to_latex(self, table):
        """将单个 HTML 表格转换为 LaTeX 代码，支持跨行跨列，处理边线和内容对齐"""
        rows = table.find_all('tr')
        max_columns = max(len(row.find_all(['th', 'td'])) for row in rows)

        # 使用 'p{<width>}' 来设置列宽，确保表格宽度占满页面
        column_format = '|' + 'p{3cm}|' * max_columns
        latex = f"\\begin{{tabular}}{{{column_format}}}\n\\hline\n"

        # rowspan_tracker 用于追踪每列的跨行状态
        rowspan_tracker = [0] * max_columns

        for i, row in enumerate(rows):
            #logging.debug(f"Processing row {i}: {row}")
            cols = row.find_all(['th', 'td'])
            col_idx = 0  # 列索引

            latex_row = []
            for col in cols:
                colspan = int(col.get('colspan', 1))
                rowspan = int(col.get('rowspan', 1))
                text = col.get_text(strip=True)

                style = col.get("style", "")
                alignment = self.get_alignment_from_style(style)

                # 检查并处理跨行单元格
                while rowspan_tracker[col_idx] > 0:
                    #logging.debug(f"Skipping column {col_idx} due to rowspan.")
                    latex_row.append("")  # 填充空位
                    col_idx += 1

                if colspan > 1:
                    # 删除跨列的左边和右边的表格线
                    latex_row.append(f"\\multicolumn{{{colspan}}}{{{self.get_multicolumn_format(col_idx, colspan, max_columns)}}}{{{text}}}")
                elif rowspan > 1:
                    # 处理跨行并保持边框控制
                    #logging.debug(f"Applying rowspan in column {col_idx}, spanning {rowspan} rows.")
                    latex_row.append(f"\\multirow{{{rowspan}}}{{*}}{{\\centering {text}}}")
                    rowspan_tracker[col_idx] = rowspan  # 标记此列需要跨行
                else:
                    latex_row.append(f"\\multicolumn{{1}}{{|{alignment}|}}{{{text}}}")

                col_idx += colspan

            while col_idx < max_columns:
                latex_row.append("")
                col_idx += 1

            latex += " & ".join(latex_row) + " \\\\\n"
            #logging.debug(f"Latex row generated: {' & '.join(latex_row)}")

            for j in range(len(rowspan_tracker)):
                if rowspan_tracker[j] > 0:
                    #logging.debug(f"Reducing rowspan tracker at column {j}.")
                    rowspan_tracker[j] -= 1

            # 如果当前行有跨行的单元格，部分列不应该绘制表格线，使用 \cline 控制
            if any(rowspan_tracker):
                # 找出哪些列不应绘制表格线
                columns_with_rowspan = [index + 1 for index, rowspan in enumerate(rowspan_tracker) if rowspan == 0]
                if columns_with_rowspan:
                    # 生成 \cline 语句，只为没有跨行的列绘制线
                    cline_ranges = []
                    start = columns_with_rowspan[0]
                    for idx in range(1, len(columns_with_rowspan)):
                        if columns_with_rowspan[idx] != columns_with_rowspan[idx - 1] + 1:
                            cline_ranges.append(f"{start}-{columns_with_rowspan[idx - 1]}")
                            start = columns_with_rowspan[idx]
                    cline_ranges.append(f"{start}-{columns_with_rowspan[-1]}")
                    cline_string = " ".join([f"\\cline{{{r}}}" for r in cline_ranges])
                    latex += f"{cline_string}\n"
                    #logging.debug(f"Adding \\cline for columns {cline_ranges}.")
            else:
                latex += "\\hline\n"
                #logging.debug(f"Adding \\hline for row {i}.")


        latex += "\\end{tabular}"

        return latex

    
    def get_alignment_from_style(self, style):
        """根据HTML中的样式信息获取文本对齐方式"""
        if "text-align: right" in style:
            return "r"
        elif "text-align: left" in style:
            return "l"
        else:
            return "c"

    def get_multicolumn_format(self, col_idx, colspan, max_columns):
        """生成用于 \multicolumn 的格式，移除跨列单元格的左右边线"""
        if col_idx == 0 and colspan == max_columns:
            return "c"  # 全表宽跨列时保留中间对齐
        elif col_idx == 0:
            return "|c"  # 保留左边线
        elif col_idx + colspan == max_columns:
            return "c|"  # 保留右边线
        else:
            return "c"  # 中间列不保留边线

def setup(app):
    #logging.basicConfig(level=logging.debug)  # Enable detailed logging for debugging
    #logging.info("html_to_latex plugin has been loaded.")
    app.add_directive("html-to-latex", HTMLTableToLaTeX)
    app.connect('builder-inited', add_latex_macros)

def add_latex_macros(app):
    if app.builder.name == 'latex':
        app.add_latex_package('multirow')
        app.add_latex_package('cellspace')
        app.add_latex_package('array')
        app.add_latex_package('caption')
        app.add_latex_package('booktabs')
