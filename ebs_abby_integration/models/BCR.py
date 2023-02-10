from builtins import print

from odoo import api, fields, models
import base64
import xlsxwriter
import io
import os
from PIL import Image
from .process import *
from .read_xml_file import *
from odoo.exceptions import UserError, ValidationError

class BusinessCardReaderWizard(models.TransientModel):
    _name = 'bcr.wizard'

    BCRimage = fields.Binary("Upload business card", attachment=True,
                             help="This field holds the image used as avatar for this contact, "
                                  "limited to 1024x1024px", )

    def runAbbySdk(self, img, DestFile):

        abby_server_url = self.env['ir.config_parameter'].sudo().get_param('serverurl'),
        application_id = self.env['ir.config_parameter'].sudo().get_param('applicationid'),
        passowrd = self.env['ir.config_parameter'].sudo().get_param('password'),
        if (abby_server_url[0] or application_id[0] or passowrd[0])== False:
            raise UserError("Please provide abby settings in settings under general settings")
        main(img, DestFile, abby_server_url[0], application_id[0], passowrd[0])

    def create_contact_company_with_address(self, name, phone, email, web, company, job, address, country):

        partner = self.env['res.partner'].create(
            {'name': name, 'company_type': 'person', 'mobile': phone, 'email': email, 'website': web, 'function': job,
             'street': address, 'country_id': country,'company_name':company})
        return partner

    def create_contact_company(self, name, phone, email, web, company, job):

        partner = self.env['res.partner'].create(
            {'name': name, 'company_type': 'person', 'mobile': phone, 'email': email, 'website': web, 'function': job,'company_name':company})

        return partner

    def read_create_contact(self):

        if self.BCRimage:
           
            BCRImages64 = self.BCRimage
            imgdata = base64.b64decode(BCRImages64)
        
            dest_file ='temp_image.xml'
            self.runAbbySdk(imgdata, dest_file)

            BCRdata = read_xmlFile()
            os.remove(dest_file)
            name = BCRdata[3].strip()
            mobile = BCRdata[0].strip()
            mobile = mobile.replace(" ", "")
            mobile = mobile.replace("-", "")
            mobile = mobile.replace("/", "")
            mobile = mobile.replace("\\", "")
            email = BCRdata[1].strip()
            web = BCRdata[2].strip()
            company = BCRdata[4].strip()
            job = BCRdata[5].strip()
            address = BCRdata[6].strip()

            if address:
                countries = self.env['res.country'].search([])
                for country in countries:
                    if country.name in address:
                        address = address.strip(country.name)
                        break;

                print('create_contact_company_with_address')
                contact = self.create_contact_company_with_address(name, mobile, email, web, company, job, address,
                                                                   country.id)
               
            else:
                print('create_contact_company')
                contact = self.create_contact_company(name, mobile, email, web, company, job)
           
            values = {'partner_id':contact.id,'name': name, 'job': job, 'email': email, 'mobile': mobile, 'web': web, 'company': company,
                      'full_address': address}
            #self.env['bcr'].create(values)


            return {
                'type': 'ir.actions.act_window',
                'name': 'Open contact',
                'res_model': 'res.partner',
                'res_id': contact.id,
                'view_mode': 'form',
                'view_type': 'form',
            };
        else:
            raise UserError('There was no image selected')
