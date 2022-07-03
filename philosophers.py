import random
import threading as th
import time

should_continue = True

class ThreadingTable:

    def __init__(self, n_philosophers: int) -> None:
        self.n_philosophers = n_philosophers
        self.chopsticks = [th.Lock() for _ in range(n_philosophers)]


    def left_chopstick(self, seat: int) -> th.Lock:
        # I'll imagine that a seat is an int
        return self.chopsticks[seat]


    def right_chopstick(self, seat: int) -> th.Lock:
        return self.chopsticks[(seat + 1) % self.n_philosophers]



class ThreadingPhilosopher(th.Thread):

    def __init__(self, table: ThreadingTable, seat: int):
        super().__init__()
        self.table_ = table
        self.seat_ = seat
        self.left_chopstick_ = self.table_.left_chopstick(seat)
        self.right_chopstick_ = self.table_.right_chopstick(seat)
        self.meals_ = 0


    def eat(self):
        self.__acquire_chopsticks()
        self.__eat_with_chopsticks()
        self.__release_chopsticks()


    def think(self):
        thought_time = random.random() * 0.25
        time.sleep(thought_time)  # think 0-0.25 seconds
        print(f'Philosopher {self.seat_} is thinking for {thought_time:4f}s')


    def run(self):
        global should_continue
        while should_continue:
            self.eat()
            self.think()


    def __acquire_chopsticks(self):
        '''
        Acquire left_chopstick_ and right_chopstick_
        '''
        # Must always try to contest first
        # It's deadlock prevention, baby
        if self.seat_ % 2 == 0:
            self.left_chopstick_.acquire()
            self.right_chopstick_.acquire()
        else:
            self.right_chopstick_.acquire()
            self.left_chopstick_.acquire()

    def __eat_with_chopsticks(self):
        time.sleep(random.random() * 5) # eat 0-5 seconds
        print(f'Philosopher {self.seat_} has eaten a meal!')
        self.meals_ += 1


    def __release_chopsticks(self):
        '''
        Release left_chopstick_ and right_chopstick_
        '''
        # Release order does not matter
        self.left_chopstick_.release()
        self.right_chopstick_.release()


if __name__ == '__main__':
    print('Starting the `threading` module based philosopher problem run...')
    print('The timer is set for 5 seconds... After that, threads are joined')

    def turn_race_off():
        global should_continue
        should_continue = False

    th_timer = th.Timer(5, turn_race_off)
    th_table = ThreadingTable(5)
    th_phils = [ThreadingPhilosopher(th_table, seat) for seat in range(th_table.n_philosophers)]

    for phil in th_phils:
        phil.start()

    th_timer.start()
    th_timer.join()

    for phil in th_phils:
        phil.join()