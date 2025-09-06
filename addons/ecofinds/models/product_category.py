# addons/ecofinds/models/product_category.py
from odoo import models, fields

class EcoFindsProductCategory(models.Model):
    _name = 'ecofinds.product.category'
    _description = 'EcoFinds Product Category'
    _order = 'name'

    name = fields.Char('Category Name', required=True, translate=True)