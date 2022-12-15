from django.shortcuts import render
from django.db.models import Max
from django.db.models.aggregates import Count
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.http.response import HttpResponse
from .main import GAStart
from .fjsp.main import FJSPStart
from common.views import id_generate, date_str, calc_date_str, comma_str, date_remove, date_plus, regex
from company.models import *
from order.models import *
import pandas as pd
import json, csv, os, datetime, calendar, random
from datetime import timedelta
from calendar import monthrange
from bson import json_util
from random import randint
from collections import Counter
import numpy as np

now = datetime.datetime.now()
# 스케쥴링실행 Execute Schedule HTML
def home(request):
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        'dateFrom': date.strftime("%Y-%m-%d"),
        'path': '스케쥴링 / 스케쥴링실행'
    }
    return render(request, 'textile/schedule/schedule.html', date)

# 스케쥴링이력 Schedule history HTML
def history(request):
    date = datetime.datetime.today() - timedelta(days=3)

    if 'dateFrom' in request.GET:
        sch_date_from = datetime.datetime.strptime(request.GET['dateFrom'], "%Y-%m-%d")
        sch_date_to = datetime.datetime.strptime(request.GET['dateTo'], "%Y-%m-%d")

        date_from = request.GET['dateFrom'].replace('-', '')
        date_to = request.GET['dateTo'].replace('-', '')

        schedule_list = Schedule.objects.raw(
            " SELECT sch_id, SUBSTRING(ANY_VALUE(sch_id), 4, 8) as exe_date, max(COUNT) as max_count " +
            " FROM company_schedule " +
            " WHERE SUBSTRING(sch_id, 4, 8) >= '" + date_from + "' AND "
                    "SUBSTRING(sch_id, 4, 8) <= '" + date_to + "'" +
            ' GROUP BY STR_TO_DATE(created_at, "%%Y-%%m-%%d")')
    else:
        sch_date_from = date
        sch_date_to = datetime.datetime.today()
        schedule_list = Schedule.objects.raw(
            "SELECT *, SUBSTRING(ANY_VALUE(sch_id), 4, 8) as exe_date, max(COUNT) as max_count " +
            "FROM company_schedule " +
            "WHERE SUBSTRING(sch_id, 4, 8) >= '" + date.strftime("%Y%m%d") + "' AND "
            "SUBSTRING(sch_id, 4, 8) <= '" + datetime.datetime.today().strftime( "%Y%m%d") + "'" +
            ' GROUP BY STR_TO_DATE(created_at, "%%Y-%%m-%%d")')

    sch_list = []
    order_id = ''
    for sch in schedule_list:
        sch_dict = {}
        sch_dict['max_count'] = sch.max_count
        sch_dict['exe_date'] = date_str(sch.exe_date)
        sch_dict['work_end_date'] = date_str(sch.work_end_date)
        sch_dict['date_from'] = sch_date_from.strftime("%Y-%m-%d")
        sch_dict['date_to'] = sch_date_to.strftime("%Y-%m-%d")
        order_list = OrderList.objects.filter(prod_id=sch.prod_id)
        if len(order_list) == 0:
            continue;
        order_id = date_str(sch.exe_date)

        for i in order_list:
            sch_dict['sch_date'] = date_str(i.sch_date)

        sch_dict['orderid'] = order_id
        sch_list.append(sch_dict)

    date = {
        'dateFrom': sch_date_from.strftime("%Y-%m-%d"),
        'dateTo': sch_date_to.strftime("%Y-%m-%d"),
        'path': '스케쥴링 / 스케쥴링이력',
        'sch_list' : sch_list
    }
    return render(request, 'textile/schedule/sch_history.html', date)

# 스케쥴링이력 간트차트 Schedule history in Gantt Chart HTML
def history_chart(request, id, schDate):
    date = datetime.datetime.today() - timedelta(days=3)

    date = {
        'dateFrom': date.strftime("%Y-%m-%d"),
        'id' : id,
        'schDate' : schDate,
        'path': '스케쥴링 / 스케쥴링이력',
    }
    return render(request, 'textile/schedule/sch_history_chart.html', date)


def test(request):
    data = {
        'id': id,
        'path': '스케쥴링 / 스케쥴링테스트',
    }
    return render(request, 'algorithm_test/schedule/sch_test.html', data)

