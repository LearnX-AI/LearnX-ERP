from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class LearnxAdmissionApplication(models.Model):
    _name = "learnx.admission.application"
    _description = "LearnX Admission Application"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

# Admision Details
    admission_number = fields.Char(
        string="Application Number",
        copy=False,
        readonly=True,
        default="New",
    )
    application_date = fields.Date(
            string="Application Date",
            default=fields.Date.context_today,
            help="Date when the application is submitted.",
    )
    preferred_start_semester = fields.Selection(
        [
            ('semester_1', 'Semester 1 (Jan-Jun)'),
            ('semester_2', 'Semester 2 (Jul-Dec)'),
            ('summer_intake', 'Summer Intake')
        ],
        string="Preferred Start Semester",
        help="Select the preferred semester when the student wants to start.",
        tracking=True,
    )
    entry_year = fields.Integer(
        string="Entry Year",
        default=lambda self: fields.Date.today().year,
        help="Year in which the student intends to start the program.",
    )
    application_type = fields.Selection(
        [
            ('new_applicant', 'New Applicant'),
            ('transfer_student', 'Transfer Student'),
            ('re_admission', 'Re-admission'),
            ('postgraduate', 'Postgraduate')
        ],
        string="Application Type",
        help="Type of the application.",
        tracking=True,
    )
    is_previous_student = fields.Boolean(
        string="Previous WPU Student",
        default=False,
        help="Check if the applicant has previously studied at WPU.",
    )
