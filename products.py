# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Products(models.Model):
    _name = 'products'
    _description = 'products'
    _rec_name = 'product_id'



    so_id = fields.Many2one('so',required=True,ondelete='cascade')
    product_id = fields.Many2one('product.product',string='product',required=True)
    price = fields.Float(string='price',required=True,compute='ProductPrice',readonly=False)
    quantity= fields.Integer(string='quantity',required=True,default=1)
    subtotal = fields.Float(string='subtotal',compute='Total')


    @api.multi
    @api.onchange('price','quantity')
    def Total(self):
        for rec in self:
            if rec.price and rec.quantity:
                rec.subtotal=rec.price * rec.quantity

    @api.multi
    @api.onchange('product_id')
    def ProductPrice(self):
        for rec in self:
            rec.price=rec.product_id.lst_price
