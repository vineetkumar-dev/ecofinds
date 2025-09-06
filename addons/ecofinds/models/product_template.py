# addons/ecofinds/models/product_template.py
from odoo import models, fields, api

class ProductTemplate(models.Model):
    # Inherit from product.template to get all the features of a standard Odoo product
    _inherit = 'product.template'

    # Add a field for our custom categories
    ecofinds_category_id = fields.Many2one(
        'ecofinds.product.category',
        string='EcoFinds Category',
        help='Select a category for this second-hand item.'
    )
    
    # Add a field to link the product to the user who listed it
    seller_id = fields.Many2one(
        'res.partner',
        string='Seller',
        default=lambda self: self.env.user.partner_id,
        readonly=True,
        help="The user who is selling this product."
    )

    # Make this product available on the website by default
    is_published = fields.Boolean(default=True)