# Eligibility Details
    entry_qualification = fields.Selection(
        [
            ('grade_12', 'Grade 12'),
            ('diploma', 'Diploma'),
            ('bachelor', 'Bachelor'),
            ('other', 'Other')
        ],
        string="Entry Qualification",
        help="Select the applicant's highest qualification. Determines eligibility.",
    )
    gpa_score = fields.Float(
        string="GPA / Aggregate Score",
        help="Enter the GPA or aggregate score from Grade 12 or prior qualification for merit-based selection.",
        tracking=True,
    )
    english_proficiency = fields.Selection(
        [
            ('ielts', 'IELTS'),
            ('toefl', 'TOEFL'),
            ('png_grade12', 'PNG Grade 12 English Grade')
        ],
        string="English Proficiency",
        help="Required for non-English speakers. Select the type of English proficiency proof.",
        tracking=True,
    )
    subject_ids = fields.Many2many(
        'learnx.subject',
        string="Prerequisite Subjects",
        help="Select subjects relevant for this admission application."
    )
    
    # Financial Details
    scholarship_type = fields.Selection(
        [
            ('government', 'Government'),
            ('private', 'Private'),
            ('merit', 'Merit')
        ],
        string="Scholarship Type",
        help="Select the type of scholarship the student is applying for.",
        tracking=True
    )
    payment_method = fields.Selection(
        [
            ('self_funded', 'Self-Funded'),
            ('sponsorship', 'Sponsorship'),
            ('loan', 'Loan'),
            ('scholarship', 'Scholarship')
        ],
        string="Tuition Payment Method",
        default='self_funded',
        help="Select how the tuition fees will be covered."
    )
    sponsor_name = fields.Char(
        string="Sponsor Name",
        help="Enter the name of the employer or government agency providing the sponsorship.",
        tracking=True
    )
    sponsor_contact = fields.Char(
        string="Sponsor Contact Info",
        help="Email or phone number of the sponsor for verification purposes.",
        tracking=True
    )
    fee_paid = fields.Boolean(
        string="Application Fee Paid",
        default=False,
        help="Check this if the application fee has been confirmed as paid.",
    )
    payment_receipt = fields.Binary(
        string="Payment Receipt",
        attachment=True,
        help="Upload the digital receipt or proof of payment.",
    )
    receipt_filename = fields.Char("Receipt Filename") # Optional: helps store the original name

    # Declaration Details
    has_disability = fields.Boolean(
        string="Disability / Special Needs",
        default=False,
        help="Check if the applicant requires specific accommodations."
    )
    disability_details = fields.Text(
        string="Accommodation Details",
        help="Describe any accommodations needed (e.g., mobility aid, learning support).",
        tracking=True
    )
    declaration_accepted = fields.Boolean(
        string="Applicant Declaration",
        help="I declare all information provided is true and complete.",
    )
    privacy_consent = fields.Boolean(
        string="Privacy Consent",
        help="Applicant consent to data processing under the privacy policy.",
    )
    signature = fields.Binary(
        string="Signature",
        help="Digital signature of the applicant.",
        copy=False,
        attachment=True,
    )
    signed_on = fields.Datetime(
        string="Signed On",
        help="Date and time when the signature was provided.",
        copy=False,
    )
    # Admin Only Fields
    admin_application_status = fields.Selection(
        [
            ('submitted', 'Submitted'),
            ('received', 'Received'),
            ('reviewed', 'Reviewed'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('waitlisted', 'Waitlisted')
        ],
        string="Application Status",
        default='submitted',
        help="Internal status managed by the admission office."
    )
    reviewer_notes = fields.Text(
        string="Reviewer Notes",
        help="Internal comments for admissions staff regarding this application.",
        tracking=True
    )
    decision_date = fields.Date(
        string="Decision Date",
        help="The date when the final admission decision was made.",
        tracking=True
    )
    acceptance_letter_sent = fields.Boolean(
        string="Acceptance Letter Sent",
        default=False,
        help="Check this if the formal acceptance letter has been sent to the applicant.",
        tracking=True
    )
    #------------------------------------
    is_admin_user = fields.Boolean(compute='_compute_is_admin_user')
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("received", "Received"),
            ("reviewed", "Reviewed"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("waitlisted", "Waitlisted"),
        ],
        default="draft",
    )
    display_header_title = fields.Char(compute="_compute_display_fields")
    state_display = fields.Char(compute="_compute_display_fields")
    current_step = fields.Selection([
        ('admission', 'Admission Info'),
        ('eligibility', 'Eligibility'),
        ('financial', 'Financial'),
        ('declaration', 'Declaration'),
        ('admin', 'Admin Only')
    ], default='admission')

    _sql_constraints = [
        (
            "unique_application_number",
            "unique(admission_number)",
            "The application number must be unique.",
        )
    ]
    @api.model
    def write(self, vals):
        if 'signature' in vals and vals['signature']:
            vals['signed_on'] = fields.Datetime.now()
            
        if 'admin_application_status' in vals:
            vals['state'] = vals['admin_application_status']
        return super(LearnxAdmissionApplication, self).write(vals)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("admission_number", "New") == "New":
                vals["admission_number"] = self.env["ir.sequence"].next_by_code(
                    "learnx.admission.application"
                ) or "New"
        return super().create(vals_list)

    def action_receive(self):
        self.write({"state": "received", "admin_application_status": "received"})

    def action_review(self):
        self.write({"state": "reviewed", "admin_application_status": "reviewed"})

    def action_accept(self):
        self.write({
            "state": "accepted",
            "admin_application_status": "accepted",
            "decision_date": fields.Date.today()
        })

    def action_reject(self):
        self.write({
            "state": "rejected",
            "admin_application_status": "rejected",
            "decision_date": fields.Date.today()
        })

    def action_waitlist(self):
        self.write({"state": "waitlisted", "admin_application_status": "waitlisted"})

    def action_set_to_draft(self):
        self.write({"state": "draft", "admin_application_status": "received"})

    def _compute_display_fields(self):
        state_labels = dict(self._fields["state"].selection)
        for rec in self:
            # For a new (unsaved) record, always show "New Admission".
            # For existing records, show the admission number (or fallback).
            if not rec.id:
                rec.display_header_title = _("New Admission")
            else:
                rec.display_header_title = rec.admission_number or _("New Admission")
            rec.state_display = state_labels.get(rec.state, "")

    def action_next_step(self):
        self.ensure_one()
        steps = ['admission', 'eligibility', 'financial', 'declaration', 'admin']
        current_index = steps.index(self.current_step)
        if current_index < len(steps) - 1:
            self.current_step = steps[current_index + 1]
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_prev_step(self):
        self.ensure_one()
        steps = ['admission', 'eligibility', 'financial', 'declaration', 'admin']
        current_index = steps.index(self.current_step)
        if current_index > 0:
            self.current_step = steps[current_index - 1]
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def _validate_required_fields(self):
        self.ensure_one()
        missing_fields = []
        
        # Step 1
        if not self.application_date:
            missing_fields.append("Application Date")
        if not self.preferred_start_semester:
            missing_fields.append("Preferred Start Semester")
        if not self.entry_year:
            missing_fields.append("Entry Year")
        if not self.application_type:
            missing_fields.append("Application Type")

        # Step 2
        if not self.entry_qualification:
            missing_fields.append("Entry Qualification")
        if not self.gpa_score:
            missing_fields.append("GPA / Aggregate Score")
        if not self.english_proficiency:
            missing_fields.append("English Proficiency")

        # Step 3
        if not self.payment_method:
            missing_fields.append("Tuition Payment Method")
        if self.payment_method == "sponsorship":
            if not self.sponsor_name:
                missing_fields.append("Sponsor Name")
            if not self.sponsor_contact:
                missing_fields.append("Sponsor Contact")
        if self.payment_method == "scholarship":
            if not self.scholarship_type:
                missing_fields.append("Scholarship Type")

        if not self.fee_paid:
            missing_fields.append("Application Fee Confirmation")

        if self.fee_paid and not self.payment_receipt:
            missing_fields.append("Payment Receipt")

        # Step 4
        if not self.declaration_accepted:
            missing_fields.append("Applicant Declaration")
        if not self.privacy_consent:
            missing_fields.append("Privacy Consent")
        if not self.signature:
            missing_fields.append("Signature")

        # If any missing → raise error
        if missing_fields:
            raise ValidationError(
                "Please complete the following required fields before submission:\n\n- "
                + "\n- ".join(missing_fields)
            )

    def action_submit(self):
        self.ensure_one()
        self._validate_required_fields()
        self.write({"state": self.admin_application_status})
        self.message_post(
            body=_("Application submitted by %s") % self.env.user.name
        )

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.depends_context('uid')
    def _compute_is_admin_user(self):
        for rec in self:
            rec.is_admin_user = self.env.user.has_group('base.group_system')