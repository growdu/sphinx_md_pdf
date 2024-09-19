from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

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
    # Define the replacement patterns
    replacements = {
        ':::note': ':::{note}',
        ':::info': ':::{info}',
        ':::warning': ':::{warning}',
        ':::tip': ':::{tip}',
        ':::danger': ':::{danger}',
    }
    
    for old, new in replacements.items():
        source[0] = source[0].replace(old, new)

def setup(app):
    # Register custom directives
    app.add_directive('note', CustomDirective)
    app.add_directive('info', CustomDirective)
    app.add_directive('warning', CustomDirective)
    app.add_directive('tip', CustomDirective)
    app.add_directive('danger', CustomDirective)

    # Register the syntax replacement function
    app.connect('source-read', replace_syntax)
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
