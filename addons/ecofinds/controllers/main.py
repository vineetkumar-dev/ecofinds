# addons/ecofinds/controllers/main.py
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class EcoFindsController(http.Controller):

    @http.route('/my/listings', type='http', auth='user', website=True)
    def my_product_listings(self, **kwargs):
        """
        Displays the list of products listed by the current user.
        """
        Product = request.env['product.template']
        user_listings = Product.search([('seller_id', '=', request.env.user.partner_id.id)])
        
        return request.render('ecofinds.my_listings_page', {
            'products': user_listings,
        })

    @http.route(['/my/listings/add', '/my/listings/edit/<model("product.template"):product>'], type='http', auth='user', website=True)
    def my_listing_form(self, product=None, **kwargs):
        """
        Renders the form to add a new or edit an existing product listing.
        """
        categories = request.env['ecofinds.product.category'].search([])
        return request.render('ecofinds.my_listing_form_page', {
            'product': product,
            'categories': categories,
        })
        
    @http.route('/my/listings/save', type='http', auth='user', website=True, methods=['POST'])
    def my_listing_save(self, **post):
        """
        Handles the submission of the add/edit product form.
        """
        Product = request.env['product.template']
        product_id = post.get('product_id')
        
        # Prepare the values for the product
        vals = {
            'name': post.get('name'),
            'list_price': post.get('list_price'),
            'description_sale': post.get('description_sale'),
            'ecofinds_category_id': int(post.get('ecofinds_category_id')) if post.get('ecofinds_category_id') else False,
            'website_published': True, # Ensure it is visible on the website
            'sale_ok': True, # Ensure it can be sold
            'type': 'product' # Make it a storable product
        }
        
        if post.get('image_1920'):
            vals['image_1920'] = post.get('image_1920').read()

        if product_id:
            # Editing an existing product
            product = Product.browse(int(product_id))
            # Security check: Ensure user is the seller
            if product.seller_id != request.env.user.partner_id:
                return request.redirect('/') # Or show an error
            product.sudo().write(vals)
        else:
            # Creating a new product
            # Seller is set automatically by the model's default
            Product.sudo().create(vals)
            
        return request.redirect('/my/listings')

    @http.route('/my/listings/delete/<model("product.template"):product>', type='http', auth='user', website=True, methods=['POST'])
    def my_listing_delete(self, product, **kwargs):
        """
        Deletes a user's product listing.
        """
        # Security check: Ensure user is the seller
        if product.seller_id == request.env.user.partner_id:
            product.sudo().unlink()
        return request.redirect('/my/listings')

# --- Inherit WebsiteSale to add category filter ---
class EcoFindsShop(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        # Run the original shop method
        res = super(EcoFindsShop, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        
        # Add our custom categories to the render context
        ecofinds_categories = request.env['ecofinds.product.category'].search([])
        res.qcontext['ecofinds_categories'] = ecofinds_categories
        
        # Handle filtering by our custom category
        if post.get('ecofinds_category'):
            # This is a basic implementation. You would search products based on this category.
            # For simplicity, we'll re-render the template with a filtered domain.
            # A full implementation would require modifying the search logic more deeply.
            domain = self._get_search_domain(search, category, attrib_values=post)
            domain += [('ecofinds_category_id', '=', int(post.get('ecofinds_category')))]
            
            # Recalculate products with the new domain
            product_count = request.env['product.template'].search_count(domain)
            products = request.env['product.template'].search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
            
            res.qcontext.update({
                'products': products,
            })
            
        return res