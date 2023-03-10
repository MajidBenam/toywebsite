from django.contrib.admin.options import InlineModelAdmin
from django.utils.html import format_html
from django.contrib import admin
from functools import partial
from django.forms.models import modelformset_factory
from django.db import models
from django.forms import TextInput, Textarea
#from tinymce.models import HTMLField, RichTextEditorWidget
from django.forms import CheckboxInput


from .models import Reference, Citation


class CertaintyFilter(admin.SimpleListFilter):
    title = format_html("<b style='color:green'>Certainty level</b>")
    parameter_name = "pagenum"

    def lookups(self, request, model_admin):
        return [
            ("Good_to_Go", format_html("<b>certainty > 57</b>")),
            ("Meh_to_Go",  format_html("<b>46 < certainty < 56</b>")),
            ("Bad_to_Go",  format_html("<b>certainty < 45</b>")),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "Good_to_Go":
            return queryset.distinct().filter(certainty__gt=57)
        if self.value() == "Meh_to_Go":
            return queryset.distinct().filter(certainty__gt=45).filter(certainty__lte=57)
        if self.value() == "Bad_to_Go":
            return queryset.distinct().filter(certainty__gte=0).filter(certainty__lte=45)



class SiteFilter(admin.SimpleListFilter):
    title = format_html("<b style='color:green'>Which Site?</b>")
    parameter_name = "wiki_or_browser"

    def lookups(self, request, model_admin):
        return [
            ("Good_to_Go", format_html("<b>Both</b>")),
            ("WIKI_to_Go", format_html("Only <b>Seshat.info</b>")),
            ("BROW_to_Go",  format_html("Only <b>Seshatdatabank.info</b>")),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "Good_to_Go":
            return queryset.distinct().filter(wiki_number__gt=0).filter(browser_number__gt=0)
        if self.value() == "WIKI_to_Go":
            return queryset.distinct().filter(wiki_number__gt=0)
        if self.value() == "BROW_to_Go":
            return queryset.distinct().filter(browser_number__gt=0)
        

class DoneFilter(admin.SimpleListFilter):
    title = format_html("<b style='color:green'>Finalized?</b>")
    parameter_name = "done_or_not"

    def lookups(self, request, model_admin):
        return [
            ("Good_to_Go", format_html("<b>Finalized</b>")),
            ("Meh_to_Go", format_html("<b>Not Yet</b>")),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "Good_to_Go":
            return queryset.distinct().filter(done=True)
        if self.value() == "Meh_to_Go":
            return queryset.distinct().filter(done=False)

@admin.display(description="Firm URL")
class ReferenceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10', })},
        # models.TextField: {'widget': RichTextEditorWidget},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 30, })},
        models.BooleanField: {'widget': CheckboxInput},
    }


    #model = Reference
    #inlines = [InlineModelAdmin]

    list_display = ('polity_wiki', 'old_ref_noescape', 'zotero_guess','new_zotero', 'sure', 'GS', '_pass', )
    #list_display_links = ('old_ref',)
    search_fields = ('polity', 'old_ref', 'year', 'creator', )
    list_editable = ('_pass', 'new_zotero')
    list_per_page = 20
    list_filter = ('_pass', CertaintyFilter)
    

    def polity_wiki(self, obj):
        return format_html("<a href='{url_link}' target='_blank'>{url_clickable}</a>",
                           url_link="http://seshatdatabank.info/browser/" + obj.polity, url_clickable=obj.polity)

    def GS(self, obj):
        if str(obj.gs_stars) != 'None' and obj.certainty >= 0 and obj.certainty <= 10:
            return format_html("<strong><a href='{url_link}' target='_blank'>{url_clickable} result(s) &#128270;</a></strong>",
                               url_link="https://scholar.google.com/scholar?q=" + obj.old_ref, url_clickable=str(obj.gs_stars))
        else:
            return format_html("<strong><a href='{url_link}' target='_blank'> &#128270;</a></strong>",
                               url_link="https://scholar.google.com/scholar?q=" + obj.old_ref)

    def sure(self, obj):
        if (str(obj.certainty)) != 'None':
            if obj.certainty > 57:
                my_color = 'green'
            elif obj.certainty <= 57 and obj.certainty >= 45:
                my_color = 'orange'
            # elif obj.certainty == 0:
            #    my_color = 'ornage'
            else:
                my_color = 'red'
            return format_html("<p style='color:{color_picked}'><strong>{cert_level}</strong></p>", color_picked=my_color, cert_level=str(obj.certainty) + "%")
        else:
            return format_html("<p><strong>{cert_level}</strong></p>", cert_level=str('0') + "%")

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
# http://seshatdatabank.info/browser/AfDurrn
#admin.site.register(Reference, ReferenceAdmin)

# better filtering:
# https://stackoverflow.com/questions/12102697/creating-custom-filters-for-list-filter-in-django-admin




@admin.display(description="Firm URL")
class CitationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '10', })},
        # models.TextField: {'widget': RichTextEditorWidget},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 30, })},
        models.BooleanField: {'widget': CheckboxInput},
    }


    #model = Reference
    #inlines = [InlineModelAdmin]

    list_display = ('link', 'citation_on_old_site', 'zotero_guess','zotero', 'sure', 'GS', 'done', )
    list_display_links = ('citation_on_old_site',)
    search_fields = ('polity', 'citation_text', 'year', 'creators', )
    list_editable = ('done', 'zotero')
    list_per_page = 20
    list_filter = (SiteFilter, DoneFilter, CertaintyFilter)
    

    def link(self, obj):
        # if we have both wiki and browser, show browser
        if obj.browser_number != 0:
            return format_html("<a href='{url_link_browser}' target='_blank'>{url_clickable_browser}</a>",
                           url_link_browser="http://seshatdatabank.info/browser/" + obj.polity + "#cite_note-" + str(obj.browser_number), url_clickable_browser=obj.polity)
        else:
            return format_html("<a href='{url_link_wiki}' target='_blank'>{url_clickable_wiki}</a> ",
                           url_link_wiki="http://seshat.info/w/index.php?title=" + obj.polity + "#cite_note-" + str(obj.wiki_number), url_clickable_wiki=obj.polity)

    def GS(self, obj):
        return format_html("<strong><a href='{url_link}' target='_blank'> &#128270;</a></strong>",
                               url_link="https://scholar.google.com/scholar?q=" + obj.citation_text)

    def sure(self, obj):
        if (str(obj.certainty)) != 'None':
            if obj.certainty > 57:
                my_color = 'green'
            elif obj.certainty <= 57 and obj.certainty >= 45:
                my_color = 'orange'
            # elif obj.certainty == 0:
            #    my_color = 'ornage'
            else:
                my_color = 'red'
            return format_html("<p style='color:{color_picked}'><strong>{cert_level}</strong></p>", color_picked=my_color, cert_level=str(obj.certainty) + "%")
        else:
            return format_html("<p><strong>{cert_level}</strong></p>", cert_level=str('0') + "%")


admin.site.register(Citation, CitationAdmin)
