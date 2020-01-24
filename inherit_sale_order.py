# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritSaleOrderSo(models.Model):
    _inherit ='sale.order'

    so_id = fields.Many2one('so',string='so')
