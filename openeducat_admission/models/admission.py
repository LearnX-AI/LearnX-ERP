

from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class OpAdmission(models.Model):
    _name = "op.admission"
    _inherit = ['mail.activity.mixin', 'mail.tracking.duration.mixin']
    _rec_name = "name"
    _description = "Student Registration"
    _order = 'id DESC'

    title = fields.Many2one(
        'res.partner.title', 'Title')
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
    # study_field = fields.Many2one(
    #     'res.study.field', 'Field of Study')
    name = fields.Char(
        'Full Name', compute='_onchange_name', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('done', 'Completed'), ('cancel', 'Cancelled')],
        string='Status', default='draft', readonly=False)
    active = fields.Boolean(string="Active", default=True)
    register_id = fields.Many2one('op.admission.register', string='Admission Register')

    @api.depends('first_name', 'last_name')
    def _onchange_name(self):
        for record in self:
            record.name = (
                (record.first_name or '') + ' ' + (record.last_name or '')
            ).strip() or 'New Registration'

    # @api.depends('register_id')
    # def _compute_course_ids(self):
    #     for data in self:
    #         if data.register_id:
    #             if data.register_id.admission_base == 'program':
    #                 course_list = []
    #                 for rec in data.register_id.admission_fees_line_ids:
    #                     course_list.append(rec.course_id.id) if rec.course_id.id not in course_list else None  # noqa
    #                 data.course_ids = [(6, 0, course_list)]
    #             else:
    #                 data.course_id = data.register_id.course_id.id
    #                 data.course_ids = [(6, 0, [data.register_id.course_id.id])]
    #         else:
    #             data.course_ids = [(6, 0, [])]


    # @api.onchange('student_id', 'is_student')
    # def onchange_student(self):
    #     if self.is_student and self.student_id:
    #         sd = self.student_id
    #         self.title = sd.title and sd.title.id or False
    #         self.first_name = sd.first_name
    #         self.middle_name = sd.middle_name
    #         self.last_name = sd.last_name
    #         self.birth_date = sd.birth_date
    #         self.gender = sd.gender
    #         self.image = sd.image_1920 or False
    #         self.street = sd.street or False
    #         self.street2 = sd.street2 or False
    #         self.phone = sd.phone or False
    #         self.email = sd.email or False
    #         self.zip = sd.zip or False
    #         self.city = sd.city or False
    #         self.country_id = sd.country_id and sd.country_id.id or False
    #         self.state_id = sd.state_id and sd.state_id.id or False
    #         self.partner_id = sd.partner_id and sd.partner_id.id or False
    #     else:
    #         self.birth_date = ''
    #         self.gender = ''
    #         self.image = False
    #         self.street = ''
    #         self.street2 = ''
    #         self.phone = ''
    #         self.mobile = ''
    #         self.zip = ''
    #         self.city = ''
    #         self.country_id = False
    #         self.state_id = False
    #         self.partner_id = False

    @api.onchange('register_id')
    def onchange_register(self):
        if self.register_id:
            if self.register_id.admission_base == 'course':
                self.program_id = self.course_id.program_id.id
                self.fees = self.register_id.product_id.lst_price
                self.company_id = self.register_id.company_id.id
            else:
                self.program_id = self.register_id.program_id.id

    # @api.onchange('course_id')
    # def onchange_course(self):
    #     self.batch_id = False
    #     term_id = False
    #     if self.course_id:
    #         if self.register_id.admission_base == 'program':
    #             for rec in self.register_id.admission_fees_line_ids:
    #                 if rec.course_id.id == self.course_id.id:
    #                     self.fees = rec.course_fees_product_id.lst_price
    #         self.program_id = self.course_id.program_id.id
    #         if self.course_id.fees_term_id:
    #             term_id = self.course_id.fees_term_id.id
    #     self.fees_term_id = term_id

    # @api.constrains('register_id', 'application_date')
    # def _check_admission_register(self):
    #     for rec in self:
    #         start_date = fields.Date.from_string(rec.register_id.start_date)
    #         end_date = fields.Date.from_string(rec.register_id.end_date)
    #         application_date = fields.Date.from_string(rec.application_date)
    #         if application_date < start_date or application_date > end_date:
    #             raise ValidationError(_(
    #                 "Application Date should be between Start Date & End Date of Admission Register."))  # noqa

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))
            elif record and record.birth_date:
                today_date = fields.Date.today()
                day = (today_date - record.birth_date).days
                years = day // 365
                if years < self.register_id.minimum_age_criteria:
                    raise ValidationError(_(
                        "Not Eligible for Admission minimum "
                        "required age is :"
                        " %s " % self.register_id.minimum_age_criteria))

    # @api.constrains('name')
    # def create_sequence(self):
    #     if not self.application_number:
    #         self.application_number = self.env['ir.sequence'].next_by_code(
    #             'op.admission') or '/'

    def submit_form(self):
        self.state = 'submit'

    # def admission_confirm(self):
    #     self.state = 'admission'

    # def confirm_in_progress(self):
    #     for record in self:
    #         record.state = 'confirm'

    # def get_student_vals(self):
        enable_create_student_user = self.env['ir.config_parameter'].get_param(
            'openeducat_admission.enable_create_student_user')
        for student in self:
            student_user = False
            if enable_create_student_user:
                student_user = self.env['res.users'].create({
                    'name': student.name,
                    'login': student.email,  # noqa
                    'image_1920': self.image or False,
                    'is_student': True,
                    'company_id': self.company_id.id if self.company_id else False,
                    'group_ids': [
                        (6, 0,
                         [self.env.ref('base.group_portal').id])]
                })
            details = {
                'name': student.name,
                'mobile': student.mobile,
                'email': student.email,
                'street': student.street,
                'city': student.city,
                'country': student.country,
                'state': student.state  and student.state or False,
                # 'image_1920': student.image,
                # 'zip': student.zip,
            }
            if enable_create_student_user:
                student_user.partner_id.write(details)
            details.update({
                'title': student.title and student.title.id or False,
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'birth_date': student.birth_date,
                'gender': student.gender if student.gender else False,
                'image_1920': student.image or False,
                'course_detail_ids': [[0, False, {
                    'course_id':
                        student.course_id and student.course_id.id or False,
                    'batch_id':
                        student.batch_id and student.batch_id.id or False,
                    'academic_years_id':
                        student.register_id.academic_years_id.id or False,
                    'academic_term_id':
                        student.register_id.academic_term_id.id or False,
                    'fees_term_id': student.fees_term_id.id,
                    'fees_start_date': student.fees_start_date,
                    'product_id': student.register_id.product_id.id,
                }]],
                'user_id': student_user.id if student_user else False,
                'company_id': self.company_id.id,
                'partner_id':student_user.partner_id.id if student_user else False
            })
            return details

    # def enroll_student(self):
        for record in self:
            if record.register_id.max_count:
                total_admission = self.env['op.admission'].search_count(
                    [('register_id', '=', record.register_id.id),
                     ('state', '=', 'done')])
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
            if not record.student_id:
                vals = record.get_student_vals()
                if vals:
                    record.student_id = student_id = self.env[
                        'op.student'].create(vals).id
                    record.partner_id = record.student_id.partner_id.id \
                        if record else False

            else:
                student_id = record.student_id.id
                record.student_id.write({
                    'course_detail_ids': [[0, False, {
                        'course_id':
                            record.course_id and record.course_id.id or False,
                        'batch_id':
                            record.batch_id and record.batch_id.id or False,
                        'fees_term_id': record.fees_term_id.id,
                        'fees_start_date': record.fees_start_date,
                        'product_id': record.register_id.product_id.id,
                    }]],
                })
            if record.fees_term_id.fees_terms in ['fixed_days', 'fixed_date']:
                val = []
                product_id = record.register_id.product_id.id
                for line in record.fees_term_id.line_ids:
                    no_days = line.due_days
                    per_amount = line.value
                    amount = (per_amount * record.fees) / 100
                    dict_val = {
                        'fees_line_id': line.id,
                        'amount': amount,
                        'fees_factor': per_amount,
                        'product_id': product_id,
                        'discount': record.discount or record.fees_term_id.discount,
                        'state': 'draft',
                        'course_id': record.course_id and record.course_id.id or False,
                        'batch_id': record.batch_id and record.batch_id.id or False,
                    }
                    if line.due_date:
                        date = line.due_date
                        dict_val.update({
                            'date': date
                        })
                    elif self.fees_start_date:
                        date = self.fees_start_date + relativedelta(
                            days=no_days)
                        dict_val.update({
                            'date': date,
                        })
                    else:
                        date_now = (datetime.today() + relativedelta(
                            days=no_days)).date()
                        dict_val.update({
                            'date': date_now,
                        })
                    val.append([0, False, dict_val])
                record.student_id.write({
                    'fees_detail_ids': val
                })
            record.write({
                'nbr': 1,
                'state': 'done',
                'admission_date': fields.Date.today(),
                'student_id': student_id,
                'is_student': True,
            })
            reg_id = self.env['op.subject.registration'].create({
                'student_id': student_id,
                'batch_id': record.batch_id.id,
                'course_id': record.course_id.id,
                'min_unit_load': record.course_id.min_unit_load or 0.0,
                'max_unit_load': record.course_id.max_unit_load or 0.0,
                'state': 'draft',
            })
            reg_id.get_subjects()

    # def confirm_rejected(self):
    #     self.state = 'reject'

    # def confirm_pending(self):
    #     self.state = 'pending'

    # def confirm_to_draft(self):
    #     self.state = 'draft'

    def confirm_cancel(self):
        self.state = 'cancel'
        # if self.is_student and self.student_id.fees_detail_ids:
        #     self.student_id.fees_detail_ids.state = 'cancel'

    # def payment_process(self):
    #     self.state = 'fees_paid'

    # def open_student(self):
    #     form_view = self.env.ref('openeducat_core.view_op_student_form')
    #     tree_view = self.env.ref('openeducat_core.view_op_student_tree')
    #     value = {
    #         'domain': str([('id', '=', self.student_id.id)]),
    #         'view_type': 'form',
    #         'view_mode': 'list, form',
    #         'res_model': 'op.student',
    #         'view_id': False,
    #         'views': [(form_view and form_view.id or False, 'form'),
    #                   (tree_view and tree_view.id or False, 'list')],
    #         'type': 'ir.actions.act_window',
    #         'res_id': self.student_id.id,
    #         'target': 'current',
    #         'nodestroy': True
    #     }
    #     self.state = 'done'
    #     return value

    # def create_invoice(self):
    #     """ Create invoice for fee payment process of student """

    #     partner_id = self.env['res.partner'].create({'name': self.name})
    #     account_id = False
    #     product = self.register_id.product_id
    #     if product.id:
    #         account_id = product.property_account_income_id.id
    #     if not account_id:
    #         account_id = product.categ_id.property_account_income_categ_id.id
    #     if not account_id:
    #         raise UserError(
    #             _('There is no income account defined for this product: "%s". \
    #                You may have to install a chart of account from Accounting \
    #                app, settings menu.') % (product.name,))
    #     if self.fees <= 0.00:
    #         raise UserError(
    #             _('The value of the deposit amount must be positive.'))
    #     amount = self.fees
    #     name = product.name
    #     invoice = self.env['account.invoice'].create({
    #         'name': self.name,
    #         'origin': self.application_number,
    #         'move_type': 'out_invoice',
    #         'reference': False,
    #         'account_id': partner_id.property_account_receivable_id.id,
    #         'partner_id': partner_id.id,
    #         'invoice_line_ids': [(0, 0, {
    #             'name': name,
    #             'origin': self.application_number,
    #             'account_id': account_id,
    #             'price_unit': amount,
    #             'quantity': 1.0,
    #             'discount': 0.0,
    #             'uom_id': self.register_id.product_id.uom_id.id,
    #             'product_id': product.id,
    #         })],
    #     })
    #     invoice.compute_taxes()
    #     form_view = self.env.ref('account.invoice_form')
    #     tree_view = self.env.ref('account.invoice_tree')
    #     value = {
    #         'domain': str([('id', '=', invoice.id)]),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'account.invoice',
    #         'view_id': False,
    #         'views': [(form_view and form_view.id or False, 'form'),
    #                   (tree_view and tree_view.id or False, 'list')],
    #         'type': 'ir.actions.act_window',
    #         'res_id': invoice.id,
    #         'target': 'current',
    #         'nodestroy': True
    #     }
    #     self.partner_id = partner_id
    #     self.state = 'payment_process'
    #     return value

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Admission'),
            'template': '/openeducat_admission/static/xls/op_admission.xls'
        }]


# class OpStudentCourseInherit(models.Model):
#     _inherit = "op.student.course"

#     product_id = fields.Many2one(
#         'product.product', 'Course Fees',
#         domain=[('type', '=', 'service')], tracking=True)


# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     enable_create_student_user = fields.Boolean(
#         config_parameter='openeducat_admission.enable_create_student_user',
#         string='Create Student User')
