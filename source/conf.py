# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'sphinx-test'
copyright = '2024, growdu'
author = 'growdu'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
#html_css_files = ['custom.css']
extensions = [
    'custom_sytax',
    'myst_parser',
    'html_to_latex',
    'custom_table_width'
]
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
latex_engine = 'xelatex'  # 或 'lualatex'
latex_elements = {
    'preamble': r'''
        \usepackage[UTF8]{ctex}
        \setCJKmainfont{SimSun}
        \usepackage{longtable}
        \usepackage{booktabs}
        \usepackage{tabularx}
    ''',
}
html_context = {
    "table_classes": ["table", "table-bordered", "table-striped", "table-hover"],
}
# 如果使用 myst_parser, 你可以添加以下配置：
myst_enable_extensions = [
    "html_admonition",
    "html_image",  # 支持 HTML 标签
    # 智能引号与替换件
    "smartquotes","replacements",
    # 冒号的代码围栏
    "colon_fence",
    # 链接
    "linkify",
    # 替换
    "substitution",
    # 任务列表
    "tasklist"
]