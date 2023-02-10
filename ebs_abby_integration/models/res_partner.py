# -*- coding: utf-8 -*-

from odoo import models, fields, api


class REsPartnerInherit(models.Model):
    _inherit= 'res.partner'

    def open_scan_wizard(self):
        print("Fuck odoo ")