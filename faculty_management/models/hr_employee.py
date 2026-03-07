from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    faculty_department_id = fields.Many2one(
        'hr.department',
        string="Department"
    )

    qualifications = fields.Text(
        string="Qualifications"
    )

    expertise_subjects = fields.Text(
        string="Expertise / Subjects Taught"
    )

    faculty_employee_id = fields.Char(
        string="Employee ID"
    )

    contract_type = fields.Selection(
        [
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('visiting', 'Visiting Lecturer'),
            ('contract', 'Contract')
        ],
        string="Contract Type"
    )