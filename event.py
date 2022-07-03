import time
import threading as th
import random

def http_query():
    time.sleep(random.random() * 0.25)
    print('Got an http result!')


def save_to_file():
    time.sleep(random.random() * 0.25)
    print('Wrote result to file!')


class MLModel:

    def __init__(self, loading_time: int, loaded_event: th.Event, inference_lock: th.Lock) -> None:
        self.loading_time = loading_time
        self.loaded_event = loaded_event
        self.inference_lock = inference_lock


    def load_model(self):
        print(f'Started loading model... Will be busy for {self.loading_time}s')
        time.sleep(self.loading_time)
        self.loaded_event.set()
        print(f'Done loading model')

    def do_inference(self):
        self.inference_lock.acquire()
        print('Did inference... indide a critical section!')
        self.inference_lock.release()

model_lock = th.Lock()
event = th.Event()
model = MLModel(5, event, model_lock)

def http_worker_func():
    global model

    http_query()

    if not model.loaded_event.is_set():
        print('Waiting for the model to load...')
        model.loaded_event.wait()

    model.do_inference()

    save_to_file()


if __name__ == '__main__':

    loader_thread = th.Thread(target=model.load_model)
    workers = [th.Thread(target=http_worker_func) for i in range(5)]

    loader_thread.start()
    for w in workers:
        w.start()

    loader_thread.join()
    for w in workers:
        w.join()