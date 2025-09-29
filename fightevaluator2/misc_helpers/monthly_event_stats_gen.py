from datetime import date
from django.db.models import Count, Sum
from ..fightEvaluator.models import EventStat, MonthlyEventStats  # replace `yourapp`

def collect_monthly_stats(year=None, month=None):
    """
    Collect stats for a given year and month.
    Defaults to the current month if none provided.
    Returns: (monthly_stats_object, created_bool)
    """
    if year is None or month is None:
        today = date.today()
        year = year or today.year
        month = month or today.month

    # filter events in the target month
    event_stats = EventStat.objects.filter(
        event__date__year=year,
        event__date__month=month,
    )

    # aggregate totals
    aggregates = event_stats.aggregate(
        total_events=Count("event", distinct=True),
        total_predictions=Sum("predictions"),
        total_correct=Sum("correct"),
    )

    # handle None values
    events = aggregates["total_events"] or 0
    predictions = aggregates["total_predictions"] or 0
    correct = aggregates["total_correct"] or 0

    # create or update the MonthlyEventStats record
    monthly_stats, created = MonthlyEventStats.objects.update_or_create(
        year=year,
        month=month,
        defaults={
            "events": events,
            "predictions": predictions,
            "correct": correct,
        },
    )

    return monthly_stats, created
