# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

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
        ], string="Title", default='mr', help="Select the appropriate title for the applicant", required=True)
    first_name = fields.Char(
        'First Name', required=True, help="Ex: John")
    last_name = fields.Char(
        'Last Name', required=True, help="Ex: Doe")
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')],
        string='Gender',
        required=True, help="Select the gender of the applicant")
    birth_province = fields.Many2one(
        'res.country.state', 
        'Birth Province', help="Ex: California")
    birth_date = fields.Date(
        'Date of Birth', required=True, help="1990-01-01")
    marital_status = fields.Selection(
        [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'),
         ('widowed', 'Widowed')], string='Marital Status', required=True, help="Select the marital status of the applicant")
    home_province = fields.Many2one(
        'res.country.state', 'Home Province', help="California")
    email = fields.Char(
        'Email', size=256, required=True, help="john.doe@example.com")
    mobile = fields.Char(
        'Mobile Number', size=16, required=True, help="Personal mobile number Ex: +1234567890 ")
    phone = fields.Char(
        'Phone Number', size=16, required=True, help="Landline number Ex: +1234567890")
    id_type = fields.Selection(
        [('passport', 'Passport'), ('driving_license', 'Driving License'),
         ('id_card', 'National ID')], string='ID Type', required=True, help="You can select Passport, Driving License, or National ID")
    id_copy = fields.Binary(
        'Copy of ID', attachment=True)
    street = fields.Char(
        'Street/ Village', size=256, required=True, help="Name of Street/ Village")
    city = fields.Char(
        'City/Town/District', size=256, required=True)
    res_province =  fields.Many2one(
        'res.country.state', 'Residential Province')
    post_address = fields.Char(
        'Postal Address', size=256, required=True)
    country = fields.Many2one(
        'res.country', 'Country')
    school_name = fields.Char(
        'Name of last school/Institute', size=256, required=True)
    school_province = fields.Many2one(
        'res.country.state', 'Province of last school/Institute')
    school_country = fields.Many2one(
        'res.country', 'Country of last school/Institute')
    graduate_date = fields.Date(
        'Date of Graduation', required=True)
    computer_skill = fields.Selection(
        [('basic', 'Basic'), ('intermediate', 'Intermediate'),
         ('advanced', 'Advanced')], string='Level of Computer Literacy', required=True)
    reason = fields.Text(
        'Reason for choosing the WPU', required=True)
    study_field = fields.Many2one(
        'student.study.field', 'Field of Study')
    name = fields.Char(
        'Full Name', compute='_onchange_name', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('done', 'Completed'), ('cancel', 'Cancelled')],
        string='Status', default='draft', readonly=False)
    active = fields.Boolean(string="Active", default=True)
    

    @api.onchange('first_name', 'last_name')
    def _onchange_name(self):
        for record in self:
            record.name = (
                (record.first_name or '') + ' ' + (record.last_name or '')
            ).strip() or 'New Registration'
    
    def submit_form(self):
        for record in self:
            record.state = 'submit'

    def confirm_cancel(self):
        for record in self:
            record.state = 'cancel'