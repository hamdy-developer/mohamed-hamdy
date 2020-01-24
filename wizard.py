# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class WizardSoReport(models.TransientModel):
    _name = 'so.report'
    _description = 'So Report'

    date_to = fields.Date(string='to',required=True)
    date_form = fields.Date(string='form',required=True)

    @api.multi
    def Show(self):
        for rec in self:
            if rec.date_form > rec.date_to:
                raise UserError("There is a mistake in history.")
            else:
                return {
                    'name': 'Report',
                    'res_model': 'so',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'tree,form',
                    'view_type': 'form',
                    'views': [(self.env.ref('so.view_so_tree').id, 'tree'), (self.env.ref('so.view_so_form').id, 'form')],
                    'view_id': False,
                    'domain':[('date','>=',rec.date_form),('date','<=',rec.date_to)],
                }
