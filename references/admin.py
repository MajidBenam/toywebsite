from django.contrib.admin.options import InlineModelAdmin
from django.utils.html import format_html
from django.contrib import admin
from functools import partial
from django.forms.models import modelformset_factory
from django.db import models
from django.forms import TextInput, Textarea
#from tinymce.models import HTMLField, RichTextEditorWidget
from django.forms import CheckboxInput

from django.db.models import F, Sum
from django.urls import reverse


from .models import Reference, Citation, ExpandedCitation


class CertaintyFilter(admin.SimpleListFilter):
    title = format_html("<b style='color:green'>Certainty level</b>")
    parameter_name = "pagenum"

    def lookups(self, request, model_admin):
        return [
            ("Good_to_Go", format_html("<b>certainty > 80</b>")),
            ("Meh_to_Go",  format_html("<b>50 < certainty < 80</b>")),
            ("Bad_to_Go",  format_html("<b>certainty < 50</b>")),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "Good_to_Go":
            return queryset.distinct().filter(certainty__gte=80)
        if self.value() == "Meh_to_Go":
            return queryset.distinct().filter(certainty__gt=50).filter(certainty__lt=80)
        if self.value() == "Bad_to_Go":
            return queryset.distinct().filter(certainty__gte=0).filter(certainty__lte=50)



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
            return queryset.distinct().filter(child_count_wiki__gt=0).filter(child_count_browser__gt=0)
        if self.value() == "WIKI_to_Go":
            return queryset.distinct().filter(child_count_wiki__gt=0).filter(child_count_browser=0)
        if self.value() == "BROW_to_Go":
            return queryset.distinct().filter(child_count_browser__gt=0).filter(child_count_wiki=0)
        

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
        
class DifficultFilter(admin.SimpleListFilter):
    title = format_html("<b style='color:green'>Too Hard?</b>")
    parameter_name = "hard_or_not"

    def lookups(self, request, model_admin):
        return [
            ("Hard_to_Go", format_html("<b>Too Hard</b>")),
            ("Easy_to_Go", format_html("<b>Not Too Hard</b>")),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "Hard_to_Go":
            return queryset.distinct().filter(difficult=True)
        if self.value() == "Easy_to_Go":
            return queryset.distinct().filter(difficult=False)
        
class FertileFilter(admin.SimpleListFilter):
    title = format_html("<b style='color:green'>Many Children?</b>")
    parameter_name = "fert_or_not"

    def lookups(self, request, model_admin):
        return [
            ("Great_to_Go", format_html("<b>50+</b> Kids")),
            ("Good_to_Go", format_html("<b>15</b> to <b>49</b> Kids")),
            ("Norm_to_Go", format_html("<b>5</b> to <b>14</b> Kids")),
            ("Ok_to_Go", format_html("<b>2</b> to <b>4</b> Kids")),
            ("Meh_to_Go", format_html("Single Child")),

        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "Great_to_Go":
            return queryset.annotate(total_count=Sum(F('child_count_browser') + F('child_count_wiki'))).filter(total_count__gte=50).order_by('-total_count')
        if self.value() == "Good_to_Go":
            return queryset.annotate(total_count=Sum(F('child_count_browser') + F('child_count_wiki'))).filter(total_count__gte=15).filter(total_count__lt=50).order_by('-total_count')
        if self.value() == "Norm_to_Go":
            return queryset.annotate(total_count=Sum(F('child_count_browser') + F('child_count_wiki'))).filter(total_count__gte=5).filter(total_count__lte=14).order_by('-total_count')
        if self.value() == "Ok_to_Go":
            return queryset.annotate(total_count=Sum(F('child_count_browser') + F('child_count_wiki'))).filter(total_count__gte=2).filter(total_count__lte=4).order_by('-total_count')
            #return queryset.distinct().filter(child_count_browser__gt=5)
        if self.value() == "Meh_to_Go":
            return queryset.annotate(total_count=Sum(F('child_count_browser') + F('child_count_wiki'))).filter(total_count__lte=1).order_by('-total_count')

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

    list_display = ('link', 'citation_on_old_site', 'zotero_guess','zotero',  'sure', 'zot', 'GS', 'done', 'difficult')
    list_display_links = ('sure',)
    search_fields = ('polity', 'citation_text', 'year', 'creators', 'zotero')
    list_editable = ('done', 'zotero', 'difficult')
    list_per_page = 20
    list_filter = (SiteFilter, DoneFilter, DifficultFilter, CertaintyFilter, FertileFilter)

    def get_queryset(self, request):
        # Apply your default filter here
        queryset = super().get_queryset(request)
        queryset = queryset.filter(certainty__gte=-1)
        return queryset

    # def view_static_file(self, obj):
    #     url = reverse('static_file_view', args=["PgOrokE.html"])
    #     return format_html(f'<a href="{url}">"PgOrokE.html"</a>')
    # view_static_file.short_description = 'View Static File'

    def link(self, obj):
        # if we have both wiki and browser, show browser
        # if obj.browser_number != 0:
        #     return format_html("<a href='{url_link_browser}' target='_blank'>{url_clickable_browser}</a>",
        #                    url_link_browser="http://seshatdatabank.info/browser/" + obj.polity + "#cite_note-" + str(obj.browser_number), url_clickable_browser=obj.polity)
        if obj.browser_number != 0:
            url = reverse('static_file_view', args=[f"full_{obj.polity}.html"])
            url_link_browser= url +  "#cite_note-" + str(obj.browser_number)
            return format_html(f"<a href='{url_link_browser}' target='_blank'>{obj.polity}</a>",)
        else:
            url = reverse('static_file_view', args=[f"{obj.polity}.html"])
            url_link_browser= url +  "#cite_note-" + str(obj.wiki_number)
            return format_html(f"<a href='{url_link_browser}' target='_blank'>{obj.polity}</a>",)

            #return format_html(f'<a href="{url}">{obj.polity}</a>')
            # html_file_name = 'PgOrokE.html'
            # html_url = reverse('static', kwargs={'html_file_name': html_file_name})
            # link_html = format_html(f'<a href="{html_url}">Link to {html_file_name}</a>')
            # return link_html


            #return format_html(f"<span> {obj.polity} <br> #{obj.wiki_number} </span>")

    def GS(self, obj):
        return format_html("<strong><a href='{url_link}' target='_blank'> &#128270;</a></strong>",
                               url_link="https://scholar.google.com/scholar?q=" + obj.citation_text)

    def sure(self, obj):
        if (str(obj.certainty)) != 'None':
            if obj.certainty >= 80:
                my_color = 'green'
            elif obj.certainty <= 80 and obj.certainty >= 50:
                my_color = 'orange'
            # elif obj.certainty == 0:
            #    my_color = 'ornage'
            else:
                my_color = 'red'
            return format_html("<h3 style='color:{color_picked}'><strong>{cert_level}</strong></h3>", color_picked=my_color, cert_level=str(obj.certainty) + "%")
        else:
            return format_html("<h3><strong>{cert_level}</strong></h3>", cert_level=str('0') + "%")

    def zot(self, obj):
        if not obj.zotero:
            return "--"
        elif "-" not in obj.zotero:
            return format_html("<h3><a  style='color:red' href='{url_link}' target='_blank'> Z </a></h3>",
                               url_link="https://www.zotero.org/groups/1051264/seshat_databank/items/" + obj.zotero)
        else:
            return "---"
        

admin.site.register(Citation, CitationAdmin)
admin.site.register(ExpandedCitation)

