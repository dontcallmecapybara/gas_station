import random


def mins_to_time(minutes):
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


def opt_machine_limits(gas_brand, mach_brands, mach_que, mach_lim):

    opt_mach = []
    for mach, brand in mach_brands.items():
        if gas_brand in brand:
            if mach_que[int(mach)] < mach_lim[mach]:
                opt_mach.append(mach)
            else:
                None
    return opt_mach


def opt_machine_limits(gas_brand, gas_vol, mach_brands, mach_que, mach_lim, lost_custom):

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

        



    # print(f'В {time} новый клиент: {time} {brand} {volume}', end=' ')
    # print(f'{refueling} встал в очередь к автомату {opt_mach}\n')

    # for machine in range(1, mach_num + 1):
    #     print(f'Автомат №{machine} максимальная очередь: {mach_lim[str(machine)]}', end=' ')
    #     print('Марки бензина: ', end='')

    #     for item in range(len(mach_brands[str(machine)])):
    #         print(mach_brands[str(machine)][item], end=' ')
    #     print('->' + '*' * mach_queue[machine] + '\n')


# Input data about machines
with open('machine_input.txt', 'r', encoding='utf-8') as f:
    input_machine_data = f.read().splitlines()

available_brands = ['АИ-80', 'АИ-92', 'АИ-95', 'АИ-98']
gasoline_price = {'АИ-80': 10, 'АИ-92': 20, 'АИ-95': 30, 'АИ-98': 40}
gasoline_volume = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}
lost_volume = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}
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
with open('input_test.txt', 'r', encoding='utf-8') as f:
    input_clients_data = f.read().splitlines()
    
dict_of_mach = {}
for itr in range(1, machine_number+1):
    dict_of_mach[itr] = [[], []]

# Output info about new client
for minutes in range(1,1441):
    for client in input_clients_data:
        client = client.split()
        time = client[0]
        volume = client[1]
        brand = client[2]

        if brand in available_brands and time == mins_to_time(minutes):
            optimal_machine = opt_machine_limits(brand, volume, machine_brands, machine_queue, machine_limits,
                                                 lost_volume)
            if len(optimal_machine) != 0:
                opt_machine_queue(optimal_machine, dict_of_mach, client)
                gasoline_volume[brand] += int(volume)
            else:
                lost_clients += 1
            print(dict_of_mach)

            for itr in range(1, len(dict_of_mach) + 1):
                if len(dict_of_mach[itr][1]) > 0:
                    data_queue = dict_of_mach[itr][1][-1].split()
                    if str(mins_to_time(minutes)) == data_queue[0]:
                        print('В ', mins_to_time(minutes),' новый клиент: ', dict_of_mach[itr][1][-1], 'встал в очередь к автомату №', itr, sep='')
                        print('Автомат №1 максимальная очередь: ', machine_limits['1'], ' Марки бензина: ', machine_brands['1'][0], ' ->', (len(dict_of_mach[1][1]) + len(dict_of_mach[1][0])) * '*', sep='')
                        print('Автомат №2 максимальная очередь: ', machine_limits['2'], ' Марки бензина: ', machine_brands['2'][0], ' ->', (len(dict_of_mach[2][1]) + len(dict_of_mach[2][0])) * '*', sep='')
                        print('Автомат №3 максимальная очередь: ', machine_limits['3'], ' Марки бензина: ', machine_brands_str['3'], '->', (len(dict_of_mach[3][1]) + len(dict_of_mach[3][0])) * '*', sep='')
                        print(dict_of_mach)
        for itr in range(1, len(dict_of_mach) + 1):
            if len(dict_of_mach[itr][0]) > 0:
                data_dict_of_mach = dict_of_mach[itr][0][0].split()
                if str(mins_to_time(minutes)) == data_dict_of_mach[0]:
                    finished_client = dict_of_mach[itr][0][0]
                    dict_of_mach[itr][0].pop(0)
                    print('В ', mins_to_time(minutes), ' клиент: ', finished_client, ' заправил свой автомобиль и покинул АЗС', sep='')
                    print('Автомат №1 максимальная очередь: ', machine_limits['1'], ' Марки бензина: ', machine_brands['1'][0], ' ->', (len(dict_of_mach[1][1]) + len(dict_of_mach[1][0])) * '*', sep='')
                    print('Автомат №2 максимальная очередь: ', machine_limits['2'], ' Марки бензина: ', machine_brands['2'][0], ' ->', (len(dict_of_mach[2][1]) + len(dict_of_mach[2][0])) * '*', sep='')
                    print('Автомат №3 максимальная очередь: ', machine_limits['3'], ' Марки бензина: ', machine_brands_str['3'], '->', (len(dict_of_mach[3][1]) + len(dict_of_mach[3][0])) * '*', sep='')
                    print(dict_of_mach)

            if len(dict_of_mach[itr][0]) == 0 and len(dict_of_mach[itr][1]) > 0:
                dict_of_mach[itr][0].append(dict_of_mach[itr][1][0])
                dict_of_mach[itr][1].pop(0)
                machine_queue[itr] -= 1

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
                print(dict_of_mach)

# Calculation lost volumes per day
for pr_brand in gasoline_price:
    for vol_brand in lost_volume:
        if pr_brand == vol_brand:
            lost_volume[vol_brand] *= gasoline_price[pr_brand]

# Calculation lost profits based on brand of gasoline per day
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
print('\n', '_' * 25)
print('\nБензина требуется на заправке:')
for br, vol in gasoline_volume.items():
    print(f'{br}: {vol} л')

# Output info: total revenue
print(f'\nОбщая сумма продаж за сутки: {total_revenue}')

# Output info: total lost income
print(f'\nОбщий потеряный доход: {total_losts}')

# Output info: total lost clients
print(f'\nКоличество потеряных клиентов: {lost_clients}\n')
