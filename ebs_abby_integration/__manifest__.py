# -*- coding: utf-8 -*-
{
    'name': "Plennix ABBY Integration",

    'summary': """
        Abby Integration""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Plennix Technology",
    'website': "http://ever-bs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'static/src/xml/templates.xml',
        # 'views/views.xml',
        'views/templates.xml',
        'views/abby_settings.xml',
        'views/business_card_reader.xml',
    ],
    'qweb': [
        "static/src/xml/contacts_form.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

}