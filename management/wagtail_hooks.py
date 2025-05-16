from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.forms.models import FormSubmission
class SubmissionAdmin(ModelAdmin):
    model         = FormSubmission
    menu_label    = "Bestilling"
    menu_icon     = "doc-full"           
    list_display  = ("submit_time", "id", "navn_pa_skoleorganisasjon", "kontaktperson",)
    search_fields = ("id",)

    def navn_pa_skoleorganisasjon(self, obj):
        return obj.form_data.get("navn_pa_skoleorganisasjon", "")

    def kontaktperson(self, obj):
        return obj.form_data.get("kontaktperson", "")

modeladmin_register(SubmissionAdmin)