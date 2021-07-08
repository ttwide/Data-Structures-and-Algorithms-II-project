class EmptyBucket:
    pass


class HashTable:
    # time O(N)
    # space O(N)
    # initiate the hash table with 40 empty buckets
    def __init__(self, initial_capacity=40):

        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()

        self.table = [self.EMPTY_SINCE_START] * initial_capacity


    # time O(1) average 0(N) worst
    # space O(1)
    # determines which bucket to insert into, if bucket is occupied moves to the next bucket
    def insert(self, key, item):
        bucket = int(key) % len(self.table)
        #print("bucket on insert", bucket)
        buckets_probed = 0
        while buckets_probed < len(self.table):
            if type(self.table[bucket]) is EmptyBucket:
                self.table[bucket] = item
                return True

            bucket = (bucket + 1) % len(self.table)
            buckets_probed = buckets_probed + 1

        return False

    # time O(1) average 0(N) worst
    # space O(1)
    # determines which bucket to look into and removes item if present if not moves to the next bucket
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        buckets_probed = 0
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):
            if self.table[bucket] == key:
                self.table[bucket] = self.EMPTY_AFTER_REMOVAL

            bucket = (bucket + 1) % len(self.table)
            buckets_probed = buckets_probed + 1

    # time O(1) average 0(N) worst
    # space O(1)
    # searches the hash table and returns the correct package
    def search(self, key):
        bucket = int(key) % len(self.table)
        buckets_probed = 0
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):
            if self.table[bucket].id == key:
                return self.table[bucket]

            # the bucket was occupied (now or previously), so continue probing.
            bucket = (bucket + 1) % len(self.table)
            buckets_probed = buckets_probed + 1

        # the entire table was probed or an empty cell was found.
        return None

    # time O(N)
    # space O(1)
    # prints the id and timestamp of all the packages in the hash table
    def print_timestamps(self):
        for x in range(len(self.table)):
            print(self.table[x].id, self.table[x].timestamp)

    # time O(N)
    # space O(1)
    # prints the correct time of all packages in the hash table
    def print_time(self):
        for x in range(39):
            print(self.table[x+1].id, self.table[x+1].timestamp)
        print(self.table[0].id, self.table[0].timestamp)

    # time O(N)
    # space O(1)
    # updates the delivery status of all packages in the hash table
    def update_status(self, check_time):
        for x in range(len(self.table)):
            if check_time < self.table[x].start:
                self.table[x].location = "At hub"
            if self.table[x].start < check_time < self.table[x].timestamp:
                self.table[x].location = "In route"
            if check_time > self.table[x].timestamp:
                self.table[x].location = "Delivered"

    # time O(N)
    # space O(1)
    # prints time and location with a timestamp
    def print_status(self):
        for x in range(39):
            print(self.table[x+1].id, self.table[x+1].timestamp, self.table[x+1].location)
        print(self.table[0].id, self.table[0].timestamp, self.table[x+1].location)

    # time O(N)
    # space O(1)
    # prints time with and location with a the proper time i.e. 8:30 am
    def print_delivery_status(self):
        for x in range(39):
            print("Package ID: " + str(self.table[x+1].id), "   Address: " + str(self.table[x+1].address), "    City: " + str(self.table[x+1].city), "  Zip: " + str(self.table[x+1].zip), "    Mass: " +  str(self.table[x+1].mass), "     Delivered at: " + str(self.table[x+1].converted_timestamp), "   Status: " + str(self.table[x+1].location))
        print("Package ID: " + str(self.table[0].id), "   Address: " + str(self.table[0].address),
              "    City: " + str(self.table[0].city), "  Zip: " + str(self.table[0].zip),
              "    Mass: " + str(self.table[0].mass),
              "     Delivered at: " + str(self.table[0].converted_timestamp),
              "   Status: " + str(self.table[0].location))

    # time O(N)
    # space O(1)
    # converts all 60 minute timestamps in minutes to a regular time for viewing purposes
    def convert_time(self, check_time_in_minutes):
        for x in range(len(self.table)):
            if (check_time_in_minutes < self.table[x].timestamp):
                self.table[x].converted_timestamp = ""
            else:
                hour = int(self.table[x].timestamp / 60)
                min = int(self.table[x].timestamp % 60)
                if (hour == 0):
                    string_hour = '8'
                elif (hour == 1):
                    string_hour = '9'
                elif (hour == 2):
                    string_hour = '10'
                elif (hour == 3):
                    string_hour = '11'
                elif (hour == 4):
                    string_hour = '12'
                elif (hour == 5):
                    string_hour = '1'
                elif (hour == 6):
                    string_hour = '2'
                elif (hour == 7):
                    string_hour = '3'
                elif (hour == 8):
                    string_hour = '4'
                elif (hour == 9):
                    string_hour = '5'
                if (min < 10):
                    self.table[x].converted_timestamp = string_hour + ":0" +  str(min)
                else:
                    self.table[x].converted_timestamp = string_hour + ":" + str(min)

    # time O(N)
    # space O(1)
    # us to see if items in the hash table are empty since start or empty after removal
    def __str__(self):
        s = "   --------\n"
        index = 0
        for bucket in self.table:
            value = str(bucket)
            if bucket is self.EMPTY_SINCE_START:
                value = 'E/S'
            elif bucket is self.EMPTY_AFTER_REMOVAL:
                value = 'E/R'
            s += '{:2}:|{:^6}|\n'.format(index, value)
            index += 1
        s += "   --------"
        return s