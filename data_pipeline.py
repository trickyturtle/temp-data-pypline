import multiprocessing as mp
import sensor
import data_processor
import data_enricher
import time

NUM_ENTRIES=5000
NUM_THREADS=8

if __name__=='__main__':
    start = time.time()
    data_processor.createTable()
    queue = mp.JoinableQueue()
    for i in range(NUM_ENTRIES):
        data_enricher.enrichAndEnqueDataMessage(sensor.getTempData(), queue)
    for i in range(NUM_THREADS):
        worker_process = mp.Process(target=data_processor.insertDataFromQueue, args=(queue, ), daemon=True, name='worker_process_{}'.format(i))
        worker_process.start()
    queue.join()
    print( "Sending %s messages to the database took %s seconds" % (NUM_ENTRIES, (time.time() - start)))
