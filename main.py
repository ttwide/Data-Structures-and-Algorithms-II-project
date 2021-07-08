#Terrence Wideman #001088428
from HashTable import HashTable
from Package import Package
import csv

# instantiates a hash table
h = HashTable()

# takes the data from the CSV file, creates a package file, and enters it into the hash table
with open('packages.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        if row[0].startswith('\ufeff'):
            id = 1
        else:
            id = row[0]
            id = int(id)
        address = row[1]
        city = row[2]
        state = row[3]
        zip = row[4]
        deadline = row[5]
        mass = row[6]
        specialNotes = row[7]
        h.insert(id, Package(id, address, city, state, zip, deadline, mass, specialNotes, 0, "at hub", 0, ''))

# puts distances and a list so they can be used in algorithm
distancesList = []
with open('distances.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    h2 = HashTable()

    for row in readCSV:
        distancesList.append(row)

# puts addresses in a list so they can be used in an algorithm=
with open('addresses.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    addressesList = []

    for row in readCSV:
        addressesList.append(row)


# time O(N)
# space O(1)
# returns the address index number when looking up an address by string
def address_lookup (location):
    for item in addressesList:
        if item[2] == location:
            if item[0].startswith('\ufeff'):
                index = 0
            else:
                index = int(item[0])
            return index


# packages loaded manually into 3 trucks
truck_1 = [15, 1, 13, 29, 30, 31, 34, 37, 40, 14, 19, 20, 16, 2, 4, 5]
truck_2 = [6, 25, 3, 39, 18, 28, 32, 36, 38, 7, 8, 10, 11, 12, 17, 21]
truck_3 = [22, 23, 24, 26, 27, 33, 35, 9]

# time O(N^2)
# space O(N)
# nearest neighbor algorithm with start time timestamps


def nearest_neighbor_with_st(truck, st):
    # initiating items to start nearest neighbor algorithm
    starting_address_index = address_lookup("4001 South 700 East")
    copy_truck_list = truck.copy()
    load_time = st
    time = st
    min = 10000
    count = 0
    shortestpid = ''
    total_distance = 0
    # iterate through the list and determine the shortest distance
    while len(truck) > 0 :
        for packId in truck:
            value = address_lookup(h.search(packId).address)
            distance = distancesList[value][starting_address_index]
            if distance == '':
                distance = distancesList[starting_address_index][value]
            if distance == 0 and packId == copy_truck_list[count]:
                continue
            else:
                if float(distance) < min:
                    min = float(distance)
                    shortestpid = packId
        # after determining the shortest distance add that distance to the total distance and remove the
        # package from the truck
        total_distance = total_distance + min
        time = time + (min/18 * 60)
        h.search(shortestpid).timestamp = time
        h.search(shortestpid).start = load_time
        truck.remove(shortestpid)
        count = count + 1
        starting_address_index = address_lookup(h.search(shortestpid).address)
        min = 10000
        shortestpid = ''
     # after unloading all the packages return to the hub by calculating the distance to the hub and adding it
    distanceToHub = distancesList[starting_address_index][0]
    total_distance = float(distanceToHub) + total_distance
    print("total distance is " + str(total_distance))
    return total_distance

# Truck 1 35.5 miles 8:00 to 9:59
# Truck 2 45.6 miles 9:05 to 11:37
# Truck 3 33.60 miles 10:20 to 12:12
# 114.7 total miles


distance_truck_1 = nearest_neighbor_with_st(truck_1, 0)
distance_truck_2 = nearest_neighbor_with_st(truck_2, 65)
distance_truck_3 = nearest_neighbor_with_st(truck_3, 140)
total_distance = distance_truck_1 + distance_truck_2 + distance_truck_3

h.print_timestamps()
h.print_time()

# this is the command line interface
# it takes the time inputted by the user and then outputs the delivery status of the packages

while (True):
    print("Enter a time or x to exit out of the program.")
    hour = input("Enter the time starting with the hour. (8am - 5pm): ")
    time_in_minutes = 0
    min = 0
    if (hour == "x"):
        break
    min = input("Enter the minutes 0 - 59: ")
    if (min == "x"):
        break
    if (hour == '8'):
        time_in_minutes = 0
    elif (hour == '9'):
        time_in_minutes = 60
    elif (hour == '10'):
        time_in_minutes = 120
    elif (hour == '11'):
        time_in_minutes = 180
    elif (hour == '12'):
        time_in_minutes = 240
    elif (hour == '1'):
        time_in_minutes = 300
    elif (hour == '2'):
        time_in_minutes = 360
    elif (hour == '3'):
        time_in_minutes = 420
    elif (hour == '4'):
        time_in_minutes = 480
    elif (hour == '5'):
        time_in_minutes = 540
    time_in_minutes = int(time_in_minutes) + int(min)
    #print(str(time_in_minutes))
    h.update_status(time_in_minutes)
    h.convert_time(time_in_minutes)
    h.print_delivery_status()
    print('estimated total distance traveled by end of route by all three trucks: %5.2f' % (total_distance))

