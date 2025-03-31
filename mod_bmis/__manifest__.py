{
    'name': 'Barangay Management Information System',
    'version': '2.0.0',
    'category': 'Government',
    'Author': 'AMB BS',
    'summary': 'Manage Barangay Residents and Services',
    'description': """
        Barangay Management Information System
        ====================================
        This module helps manage barangay residents and services.
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/resident_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
