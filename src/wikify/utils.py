from django import forms
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy

def get_model_wiki_form(model):
    """Creates a form for the given model, excluding the primary key."""

    primary_key_field = model._meta.pk.name

    # Create the model form and exclude the primary key
    form_class = modelform_factory(model, exclude=(primary_key_field,))

    # Add a comment widget
    comment_widget = forms.TextInput(
                          attrs={'placeholder': ugettext_lazy("Add a comment")})
    comment_field = forms.CharField(widget=comment_widget,
                                    required=False,
                                    label=ugettext_lazy("Comment"))
    form_class.base_fields['wikify_comment'] = comment_field
    return form_class

def model_field_iterator(instance):
    """
    Iterates over the instance's fields (excluding the primary key) and returns
    each field with its value in the order of declaration inside the model.
    """
    for field in instance._meta.fields:
        if field != instance._meta.pk:
            yield (field, getattr(instance, field.name))

def version_field_iterator(old_version, new_version):
    """
    Iterates over the instance's fields (excluding the primary key) and returns
    each field with its old and new value in the order of declaration inside the
    model.
    """
    old_obj = old_version.object_version.object if old_version else None
    new_obj = new_version.object_version.object
    for field in new_obj._meta.fields:
        if field != new_obj._meta.pk:
            yield (field,
                   getattr(old_obj, field.name, None),
                   getattr(new_obj, field.name))
