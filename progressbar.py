import time
import sys


class ProgressBar(object):
    def __init__(self, width=40, disabled=False, timeout=None):
        self.t0 = None
        self.width = int(width)
        self.last_call = time.clock()
        self.disabled = bool(disabled)
        self.timeout = 1e12 if timeout is None else int(timeout)

    def update(self, progress):
        now = time.clock()
        self.t0 = now if self.t0 is None else self.t0
        deltaT = now - self.t0

        # only update stuff evey now and then
        if now - self.last_call < 0.5:
            return
        self.last_call = now

        # timeout protection
        if deltaT > self.timeout:
            raise ProgressBarTimeoutError(deltaT, self.timeout)

        if self.disabled:
            return
        self.forced_update(progress, deltaT)

    def forced_update(self, progress, deltaT=None):

        deltaT = time.clock() - self.t0 if deltaT is None else deltaT

        if self.disabled:
            sys.stdout.write("elapsed time: {:0.1f}s\n"
                             .format(deltaT))
            sys.stdout.flush()
            return

        # draw a nice progress bar
        hashes = '=' * int(round(progress*self.width))
        msg = ["\rSimulation: [{:<40s}] {:5.1f}%".format(hashes, progress*100)]
        msg.append("elapsed time: {:<5.1f}s".format(deltaT))
        if progress < 1:
            eta = (deltaT/progress-deltaT) if progress > 0 else 0
            msg.append("ETA: {:0.1f}s".format(eta))
        sys.stdout.write(" - ".join(msg))
        sys.stdout.flush()


class ProgressBarTimeoutError(Exception):

    def __init__(self, deltaT, timeout):
        msg = "Process got interrupted after {} s (timeout: {} s)"
        msg = msg.format(deltaT, timeout)
        super(ProgressBarTimeoutError, self).__init__(msg)
