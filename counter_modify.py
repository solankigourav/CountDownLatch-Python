import time
from threading import Thread, Condition
import logging,threading
# import time

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

def fc_hacked():
    logging.info("its just a prank")

def print_number(latch, number):
    thread_name = threading.current_thread().name
    logging.info(f"Thread {thread_name}: {number}")
    latch.count_down()


# Create the countdown latch
latch = CountDownLatch(10)

# Create and start threads, passing the latch
threads = []
counter = 0

for i in range(10):
    thread = Thread(target=print_number, args=(latch, i,))
    threads.append(thread)
    thread.start()
    logging.info(f"Started thread: {thread.name}")

    # Check and sleep after every 5 threads finish
    counter += 1
    if counter % 5 == 0:
        #We can perform any operations or any functions call here,  so I am executing just a simple function
        logging.info(f"Pausing execution for 5 seconds after {counter} threads.")
        fc_hacked()


# Wait for all threads to finish before proceeding
for thread in threads:
    thread.join()
    logging.info(f"Finished thread: {thread.name}")

# Now, wait on the latch to ensure all threads have finished printing
latch.wait()
logging.info("All threads finished, program is stopping.")