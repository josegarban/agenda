from django import forms
from dal import autocomplete

from .models import Upload
from django.utils.translation import ugettext_lazy as _

class UploadForm(forms.ModelForm):

    uploadtype  = forms.ChoiceField(    label   = _("Upload type"),
                                        choices = Upload.UPLOADTYPES_CHOICES,
                                        widget  = forms.Select(attrs    = { 'class':'select',
                                                                            'style': 'margin-bottom:2rem;width:100%;',
                                                                            },)
                                        )
    description = forms.CharField(      label = _("Description"),
                                        help_text = _('Optional'),
                                        widget = forms.TextInput(attrs = {  'class':'input',
                                                                            'style': 'margin-bottom:.1rem;width:100%;padding-bottom:0.5rem;',
                                                                            },)
                                        )
    upload      = forms.FileField(      label="",
                                        widget = forms.FileInput(attrs = {  'type':"file",
                                                                            }))

    class Meta:
        model = Upload
        fields = ('uploadtype', 'description', 'upload')
