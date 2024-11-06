from threading import Thread,Condition
import time,logging

logging.basicConfig(level=logging.INFO)

#making countdown latch class for implementing countdownlatch in python
class CountDownLatch:

    # constructor for mainly initialising the count and creating a condition object
    def __init__(self, count):
        self.count = count
        # control access to the count and notify when latch is open
        self.condition = Condition()


    # count down the latch by one decrement
    def count_down(self):
        # acquire the lock on the condition
        with self.condition:
            # check if the latch is already open
            if self.count == 0:
                logging.info("first return")
                return
            # decrement the counter
            self.count -= 1
            # check if the latch is now open
            if self.count == 0:
                # notify all waiting threads that the latch is open
                self.condition.notify_all()


    # wait for the latch to open
    def wait(self):
        # acquire the lock on the condition
        with self.condition:
            # check if the latch is already open
            if self.count == 0:
                return
            # wait to be notified when the latch is open
            self.condition.wait()


#simple function for printing the numbers
def print_number(number):
    time.sleep(1)
    logging.info(number)


# create the countdown latch
latch = CountDownLatch(11)
start=time.time()

for i in range(11):
    thread = Thread(target=print_number, args=(i,))
    thread.start()
    logging.info(f"Started thread: {thread.name}")
    #print thread name
    thread.join()
    latch.count_down()

end=time.time()
logging.info(end-start)
# wait for the latch to close
latch.wait()




