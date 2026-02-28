{
    "name": "LearnX University Admission",
    "summary": "Modern admission management for a University",
    "description": """
                LearnX University Admission
                ===========================
                Manage the full admission lifecycle for a university:
                - Collect and track applications
                - Score candidates and manage programs
                - Visual kanban pipeline and rich forms
                """,
    "version": "19.0.1.0.0",
    "author": "LearnX",
    "category": "Education",
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    'auto_install': False,
    "depends": ["base", "mail", "web"],
    "data": [
        "data/admission_sequence.xml",
        "security/admission_security.xml",
        "security/ir.model.access.csv",
        "views/subject_view.xml",
        "views/admission_views.xml",
        "views/admission_menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "learnx_university_admission/static/src/scss/admission.scss",
            "learnx_university_admission/static/src/js/admission_steps.js",
        ],
    },
}

