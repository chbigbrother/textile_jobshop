# schedule/urls.py

from django.urls import path

from .views import *
app_name = 'schedule'
urlpatterns = [
    path('', home, name='textile.schedule.index'),
    path('history/', history, name='textile.schedule.history'),
    path('confirmed/', sch_confirmed, name='textile.schedule.sch_confirmed'),
    path('confirmed/monthly/', monthly_confirmed_order, name='schedule.monthly_confirmed_order'),
    path('history/chart/<str:id>/<str:schDate>/', history_chart, name='textile.schedule.history_chart'),
    path('history/graph/chart/', draw_history_chart, name='draw_history_chart'),
    path('graph/csv/generate/', generate_data, name='generate_data'),
    path('graph/draw/', draw_graph, name='draw_graph'),
    path('avail/comp/', available_comp, name='available_comp'),
    path('test/data/', test_data, name='test_data'),
    path('fixed/order/', fixed_order, name='fixed_order'),
    path('confirmed/order/', confirmed_order, name='confirmed_order'),
    path('delete/order/', delete_order, name='delete_order'),
    path('schedule/history/', schedule_history, name='schedule_history'),

    ## algorithm test urls
    path('test/', test, name='algorithm.schedule.test'),
    path('fjsp/test/', fjsp_test, name='algorithm.schedule.fjsp_test'),
    path('fjsp/chart/', fjsp_chart, name='schedule.fjsp_chart'),
    path('test/chart/', test_chart, name='schedule.test_chart'),
]