from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    title = fields.Char(string='Book Title', required=True)
    image = fields.Boolean(string='Image')
    publish_date = fields.Date(string='Publish Date')
    category = fields.Selection([
        ('fiction', 'Fiction'),                                   # خيالي
        ('non_fiction', 'Non-fiction'),                           # غير خيالي
        ('science', 'Science'),                                   # علمي
        ('history', 'History'),                                   # تاريخي
    ], string='Category')
    available_count = fields.Integer(string='Available Count')    # العدد المتاح
    isbn = fields.Char(string='Isbn', required=True)        #  رقم الكتاب الدولي الموحد
    status = fields.Selection([
        ('available', 'Available'),                               # متاح
        ('borrowed', 'Borrowed')                                  # مستعار
    ], string='Status')
    description = fields.Text(string='Description')
    library_id = fields.Many2one('library.library', string='Library')
    author_id = fields.Many2one('library.author', string='Author')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('library.book') or _('New')
        return super(LibraryBook, self).create(vals_list)

    @api.constrains('isbn')
    def _check_unique_isbn(self):
        for record in self:
            existing_book = self.search([('isbn', '=', record.isbn), ('id', '!=', record.id)], limit=1)
            if existing_book:
                raise ValidationError(f"The ISBN {record.isbn} is already used by another book.")

    def action_available(self):
        for rec in self:
            rec.status = 'available'

    def action_borrowed(self):
        for rec in self:
            rec.status = 'borrowed'