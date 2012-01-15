from django import forms

from apps.serverinfo.models import AttributeType

class AddAttributeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """
        Handle attributes field here in __init__ so we can avoid Django caching our Attributes
        """
        super(AddAttributeForm, self).__init__(*args, **kwargs)
        types = []
        for t in AttributeType.objects.all().order_by('name'):
            types.append((t.id, t.name))
        validTypes = tuple(types)
        self.fields['attrtype'] = forms.ChoiceField(label='Type', choices=validTypes)
        self.fields['value'] = forms.CharField(max_length=255)

    class Meta:
        # FIXME
        # Doesnt work, but for more dynamic choise of attributes data,
        # we can use onchange and get other "helperfields" over ajax.
        # Then we can populate the value field..
        # Put it up like "value" above..
        widgets = {
            'attrtype': forms.Select(attrs={'onchange': 'getAttributeForm'}),
            }


class AddIPForm(forms.Form):
    '''
    There are some magic here..
    The dynamic form which we are changing out via ajax is calculated from helpers/attribute_dynamics.py
    Also, take a look in views.py and serverinfo/network_extraform.html
    There is also an own api function to populate this.
    '''

    value = forms.CharField(
        max_length=255,
        widget=forms.TextInput({'placeholder': 'Value', 'class': 'ip'}),
        )