def fjsp_test(request):
    data = {
        'id': id,
        'path': '스케쥴링 / FJSP 스케쥴링테스트',
    }
    return render(request, 'algorithm_test/schedule/fjsp_sch_test.html', data)


def fjsp_chart(request):

    time_comb = []
    data = open("./schedule/fjsp/test_data/fjsp_data.txt", "w", newline="", encoding="UTF-8")

    for i in request.GET:
        request = json.loads(i)
    machine_num = int(request['machine_num']) # 기계대수
    job_num = int(request['job_num']) # 작업개수
    operation = request['operation']  # 작업별 operation
    demands = request['demands']  # 작업별수량

    data.writelines('{0} {1} {2} \n'.format(job_num, machine_num, 1))

    for i in range(job_num):
        inner_string = ''
        inner_string += '{0} {1} '.format(operation[i], machine_num)
        for j in range(operation[i]):
            if j != 0:
                inner_string += '{0} '.format(machine_num)
            for k in range(machine_num):
                inner_string += '{0} {1} '.format(k+1, demands[k])
        data.write(inner_string + '\n')
    data.close()

    FJSPStart()
    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(time_comb, default=json_default, ensure_ascii=False),
                        content_type="application/json")




def test_chart(request):

    for i in request.GET:
        request = json.loads(i)
    machine_num = int(request['machine_num']) # 기계대수
    job_num = int(request['job_num']) # 작업개수
    demands = request['demands']  # 작업별수량

    time_comb = []
    # [[], [], []]
    for i in range(machine_num):
        time_comb.append([])

    colorbox = []
    color_dict = {}
    for i in range(100):
        colorArr = ['1', '2', '3', '4', '5', '6', '7',
                    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        colorbox.append("#" + color)

    for i in range(job_num):
        if demands[i] > 1000:
            for j in range(demands[i] // 1000):
                if len(time_comb[j%machine_num]) == 0:
                    time_comb[j % machine_num].append([0,1000,i,colorbox[i]])
                else:
                    prev_end = time_comb[j % machine_num][len(time_comb[j % machine_num])-1][1]
                    time_comb[j % machine_num].append([prev_end, int(prev_end) + 1000, i, colorbox[i]])
        else:
            time_comb[i % machine_num].append([0, 1000, i, colorbox[i]])
    # print(time_comb)

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(time_comb, default=json_default, ensure_ascii=False),
                        content_type="application/json")

# 스케쥴링이력 간트차트 그리기
def draw_history_chart(request):

    for i in request.GET:
        request = json.loads(i)

    id = request['orderId'] # 스케줄일자
    schDate = request['schDate'] # 주문일자

    sch_list, count = schedule_list(id, schDate)

    result = {}
    result_list = []
    final_list = []

    for cnt in range(int(count)+1):
        result['max_count'] = int(cnt)+1
        for sch in sch_list:
            product = Product.objects.filter(prod_id=sch.prod_id)[0]
            if sch.count == int(cnt)+1:
                result_dict = {}
                result_dict['facility_id'] = sch.facility_id.facility_name
                result_dict['prod_name'] = product.prod_name
                result_dict['order_id_num'] = sch.order_id_num
                result_dict['count'] = sch.count
                result_dict['sch_color'] = sch.sch_color
                result_dict['x_axis_1'] = sch.x_axis_1
                result_dict['x_axis_2'] = sch.x_axis_2
                result_dict['y_axis_1'] = sch.y_axis_1
                result_dict['work_str_date'] = date_str(sch.work_str_date)
                result_dict['work_end_date'] = date_str(sch.work_end_date)
                result_list.append(result_dict)
        result['chart_draw'] = result_list
    final_list.append(result)

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(final_list, default=json_default, ensure_ascii=False), content_type="application/json")

# 확정 스케쥴 Fixed Schedule HTML
def sch_confirmed(request):
    date = datetime.datetime.today()
    date = date.strftime("%Y%m%d")
    year = date[0:4]
    month = date[4:6]

    lastday = calendar.monthrange(int(year), int(month))[1]
    final_result = OrderSchedule.objects.filter(sch_id__work_end_date__gte=date, use_yn='Y')
    available_list = []
    for i in final_result:
        available_dict = {}
        available_dict['work_str_date'] = date_str(i.sch_id.work_str_date)
        available_dict['work_end_date'] = date_str(i.sch_id.work_end_date)
        available_dict['order_id'] = i.order_id_id
        orderlist = OrderList.objects.get(order_id=i.order_id_id)
        available_dict['sch_date'] = date_str(orderlist.sch_date)
        available_dict['sch_id'] = i.sch_id
        available_list.append(available_dict)

    date = {
        'order_list': available_list,
        'path': '스케쥴링 / 확정스케쥴조회'
    }
    return render(request, 'textile/schedule/sch_confirmed.html', date)

