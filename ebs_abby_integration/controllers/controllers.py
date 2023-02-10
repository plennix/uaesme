# -*- coding: utf-8 -*-
from odoo import http

# class Abby(http.Controller):
#     @http.route('/abby/abby/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/abby/abby/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('abby.listing', {
#             'root': '/abby/abby',
#             'objects': http.request.env['abby.abby'].search([]),
#         })

#     @http.route('/abby/abby/objects/<model("abby.abby"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('abby.object', {
#             'object': obj
#         })