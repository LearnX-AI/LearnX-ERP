from odoo import api, fields, models, _

class LearnxSubject(models.Model):
    _name = "learnx.subject"
    _description = "Prerequisite Subjects"
    _order = "name"

    name = fields.Char(string="Subject Name", required=True, translate=True)
    code = fields.Char(string="Subject Code", required=True)
    description = fields.Text(string="Description")