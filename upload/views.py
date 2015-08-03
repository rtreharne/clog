from django.views.generic.edit import FormView, CreateView
from django.shortcuts import render
from .forms import ContactForm
from .models import Cell


class ContactView(CreateView):
    model = Cell
    submitted = False
    form_class = ContactForm
    template_name = 'upload.html'
    success_url = '?success'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ContactView, self).get_form_kwargs(*args, **kwargs)
        kwargs.update(self.kwargs)
        return kwargs

    def form_valid(self, form):
        self.submitted = True
        super(ContactView, self).form_valid(form)
        return render(self.request, self.template_name, self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(ContactView, self).get_context_data(**kwargs)
        ctx['submitted'] = self.submitted
        ctx['id'] = self.kwargs['project_id']
        return ctx
