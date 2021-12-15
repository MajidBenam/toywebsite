from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django import forms



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

    def __str__(self):
        #end_of_title = min(len(self.title), 16)
        #return f'{self.year}_{self.creator}_{self.title[0:end_of_title]} ...'
        return f'{self.year}_{self.creator}'

    # def clean(self):
    #     if self._pass == self._fail:
    #         raise ValidationError('Impossibble')