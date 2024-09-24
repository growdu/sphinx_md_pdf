from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
import re  # 导入正则表达式模块

class CustomDirective(SphinxDirective):
    has_content = True
    optional_arguments = 1
    required_arguments = 0
    final_argument_whitespace = True

    def run(self):
        # Create the admonition node
        admonition_node = nodes.admonition()
        
        # Add a title node to the admonition
        title = nodes.title(text=self.arguments[0] if self.arguments else self.name.capitalize())
        admonition_node += title
        
        # Add content to the admonition
        content = nodes.paragraph(text='\n'.join(self.content))
        admonition_node += content
        
        # Return the admonition node
        return [admonition_node]

def replace_syntax(app, docname, source):
    if not source or len(source) < 1:
        print("Debug: Source is empty or invalid!")  # 调试信息
        return  # 直接返回，避免后续处理

    # Define the replacement patterns for admonitions
    replacements = {
        ':::note': ':::{note}',
        ':::info': ':::{info}',
        ':::warning': ':::{warning}',
        ':::tip': ':::{tip}',
        ':::danger': ':::{danger}',
    }
    
    for old, new in replacements.items():
        source[0] = source[0].replace(old, new)

    # 定义正则表达式模式来匹配:::{table}及其后续内容
    table_pattern = r'```\{table\}\s*\n((?:.*\n)*?)(?=\n|$)'

    # 查找所有匹配
    matches = re.finditer(table_pattern, source[0])
    print("Debug: Starting to process table matches...")  # 调试信息
    for match in matches:
        # 获取匹配的内容并保留换行符
        table_content = match.group(1)  # 获取内容
        table_content = table_content.rstrip()  # 去掉末尾的空格
        
        print(f"Debug: Found table content before merging:\n{table_content}")  # 调试信息

        # 查找后续行直到遇到空行
        following_lines = []
        match_lines = table_content.splitlines()
        print("match lines is ", match_lines)
        for line in match_lines:
            print("line is "+line)
            if line.strip() == "```":
                continue
            following_lines.append(line + "\n")
        
        print(f"Debug: Following lines found after the table:\n{''.join(following_lines)}")  # 调试信息

        # 生成新的表格语法
        #new_table_syntax = f':::{table}\n{new_table_content.strip()}\n:::'
        new_table_syntax = ':::{table}\n' + ''.join(following_lines).rstrip() + '\n:::'
        print(f"Debug: New table syntax generated:\n{new_table_syntax}")  # 调试信息
        
        # 替换源文本中的原内容
        source[0] = source[0].replace(match.group(0), new_table_syntax)

def setup(app):
    # 注册自定义指令
    app.add_directive('note', CustomDirective)
    app.add_directive('info', CustomDirective)
    app.add_directive('warning', CustomDirective)
    app.add_directive('tip', CustomDirective)
    app.add_directive('danger', CustomDirective)

    # 注册语法替换函数
    app.connect('source-read', replace_syntax)
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
