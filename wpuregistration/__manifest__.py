
{
    'name': "WPU Registration",
    'version': '19.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 3,
    'complexity': "easy",
    'author': 'LearnX',
    'depends': ['base','web','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/registration_view.xml',
    ],
    'demo': [],
    'test': [],
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
