from odoo import api, fields, models, _
from lxml import etree
try:
    import simplejson
except ImportError:
    import json


class MakeFormReadonly(models.Model):
    _name = 'make.form.readonly'
    _description = 'Form view become readonly using fields_view_get().'

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        res = super(MakeFormReadonly, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        if view_type == 'form' and True:  # When Form View is loaded, and condition met.
            for node in doc.xpath('//field'):
                modifiers = simplejson.loads(node.get('modifiers'))
                modifiers['readonly'] = True
                node.set('modifiers', simplejson.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res
