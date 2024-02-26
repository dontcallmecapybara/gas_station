def customer_distribution(brand, )


    print(opt_mach)
    print(mach)
    print(item)
    # print(f'В {time} новый клиент: {time} {brand} {volume}', end=' ')
    # print(f'{refueling} встал в очередь к автомату {opt_mach}\n')

    # for machine in range(1, mach_num + 1):
    #     print(f'Автомат №{machine} максимальная очередь: {mach_lim[str(machine)]}', end=' ')
    #     print('Марки бензина: ', end='')

    #     for item in range(len(mach_brands[str(machine)])):
    #         print(mach_brands[str(machine)][item], end=' ')
    #     print('->' + '*' * mach_queue[machine] + '\n')
    
    # return lst_clnts


# Input data about machines
with open('machine_input.txt', 'r') as f:
    input_machine_data = f.read().splitlines()

available_brands = ['АИ-80', 'АИ-92', 'АИ-95', 'АИ-98']
gasoline_price = {'АИ-80': 10, 'АИ-92': 20, 'АИ-95': 30, 'АИ-98': 40}
gasoline_volume = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}

# Creating dictionary with machines limits and brands
machine_limits = {}
machine_brands = {}
for machine in input_machine_data:
    data = machine.split()
    machine_limits[data[0]] = int(data[1])
    machine_brands[data[0]] = []

    for brand in range(2, len(data)):
        machine_brands[data[0]].append(data[brand])

# Getting number of machines
machine_number = len(machine_brands)

# Creating dictionary with machinces queue
machine_queue = {}
for item in range(1, machine_number + 1):
    temp_data = {item: 0}
    machine_queue.update(temp_data)

# Input data about new clients
with open('input_test.txt', 'r') as f:
    input_clients_data = f.read().splitlines()

# Output info about new client
for client in input_clients_data:
    client = client.split()
    time = client[0]
    volume = client[1]
    brand = client[2]

    if brand in available_brands:
        lost_clients = new_client(time, volume, brand, volume, machine_number, machine_queue, machine_limits, machine_brands)
        gasoline_volume[brand] += int(volume)

# Result of model: how many liters of which brand is required
# print('Бензина требуется на заправке:')
# for br, vol in gasoline_volume.items():
#     print(f'{br}: {vol} л')

# print(f'Количество уехавших клиентов: {lost_clients}')
print(machine_queue)