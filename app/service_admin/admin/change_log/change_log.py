#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

# Internal: 
from ...models.change_log import ChangeLog

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLogAdmin'
]


class ChangeLogMetricsAdmin(admin.TabularInline):
    verbose_name = "Metric association"
    verbose_name_plural = "Metric associations"
    model = ChangeLog.metrics.through
    readonly_fields = ['id']
    extra = 10


class ChangeLogPagesAdmin(admin.TabularInline):
    verbose_name = "Page association"
    verbose_name_plural = "Page associations"
    model = ChangeLog.pages.through
    readonly_fields = ['id']
    extra = 5


class ChangeLogAdminFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].widget.choices = self.fields['area'].choices[1:]

    class Meta:
        model = ChangeLog
        widgets = {
          'area': forms.SelectMultiple(choices=ChangeLog.area_choices)
        }
        fields = '__all__'


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    search_fields = [
        'heading'
    ]

    readonly_fields = [
        'id'
    ]

    list_display = [
        "heading",
        "date",
        "expiry",
        "display_banner",
        "high_priority",
        "log_type",
    ]

    list_filter = [
        ('display_banner', admin.BooleanFieldListFilter),
        ('high_priority', admin.BooleanFieldListFilter),
        ('date', admin.DateFieldListFilter),
        ('type', admin.RelatedOnlyFieldListFilter),
    ]

    form = ChangeLogAdminFrom

    inlines = [
        ChangeLogPagesAdmin,
        ChangeLogMetricsAdmin
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'type',
                    ('display_banner', 'high_priority'),
                    ('date', 'expiry'),
                    'heading',
                ),
            },
        ),
        (
            "Log content",
            {
                "fields": (
                    "body",
                    "details"
                )
            }
        ),
        (
            "Area associations",
            {
                "fields": (
                    'area',
                )
            }
        )
    )

    @admin.display(
        boolean=False,
        ordering='-type',
        description='Type',
    )
    def log_type(self, obj):
        colours = obj.get_type_colours()
        bg_colour = colours.get("background", "transparent")
        text_colour = colours.get("text", "#000000")
        return mark_safe(f'''\
<span class="table-tag" \
 style="margin-right: 2px; margin-bottom: 2px; font-size: x-small; color: {text_colour}; background: {bg_colour}">\
{obj.type.tag.upper().replace(" ", "&nbsp;")}\
</span>''')
