from odoo import models, fields, api

class Author(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char('Name', required=True)
    biography = fields.Text('Biography')     # السيرة الذاتية
    birth_date = fields.Date('Birth Date')

    book_ids = fields.One2many('library.book', 'author_id', string='Books')
    book_count = fields.Integer('Number of Books', compute='_compute_book_count', store=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.book_ids)