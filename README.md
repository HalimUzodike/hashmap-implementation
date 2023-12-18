# hashmap-implementation


## Introduction
A HashMap, also known as a Hash Table, is a data structure that stores key-value pairs. It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found. This approach allows for efficient data retrieval and storage, as it typically offers O(1) time complexity for search, insert, and delete operations.

## Files in this Repository

### 1. `hash_map_oa.py` - Open Addressing
This file contains the implementation of HashMap using the Open Addressing technique. In open addressing, all elements are stored in the hash table itself. When a new key is inserted, the hash table is searched from the slot given by the hash function until an empty slot is found. When searching for an element, the slots are scanned in the sequence until the element is found or it is clear that the element is not in the table.

Key Features:
- **Collision Resolution**: Handles collisions using the Quadratic Probing technique.

### 2. `hash_map_sc.py` - Separate Chaining
This file contains the implementation of HashMap using the Separate Chaining technique. Separate Chaining involves each slot of the hash table containing a link to a linked list containing key-value pairs. This way, the hash table never gets full, and we can always add more elements to the chain.

Key Features:
- **Linked List Structure**: Uses a Singly Linked List to store the key-value pairs.
- **Load Factor and Rehashing**: The load factor is the ratio between the number of elements stored in the hash table and the capacity. When the load factor exceeds a predefined threshold, the hash table is rehashed (doubled in size) and all the elements are reinserted.

## Usage

```python
# Example of using the HashMap with Open Addressing

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
    
# Example of using the HashMap with Separate Chaining

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
```
