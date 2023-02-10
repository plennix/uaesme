from odoo import api, fields, models



class abby_settings(models.TransientModel):

    _inherit = 'res.config.settings'


    serverurl = fields.Char(string="Abby Server URL")
    applicationid = fields.Char(string="Application ID")
    password = fields.Char(string="Password")

    def get_values(self):
        res = super(abby_settings, self).get_values()
        res.update(
            serverurl=self.env['ir.config_parameter'].sudo().get_param('serverurl'),
            applicationid=self.env['ir.config_parameter'].sudo().get_param('applicationid'),
            password=self.env['ir.config_parameter'].sudo().get_param('password'),

        )
        return res

    def set_values(self):
        super(abby_settings, self).set_values()
        self.env['ir.config_parameter'].set_param('serverurl', self.serverurl)
        self.env['ir.config_parameter'].set_param('applicationid', self.applicationid)
        self.env['ir.config_parameter'].set_param('password',self.password)