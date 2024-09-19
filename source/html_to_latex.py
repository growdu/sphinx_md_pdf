import logging
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from bs4 import BeautifulSoup

class HTMLTableToLaTeX(SphinxDirective):
    has_content = True

    def run(self):
        logging.info("HTML to LaTeX directive triggered.")
        html_content = "\n".join(self.content)
        logging.info(f"Received HTML content: {html_content}")

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

        # 读取表格的整体宽度
        total_width = self.get_table_total_width(table)
        logging.info(f"Total table width: {total_width}")

        # 动态设置列宽，依据每列的宽度样式，且相对于总宽度调整
        column_format = '|'
        for col_idx in range(max_columns):
            column_width = self.get_column_width(table, col_idx, total_width)
            column_format += f'p{{{column_width}}}|'
        
        latex = f"\\begin{{tabular}}{{{column_format}}}\n\\hline\n"

        rowspan_tracker = [0] * max_columns

        for i, row in enumerate(rows):
            cols = row.find_all(['th', 'td'])
            col_idx = 0  # 列索引

            latex_row = []
            for col in cols:
                colspan = int(col.get('colspan', 1))
                rowspan = int(col.get('rowspan', 1))
                text = col.get_text(strip=True)

                style = col.get("style", "")
                alignment = self.get_alignment_from_style(style)

                while rowspan_tracker[col_idx] > 0:
                    latex_row.append("")  # 填充空位
                    col_idx += 1

                if colspan > 1:
                    latex_row.append(f"\\multicolumn{{{colspan}}}{{|{alignment}|}}{{{text}}}")
                elif rowspan > 1:
                    latex_row.append(f"\\multirow{{{rowspan}}}{{*}}{{\\centering {text}}}")
                    rowspan_tracker[col_idx] = rowspan
                else:
                    latex_row.append(f"\\multicolumn{{1}}{{|{alignment}|}}{{{text}}}")

                col_idx += colspan

            while col_idx < max_columns:
                latex_row.append("")
                col_idx += 1

            latex += " & ".join(latex_row) + " \\\\\n"

            for i in range(len(rowspan_tracker)):
                if rowspan_tracker[i] > 0:
                    rowspan_tracker[i] -= 1
                else:
                    rowspan_tracker[i] = 0

            if any(rowspan_tracker):
                latex += "\\cline{1-" + str(max_columns) + "}\n"
            else:
                latex += "\\hline\n"

        latex += "\\end{tabular}"

        return latex

    def get_table_total_width(self, table):
        """获取表格的整体宽度，依据HTML的style或宽度属性"""
        style = table.get('style', '')
        width = self.extract_width_from_style(style)
        if width:
            return width
        # 如果没有明确的宽度，设定默认宽度（例如15cm）
        return "15cm"

    def get_column_width(self, table, col_idx, total_width):
        """获取指定列的宽度，依据HTML的style或宽度属性，考虑表格的总宽度"""
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if col_idx < len(cols):
                style = cols[col_idx].get('style', '')
                width = self.extract_width_from_style(style)
                if width:
                    return width
        # 如果没有找到具体的列宽，则分配平均宽度
        return f"{float(total_width[:-2]) / table.find_all('tr')[0].find_all(['th', 'td']).__len__()}cm"

    def extract_width_from_style(self, style):
        """从HTML style中提取宽度"""
        if 'width' in style:
            parts = style.split(';')
            for part in parts:
                if 'width' in part:
                    width_value = part.split(':')[1].strip()
                    # 处理宽度值（确保它以cm为单位，如果不是，转换为cm）
                    if width_value.endswith('%'):
                        # 转换百分比为LaTeX支持的宽度（这里简单设置一个映射）
                        return f"{float(width_value[:-1]) / 100 * 15}cm"
                    elif width_value.endswith('px'):
                        # 将像素值转为cm (假设96px = 2.54cm)
                        return f"{float(width_value[:-2]) * 2.54 / 96}cm"
                    else:
                        return width_value
        return None

    def get_alignment_from_style(self, style):
        """根据HTML中的样式信息获取文本对齐方式"""
        if "text-align: right" in style:
            return "r"
        elif "text-align: left" in style:
            return "l"
        else:
            return "c"

def setup(app):
    logging.basicConfig(level=logging.INFO)  # Enable logging
    logging.info("html_to_latex plugin has been loaded.")
    app.add_directive("html-to-latex", HTMLTableToLaTeX)
    app.connect('builder-inited', add_latex_macros)

def add_latex_macros(app):
    if app.builder.name == 'latex':
        app.add_latex_package('multirow')
        app.add_latex_package('cellspace')
        app.add_latex_package('array')
        app.add_latex_package('caption')
        app.add_latex_package('booktabs')
