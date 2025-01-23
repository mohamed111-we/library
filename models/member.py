from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', default='@gmail.com')
    phone = fields.Char(string='Phone')
    registration_date = fields.Date(string='Registration Date', default=fields.Date.context_today)  # تاريخ التسجيل
    state = fields.Selection([
        ('draft', 'Draft'),  # تمثل حالة المسودة.
        ('active', 'Active'),  # تمثل الحالة النشطة.
        ('banned', 'Banned')  # تمثل الحالة المحظورة.
    ], string="State", default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('library.member') or _('New')
        return super(LibraryMember, self).create(vals_list)

    _sql_constraints = [
        ('uniq_email', 'UNIQUE("email")', "A tag with the same email already exists."),
        ('uniq_phone', 'UNIQUE("phone")', "A tag with the same phone already exists.")
    ]

    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if not rec.phone.isdigit():
                raise ValidationError('Phone number must contain only digits.')


    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_set_active(self):
        for record in self:
            record.state = 'active'

    def action_set_banned(self):
        for record in self:
            record.state = 'banned'