from odoo import api, fields, models, _

class LearnxAdmissionApplication(models.Model):
    _name = "learnx.admission.application"
    _description = "LearnX Admission Application"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    admission_number = fields.Char(
        string="Application Number",
        required=True,
        copy=False,
        readonly=True,
        default="New",
        tracking=True,
    )
    application_date = fields.Date(
            string="Application Date",
            required=True,
            default=fields.Date.context_today,
            help="Date when the application is submitted.",
            tracking=True,
    )
    preferred_start_semester = fields.Selection(
        [
            ('semester_1', 'Semester 1 (Jan-Jun)'),
            ('semester_2', 'Semester 2 (Jul-Dec)'),
            ('summer_intake', 'Summer Intake')
        ],
        string="Preferred Start Semester",
        required=True,
        help="Select the preferred semester when the student wants to start.",
        tracking=True   
    )
    entry_year = fields.Integer(
        string="Entry Year",
        required=True,
        default=lambda self: fields.Date.today().year,
        help="Year in which the student intends to start the program.",
        tracking=True,
    )
    application_type = fields.Selection(
        [
            ('new_applicant', 'New Applicant'),
            ('transfer_student', 'Transfer Student'),
            ('re_admission', 'Re-admission'),
            ('postgraduate', 'Postgraduate')
        ],
        string="Application Type",
        required=True,
        help="Type of the application.",
        tracking=True
    )
    is_previous_student = fields.Boolean(
        string="Previous WPU Student",
        default=False,
        help="Check if the applicant has previously studied at WPU.",
        tracking=True,
    )
    entry_qualification = fields.Selection(
        [
            ('grade_12', 'Grade 12'),
            ('diploma', 'Diploma'),
            ('bachelor', 'Bachelor'),
            ('other', 'Other')
        ],
        string="Entry Qualification",
        required=True,
        help="Select the applicant's highest qualification. Determines eligibility.",
        tracking=True,
    )
    gpa_score = fields.Float(
        string="GPA / Aggregate Score",
        required=True,
        help="Enter the GPA or aggregate score from Grade 12 or prior qualification for merit-based selection.",
        tracking=True
    )
    english_proficiency = fields.Selection(
        [
            ('ielts', 'IELTS'),
            ('toefl', 'TOEFL'),
            ('png_grade12', 'PNG Grade 12 English Grade')
        ],
        string="English Proficiency",
        required=True,
        help="Required for non-English speakers. Select the type of English proficiency proof.",
        tracking=True
    )
    subject_ids = fields.Many2many(
        'learnx.subject',
        string="Prerequisite Subjects",
        help="Select subjects relevant for this admission application."
    )
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
    has_disability = fields.Boolean(
        string="Disability / Special Needs",
        default=False,
        tracking=True,
        help="Check if the applicant requires specific accommodations."
    )
    disability_details = fields.Text(
        string="Accommodation Details",
        help="Describe any accommodations needed (e.g., mobility aid, learning support).",
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
        required=True,
        default='self_funded',
        tracking=True,
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
        required=True,
        tracking=True,
        help="Check this if the application fee has been confirmed as paid."
    )
    payment_receipt = fields.Binary(
        string="Payment Receipt",
        attachment=True,
        help="Upload the digital receipt or proof of payment.",
    )
    receipt_filename = fields.Char("Receipt Filename") # Optional: helps store the original name
    declaration_accepted = fields.Boolean(
        string="Applicant Declaration",
        required=True,
        tracking=True,
        help="I declare all information provided is true and complete."
    )
    privacy_consent = fields.Boolean(
        string="Privacy Consent",
        required=True,
        tracking=True,
        help="Applicant consent to data processing under the privacy policy."
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
            ('received', 'Received'),
            ('reviewed', 'Reviewed'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('waitlisted', 'Waitlisted')
        ],
        string="Application Status",
        default='received',
        tracking=True,
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
        tracking=True,
    )
    display_header_title = fields.Char(compute="_compute_display_fields")
    state_display = fields.Char(compute="_compute_display_fields")
    current_step = fields.Integer(default=1)

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
        return super(LearnxAdmissionApplication, self).write(vals)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("admission_number", "New") == "New":
                vals["admission_number"] = self.env["ir.sequence"].next_by_code(
                    "learnx.admission.application"
                ) or "New"
        return super().create(vals_list)

    def action_submit(self):
        self.ensure_one()
        self.state = 'submitted'
        self.message_post(
            body=_("Application submitted by %s") % self.env.user.name
        )

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_receive(self):
        self.write({"state": "received"})

    def action_review(self):
        self.write({"state": "reviewed"})

    def action_accept(self):
        self.write({"state": "accepted", "decision_date": fields.Date.today()})

    def action_reject(self):
        self.write({"state": "rejected", "decision_date": fields.Date.today()})

    def action_waitlist(self):
        self.write({"state": "waitlisted"})

    def action_set_to_draft(self):
        self.write({"state": "draft"})

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
        if self.current_step < 7:
            self.current_step += 1
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_prev_step(self):
        self.ensure_one()
        if self.current_step > 1:
            self.current_step -= 1
        return {'type': 'ir.actions.client', 'tag': 'reload'}

