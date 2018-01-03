# Copyright (c) 2012-2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import logging
import sys
from Queue import *
import threading
import traceback
from fei.tem.omp.api import IInstrumentControl
import fei.tem.omp.api as omp
logger = logging.getLogger(__name__)


class OmpBackGroundWorker(object):
    def __init__(self):
        logger.info("OmpBackGroundWorker constructor")
        self._worker_queue = Queue()
        self._results_queue = Queue()
        self._quit = False
        self._worker_thread = None
        self.instrument_control = None
        self.instrument = None
        self.execute_lock = threading.Lock()

    def start(self):
        logger.info("[{}] OmpBackGroundWorker start".format(threading.current_thread().name))
        self._quit = False
        self._worker_thread = threading.Thread(name='OmpBackGroundWorkerThread',
                                               target=self._worker_thread_run)
        self._worker_thread.daemon = True
        self._worker_thread.start()

        logger.info("OmpBackGroundWorker initializing OMP")
        self.execute_on_worker(lambda: self._init_omp(), description="lambda: self._init_omp()")
        logger.info("OmpBackGroundWorker initialisation of OMP finished")

    def stop(self):
        logger.info("[{}] OmpBackGroundWorker stop".format(threading.current_thread().name))
        self._quit = True
        self._worker_thread.join()
        self.instrument = None
        self.instrument_control = None
        logger.info("[{}] OmpBackGroundWorker stopped".format(threading.current_thread().name))

    def get_instrument(self):
        logger.info("[thread:{}] OmpBackGroundWorker get instrument".format(
            threading.current_thread().name))
        return self.instrument

    def execute_on_worker(self, lambda_expression, description=""):
        with self.execute_lock:
            logger.debug("[thread:{}] OmpBackGroundWorker execute_on_worker({})".format(
                threading.current_thread().name, description))
            self._worker_queue.put(lambda_expression)
            self._worker_queue.join()
            results = self._results_queue.get()
            logger.debug("[thread:{}] {} Results object retrieved from results queue: {}".format(
                threading.current_thread().name, description, results))
            self._results_queue.task_done()
            return results

    def _init_omp(self):
        logger.info("[{}] OmpBackGroundWorker _init_omp".format(threading.current_thread().name))
        try:
            # required to initialize the thread according to OMP threading model
            #from fei.tem.omp.api import IInstrumentControl
            omp.com_initialize_multithreaded()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.exception("OmpBackGroundWorker _init_omp exception: \n{0}".format(
                repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
            print("OmpBackGroundWorker _init_omp exception: \n{0}".format(
                repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
            raise

        logger.info("[{}] OmpBackGroundWorker creating InstrumentControl".format(
            threading.current_thread().name))
        self.instrument_control = IInstrumentControl.create()
        logger.info("[{}] OmpBackGroundWorker getting instrument".format(
            threading.current_thread().name))
        self.instrument = self.instrument_control.get_instrument()
        logger.info("[{}] OmpBackGroundWorker InstrumentControl created".format(
            threading.current_thread().name))

    def _worker_thread_run(self):
        logger.info("[{}] OmpBackGroundWorker thread Started".format(
            threading.current_thread().name))
        while not self._quit:
            if not self._worker_queue.empty():
                callable_function = self._worker_queue.get()
                try:
                    while not self._results_queue.empty():
                        item = self._results_queue.get()
                        logger.error(
                            "[thread:{}] Error, results object still in results queue: {}".format(
                            threading.current_thread().name, item))
                    results = callable_function()
                    logger.debug("[thread:{}] Results object putting in results queue: {}".format(
                        threading.current_thread().name, results))
                    self._results_queue.put(results)
                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    logger.exception("OmpBackGroundWorker exception: \n{0}".format(
                        repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
                    print("OmpBackGroundWorker exception: \n{0}".format(
                        repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
                    raise
                finally:
                    self._worker_queue.task_done()
        logger.info("OmpBackGroundWorker thread Finished")
