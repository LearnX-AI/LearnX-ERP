# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = "student.registration"
    _description = "Student Registration"
    _order = 'id DESC'
    _rec_name = 'name'

    title = fields.Selection([
        ('mr', 'Mr.'),
        ('ms', 'Ms.'),
        ('mrs', 'Mrs.'),
        ('dr', 'Dr.'),
        ], string="Title", default='mr', help="Select the appropriate title for the applicant")
    first_name = fields.Char(
        'First Name', help="Ex: John", required=True)
    last_name = fields.Char(
        'Last Name',  help="Ex: Doe", required=True)
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')],
        default='m',
        string='Gender',
        help="Select the gender of the applicant")
    birth_province = fields.Many2one(
        'res.country.state', 
        'Birth Province', help="Ex: California", required=True)
    birth_date = fields.Date(
        'Date of Birth', help="1990-01-01", required=True)
    marital_status = fields.Selection(
        [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'),
         ('widowed', 'Widowed')], string='Marital Status', help="Select the marital status of the applicant", required=True)
    home_province = fields.Many2one(
        'res.country.state', 'Home Province', help="California", required=True)
    email = fields.Char(
        'Email', size=256, help="john.doe@example.com", required=True, )
    mobile = fields.Char(
        'Mobile Number', size=16,help="Personal mobile number Ex: +1234567890 ",required=True)
    phone = fields.Char(
        'Phone Number', size=16, help="Landline number Ex: +1234567890")
    id_type = fields.Selection(
        [('passport', 'Passport'), ('driving_license', 'Driving License'),
         ('id_card', 'National ID')], string='ID Type',help="You can select Passport, Driving License, or National ID", required=True)
    id_copy = fields.Binary(
        'Copy of ID', attachment=True,required=True, help="Upload a scanned copy of the selected ID")
    street = fields.Char(
        'Street/ Village', size=256,  help="Name of Street/ Village")
    city = fields.Char(
        'City/Town/District', size=256)
    res_province =  fields.Many2one(
        'res.country.state', 'Residential Province')
    post_address = fields.Char(
        'Postal Address', size=256)
    country = fields.Many2one(
        'res.country', 'Country',required=True)
    school_name = fields.Char(
        'Name of last school/Institute', size=256)
    school_province = fields.Many2one(
        'res.country.state', 'Province of last school/Institute')
    school_country = fields.Many2one(
        'res.country', 'Country of last school/Institute')
    graduate_date = fields.Date(
        'Date of Graduation')
    computer_skill = fields.Selection(
        [('basic', 'Basic'), ('intermediate', 'Intermediate'),
         ('advanced', 'Advanced')], string='Level of Computer Literacy')
    reason = fields.Text(
        'Reason for choosing the WPU')
    study_field = fields.Many2one(
        'student.study.field', 'Field of Study')
    name = fields.Char(
        'Full Name', compute='_onchange_name', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('done', 'Completed'), ('cancel', 'Cancelled')],
        string='Status', default='draft', readonly=False)
    active = fields.Boolean(string="Active", default=True)
    

    @api.depends('first_name', 'last_name')
    def _onchange_name(self):
        for record in self:
            record.name = (
                (record.first_name or '') + ' ' + (record.last_name or '')
            ).strip() or 'New Registration'
    
    def submit_form(self):
      self.state = 'submit'

    def confirm_cancel(self):
        self.state = 'cancel'