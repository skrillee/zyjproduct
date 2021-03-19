# -*- coding: utf-8 -*-
from odoo import http

# class Zyjproduct(http.Controller):
#     @http.route('/zyjproduct/zyjproduct/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zyjproduct/zyjproduct/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zyjproduct.listing', {
#             'root': '/zyjproduct/zyjproduct',
#             'objects': http.request.env['zyjproduct.zyjproduct'].search([]),
#         })

#     @http.route('/zyjproduct/zyjproduct/objects/<model("zyjproduct.zyjproduct"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zyjproduct.object', {
#             'object': obj
#         })