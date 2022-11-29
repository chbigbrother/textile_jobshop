import copy
import random

# times: [[21, 53], [21, 71, 70], [42, 12], [77, 55], [83, 50]]
# machines: [[0, 1], [1, 0, 2], [0, 1], [1, 0], [0, 2]]
# config: range(n*mn)
# n: number of job
def calculateMakespan(times, machines, config, n, mn):
    time_table = []
    times = copy.deepcopy(times)
    machines = copy.deepcopy(machines)

    for i in range(mn):
        time_table.append([])
    # print(machines)
    current_times = [0]*n
    total_time = 0
    job_list = []
    job_list_final = []
    for j in config:
        job = j % n
        job_list.append(job)

    job_list = list(dict.fromkeys(job_list))
    for i in job_list:
        for j in range(0, mn):
            job_list_final.append(i)

    for k in job_list_final:
        job = k;
        try:
            current_machine = machines[job].pop(0)
            current_time = current_times[job]
            machine_usage = time_table[current_machine]  # [[0, 21, 0], [21, 98, 3], [98, 140, 2], [140, 211, 1]]
            usage_time = times[job].pop(0)
            current_time, total_time = fillTimeSlot(machine_usage, current_time, usage_time, job, total_time)

            current_times[job] = current_time
        except:
            continue;


    return total_time, time_table

# start, end, job number
# [[0, 83, 4], [83, 95, 2], [95, 116, 1], [116, 169, 0]] 140 55 3 211
def fillTimeSlot(machine_usage, current_time, usage_time, job, total_time):
    if len(machine_usage) > 0:
        prev = 0
        slot = None
        cnt = 1
        for used_slots in machine_usage:
            start = used_slots[0]
            end = used_slots[1]
            cnt += 1
            if start < current_time and current_time < end:
                current_time = current_time - start # end

            if prev == 0 and start > current_time + usage_time:
                slot = [current_time, usage_time + current_time, '{0}.{1}'.format(job, cnt)]
                break
            elif start - prev >= usage_time and current_time <= prev:
                slot = [current_time, usage_time + current_time, '{0}.{1}'.format(job, cnt)]
                break

            prev = end
            if end > current_time:
                current_time = end

        if slot == None:
            slot = [prev, prev + usage_time, '{0}.{1}'.format(job, cnt)]


        current_time = slot[1]
        machine_usage.append(slot)
        machine_usage.sort(key=lambda x: x[1])

        if slot[1] > total_time:
            total_time = slot[1]
    else:
        # 각 기계별 시작하는 time 0으로 맞추기
        machine_usage.append([0, usage_time, '{0}.{1}'.format(job, 1)])
        current_time = usage_time


    return current_time, total_time