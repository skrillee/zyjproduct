# -*-coding: utf-8 -*-
# freight.py
# !/usr/bin/env python3
"""
    Product module: Provides the system with product definition criteria

"""
from odoo import models, fields, api
import datetime
import pytz


class ZYJProductManufacturers (models.Model):
    _name = 'zyjproduct.product_manufacturers'
    _description = 'product manufacturers'
    manufacturer_of_manufacturer = fields.Char(string='名称')
    image_of_manufacturer = fields.Binary("头像", attachment=True, help="This field holds the image used as avatar for this contact, limited to 1024x1024px",)
    address_of_manufacturer = fields.Char(string='厂家地址')
    phone_number_of_manufacturer = fields.Char(string='厂家联系方式')
    product_quantity_of_manufacturer = fields.Integer(string='版本数量')
    qq_number_of_manufacturer = fields.Char(string='QQ号码')
    wechat_number_of_manufacturer = fields.Char(string='微信号码')
    # currency_id = fields.Many2one('res.currency', string='Currency',
    #                               required=True, readonly=True, states={'draft': [('readonly', False)]},
    #                               track_visibility='always'
    #                               )

    # manufacturers_line_ids = fields.One2many('zyjproduct.product_versions', 'manufacturers_id',
    #                                          string='Product Versions Lines',
    #                                          states={'open': [('readonly', False)]},
    #                                          readonly=True,
    #                                          copy=True)
    state = fields.Selection([
            ('open', 'Open'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='open',
        track_visibility='onchange', copy=False,
        help=" * The 'Open' status is used when user creates invoice, an invoice number is generated. "
             "          It stays in the open status till the user pays the invoice.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")


class ZYJProductVersions (models.Model):
    _name = 'zyjproduct.product_versions'
    _description = 'product versions'
    # _rec_name = 'position_id'

    @api.model
    def get_location_time(self):
        now_time = datetime.datetime.utcnow()
        tz = self.env.user.tz or 'Asia/Shanghai'
        return str(now_time.replace(tzinfo=pytz.timezone(tz)))

    # manufacturers_id = fields.Many2one('zyjproduct.product_manufacturers', string='manufacturers Reference',
    #                                    ondelete='cascade', index=True)
    version_brand = fields.Char(string='版本所属厂家')
    version_name = fields.Char(string='版本名称')
    version_date = fields.Date(string='版本日期', readonly=True, index=True, states={'open': [('readonly', False)]},
                               help="Keep empty to use the current date", copy=False,
                               default=lambda self: self.env['fixed.freight_bill'].get_location_time())
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, readonly=True, states={'draft': [('readonly', False)]},
                                  track_visibility='always'
                                  )
    version_purchasing_price = fields.Monetary(string='版本进价', store=True, currency_field='currency_id')
    version_sale_price = fields.Monetary(string='版本售价', store=True, currency_id='currency_id')
    level_position_version = fields.Selection([
            ('high-end', '高端'),
            ('high-level', '中端'),
            ('high-ranking', '廉价')
        ], string='level position', index=True, readonly=True,
        track_visibility='onchange', copy=False,)

    state = fields.Selection([
            ('open', 'Open'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='open',
        track_visibility='onchange', copy=False,
        help=" * The 'Open' status is used when user creates invoice, an invoice number is generated. "
             "          It stays in the open status till the user pays the invoice.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")

    versions_line_ids = fields.One2many('zyjproduct.product_model_number', 'versions_id',
                                        string='Product Model Number Lines',
                                        states={'open': [('readonly', False)]},
                                        readonly=True,
                                        copy=True)


class FreightBillLine(models.Model):
    _name = "zyjproduct.product_model_number"
    _description = "product model number"

    versions_id = fields.Many2one('zyjproduct.product_versions', string='Versions Reference',
                                  ondelete='cascade', index=True)
    model_number_name = fields.Char(string='型号名称')
    # model_number_versions = fields.Many2one('zyjproduct.product_versions', string='所属版本')
    model_number_height = fields.Float(string='高度(米)', help='Describe the length of the goods.')
    model_number_unit_price = fields.Float(string='单价(平方米/元)', help='The price of a single item')
    currency_id = fields.Many2one('res.currency', related='versions_id.currency_id', store=True,
                                  related_sudo=False, readonly=False
                                  )
    remark = fields.Text(string='备注')
