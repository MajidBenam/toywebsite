from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django import forms
from .custom_filters import noescape

# To get all the data in json format and save it in your local repo:
# $ python manage.py dumpdata references.Reference --indent 4 > toywebsite/references.json

# for references:
# $ python manage.py dumpdata references.Citation --indent 4 > toywebsite/citations_backup_July_24_1708.json

# to load data:
# $ python manage.py loaddata toywebsite/references.json
# $ python manage.py loaddata toywebsite/citations.json
# python manage.py loaddata toywebsite/test_new_row.json


class Reference(models.Model):
    class Meta:
        db_table = 'refs'

    old_ref = models.TextField()
    polity =  models.CharField(max_length=20)
    creator = models.CharField(max_length=60, null=True, blank=True)
    year = models.IntegerField(blank=True, null=True)
    #title = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    certainty = models.IntegerField(default = 0, blank=True, null=True)
    #old_zotero = models.URLField()

    gs_stars = models.IntegerField(default = 0, blank=True, null=True)

    pass_or_fail_opts = [
        ('PASS', 'Approved'),
        ('FAIL', 'Rejected'),
    ]
    # pass_or_fail = models.CharField(
    #     max_length=5,
    #     choices=pass_or_fail_opts,
    #     default='FAIL',
    # )
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    _pass = models.BooleanField(default=False, null=True)
    #_fail = models.BooleanField(default=True)
    #_reviewed = models.BooleanField(default=False, null=True)
    #final_check = models.Choices('Not sure', 'Approved', 'New_Pick')
    new_zotero = models.CharField(max_length=300, default='NO_ZOTERO', blank=True, null=True)
    #new_zotero = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def creator_noescape(self):
        return noescape(self.creator)
    
    def old_ref_noescape(self):
        if self.year == 2015:
            return noescape("<b> OOOPS   " + self.old_ref + "</b>")
        else:
            return noescape("<b>" + self.old_ref + "</b>")
    def zotero_guess(self):
        return noescape(f"<span style='color:teal;'><b>{self.year}, {self.creator}:</b><br> {self.title} </span>")
    


    def __str__(self):
        #end_of_title = min(len(self.title), 16)
        #return f'{self.year}_{self.creator}_{self.title[0:end_of_title]} ...'
        return f'{self.year}_{self.creator}'

    # def clean(self):
    #     if self._pass == self._fail:
    #         raise ValidationError('Impossibble')

# citation 5738 was problematic. as it had no Zotero link.
class Citation(models.Model):
    class Meta:
        db_table = 'citations'

    citation_text = models.TextField()
    polity =  models.CharField(max_length=20)
    creators = models.CharField(max_length=60, null=True, blank=True)
    year = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    certainty = models.IntegerField(default = 0, blank=True, null=True)
    difficult = models.BooleanField(default=False, null=True)

    BOOL_CHOICES = ((True, 'Yessss'), (False, 'No'))

    WEBSITE_CHOICES = (
        ("wiki", "Seshat.info"),
        ("browser", "seshatdatabank.info"),
    )
    wiki_number = models.IntegerField(default = 0, blank=True, null=True)
    browser_number = models.IntegerField(default = 0, blank=True, null=True)

    child_count_wiki = models.IntegerField(default = 0, blank=True, null=True)
    child_count_browser = models.IntegerField(default = 0, blank=True, null=True)

    citation_number = models.IntegerField(default = 0, blank=True, null=True)

    site = models.CharField(max_length=8, choices=WEBSITE_CHOICES, blank=True, null=True)

    done = models.BooleanField(default=False, null=True)

    zotero = models.CharField(max_length=300, default='--------', blank=True, null=True)

    
    def citation_on_old_site(self):
        #chunks = [self.citation_text[i:i+30] for i in range(0, len(self.citation_text), 30)]
        #my_string_with_br = "<br>".join(chunks)

        return noescape("<b>" + self.citation_text + "</b>")
    def zotero_guess(self):
        if self.title == "abc xyz":
            return noescape(f"<span style='color:#a41515;'><b>---, ---:</b><br> --------------- </span>")
        elif self.certainty < 50:
            return noescape(f"<span style='color:#a41515;'><b>{self.year}, {self.creators}:</b><br> {self.title} </span>")
        else:
            return noescape(f"<span style='color:teal;'><b>{self.year}, {self.creators}:</b><br> {self.title} </span>")
    


    def __str__(self):
        if self.year and self.creators:
            return f'{self.id}: {self.year}_{self.creators} {self.citation_text[0:50]}'
        else:
            return f'{self.id}:  {self.citation_text[0:50]}'
        
class ExpandedCitation(models.Model):
    class Meta:
        db_table = 'expandedcitations'

    WEBSITE_CHOICES = (
        ("wiki", "Seshat.info"),
        ("browser", "seshatdatabank.info"),
    )

    expanded_citation_text = models.TextField(max_length=900)
    citation_on_toy = models.ForeignKey(Citation, on_delete=models.SET_NULL, null=True, blank=True,related_name="ref1")
    expanded_polity =  models.CharField(max_length=20)
    expanded_site = models.CharField(max_length=8, choices=WEBSITE_CHOICES, blank=True, null=True)
    expanded_citation_number = models.IntegerField(default = 0, blank=True, null=True)
    citation_on_toy_2 = models.ForeignKey(Citation, on_delete=models.SET_NULL, null=True, blank=True,related_name="ref2")
    citation_on_toy_3 = models.ForeignKey(Citation, on_delete=models.SET_NULL, null=True, blank=True,related_name="ref3")

    def __str__(self):
        return f'({self.expanded_polity}: {self.expanded_site}: {self.expanded_citation_number}) {self.expanded_citation_text}'



""" expanded_citation_text:     Aliyadeh Good life in Bordsioy 123, 125
    citation_on_toy:            Aliyadeh Good life in Bordsioy
    expanded_polity:  AfDurrn
    expanded_site:   wiki 
    expanded_citation_number: 14



"""
