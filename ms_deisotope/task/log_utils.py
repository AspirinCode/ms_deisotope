from __future__ import print_function
import logging
import multiprocessing
import threading
import traceback

from datetime import datetime

logger = logging.getLogger("ms_deisotope.task")


def fmt_msg(*message):
    return "%s %s" % (datetime.now().isoformat(' '), ', '.join(map(str, message)))


def printer(obj, *message):
    print(fmt_msg(*message))


def debug_printer(obj, *message):
    if obj.in_debug_mode():
        print("DEBUG:" + fmt_msg(*message))


class CallInterval(object):
    """Call a function every `interval` seconds from
    a separate thread.

    Attributes
    ----------
    stopped: threading.Event
        A semaphore lock that controls when to run `call_target`
    call_target: callable
        The thing to call every `interval` seconds
    args: iterable
        Arguments for `call_target`
    interval: number
        Time between calls to `call_target`
    """

    def __init__(self, interval, call_target, *args):
        self.stopped = threading.Event()
        self.interval = interval
        self.call_target = call_target
        self.args = args
        self.thread = threading.Thread(target=self.mainloop)
        self.thread.daemon = True

    def mainloop(self):
        while not self.stopped.wait(self.interval):
            try:
                self.call_target(*self.args)
            except Exception as e:
                logger.exception("An error occurred in %r", self, exc_info=e)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stopped.set()


class MessageSpooler(object):
    """An IPC-based logging helper

    Attributes
    ----------
    halting : bool
        Whether the object is attempting to
        stop, so that the internal thread can
        tell when it should stop and tell other
        objects using it it is trying to stop
    handler : Callable
        A Callable object which can be used to do
        the actual logging
    message_queue : multiprocessing.Queue
        The Inter-Process Communication queue
    thread : threading.Thread
        The internal listener thread that will consume
        message_queue work items
    """
    def __init__(self, handler):
        self.handler = handler
        self.message_queue = multiprocessing.Queue()
        self.halting = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.halting:
            try:
                message = self.message_queue.get(True, 2)
                self.handler(*message)
            except Exception:
                continue

    def stop(self):
        self.halting = True
        self.thread.join()

    def sender(self):
        return MessageSender(self.message_queue)


class MessageSender(object):
    """A simple callable for pushing objects into an IPC
    queue.

    Attributes
    ----------
    queue : multiprocessing.Queue
        The Inter-Process Communication queue
    """
    def __init__(self, queue):
        self.queue = queue

    def __call__(self, *message):
        self.send(*message)

    def send(self, *message):
        self.queue.put(message)


class LogUtilsMixin(object):

    logger_state = None
    print_fn = printer
    debug_print_fn = debug_printer
    error_print_fn = printer
    warn_print_fn = printer

    @classmethod
    def log_with_logger(cls, logger):
        cls.logger_state = logger
        cls.print_fn = logger.info
        cls.debug_print_fn = logger.debug
        cls.error_print_fn = logger.error
        cls.warn_print_fn = logger.warn

    def in_debug_mode(self):
        if self._debug_enabled is None:
            logger_state = self.logger_state
            if logger_state is not None:
                self._debug_enabled = logger_state.isEnabledFor("DEBUG")
        return bool(self._debug_enabled)

    def log(self, *message):
        self.print_fn(', '.join(map(str, message)))

    def warn(self, *message):
        self.warn_print_fn(', '.join(map(str, message)))

    def debug(self, *message):
        self.debug_print_fn(', '.join(map(str, message)))

    def error(self, message, exception=None):
        self.error_print_fn(', '.join(map(str, message)))
        if exception is not None:
            self.error_print_fn(traceback.format_exc(exception))

    def ipc_logger(self, handler=None):
        if handler is None:
            def handler(message):
                self.log(message)
        return MessageSpooler(handler)
