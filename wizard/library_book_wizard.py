# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LibraryBookWizard(models.TransientModel):
    _name = 'library.book.wizard'
    _description = 'Library Book Wizard'

    title = fields.Char(string='Book Title', required=True)
    publish_date = fields.Date(string='Publish Date')
    category = fields.Selection([
        ('fiction', 'Fiction'),  # خيالي
        ('non_fiction', 'Non-fiction'),  # غير خيالي
        ('science', 'Science'),  # علمي
        ('history', 'History'),  # تاريخي
    ], string='Category')
    available_count = fields.Integer(string='Available Count')  # العدد المتاح
    isbn = fields.Char(string='Isbn', required=True)  # رقم الكتاب الدولي الموحد
    library_id = fields.Many2one('library.library', string='Library')
    author_id = fields.Many2one('library.author', string='Author')

    def action_create_book(self):
        """Creates a new book and links it to the selected library."""
        self.env['library.book'].create({
            'title' : self.title,
            'publish_date' : self.publish_date,
            'category' : self.category,
            'available_count' : self.available_count,
            'isbn' : self.isbn,
            'library_id' : self.library_id.id,
            'author_id' : self.author_id.id,
        })