def schedule_list(id, schDate):

    date_from = id.replace('-', '')

    schedule_list = Schedule.objects.raw(
        "SELECT * " +
        "FROM company_schedule " +
        "WHERE SUBSTRING(sch_id, 4, 8) = '" + date_from + "' ")

    count = Schedule.objects.raw(
        ' SELECT sch_id, MAX(COUNT) as count ' +
        ' FROM company_schedule' +
        ' WHERE SUBSTRING(sch_id, 4, 8) = "' + date_from + '"')
    sch_list = []
    for i in schedule_list:
        sch_list.append(i)
    for j in count:
        count = j.count

    return sch_list, count


# 수락한 오더 리스트 조회 (월별)
def monthly_confirmed_order(request):
    date = datetime.datetime.today().strftime("%Y%m")
    for i in request.GET:
        request = json.loads(i)
    available_list = []
    id = request['id']
    if len(id) > 0:
        final_result = OrderSchedule.objects.filter(order_id=id, use_yn='Y')
    else:

        if request['str_year'] != None:
            str_year = request['str_year']
            str_month = request['str_month']
            end_year = request['end_year']
            end_month = request['end_month']

            final_result = OrderSchedule.objects.filter(sch_id__work_end_date__lte=str(end_year) + str(end_month) + '31', use_yn='Y')
        else:
            year = date[0:4]
            month = date[4:6]
            lastday = calendar.monthrange(int(year), int(month))[1]
            final_result = OrderSchedule.objects.filter(sch_id__work_str_date__gte=date + '01').filter(
                sch_id__work_end_date__lte=date + str(lastday), use_yn='Y')

    for i in final_result:
        available_dict = {}
        available_dict['work_str_date'] = i.sch_id.work_str_date
        available_dict['work_end_date'] = i.sch_id.work_end_date
        available_dict['order_id'] = i.order_id_id
        available_dict['sch_id'] = i.sch_id_id
        available_dict['sch_date'] = i.sch_id_id[3:11]
        available_list.append(available_dict)

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(available_list, default=json_default, ensure_ascii=False), content_type="application/json")

