import numpy as np
places = ['1', '13', '4132']
places = np.concatenate((places, np.zeros(3)))


with open('listfile.txt', 'w') as filehandle:
    for listitem in places:
        filehandle.write('{}\n'.format(listitem))

with open('listfile.txt') as f:
    place1 = []
    for line in f:
        for x in line.split():
            place1.append(float(x))
#s        place1.append(int(x) for x in line.split())
#
print(place1)
print('')
