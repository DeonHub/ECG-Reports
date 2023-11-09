from datetime import datetime

from django.shortcuts import redirect


def counter(request):

    now = datetime.now()
    year = now.year

    date = now.strftime("%A, %d %B, %Y")

    time = now.strftime("%H:%M %p")

    return { 'date': date, 'time': time, 'year':year }
