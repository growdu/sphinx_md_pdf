import logging
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from bs4 import BeautifulSoup

import logging
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from bs4 import BeautifulSoup

class HTMLTableToLaTeX(SphinxDirective):
    has_content = True

    def run(self):
        logging.info("HTML to LaTeX directive triggered.")

        # 获取 HTML 内容
        html_content = "\n".join(self.content)
        logging.info(f"Received HTML content: {html_content}")

        # 解析并转换所有 HTML 表格为 LaTeX
        latex_code = self.convert_html_tables_to_latex(html_content)

        if not latex_code:
            logging.warning("No LaTeX code generated from HTML tables.")

        # 插入 LaTeX 节点
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
            latex_output += "\n\n"  # 表格之间的空行

        return latex_output

    def convert_single_table_to_latex(self, table):
        #将单个 HTML 表格转换为 LaTeX 代码
        columns = max(len(row.find_all(['th', 'td'])) for row in table.find_all('tr'))
    
        # 根据最大列数生成 LaTeX 列对齐格式
        column_format = '|' + 'l|' * columns
        latex = f"\\begin{{tabular}}{{{column_format}}}\n\\hline\n"

        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            # 确保每行的列数与表头列数一致
            row_data = [col.get_text(strip=True) for col in cols]
            row_data += [''] * (columns - len(row_data))  # 填充空单元格
            latex += " & ".join(row_data) + " \\\\\n\\hline\n"

        latex += "\\end{tabular}"

        return latex


def setup(app):
    logging.basicConfig(level=logging.INFO)  # Enable logging
    logging.info("html_to_latex plugin has been loaded.")  # Add this line
    app.add_directive("html-to-latex", HTMLTableToLaTeX)
    
