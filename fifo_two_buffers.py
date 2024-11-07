import threading
import random
import time

# Set buffer size (max 1000)
buffer_size = min(int(input("Enter buffer size (max 1000): ")), 1000)

# Buffers
input_buffer = []
output_buffer = []

# Locks
input_mutex = threading.Lock()
output_mutex = threading.Lock()

# Semaphores
input_full = threading.Semaphore(0)         # Items in input buffer
input_empty = threading.Semaphore(buffer_size)  # Empty slots in input buffer
output_full = threading.Semaphore(0)        # Items in output buffer
output_empty = threading.Semaphore(buffer_size) # Empty slots in output buffer

# Producer: adds items to input buffer
def producer():
    while True:
        item = random.randint(1, 100)
        input_empty.acquire()
        with input_mutex:
            input_buffer.append(item)
            print(f"{item} inserting")
        input_full.release()
        time.sleep(1)

# Copier: moves items from input buffer to output buffer
def copier():
    while True:
        input_full.acquire()
        with input_mutex:
            item = input_buffer.pop(0)
        output_empty.acquire()
        with output_mutex:
            output_buffer.append(item)
        output_full.release()

# Consumer: removes items from output buffer
def consumer():
    while True:
        output_full.acquire()
        with output_mutex:
            item = output_buffer.pop(0)
            print(f"{item} consuming")
        output_empty.release()
        time.sleep(1)

# Create threads for Producers, Copiers, and Consumers
num_threads = buffer_size

producers = [threading.Thread(target=producer) for _ in range(num_threads)]
for p in producers:
    p.start()

copiers = [threading.Thread(target=copier) for _ in range(num_threads)]
for c in copiers:
    c.start()

consumers = [threading.Thread(target=consumer) for _ in range(num_threads)]
for c in consumers:
    c.start()

# Keep threads running
for p in producers + copiers + consumers:
    p.join()
