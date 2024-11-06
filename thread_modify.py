from threading import Thread, Condition
import time, logging, threading

logging.basicConfig(level=logging.INFO)

class CountDownLatch:

    def __init__(self, count):
        self.count = count
        self.condition = Condition()

    def count_down(self):
        with self.condition:
            # logging.info(self.count)
            if self.count == 0:
                logging.info("first return")
                return
            self.count -= 1
            if self.count == 0:
                self.condition.notify_all()

    def wait(self):

        with self.condition:
            if self.count == 0:
                return
            self.condition.wait()


# Create the countdown latch
latch = CountDownLatch(10)
counter = 1

def print_number(latch, number):
    thread_name = threading.current_thread().name
    logging.info(f"Printing Thread {thread_name}: {number}")
    latch.count_down()

# Using a separate thread to monitor and pause execution
def to_check():
    while True:
        # Check if 5 threads have finished using counter
        if counter % 5 == 0:
            logging.info("Pausing execution for 5 seconds.")
            time.sleep(1)

        # Check if all threads have finished
        if latch.count == 0:
            logging.info("breaking the loop through countdown latch")
            break

# Start the monitoring thread
monitor_thread = Thread(target=to_check)
monitor_thread.start()

# Create and start threads, passing the latch
threads = []
for i in range(10):
    thread = Thread(target=print_number, args=(latch, i))
    threads.append(thread)
    thread.start()
    logging.info(f"Started thread: {thread.name}")
    counter += 1


# Wait for all threads to finish before proceeding
for thread in threads:
    thread.join()
    logging.info(f"Finished thread: {thread.name}")

# Now, wait on the latch to ensure all threads have finished printing
latch.wait()
logging.info("All threads finished, program is stopping.")