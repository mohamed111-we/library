from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Library Borrow'
    _rec_name= 'member_id'

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    member_id = fields.Many2one('library.member', string="Member", required=True)
    book_id = fields.Many2one('library.book', string="Book", required=True)
    borrow_date = fields.Date(string='Borrow Date',
                              required=True,
                              default=fields.Date.context_today,
                              domain=[('state', '!=', 'banned')],
                              help='The date when the book was borrowed.')
    return_date = fields.Date(string='Return Date',
                              help='The expected return date for the book.')
    state = fields.Selection([
        ('draft', 'Draft'),  # المسودة - استعارة غير مؤكدة
        ('borrowed', 'Borrowed'),  # تم استعارة الكتاب
        ('returned', 'Returned'),  # الكتاب تم إرجاعه
        ('overdue', 'Overdue')],  # تأخر عن موعد الإرجاع
        string='Status', default='draft', )

    @api.constrains('return_date')
    def _check_return_date(self):
        for rec in self:
            if rec.return_date and rec.return_date < rec.borrow_date:
                raise ValidationError('Return date must be after borrow date.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('library.borrow') or _('New')
        return super(LibraryBorrow, self).create(vals_list)