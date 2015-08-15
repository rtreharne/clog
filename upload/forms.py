from django import forms
from multiupload.fields import MultiFileField
from .rip import DataRip, get_cell_param
from .models import Cell
from projects.models import Project


class ContactForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = ['notes', 'date', 'cell_area']

    files = MultiFileField(min_num=1, max_num=100, max_file_size=1024*1024*5)

    def __init__(self, project_id=None, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.project = project_id 

    def save(self):
        instance = Project.objects.get(id=self.project)
        attachment_inst = super(ContactForm, self).save(commit=False)

        for each in self.cleaned_data['files']:
            params = get_cell_param(each, self.cleaned_data['cell_area'])
            
            if params == None:
                continue    

            jsc = round(params.extract_jsc(), 2)
            voc = round(params.extract_voc(), 2)
            ff = round(params.extract_ff(), 2)
            eff = round(params.extract_eff(), 2)
            Cell.objects.create(file=each, notes=attachment_inst.notes, date=attachment_inst.date, label=each.name, project=instance, jsc=jsc, voc=voc, ff=ff, eff=eff)
            
        return instance
