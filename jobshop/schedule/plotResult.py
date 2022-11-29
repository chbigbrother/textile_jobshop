import datetime
import numpy as np
import random


# {'sch_id': ['20220929', '20220929', '20220929', '20220929'], 'color': ['#8922f0', '#8922f0', '#e7eb1c', '#e7eb1c'],
#  'order_id_num': ['2.1', '2.2', '1.1', '1.2'],
#  'machine_num': ['Machine-1', 'Machine-2', 'Machine-3', 'Machine-5', 'Mach
#                  ine - 1', 'Machine - 2', 'Machine - 3', 'Machine - 5', 'Machine - 1', 'Machine - 2', 'Machine - 3
#                  ', 'Machine - 5', 'Machine - 1', 'Machine - 2', 'Machine - 3', 'Machine - 5'], 'x1
#                  ': [0, 0, 0, 0], 'x2': [20, 40, 16, 39], 'y1': ['1', '2', '3', '5']}
def plotResult(table, maxValue):
    df = []
    mn = 0
    colors = []
    color_dict = {}
    colorbox = []

    for i in range(100):
        colorArr = ['1', '2', '3', '4', '5', '6', '7',
                    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colorArr[random.randint(0, 14)]
        colorbox.append("#" + color)

    # Data setting for DB insert
    # variables : result, sch_id, order_id_num, machine_num, x1, x2, y1
    result = {}
    sch_id = []
    order_id_num = []
    machine_num = []
    x1 = []
    x2 = []
    y1 = []

    # table:
    # [[[0, 3, '1.1'], [3, 5, '0.2']], [], [[0, 2, '0.1']], [], [[0, 3, '1.1']]]

    for row in table:
        mn += 1
        color_mn = 0
        job_cnt = 0
        for slot in row:
            color_mn += 1
            job_cnt += 1
            sch_id.append(datetime.datetime.today().strftime("%Y%m%d"))
            order_id_num.append('{0}.{1}'.format(int(slot[2].split(".")[0]) + 1, slot[2].split(".")[1]))
            machine_num.append('Machine - {0}'.format(mn))
            x1.append(slot[0])
            x2.append(slot[1])
            y1.append(mn)
            start_time=str(datetime.timedelta(seconds=slot[0]))
            end_time=str(datetime.timedelta(seconds=slot[1]))
            today = datetime.date.today()
            entry = dict(
                Task='Machine-{0}'.format(mn), 
                Start="{0} {1}".format(today, start_time), 
                Finish="{0} {1}".format(today, end_time),
                duration=slot[1] - slot[0],
                Resource='Job {0}'.format(int(slot[2].split(".")[0]) + 1)
                )
            df.append(entry)

            color_dict[' {0}'.format(slot[2])] = colorbox[color_mn];
            colors.append(colorbox[int(slot[2].split(".")[0])])
    #In order to see the line ordered by integers and not by dates we need to generate the dateticks manually
    #we create 11 linespaced numbers between 0 and the maximum value
    num_tick_labels = np.linspace(start = 0, stop = maxValue, num = 11, dtype = int)
    date_ticks = ["{0} {1}".format(today, str(datetime.timedelta(seconds=int(x)))) for x in num_tick_labels]
    result['sch_id'] = sch_id
    result['color'] = colors
    result['order_id_num'] = order_id_num
    result['machine_num'] = machine_num
    result['x1'] = x1
    result['x2'] = x2
    result['y1'] = y1

    return result
