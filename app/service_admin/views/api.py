#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from json import loads, dumps

# 3rd party:
from django.shortcuts import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from textstat import text_standard, flesch_reading_ease

# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'text_stats_api_view'
]


def get_flesch_level(score):
    if score >= 90:
        return "Very easy"
    elif score >= 80:
        return "Easy"
    elif score >= 70:
        return "Fairly easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Confusing"


@login_required()
@csrf_exempt
def text_stats_api_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and not request.method == "POST":
        raise Http404()

    payload = loads(request.body)['payload']

    flesch_score = flesch_reading_ease(payload)
    result = dumps({
        "estimated_school_grade": text_standard(payload),
        "flesch_score": flesch_score,
        "flesch_level": get_flesch_level(flesch_score)
    })

    return HttpResponse(result, content_type="application/json")
