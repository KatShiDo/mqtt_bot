import json
import matplotlib.pyplot as plt
import tempfile


def divide_values_into_groups(array):
    groups = [0, 0, 0, 0]
    minimal = min(array)
    maximal = max(array)
    step = (maximal - minimal) / 4
    # print(minimal, maximal, step, step*2, step*3, step*4)
    for i in range(len(array)):
        if array[i] < minimal + step:
            groups[0] += 1
        elif array[i] < minimal + 2 * step:
            groups[1] += 1
        elif array[i] < minimal + 3 * step:
            groups[2] += 1
        else:
            groups[3] += 1
    return groups


def temperature_charts(json_path):
    with open(json_path) as f:
        data = json.load(f)

    temperature_data = [d['temperature'] for d in data]

    plt.bar(range(len(temperature_data)), temperature_data, width=0.5)
    plt.title('Temperature Bar Chart')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    # Если не задать axis, то будет слишком мелкий масштаб и не видна разница
    # plt.axis([0, len(temperature_data), sum(temperature_data) / len(temperature_data) - 0.15,
    #           sum(temperature_data) / len(temperature_data) + 0.15])
    plt.savefig('charts/temperature_bar.png')
    plt.close()

    plt.plot(range(len(temperature_data)), temperature_data)
    plt.title('Temperature Line Chart')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.savefig('charts/temperature_line.png')
    plt.close()


def co2_charts(json_path):
    with open(json_path) as f:
        data = json.load(f)

    co2_data = [d['CO2'] for d in data]

    plt.bar(range(len(co2_data)), co2_data, width=0.5)
    plt.title('CO2 Bar Chart')
    plt.xlabel('Time')
    plt.ylabel('CO2')
    # plt.axis([0, len(co2_data), sum(co2_data) / len(co2_data) - 25,
    #           sum(co2_data) / len(co2_data) + 25])
    plt.savefig('charts/co2_bar.png')
    plt.close()

    plt.plot(range(len(co2_data)), co2_data)
    plt.title('CO2 Line Chart')
    plt.xlabel('Time')
    plt.ylabel('CO2')
    plt.savefig('charts/co2_line.png')
    plt.close()

    mini = min(co2_data)
    maxi = max(co2_data)
    plt.pie(divide_values_into_groups(co2_data), labels=[
        f'{mini}-{mini + ((maxi - mini) / 4 )}',
        f'{mini + ((maxi - mini) / 4 )}-{mini + 2*((maxi - mini) / 4)}',
        f'{mini + 2*((maxi - mini) / 4)}-{mini + 2*((maxi - mini) / 4)}',
        f'{mini + 3*((maxi - mini) / 4)}-{mini + 4*((maxi - mini) / 4)}'
    ])
    plt.title('CO2 Pie Chart')
    plt.savefig('charts/co2_pie.png')
    plt.close()
