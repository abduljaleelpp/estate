# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary':  "manage properties",

    'description': """Long description of module's purpose""",

    'author': "cyberaisystems",
    'website': "https://www.cyberaisystems.com",
    'application': "True",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],
  
    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

