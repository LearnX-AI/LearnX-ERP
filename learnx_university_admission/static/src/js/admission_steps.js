/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { registry } from "@web/core/registry";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";

const { onMounted, useRef } = owl;

class AdmissionStepsController extends FormController {
    setup() {
        super.setup();
        this.step = 1;
        this.maxStep = 5;

        this.nextBtn = useRef("next_step");
        this.prevBtn = useRef("prev_step");
        this.submitBtn = useRef("submit_app");

        this.dialog = useService("dialog");
        this.notification = useService("notification");

        onMounted(() => this._initSteps());
    }

    _initSteps() {
        this._updateView();

        if (this.nextBtn.el) {
            this.nextBtn.el.addEventListener("click", () => this._goNext());
        }
        if (this.prevBtn.el) {
            this.prevBtn.el.addEventListener("click", () => this._goPrev());
        }
        if (this.submitBtn.el) {
            this.submitBtn.el.addEventListener("click", () => this._confirmSubmit());
        }
    }

    _updateView() {
        document.querySelectorAll(".step-panel").forEach(el => el.classList.add("d-none"));
        const current = document.querySelector(`.step-panel[data-step="${this.step}"]`);
        if (current) current.classList.remove("d-none");

        this.prevBtn.el.disabled = (this.step <= 1);
        this.nextBtn.el.classList.toggle("d-none", this.step >= this.maxStep);
        this.submitBtn.el.classList.toggle("d-none", this.step < this.maxStep);
    }

    _goNext() {
        if (!this._validateCurrentStep()) return;
        if (this.step < this.maxStep) {
            this.step++;
            this._updateView();
        }
    }

    _goPrev() {
        if (this.step > 1) {
            this.step--;
            this._updateView();
        }
    }

    _validateCurrentStep() {
        const currentPanel = document.querySelector(`.step-panel[data-step="${this.step}"]`);
        if (!currentPanel) return true;

        let valid = true;
        const required = currentPanel.querySelectorAll("[required]");

        required.forEach(el => {
            if (!el.value.trim() && el.type !== "checkbox" && el.type !== "file") {
                el.classList.add("is-invalid");
                valid = false;
            } else {
                el.classList.remove("is-invalid");
            }
        });

        if (!valid) {
            this.notification.add("Please fill all required fields in this section.", { type: "danger" });
        }

        return valid;
    }

    async _confirmSubmit() {
        if (!this._validateCurrentStep()) return;

        const confirmed = await new Promise(resolve => {
            this.dialog.add(ConfirmationDialog, {
                title: "Submit Your Application?",
                body: `
                    <div class="text-center py-4">
                        <h4 class="mb-3 text-primary">Review Before Final Submission</h4>
                        <p class="mb-3">Please make sure all information is correct.<br/>
                        You can still go back using the Previous button.</p>
                        <small class="text-muted">After submission your application will be reviewed by an administrator.</small>
                    </div>
                `,
                confirmLabel: "Yes, Submit Now",
                cancelLabel: "Review Again",
                confirmClass: "btn-success",
                cancelClass: "btn-secondary",
            }, {
                onConfirm: () => resolve(true),
                onCancel: () => resolve(false),
            });
        });

        if (confirmed) {
            try {
                await this.model.root.save();
                this.notification.add("Application submitted successfully!", { type: "success" });
                await this.model.orm.call("learnx.admission.application", "action_submit", [[this.model.root.resId]]);
            } catch (err) {
                this.notification.add("Error while submitting. Please check your data.", { type: "danger" });
            }
        }
    }
}

registry.category("views").add("view_learnx_admission_application_form", {
    ...registry.category("views").get("form"),
    Controller: AdmissionStepsController,
});