# draw Gantt Chart data
def draw_graph(request):
    count = Schedule.objects.filter(comp_id=request.user.groups.values('id')[0]['id'],
                                    created_at__year=now.year, created_at__month=now.month, created_at__day=now.day)
    count = count.aggregate(Max('count'))

    for i in Group.objects.all():
        for j in Group.objects.filter(name=i).values():
            schedule_list = Schedule.objects.filter(count=count['count__max'],
                                                    created_at__year=now.year, created_at__month=now.month,
                                                    created_at__day=now.day).order_by('facility_id')
            schedule_list = tuple(schedule_list.values())

    prev_fac = []
    prod = []
    prev_x_2 = []
    prev_x_1 = []
    str_date = []
    sch_color = []
    sch_id = []
    for i in schedule_list:
        prev_fac.append(i['facility_id_id'])
        prod.append(i['prod_id'])
        prev_x_1.append(i['x_axis_1'])
        prev_x_2.append(i['x_axis_2'])
        str_date.append(i['work_str_date'])
        sch_color.append(i['sch_color'])
        sch_id.append(i['sch_id'])
    cnt = Counter(prev_fac)
    cnt = dict(cnt)
    schedule_dict = {}

    for i in cnt:
        arr = []
        fac = []
        color = []
        prd = []
        x_1 = []
        x_2 = []
        str_d = []
        sch_i = []
        for j in range(len(prev_fac)):
            if i == prev_fac[j]:
                fac.append(prev_fac[j])
                prd.append(prod[j])
                color.append(sch_color[j])
                x_1.append(prev_x_1[j])
                x_2.append(prev_x_2[j])
                str_d.append(str_date[j])
                sch_i.append(sch_id[j])
        arr.append(x_1)
        arr.append(x_2)
        arr.append(str_d)
        arr.append(fac)
        arr.append(prd)
        arr.append(color)
        arr.append(sch_i)
        schedule_dict[i] = arr

    x_1 = []
    x_2 = []
    str_d = []
    fac = []
    prd = []
    cl = []
    sch_i = []
    date = datetime.datetime.today().strftime("%Y%m%d")
    cnt = 0
    for i in schedule_dict:
        sequence = []
        for j in range(len(schedule_dict[i][2])):
            sequence = list(np.argsort(schedule_dict[i][2]))
        for k, h in enumerate(sequence):

            if k == 0:
                x_1.append(0.0)
                x_2.append(schedule_dict[i][1][h] - schedule_dict[i][0][h])
                str_d.append(schedule_dict[i][2][h])
                fac.append(schedule_dict[i][3][h])
                prd.append(schedule_dict[i][4][h])
                cl.append(schedule_dict[i][5][h])
                sch_i.append(schedule_dict[i][6][h])
            else:  # 이전거랑 현재거랑 비교 k, k-1
                # if schedule_dict[i][2][h+1] ==  min(schedule_dict[i][2]):
                if(h + 1 < len(sequence)):
                    prev_end_date = date_plus(schedule_dict[i][2][h+1],
                                              x_2[cnt - 1])
                else:
                    prev_end_date = date_plus(min(schedule_dict[i][2]),
                                              x_2[cnt - 1])
                # 전 작업의 끝에서 현재 작업의 시작점을 빼고
                prev_m_pres_str = int(calc_date_str(prev_end_date, schedule_dict[i][2][h]).days)
                # 거기서 x1 에서 x2까지의 거리를 계산한다.
                calc_x1_x2 = abs(prev_m_pres_str) + (schedule_dict[i][1][h] - schedule_dict[i][0][h])
                if prev_m_pres_str > 0:
                    prev_m_pres_str = schedule_dict[i][0][h]
                    calc_x1_x2 = schedule_dict[i][1][h]

                pres_m_prev = int(calc_date_str(date, prev_end_date).days)
                pre_m_this = int(calc_date_str(date, schedule_dict[i][2][sequence[h]]).days)
                if (pres_m_prev > pre_m_this):
                    if schedule_dict[i][0][sequence[h]] == 0.0:
                        x_2.append(calc_x1_x2) # int(calc_date_str(date, prev_end_date).days) + (schedule_dict[i][1][sequence[h - 1]] - schedule_dict[i][0][sequence[h - 1]]))
                    else:
                        x_2.append(calc_x1_x2)# int(calc_date_str(date, prev_end_date).days) + (schedule_dict[i][1][sequence[h - 1]] - schedule_dict[i][0][sequence[h - 1]]))

                    x_1.append(abs(prev_m_pres_str))# int(calc_date_str(date, prev_end_date).days))
                    str_d.append(schedule_dict[i][2][h])
                    fac.append(schedule_dict[i][3][h])
                    prd.append(schedule_dict[i][4][h])
                    cl.append(schedule_dict[i][5][h])
                    sch_i.append(schedule_dict[i][6][h])
                else:
                    x_1.append(schedule_dict[i][0][h])  # schedule_dict[i][0][k] = plus_diff + schedule_dict[i][1][k-1]
                    x_2.append(schedule_dict[i][1][h])
                    str_d.append(schedule_dict[i][2][h])
                    fac.append(schedule_dict[i][3][h])
                    prd.append(schedule_dict[i][4][h])
                    cl.append(schedule_dict[i][5][h])
                    sch_i.append(schedule_dict[i][6][h])

                cnt += 1
    for i in range(len(schedule_list)):
        entry = Schedule.objects.get(sch_id=sch_i[i])

        entry.x_axis_1 = x_1[i];
        entry.x_axis_2 = x_2[i];
        # print(entry.sch_id, entry.x_axis_1, entry.x_axis_2, x_1[i], x_2[i])
        entry.save();

        # fac_name = Facility.objects.get(facility_id=schedule_list[i]['facility_id_id'])
        fac_name = Facility.objects.get(facility_id=fac[i])
        # fac_name = prev_fac[i]
        schedule_list[i]['work_str_date'] = date_str(str_d[i])  # date_str(schedule_list[i]['work_str_date'])
        schedule_list[i]['work_end_date'] = date_str(schedule_list[i]['work_end_date'])
        schedule_list[i]['x_axis_1'] = float(x_1[i])
        schedule_list[i]['x_axis_2'] = float(x_2[i])
        schedule_list[i]['y_axis_1'] = fac_name.facility_name
        product = Product.objects.get(prod_id=prd[i])  # schedule_list[i]['prod_id'])
        schedule_list[i]['prod_id'] = prd[i]
        schedule_list[i]['prod_name'] = product.prod_name
        schedule_list[i]['sch_color'] = cl[i]

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(schedule_list, default=json_default))

