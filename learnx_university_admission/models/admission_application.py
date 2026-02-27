from odoo import api, fields, models, _


class LearnxAdmissionProgram(models.Model):
    _name = "learnx.admission.program"
    _description = "LearnX Admission Program"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    description = fields.Text()
    capacity = fields.Integer()
    color = fields.Integer("Color Index")


class LearnxAdmissionApplication(models.Model):
    _name = "learnx.admission.application"
    _description = "LearnX Admission Application"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(
        string="Admission Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    admission_title = fields.Char(string="Admission Title", required=True, tracking=True)
    academic_year = fields.Char(
        string="Academic Year",
        required=True,
        default=lambda self: str(fields.Date.today().year),
        tracking=True,
    )
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    application_deadline = fields.Date(string="Application Deadline", required=True)

    available_program_ids = fields.Many2many(
        "learnx.admission.program",
        "learnx_admission_program_rel",
        "admission_id",
        "program_id",
        string="Available Programs",
    )
    max_intake_per_program = fields.Integer(
        string="Maximum Intake per Program",
        help="Maximum number of students that can be admitted per program.",
    )
    application_fee = fields.Float(
        string="Application Fee",
        help="Fee required when applying for this admission.",
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("gathering", "Application Gathering"),
            ("processing", "Admission Process"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    display_header_title = fields.Char(compute="_compute_display_fields")
    state_display = fields.Char(compute="_compute_display_fields")

    _sql_constraints = [
        (
            "unique_application_name",
            "unique(name)",
            "The application reference must be unique.",
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "learnx.admission.application"
                ) or _("New")
        return super().create(vals_list)

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_gather(self):
        self.write({"state": "gathering"})

    def action_process(self):
        self.write({"state": "processing"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def _compute_display_fields(self):
        state_labels = dict(self._fields["state"].selection)
        for rec in self:
            # For a new (unsaved) record, always show "New Admission".
            # For existing records, show the admission title (or fallback).
            if not rec.id:
                rec.display_header_title = _("New Admission")
            else:
                rec.display_header_title = rec.admission_title or _("New Admission")
            rec.state_display = state_labels.get(rec.state, "")

