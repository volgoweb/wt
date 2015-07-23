# -*- coding: utf-8 -*-
from .views import (
    TodayTasksPage,
    # FavoriteTasksPage,
    OverdueTasksPage,
    LaterTasksPage,
    CompletedTasksPage,
    OutboundTasksPage,
)


def task_counts(request):
    context = {}
    if request.user.is_authenticated():
        context = {
            'task_counts': {
                'today': TodayTasksPage.get_base_count_from_class(request),
                # 'favorite': FavoriteTasksPage.get_base_count_from_class(request),
                'overdue': OverdueTasksPage.get_base_count_from_class(request),
                'later': LaterTasksPage.get_base_count_from_class(request),
                'completed': CompletedTasksPage.get_base_count_from_class(request),
                'outbound': OutboundTasksPage.get_base_count_from_class(request),
            }
        }
    return context
