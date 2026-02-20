from odoo import models, fields

class StudyField(models.Model):
    _name = 'student.study.field'
    _description = 'Study Field'

    name = fields.Char(required=True)