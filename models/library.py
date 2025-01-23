from odoo import models, fields, api, _

class LibraryLibrary(models.Model):
    _name = 'library.library'
    _description = 'Library'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    name = fields.Char(string='Library Name', required=True)
    phone = fields.Char(string='Library Phone', required=False)
    email = fields.Char(string='Library Email', required=False)
    address = fields.Text(string='Library Address', required=False)
    image = fields.Boolean(string='Image')
    established_date = fields.Date(string='Established Date')    # تاريخ التأسيس
    working_hours = fields.Text(string='Working Hours')
    library_type = fields.Selection([
        ('public', 'Public'),                      # مكتبة عامة
        ('specialized', 'Specialized'),            # مكتبة متخصصة
        ('digital', 'Digital'),                    # مكتبة رقمية
    ], string='Library Type', default='public')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='Status', default='draft', required=True)

    book_ids = fields.One2many('library.book', 'library_id', string='Book')
    book_count = fields.Integer(string='Book Count', compute='_compute_book_count')

    @api.depends('book_ids')
    def _compute_book_count(self):
        for record in self:
            record.book_count = len(record.book_ids)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref') or vals['ref'] == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('library.library') or _('New')
        return super(LibraryLibrary , self).create(vals_list)

    def action_draft(self):
        self.state = 'draft'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The action has been successfully completed.',
                'type': 'rainbow_man',
            }
        }

    def action_open(self):
        self.state = 'open'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The action has been successfully completed.',
                'type': 'rainbow_man',
            }
        }

    def action_closed(self):
        self.state = 'closed'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'The action has been successfully completed.',
                'type': 'rainbow_man',
            }
        }

    def action_view_book(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Books',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
            'domain': [('library_id', '=', self.id)],
            'context': {'default_library_id': self.id},
        }