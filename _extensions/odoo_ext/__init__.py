# -*- coding: utf-8 -*-

from . import pygments_override
from . import switcher
from . import translator

import sphinx.environment
try:
    from sphinx.environment.adapters import toctree
except ImportError:
    toctree = None

import sphinx.builders.html
from docutils import nodes
def setup(app):
    if hasattr(app, 'set_translator'):
        app.set_translator('html', translator.BootstrapTranslator)
    else:
        if getattr(app.config, 'html_translator_class', None):
            app.warn("Overriding the explicitly set html_translator_class setting",
                     location="odoo extension")
        app.config.html_translator_class = 'odoo_ext.translator.BootstrapTranslator'

    add_js_file = getattr(app, 'add_js_file', None) or app.add_javascript
    add_js_file('js/doc.js')
    # for f in ['jquery.min.js', 'bootstrap.js', 'doc.js', 'jquery.noconflict.js']:
    #     add_js_file(f)

    switcher.setup(app)
    app.add_config_value('odoo_cover_default', None, 'env')
    app.add_config_value('odoo_cover_external', {}, 'env')
    app.add_config_value('odoo_cover_default_external', lambda conf: conf.odoo_cover_default, 'env')
    app.connect('html-page-context', update_meta)

def update_meta(app, pagename, templatename, context, doctree):
    meta = context.get('meta')
    if meta is None:
        meta = context['meta'] = {}
    meta.setdefault('banner', app.config.odoo_cover_default)
