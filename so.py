# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SO(models.Model):
    _name = 'so'
    _inherit = ['mail.thread', 'mail.activity.mixin','utm.mixin']
    _description = 'TO SO'
    _rec_name = 'customer_id'






    customer_id = fields.Many2one('res.partner',string='Customer',required=True)
    date =fields.Date(string='Date',default=fields.Date.context_today)
    products_ids = fields.One2many('products','so_id',string='Products')
    amount_total = fields.Float(string='total',compute='Total')
    sale_order_count = fields.Integer(string='sale',compute='SoSaleOrderCount' )

    @api.multi
    def SoSaleOrderCount(self):
        for rec in self:
            rec.sale_order_count=self.env['sale.order'].search_count([('so_id','=',rec.id)])

    @api.multi
    @api.onchange('products_ids')
    def Total(self):
        for rec in self:
            total=0.0
            if rec.products_ids:
                for product in rec.products_ids:
                    total+=product.subtotal
                rec.amount_total=total

    @api.multi
    def CreateSo(self):
        for rec in self:
            products=[]
            for product in rec.products_ids:
                products.append((0, 0, {
                    'name': product.product_id.name,
                    'product_id': product.product_id.id,
                    'product_uom_qty': product.quantity,
                    'price_unit': product.price,

                }),)
            self.env['sale.order'].create({
            'partner_id': rec.customer_id.id,
            'order_line': products,
            'state': 'sale', # for display on Sale Order Screen
            'so_id': rec.id,
        })

    def Sales(self):
        return {
            'name': 'sale_order',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [(self.env.ref('sale.view_order_tree').id, 'tree'), (self.env.ref('sale.view_order_form').id, 'form')],
            'view_id': False,
            'domain':[('so_id','=',self.id)],
        }
