import numpy as np

def get_std_dev(data):
    return np.std(data, axis=0)

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines.pop(0) # removing the titles
        lines = [float(item.split(',')[1]) for item in lines]
        lines = np.array(lines)
    return lines

gps_data = load_data('Graph1.txt')
print(get_std_dev(gps_data))

accel_data = load_data('Graph2.txt')
print(get_std_dev(accel_data))