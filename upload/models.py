from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from time import time
from django.core.exceptions import ValidationError
from decimal import Decimal
from projects.models import Project


class Cell(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('Project'))
    notes = models.TextField(max_length=500)
    file = models.FileField(_('Cell'), upload_to='cells')
    jsc = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.000))
    voc = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.000))
    ff = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.000))
    eff = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.000))
    cell_area = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.25))

    date = models.DateTimeField(default=timezone.datetime.today)
    label = models.CharField(max_length=128)

    def __unicode__(self):
        return self.file.name
