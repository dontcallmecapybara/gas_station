'''
Case: Gas Station
Group:
Gagol Egor = 90
Tarlo Evgeny = 90
'''

import random
import ru_local as ru


def mins_to_time(minutes):
    '''Turning amount of minutes to time with hours and minutes
    
    args:
    
    minutes -- number of minutes
    '''
    time = ''
    hours = minutes // 60
    mins = minutes % 60

    if hours < 10:
        time += '0'
        time += str(hours)
    else:
        time += str(hours)

    time += ':'

    if mins < 10:
        time += '0'
        time += str(mins)
    else:
        time += str(mins)

    return time


def opt_machine_limits(gas_brand, gas_vol, mach_brands, mach_que, mach_lim, lost_custom):
    '''Determines suitable gas stations by the maximum queue and type of fuel;
    returns list with numbers of suitable stations

    Args:

    gas_brand -- petrol brand the customer needs
    mach_brand -- list with brands of each station
    mach_que -- current queue for stations
    mach_lim -- maximum queue for stations

    '''
    opt_mach = []
    for mach, brand in mach_brands.items():
        if gas_brand in brand:
            if mach_que[int(mach)] < mach_lim[mach]:
                mach_que[int(mach)] += 1
                opt_mach.append(mach)
                return opt_mach
            else:
                lost_custom[brand[0]] += int(gas_vol)
                return opt_mach


def opt_machine_queue(opt_lim, mac_que, customer):
    '''Determines the optimal station by the smallest queue and adds
    the client to the desired one

    Args:

    opt_lim -- list with suitable stations
    mac_que -- dictionary with current queue
    customer -- info about client to add it to the queue

    '''
    if len(opt_lim) == 1:
        new_customer = ''
        for itr in customer:
            new_customer += itr
            new_customer += ' '
        mac_que[int(opt_lim[0])][1].append(new_customer)
    else:
        min_mac = None
        min_que = None
        for item in opt_lim:
            for k, v in mac_que.items():
                if int(item) == k:
                    if min_que == None:
                        min_que = len(v[1])
                        min_mac = k
                    else:
                        if min_que > len(v[1]):
                            min_que = len(v[1])
                            min_mac = k
        new_customer = ''
        for itr in customer:
            new_customer += itr
            new_customer += ' '
        mac_que[min_mac][1].append(new_customer)


# Input data about machines
with open('machine_input.txt', 'r', encoding='utf-8') as f:
    input_machine_data = f.read().splitlines()

available_brands = [ru.ai80, ru.ai92, ru.ai95, ru.ai98]
gasoline_price = {ru.ai80: 25, ru.ai92: 49, ru.ai95: 53, ru.ai98: 68}
gasoline_volume = {ru.ai80: 0, ru.ai92: 0, ru.ai95: 0, ru.ai98: 0}
lost_volume = {ru.ai80: 0, ru.ai92: 0, ru.ai95: 0, ru.ai98: 0}
lost_clients = 0

# Creating dictionary with machines limits and brands
machine_limits = {}
machine_brands = {}
machine_brands_str = {}
for machine in input_machine_data:
    data = machine.split()
    machine_limits[data[0]] = int(data[1])
    machine_brands[data[0]] = []
    machine_brands_str[data[0]] = ''

    for brand in range(2, len(data)):
        machine_brands[data[0]].append(data[brand])
        machine_brands_str[data[0]] += data[brand]
        machine_brands_str[data[0]] += ' '

# Getting number of machines
machine_number = len(machine_brands)

# Creating dictionary with machinces queue
machine_queue = {}
for item in range(1, machine_number + 1):
    temp_data = {item: 0}
    machine_queue.update(temp_data)

# Input data about new clients
with open('input.txt', 'r', encoding='utf-8') as f:
    input_clients_data = f.read().splitlines()

dict_of_mach = {}
for itr in range(1, machine_number + 1):
    dict_of_mach[itr] = [[], [], []]

