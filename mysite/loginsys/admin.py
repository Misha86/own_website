from django.contrib import admin
from loginsys.models import Profile
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.core import serializers

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('профіль')



# Define a new_profile User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    # actions = [select_men]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions_on_top = False
    date_hierarchy = 'profile_create'
    fields = ['user', 'sex', 'avatar']
    list_filter = ['user']
    search_fields = ['user']
    list_display = ['__str__', 'sex', 'avatar']
    actions = ['make_man', 'make_woman', 'export_as_json', 'export_selected_objects', 'make']

    # action function for Profile (select users for change sex)
    def make_man(self, request, queryset):
        rows_updated = queryset.update(sex='Man')
        if rows_updated == 1:
            message_bit = _("1 користувачу ")
        else:
            message_bit = _("%s користувачам" % rows_updated)
        self.message_user(request, _("%s успісно змінили стать профіля на 'Чоловік'.") % message_bit)
    make_man.short_description = _("Змінити стать користувача на 'Чоловік'")

    def make_woman(self, request, queryset):
        rows_updated = queryset.update(sex='Woman')
        if rows_updated == 1:
            message_bit = _("1 користувачу ")
        else:
            message_bit = _("%s користувачам" % rows_updated)
        self.message_user(request, _("%s успісно змінили стать профіля на 'Жінка'.") % message_bit)
    make_woman.short_description = _("Змінити стать користувача на 'Жінка'")

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response
    export_as_json.short_description = _("Експортувати як Json")

    def export_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect(reverse('loginsys:show_users', kwargs={'ct': ct.pk, 'ids': ",".join(selected)}))
    export_selected_objects.short_description = _("Експортувати вибране на сайт")

    admin.site.add_action(export_as_json, _("Експортувати як Json"))  # added actions in all admin`s models


admin.site.register(Profile, ProfileAdmin)

