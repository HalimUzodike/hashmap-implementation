# Name: Chukwuhalim Uzodike
# OSU Email: uzodikec@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 HashMap Implementation
# Due Date: 03/17/2023
# Description: This program contains the implementation of a HashMap class that uses separate chaining for collision resolution.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map.
        If the given key already exists in the hash map, its associated value will be replaced with the new value
        If the given key does not exist in the hash map, a new key/value pair must be added
        """

        if self.table_load() >= 1:
            self.resize_table(self._next_prime(
                self._capacity * 2))  # resizes the current load factor if the load factor is greater than or equal to 1.

        bucket_index = self._hash_function(key) % self._capacity  # Calculate the hash index for the given key
        bucket = self._buckets[bucket_index]
        node = bucket.contains(key)

        if node:
            node.value = value  # If the key already exists, update the value

        if not node:  # If the key doesn't exist, add it to the hash table
            bucket.insert(key, value)
            self._size += 1

        return None

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """

        empty_buckets = 0

        for bucket_index in range(self._capacity):
            if self._buckets.get_at_index(
                    bucket_index).length() == 0:  # If the bucket is empty, increment the empty bucket counter
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """

        load_factor = self._size / self._capacity  # Calculate the hash table load factor. 𝝺=n/m where 𝝺 is the load factor, n is self._size and m is self._capacity

        return load_factor

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """

        self._size = 0

        for index in range(self._capacity):
            self._buckets[index] = LinkedList()  # Each bucket index has their linked list reset.

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.
        All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed.
        First check that new_capacity is not less than 1; if so, the method does nothing.
        If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next highest prime number.
        """

        if new_capacity >= 1:
            prime_checker_result = self._is_prime(new_capacity)

            if prime_checker_result is False:
                checked_capacity = self._next_prime(new_capacity)

            if prime_checker_result is True:
                checked_capacity = new_capacity       # The new capacity is checked to see if it is a prime number. If it isn't, the next prime number is found.

            store = DynamicArray()
            amount_of_buckets = self._buckets.length()
            bucket = self._buckets

            for element in range(amount_of_buckets):
                if bucket[element] is not None and bucket[element].length() != 0:
                    for node in bucket[element]:
                        store.append(node)
            self.clear()
            self._capacity = checked_capacity

            self._buckets = DynamicArray()          # The hash table is reset and the new capacity is set.
            for _ in range(self._capacity):
                self._buckets.append(LinkedList())

            number_of_values = store.length()
            for bucket_index in range(number_of_values):
                self.put(store[bucket_index].key, store[bucket_index].value)    # The values are rehashed and added to the new hash table.

        return None

    def get(self, key: str):
        """
        This method returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """

        bucket_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[bucket_index]
        node = bucket.contains(key)

        if node:
            return node.value       # If the key exists, return the value.

        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """

        bucket_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[bucket_index]
        node_position = bucket._head

        while node_position:
            if node_position.key == key:
                return True         # If the key exists, return True.

            node_position = node_position.next
        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """

        bucket_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[bucket_index]
        node = bucket.contains(key)

        if node:
            bucket.remove(key)
            self._size -= 1     # If the key exists, remove it from the hash table.

        return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        The order of the keys in the dynamic array does not matter.
        """

        new_array = DynamicArray()  # Create new array.

        bucket = self._buckets

        for pair in range(self._capacity):
            if bucket[pair] is not None and bucket[pair].length != 0:
                for node in bucket[pair]:
                    container = (node.key, node.value)
                    new_array.append(container)         # Add the key/value pairs to the new array.

        return new_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing, in this order, a dynamic array comprising the mode value/s of the array, and an integer that represents the highest frequency.
    If there is more than one value with the highest frequency, all values at that frequency should be included in the array being returned.
    If there is only one mode, the dynamic array will only contain that value.
    You may assume that the input array will contain at least one element, and that all values stored in the array will be strings.
    This function is implemented with O(N) time complexity.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length())
    new_array = DynamicArray()

    element_frequency = 1
    input_array_length = da.length()

    for element in range(input_array_length):

        required_key = da[element]
        key_checker = map.contains_key(required_key)

        if key_checker is True:
            count = map.get(required_key) + 1
            map.put(required_key, count)

            if map.get(required_key) >= element_frequency:
                element_frequency = map.get(required_key)

        if key_checker is False:
            count = 1
            map.put(required_key, count)        # The frequency of each element is counted and stored in the hash table.

    array_keys_and_values = map.get_keys_and_values()
    array_length = array_keys_and_values.length()

    for element in range(array_length):
        if array_keys_and_values[element][1] == element_frequency:
            new_array.append(array_keys_and_values[element][0])         # The elements with the highest frequency are added to the new array.

    return new_array, element_frequency

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
