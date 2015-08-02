from django import forms
from multiupload.fields import MultiFileField
from .rip import DataRip
from .models import Cell
from projects.models import Project


class ContactForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = ['notes']

    files = MultiFileField(min_num=1, max_num=100, max_file_size=1024*1024*5)

    def __init__(self, project_id=None, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.project = project_id 

    def save(self):
        instance = Project.objects.get(id=self.project)
        attachment_inst = super(ContactForm, self).save(commit=False)

        for each in self.cleaned_data['files']:
            params = self.get_cell_param(each)
            jsc = round(params.extract_jsc(), 2)
            voc = round(params.extract_voc(), 2)
            ff = round(params.extract_ff(), 2)
            eff = round(params.extract_eff(), 2)
            Cell.objects.create(file=each, notes=attachment_inst.notes, label=each.name, project=instance, jsc=jsc, voc=voc, ff=ff, eff=eff)
            
        return instance

    def get_cell_param(self, filename):
        import numpy as np
        x = np.loadtxt(filename, usecols=(0,))
        y = np.loadtxt(filename, usecols=(1,))
        data = DataRip(x, y)
        return data

