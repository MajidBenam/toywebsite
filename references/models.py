from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django import forms
from .custom_filters import noescape

# To get all the data in json format and save it in your local repo:
# $ python manage.py dumpdata references.Reference --indent 4 > toywebsite/references.json

# for references:
# $ python manage.py dumpdata references.Citation --indent 4 > toywebsite/citations.json

# to load data:
# $ python manage.py loaddata toywebsite/references.json
# $ python manage.py loaddata toywebsite/citations.json


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


class Citation(models.Model):
    class Meta:
        db_table = 'citations'

    citation_text = models.TextField()
    polity =  models.CharField(max_length=20)
    creators = models.CharField(max_length=60, null=True, blank=True)
    year = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    certainty = models.IntegerField(default = 0, blank=True, null=True)
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
        if self.year == 2015:
            return noescape("<b>" + self.citation_text + "</b>")
        else:
            return noescape("<b>" + self.citation_text + "</b>")
    def zotero_guess(self):
        return noescape(f"<span style='color:teal;'><b>{self.year}, {self.creators}:</b><br> {self.title} </span>")
    


    def __str__(self):
        if self.year and self.creators:
            return f'{self.year}_{self.creators}'
        else:
            return f'{self.id}'