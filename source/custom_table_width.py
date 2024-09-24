# extensions/table_width_extension.py

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.builders.latex import LaTeXTranslator
from sphinx.application import Sphinx
from sphinx import addnodes
from sphinx.util import logging
from docutils.nodes import Node

# 获取 Sphinx 的日志器
logger = logging.getLogger(__name__)

class TableWidthDirective(SphinxDirective):
    """
    自定义指令，用于设置表格宽度和列宽。
    使用方法：

    .. table-width::
        :width: 50%
        :columns: 20% 80%
    """
    has_content = False
    option_spec = {
        'width': directives.unchanged,
        'columns': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        # 存储当前文档的表格宽度信息
        table_info = {
            'width': self.options.get('width', '100%'),
            'columns': self.options.get('columns', '').split(),
        }
        if not hasattr(env, 'table_width_info'):
            env.table_width_info = []
        env.table_width_info.append(table_info)
        logger.info(f"TableWidthDirective: Stored table info: {table_info}")
        return []

def process_table_nodes(app: Sphinx, doctree: Node, fromdocname: str):
    """
    处理文档中的表格节点，应用存储的宽度信息。
    """
    if app.builder.name != 'latex':
        logger.info("process_table_nodes: Builder is not LaTeX. Skipping.")
        return  # 仅在生成 PDF（LaTeX）时应用

    env = app.builder.env
    table_width_info = getattr(env, 'table_width_info', [])

    logger.info(f"process_table_nodes: Found {len(table_width_info)} table width info entries.")

    for node in doctree.traverse(nodes.table):
        if table_width_info:
            info = table_width_info.pop(0)
            width = info.get('width', '100%')
            columns = info.get('columns', [])
            logger.info(f"process_table_nodes: Applying width {width} and columns {columns} to table.")

            # 将宽度信息存储到节点属性中，以便在 LaTeX 构建时使用
            node['custom_width'] = width
            node['custom_columns'] = columns
        else:
            logger.info("process_table_nodes: No table width info available for this table.")

class CustomLaTeXTranslator(LaTeXTranslator):
    def visit_table(self, node):
        if 'custom_width' in node and 'custom_columns' in node:
            width = node['custom_width']
            columns = node['custom_columns']
            num_cols = len(node.children[0].children)

            logger.info(f"CustomLaTeXTranslator: Found custom_width={width}, custom_columns={columns}")

            if columns and len(columns) == num_cols:
                column_spec = ' | '.join(['p{' + col + '}' for col in columns])
                logger.info(f"CustomLaTeXTranslator: Using column_spec='{column_spec}'")
            else:
                # 默认列规格
                column_spec = ' | '.join(['l' for _ in range(num_cols)])
                logger.warning(f"CustomLaTeXTranslator: Number of columns specified does not match table columns. Using default column_spec='{column_spec}'")

            self.body.append('\\begin{table}[ht]\n\\centering\n')
            self.body.append(f'\\begin{{tabular}}{{|{column_spec}|}}\n\\hline\n')
        else:
            # 默认表格处理
            logger.info("CustomLaTeXTranslator: No custom width information. Using default table formatting.")
            super().visit_table(node)

    def depart_table(self, node):
        if 'custom_width' in node and 'custom_columns' in node:
            self.body.append('\\end{tabular}\n\\end{table}\n')
            logger.info("CustomLaTeXTranslator: Closed custom table environment.")
        else:
            # 默认表格处理
            super().depart_table(node)

def add_custom_translator(app: Sphinx):
    if app.builder.name == 'latex':
        app.builder.translator_class = CustomLaTeXTranslator
        logger.info("add_custom_translator: Set CustomLaTeXTranslator as the translator for LaTeX builder.")

def setup(app: Sphinx):
    app.add_directive("table-width", TableWidthDirective)
    app.connect('doctree-resolved', process_table_nodes)
    app.connect('builder-inited', add_custom_translator)
    logger.info("setup: table_width_extension has been initialized.")
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
