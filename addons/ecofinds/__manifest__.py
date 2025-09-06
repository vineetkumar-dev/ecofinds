# addons/ecofinds/__manifest__.py
{
    'name': 'EcoFinds Marketplace',
    'version': '1.0',
    'summary': 'A sustainable second-hand marketplace.',
    'description': """
        EcoFinds – Empowering Sustainable Consumption through a Second-Hand Marketplace.
        Allows users to buy and sell pre-owned goods.
    """,
    'author': 'Your Hackathon Team Name',
    'category': 'Website/eCommerce',
    'depends': [
        'website',
        'website_sale', # We depend on the eCommerce app for cart, products
        'portal', # For user dashboard
    ],
    'data': [
        # Security first
        'security/ir.model.access.csv',
        'security/ecofinds_security.xml',

        # Backend views
        'views/product_views.xml',
        'views/category_views.xml',

        # Frontend templates
        'templates/website_templates.xml',
        'templates/my_listings.xml',
        'templates/product_form.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}