from tasks.models import Task


def get_daily_progress(user, date):
    tasks = Task.objects.filter(project__user=user, date=date)
    completed = tasks.filter(is_completed=True).count()
    incomplete = tasks.filter(is_completed=False).count()

    return {"date": date, "completed": completed, "incomplete": incomplete}
