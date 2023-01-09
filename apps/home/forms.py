from django import forms
from apps.home.models import *
from django.utils.translation import ugettext_lazy as _

REPORT_TYPE = (
          ('inburst', 'In Burst'),
          ('outburst', 'Out Burst'),
          ('applications', 'Extract Applications'),
    )
class TimestampForm(forms.Form):
    date_from = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'id': 'datetimepicker1',
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    date_to = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'id': 'datetimepicker2',
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    report_type = forms.ChoiceField(choices=REPORT_TYPE)

APP_REPORT_TYPE = (
          ('octets', 'Total Octets per Site'),
          ('outburst', 'Top 30 Apps'),
          ('applications', 'Top Interfaces per App'),
    )
class AppReportForm(forms.Form):
    date_from = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'id': 'datetimepicker1',
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    date_to = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'id': 'datetimepicker2',
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    report_type = forms.ChoiceField(choices=APP_REPORT_TYPE)