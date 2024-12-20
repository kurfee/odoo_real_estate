{
    'name': 'Real Estate',
    'author': 'Abdalrhman Abdalla',
    'summary': 'A Real Estate App that was built to help all the real estate agents in achieving a success',
    'category': 'Business',
    'license': 'LGPL-3',
    'version': '1.0',
    'depends': [
                'mail',
                'board',
                'sale',
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'data/tags.xml',
        'data/types.xml',
        'data/properties.xml',

        'views/sequence.xml',
        'views/quotation_fields.xml',
        'views/res_partner.xml',
        'views/offers.xml',
        'views/sale_order.xml',
        'views/dashboard.xml',
        'views/property_views.xml',
        'views/estate_tag.xml',
        'views/estate_type.xml',
        'views/property_menus.xml',

        'reports/property_card.xml',
        'reports/report.xml',

    ],
    'installable': True,
    'application': True,
    'auto_installable': False,
    'images': ['static/description/icon.png'
               ],
}