# Output info about new client
for minutes in range(1, 1441):
    for client in input_clients_data:
        client = client.split()
        time = client[0]
        volume = client[1]
        brand = client[2]

        # Checking for gasoline brand and time
        if brand in available_brands and time == mins_to_time(minutes):
            optimal_machine = opt_machine_limits(brand, volume,
                                                 machine_brands, machine_queue, machine_limits, lost_volume)
            if len(optimal_machine) != 0:
                opt_machine_queue(optimal_machine, dict_of_mach, client)
                gasoline_volume[brand] += int(volume)
            else:
                lost_clients += 1

            for itr in range(1, len(dict_of_mach) + 1):
                if len(dict_of_mach[itr][1]) > 0:
                    data_queue = dict_of_mach[itr][1][-1].split()
                    if str(mins_to_time(minutes)) == data_queue[0]:
                        print('\U000026FD', ru.at_ru, mins_to_time(minutes), ru.new_client_ru, dict_of_mach[itr][1][-1],
                              ru.in_queue_ru, itr, sep='')
                        print(ru.gasoline_1, machine_limits['1'], ru.petrol_brand,
                              machine_brands['1'][0], ' ->', (len(dict_of_mach[1][1]) + len(dict_of_mach[1][0])) * '*',
                              sep='')
                        print(ru.gasoline_2, machine_limits['2'], ru.petrol_brand,
                              machine_brands['2'][0], ' ->', (len(dict_of_mach[2][1]) + len(dict_of_mach[2][0])) * '*',
                              sep='')
                        print(ru.gasoline_3, machine_limits['3'], ru.petrol_brand,
                              machine_brands_str['3'], '->', (len(dict_of_mach[3][1]) + len(dict_of_mach[3][0])) * '*',
                              sep='')

        # Clients that finished
        for itr in range(1, len(dict_of_mach) + 1):
            if len(dict_of_mach[itr][0]) > 0:
                data_dict_of_mach = dict_of_mach[itr][0][0].split()
                if str(mins_to_time(minutes)) == data_dict_of_mach[0]:
                    finished_client = dict_of_mach[itr][2][0]
                    dict_of_mach[itr][0].pop(0)
                    dict_of_mach[itr][2].pop(0)
                    print('\U0001F697', ru.at_ru, mins_to_time(minutes), ru.client_ru, finished_client,
                          ru.finished_client, sep='')
                    print(ru.gasoline_1, machine_limits['1'], ru.petrol_brand,
                          machine_brands['1'][0], ' ->', (len(dict_of_mach[1][1]) + len(dict_of_mach[1][0])) * '*',
                          sep='')
                    print(ru.gasoline_2, machine_limits['2'], ru.petrol_brand,
                          machine_brands['2'][0], ' ->', (len(dict_of_mach[2][1]) + len(dict_of_mach[2][0])) * '*',
                          sep='')
                    print(ru.gasoline_3, machine_limits['3'], ru.petrol_brand,
                          machine_brands_str['3'], '->', (len(dict_of_mach[3][1]) + len(dict_of_mach[3][0])) * '*',
                          sep='')

            if len(dict_of_mach[itr][0]) == 0 and len(dict_of_mach[itr][1]) > 0:
                dict_of_mach[itr][0].append(dict_of_mach[itr][1][0])
                dict_of_mach[itr][2].append(dict_of_mach[itr][1][0])
                dict_of_mach[itr][1].pop(0)
                machine_queue[itr] -= 1

                # Counting time for fueling
                for itr1 in dict_of_mach[itr][0][0].split():
                    if len(itr1) < 4:
                        num_litres = int(itr1)
                        if num_litres <= 10:
                            new_minutes = minutes + 1 + random.randint(0, 1)
                        else:
                            if num_litres % 10 == 0:
                                new_minutes = minutes + num_litres // 10 + random.randint(-1, 1)
                            if num_litres % 10 != 0:
                                new_minutes = minutes + num_litres // 10 + 1 + random.randint(-1, 1)

                new_minutes = mins_to_time(new_minutes)

                data_dict_of_mach = dict_of_mach[itr][0][0].split()
                dict_of_mach[itr][0][0] = new_minutes + ' ' + data_dict_of_mach[1] + ' ' + data_dict_of_mach[2]

# Calculation of lost volumes per day
for pr_brand in gasoline_price:
    for vol_brand in lost_volume:
        if pr_brand == vol_brand:
            lost_volume[vol_brand] *= gasoline_price[pr_brand]

# Calculation of lost profits based on brand of gasoline per day
pet_vol_price = gasoline_volume.copy()
for pr_pet in gasoline_price:
    for vol_pet in gasoline_volume:
        if pr_pet == vol_pet:
            pet_vol_price[vol_pet] *= gasoline_price[pr_pet]

# Calculation of total revenue per day
total_revenue = 0
for item in pet_vol_price:
    total_revenue += pet_vol_price[item]

# Calculation of total lost income per day
total_losts = 0
for item in lost_volume:
    total_losts += lost_volume[item]

# Output info: how many liters of which brand is required
print('\n\n', ru.need_gasoline_volume, sep='')
for br, vol in gasoline_volume.items():
    print(f'{br}: {vol}', ru.liters)

# Output info: total revenue
print('\n', ru.total_revenue_day, total_revenue, ru.rubles, sep='')

# Output info: total lost income
print(f'\n', ru.total_revenue_lost_day, total_losts, ru.rubles, sep='')

# Output info: total lost clients
print(f'\n', ru.total_lost_clients, lost_clients, ru.person, '\n', sep='')
