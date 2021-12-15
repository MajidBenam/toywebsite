from django.contrib.admin.options import InlineModelAdmin
from django.utils.html import format_html
from django.contrib import admin
from functools import partial
from django.forms.models import  modelformset_factory
from django.db import models
from django.forms import TextInput, Textarea
#from tinymce.models import HTMLField, RichTextEditorWidget




from .models import Reference

@admin.display(description="Firm URL")
class ReferenceAdmin(admin.ModelAdmin):
    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'10',})},
    #models.TextField: {'widget': RichTextEditorWidget},
    models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60,})},
    }
    #model = Reference
    #inlines = [InlineModelAdmin]

    list_display = ('polity_wiki', 'old_ref', 'year', 'creator', 'title', 'sure', 'google_scholar', '_pass','new_zotero',)
    list_display_links = ('old_ref',)
    search_fields = ('polity', 'old_ref', 'year', 'creator', )
    list_editable = ('_pass','new_zotero')
    list_per_page = 20
    list_filter = ('_pass', 'certainty')

    def polity_wiki(self, obj):
        return format_html("<a href='{url_link}' target='_blank'>{url_clickable}</a>", 
                                url_link="http://seshatdatabank.info/browser/" + obj.polity, url_clickable=obj.polity)

    def google_scholar(self, obj):
        if str(obj.gs_stars) != 'None' and obj.certainty >= 0 and obj.certainty <= 10:
            return format_html("<strong><a href='{url_link}' target='_blank'>{url_clickable} result(s) &#128270;</a></strong>", 
                                url_link="https://scholar.google.com/scholar?q=" + obj.old_ref, url_clickable=str(obj.gs_stars))
        else:
            return format_html("<strong><a href='{url_link}' target='_blank'>GS_Search &#128270;</a></strong>", 
                                url_link="https://scholar.google.com/scholar?q=" + obj.old_ref)
 
    def sure(self, obj):
        if (str(obj.certainty)) != 'None':
            if obj.certainty > 57:
                my_color = 'green'
            elif obj.certainty <= 57 and obj.certainty >= 45:
                my_color = 'orange'
            #elif obj.certainty == 0:
            #    my_color = 'ornage'
            else:
                my_color = 'red'
            return format_html("<p style='color:{color_picked}'><strong>{cert_level}</strong></p>",color_picked = my_color, cert_level = str(obj.certainty) + "%")
        else:
            return format_html("<p><strong>{cert_level}</strong></p>", cert_level = str('0') + "%")


    # def reviewed(self, obj): 
    #     return format_html("<input type='radio'{review}><label for='{review}'>JavaScript</label>", review = str(obj.reviewed))

    # def get_inline_instances(self, request, obj=None):
    #     if not obj or obj.year >= 1500: return []
    #     return super(ReferenceAdmin, self).get_inline_instances(request, obj)
    
    # def get_changelist_formset(self, request, **kwargs):
    #     defaults = {
    #         'formfield_callback': partial(self.formfield_for_dbfield, request=request),
    #         **kwargs,
    #     }
    #     return modelformset_factory(
    #         self.model, self.get_changelist_form(request), extra=0,
    #         fields=self.list_editable, **defaults
    #     )
#http://seshatdatabank.info/browser/AfDurrn
admin.site.register(Reference, ReferenceAdmin)

## better filtering:
# https://stackoverflow.com/questions/12102697/creating-custom-filters-for-list-filter-in-django-admin

