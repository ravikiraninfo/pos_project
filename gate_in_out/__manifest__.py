{
    'name': 'Gate In/Out',
    'version': '16.0.1.0.0',
    'category': 'Gate',
    'author': 'Tanay Goyal',
    'maintainer': 'Tanay Goyal',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/gate_in_out_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