## GA JSSP algorithm execution
def generate_data(request):
    # 회사 아이디를 얻기 위한 유저 정보
    user_id = request.user.groups.values('id')[0]['id']

    # generate data set in .txt
    data = open("./schedule/cases/scheduling_set.txt", "w", newline="", encoding="UTF-8")
    product_list = []   # 제품 리스트 (Queryset 담기)
    product_name_list = []  # 제품명 리스트
    column = []
    mn = 0
    # POST 로 받아온 값 dict 로 담기
    if request.method == 'POST':
        request = json.loads(request.body)
        ord_id = request['ord_id']
        ord = request['ord']    # 제품명
        fac = request['fac']    # 기계호기
        amt = request['amt']    # 오더 수량
        work_str = request['work_str_date']        # 작업시작일자
        work_exp_date = request['work_exp_date']   # 작업종료일자

    # 제품 정보 가져오기
    mn_list = []
    for i in range(len(fac)):
        for j in fac[i]:
            mn_list.append(j.replace('호기', ''))
    mn_set = set(mn_list)
    mn_list = list(mn_set)
    data.writelines('{0} {1} \n'.format(len(ord), int(max(mn_list).replace('호기', '').split('#')[1]) - 100))

    for i in range(len(ord)):
        print("schedule info :: ", ord[i], user_id)
        product = Product.objects.filter(prod_name=ord[i])[0]
        product_name = product.prod_name
        dpr = (product.rpm * 40 * 0.95) // product.density
        col_string = ''
        # 선택한 기계 정보 가져오기
        for j in range(len(fac[i])):
            demand = (int(amt[i]) // len(fac[i])) // dpr
            demand_rest = (int(amt[i]) // len(fac[i])) % dpr
            if len(col_string) > 1:
                col_string += ' '
            if demand_rest != 0.0:
                col_string += '{0} {1}'.format((int(fac[i][j].replace('호기', '').split('#')[1]) - 101), (int(demand+1)))
            else:
                col_string += '{0} {1}'.format((int(fac[i][j].replace('호기', '').split('#')[1]) - 101), int(demand))
        if i == len(ord)-1:
            data.writelines(col_string)
        else:
            data.writelines(col_string + '\n')

        product_list.append(Product.objects.filter(prod_name=ord[i])[0])
        product_name_list.append(product)

    data.close()

    result = GAStart()  # ss-lstm 실행

    #
    # # 회사명, 취급 섬유 유형 종류, 오더한 사람이 요청한 섬유 유형 종류
    count = Schedule.objects.filter()
    count = Schedule.objects.filter(created_at__year=now.year, created_at__month=now.month, created_at__day=now.day)
    count = count.aggregate(Max('count'))
    count = str(count['count__max'])

    if count == 'None':
        count = '0'

    keys_list = []  # 'color', 'order_id_num', 'machine_num', 'x1', 'y1'
    for i in result.keys():
        keys_list.append(i)

    s_list = []

    for i in range(len(result['color'])):
        line = []
        for keys in keys_list:
            line.append(result[keys][i])
        s_list.append(line)

    # sch_id  comp_id  facility_id  count  order_id_num  x_axis_1  y_axis_1  work_str_date   work_end_date
    for i in range(len(product_name_list)):
        for j in range(len(s_list)):
            if product_name_list[i] == product_name_list[int(s_list[j][2][:1]) - 1]:
                sch_id_cnt = len(Schedule.objects.all())
                str_date_in = work_str[i]
                exp_date = work_exp_date[i]
                y_axis = s_list[j][6]
                Schedule.objects.update_or_create(
                    sch_id='SCH' + s_list[j][0] + str(int(sch_id_cnt) + 1),
                    facility_id=Facility.objects.get(facility_name=y_axis),
                    comp_id=Information.objects.get(comp_id=user_id),
                    prod_id=product_name_list[i].prod_id,
                    order_id =OrderList.objects.get(order_id=ord_id[i]),
                    count=int(count) + 1,
                    sch_color=s_list[j][1],
                    order_id_num=s_list[j][2],  # 추후 오더 데이터에서 가져오기
                    x_axis_1=s_list[j][4],
                    x_axis_2=s_list[j][5],
                    y_axis_1=y_axis,
                    work_str_date=date_remove(str_date_in),
                    work_end_date=date_remove(exp_date)
                )

    return JsonResponse({"message": 'success'})


# 처리 가능 오더 리스트 표출
def available_comp(request):
    result = available_list(request)

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')
    # print(json.dumps(schedule_list, default=json_default))
    return HttpResponse(json.dumps(result, default=json_default))

# 처리 가능 오더 리스트 추출 (작업 완료 기한 기준)
def available_list(request):
    color_list = []
    final_list = []
    dict_list = []
    result = []
    now = datetime.datetime.now();
    # 당일 확정 스케쥴 존재 시
    if len(fixed_list(request, request.user.groups.values('id')[0]['id']))>0:
        for i in fixed_list(request, request.user.groups.values('id')[0]['id']):
            if i['use_yn'] == 'Y' and i['schedule'] is not None:
                for j in i['schedule']:
                    product_ids = j['prod_id']
                    product_id = Product.objects.get(prod_id=product_ids)
                    order_id = OrderList.objects.filter(prod_id=product_ids)
                    order_num = ''
                    comma_list = []
                    for k in order_id.values():
                        comma_list.append(k['order_id'])

                    prod_name = product_id.prod_name
                    j['prod_id'] = prod_name
                    j['order_id_num'] = comma_str(comma_list)
                    j['use_yn'] = i['use_yn']
                    result.append(j)
            else:
                sch_list = Schedule.objects.filter(comp_id=request.user.groups.values('id')[0]['id'],
                                                   created_at__year=now.year, created_at__month=now.month,
                                                   created_at__day=now.day)
                count = sch_list.aggregate(Max('count'))
                count = str(count['count__max'])
                available_list = Schedule.objects.raw(
                    ' SELECT * FROM company_schedule WHERE count=' + count +
                    ' AND STR_TO_DATE(created_at, "%%Y-%%m-%%d")= "' + now.strftime('%Y-%m-%d') + '"' +
                    ' AND comp_id=' + str(request.user.groups.values('id')[0]['id']) + ' AND x_axis_2 IN ' +
                    ' (SELECT MAX(x_axis_2) FROM company_schedule WHERE count=' + count +
                    ' AND STR_TO_DATE(created_at, "%%Y-%%m-%%d")= "' + now.strftime(
                        '%Y-%m-%d') + '" GROUP BY prod_id)' +
                    ' GROUP BY prod_id'
                )
                avail_list = []
                for i in available_list:
                    date_diff = calc_date_str(i.work_str_date, i.work_end_date)
                    if i.x_axis_2 < int(date_diff.days):
                        avail_list.append(i)

                color_list = []
                final_list = []
                dict_list = []
                result = []
                test_list = []
                for p in avail_list:
                    test_list.append(p)
                    color_list.append(p.sch_color)

                for tst in test_list:
                    test = Schedule.objects.get(sch_id=tst.sch_id)
                    color = Schedule.objects.filter(sch_id=tst.sch_id, comp_id=request.user.groups.values('id')[0]['id'])
                    color.group_by = ['sch_color']
                    final_list.append(color.aggregate(Max('sch_id')))

                for i in range(len(final_list)):
                    dict_list.append(final_list[i]['sch_id__max'])

                for i in dict_list:
                    schedule_list = Schedule.objects.filter(sch_id=i)
                    result.append(list(schedule_list.values()))

                for i in range(len(result)):
                    product_ids = result[i][0]['prod_id']
                    product_id = Product.objects.get(prod_id=product_ids)
                    order_id = OrderList.objects.filter(prod_id=product_ids)
                    comma_list = []
                    for j in order_id.values():
                        comma_list.append(j['order_id'])

                    prod_name = product_id.prod_name
                    result[i][0]['prod_id'] = prod_name
                    result[i][0]['order_id_num'] = comma_str(comma_list)
    else:
        # 당일 확정 스케쥴이 존재하지 않을 때
        sch_list = Schedule.objects.filter(comp_id=request.user.groups.values('id')[0]['id'],
                                        created_at__year=now.year, created_at__month=now.month, created_at__day=now.day)
        if len(sch_list) > 0:
            count = sch_list.aggregate(Max('count'))
            count = str(count['count__max'])
            available_list = Schedule.objects.raw(
                ' SELECT * FROM company_schedule WHERE count=' + count +
                ' AND STR_TO_DATE(created_at, "%%Y-%%m-%%d")= "' + now.strftime('%Y-%m-%d') + '"'+
                ' AND comp_id=' + str(request.user.groups.values('id')[0]['id']) + ' AND x_axis_2 IN ' +
                ' (SELECT MAX(x_axis_2) FROM company_schedule WHERE count=' + count +
                ' AND STR_TO_DATE(created_at, "%%Y-%%m-%%d")= "' + now.strftime('%Y-%m-%d') + '" GROUP BY prod_id)' +
                ' GROUP BY prod_id'
            )
            avail_list = []
            for i in available_list:
                date_diff = calc_date_str(i.work_str_date, i.work_end_date)
                if i.x_axis_2 < int(date_diff.days):
                    avail_list.append(i)

            for p in avail_list:
                color_list.append(p.sch_color)

            for i in color_list:
                # color = Schedule.objects.raw('SELECT * FROM company_schedule WHERE sch_color = "' +  i + '" GROUP BY sch_color HAVING MAX(sch_id)')
                color = Schedule.objects.filter(sch_color=i, comp_id=request.user.groups.values('id')[0]['id'])
                final_list.append(color.aggregate(Max('sch_id')))

            for i in range(len(final_list)):
                dict_list.append(final_list[i]['sch_id__max'])

            for i in dict_list:
                schedule_list = Schedule.objects.filter(sch_id=i)
                result.append(list(schedule_list.values()))

            for i in range(len(result)):
                print(result[i][0])
                product_ids=result[i][0]['prod_id']
                product_id=Product.objects.get(prod_id=product_ids)
                order_id=OrderList.objects.filter(prod_id=product_ids, order_id=result[i][0]['order_id_id'])
                comma_list = []
                for j in order_id.values():
                    comma_list.append(j['order_id'])

                prod_name=product_id.prod_name
                result[i][0]['prod_id'] = prod_name
                result[i][0]['order_id_num'] = comma_str(comma_list)

    return result

# 처리 확정 히스토리 표출
def schedule_history(request):
    result = fixed_list(request, request.user.groups.values('id')[0]['id'])

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    # print(json.dumps(schedule_list, default=json_default))
    return HttpResponse(json.dumps(result, default=json_default))

# 처리 확정 히스토리 리스트 추출
def fixed_list(request, user_group):

    if user_group is None:
        user_group = request.user.groups.values('id')[0]['id'];
    date = datetime.datetime.today().strftime("%Y%m%d")

    print('user_group : ', user_group)

    use_yn_list = OrderSchedule.objects.raw(
        ' SELECT * FROM order_orderschedule ' +
        ' WHERE SUBSTRING(sch_id, 4, 8) = ' + date +
        ' GROUP BY use_yn'
    )
    if len(use_yn_list)%2 == 1:
        available_list = OrderSchedule.objects.raw(
            ' SELECT * FROM order_orderschedule WHERE SUBSTRING(sch_id, 4, 8) = ' + date +
            ' GROUP BY sch_id ')
    else:
        available_list = OrderSchedule.objects.raw(
            ' SELECT * FROM order_orderschedule WHERE SUBSTRING(sch_id, 4, 8) = ' + date +
            ' AND use_yn = "Y" ' +
            ' GROUP BY sch_id ')
        
    result = []
    for p in available_list:
        avail_dict = {}
        avail_dict['use_yn'] = p.use_yn
        avail_dict['schedule'] = list(
            Schedule.objects.filter(comp_id=user_group, sch_id=p.sch_id.sch_id).values())

        if len(avail_dict['schedule']) == 0:
            continue;
        else:
            result.append(avail_dict)

    return result

# 처리 가능 오더 확정
def fixed_order(request):
    user_group = request.user.groups.values('id')[0]['id'];
    if request.method == 'POST':
        request = json.loads(request.body)

    if request['type'] == 'customer':
        comp_name = request['comp_name']    # 회사명
        order_id = request['order_id']  # 오더 아이디
        order_ids = OrderSchedule.objects.filter(order_id=order_id)

        for j in order_ids:
            OrderSchedule.objects.filter(sch_id=j.sch_id).update(use_yn='Y')
            OrderList.objects.filter(order_id=j.order_id_id).update(order_status=2)

    else:
        orders = request['order_list']
        prices = request['price_list']
        schedules = request['sch_list']

        if len(fixed_list(request, user_group)) > 0:
            result = fixed_list(request, user_group)
            for sch in result:
                OrderSchedule.objects.filter(sch_id=sch).update(use_yn='N')


        # 오더 아이디로 넘어옴
        for ord in range(len(orders)):
            ords = OrderSchedule.objects.filter(sch_id_id=schedules[ord])  # order_id 나중에 order_list 에서 조회해 오기
            if not ords: # 최초 수락일 때,
                # OrderSchedule.objects.filter(sch_id=ord).update(use_yn='Y')
                # OrderSchedule.objects.update_or_create(sch_id_id=orders.sch_id_id).update(use_yn='N', offer_price=prices[ord], order_status=0)
                OrderSchedule.objects.update_or_create(
                    order_id=OrderList.objects.get(order_id=orders[ord]),
                    sch_id=Schedule.objects.get(sch_id=schedules[ord]),
                    offer_price=prices[ord],
                    # use_yn='Y'
                    use_yn='N'
                )
                OrderList.objects.filter(order_id=orders[ord]).update(order_status=1)
                # OrderList.objects.filter(order_id=orders[ord]).update(order_status=1)
            else: # 최초 수락이 아닐 때,
                for ord in range(len(orders)):
                    order_ids = OrderList.objects.filter(sch_id=Schedule.objects.get(sch_id=schedules[ord])).update(use_yn='N',offer_price=prices[ord])


    return JsonResponse({"message": 'success'})

# 수락한 오더 리스트 조회
def confirmed_order(request):
    result = available_list(request)
    final_result = []
    confirmed_list = []
    use_yn_list = []

    for i in range(len(result)):
        try:
            sch_id = result[i]['sch_id']
            confirmed = OrderSchedule.objects.filter(sch_id=sch_id).filter(use_yn=result[i]['use_yn']).values()
            confirmed_list.append(confirmed)
            for j in confirmed:
                use_yn_list.append(j['use_yn'])
        except:
            sch_id = result[i][0]['sch_id']
            confirmed = OrderSchedule.objects.filter(sch_id=sch_id).values()
            if len(confirmed) == 0:
                confirmed_list.append(result[i])
            else:
                confirmed_list.append(confirmed)
            for j in confirmed:
                use_yn_list.append(j['use_yn'])

    use_yn_list = set(use_yn_list)
    use_yn_list = list(use_yn_list)

    if len(use_yn_list) > 1:
        for i in confirmed_list:
            if i[0]['use_yn'] == 'Y':
                final_result.append(list(i))
    else:
        for i in confirmed_list:
            final_result.append(list(i))

    def json_default(value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    # print(json.dumps(schedule_list, default=json_default))
    return HttpResponse(json.dumps(final_result, default=json_default))

# 스케줄 새로 생성시 삭제
def delete_order(request):
    # orders = request.POST.getlist('order_list[]')
    schs = request.POST.getlist('sch_list[]')
    # 오더 아이디로 넘어옴
    for sch in schs:
        OrderSchedule.objects.filter(sch_id=sch).update(use_yn = 'N')

        # OrderSchedule.objects.update_or_create(
            # use_yn='N',
        # )
        # OrderSchedule.objects.filter(order_id=ord.split('.')[0]).delete()  # order_id 나중에 order_list 에서 조회해 오기

    return JsonResponse({"message": 'success'})

def test_data(request):
    generate_data(request)

    # print(json.dumps(schedule_list, default=json_default))
    # return HttpResponse(json.dumps(list(final_result.values()), default=json_default))
    return JsonResponse({"message": 'success'})
