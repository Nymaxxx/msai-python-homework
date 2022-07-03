import random
import multiprocessing as mp
import multiprocessing.synchronize as sync
import time

class MultiprocessingTable:

    def __init__(self, n_philosophers: int) -> None:
        self.n_philosophers = n_philosophers
        self.chopsticks = [mp.Lock() for _ in range(n_philosophers)]


    def left_chopstick(self, seat: int) -> sync.Lock:
        # I'll imagine that a seat is an int
        return self.chopsticks[seat]


    def right_chopstick(self, seat: int) -> sync.Lock:
        return self.chopsticks[(seat + 1) % self.n_philosophers]



class MultiprocessingPhilosopher(mp.Process):

    def __init__(self, table: MultiprocessingTable, seat: int, should_continue):
        super().__init__()
        self.table_ = table
        self.seat_ = seat
        self.left_chopstick_ = self.table_.left_chopstick(seat)
        self.right_chopstick_ = self.table_.right_chopstick(seat)
        self.meals_ = 0
        self.should_continue = should_continue


    def eat(self):
        self.__acquire_chopsticks()
        self.__eat_with_chopsticks()
        self.__release_chopsticks()


    def think(self):
        thought_time = random.random() * 0.25
        time.sleep(thought_time)  # think 0-0.25 seconds
        print(f'Philosopher {self.seat_} is thinking for {thought_time:4f}s')


    def run(self):
        while self.should_continue.get():
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
    print('The timer is set for 5 seconds... After that, processes are joined.')

    with mp.Manager() as mgr:
        shared_flag = mgr.Value('bool', True)

        mp_table = MultiprocessingTable(5)
        mp_phils = [MultiprocessingPhilosopher(mp_table, seat, shared_flag) for seat in range(mp_table.n_philosophers)]

        for phil in mp_phils:
            phil.start()

        time.sleep(5)
        shared_flag.set(False)
        for phil in mp_phils:
            phil.join()