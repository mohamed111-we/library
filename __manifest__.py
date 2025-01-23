{
    'name': 'Library Management',
    'version': '17.0',
    'category': 'Services/Library',
    'summary': 'Manage library books, authors, readers, and borrowings.',
    'description': """
                Library Management Module
                ==========================
                This module helps you to manage:
                - Books
                - Authors
                - Readers
                - Borrowings""",
    'author': 'Arafa',
    'website': 'http://www.yourwebsite.com',
    'depends': ['base', 'sale_management', 'crm'],
    'data': [
        'security/ir.model.access.csv',

        'data/sequence.xml',

        'views/library_view.xml',
        'views/book_view.xml',
        'views/author_view.xml',
        'views/member_view.xml',
        'views/borrow_view.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
