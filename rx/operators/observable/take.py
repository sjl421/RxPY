from rx import Observable, AnonymousObservable
from rx.internal import ArgumentOutOfRangeException


def take(source: Observable, count: int, scheduler=None):
    """Returns a specified number of contiguous elements from the start of
    an observable sequence, using the specified scheduler for the edge case
    of take(0).

    1 - source.take(5)
    2 - source.take(0, rx.Scheduler.timeout)

    Keyword arguments:
    count -- The number of elements to return.
    scheduler -- [Optional] Scheduler used to produce an OnCompleted
        message in case count is set to 0.

    Returns an observable sequence that contains the specified number of
    elements from the start of the input sequence.
    """

    if count < 0:
        raise ArgumentOutOfRangeException()

    if not count:
        return Observable.empty(scheduler)

    observable = source

    def subscribe(observer):
        remaining = count

        def send(value):
            nonlocal remaining

            if remaining > 0:
                remaining -= 1
                observer.send(value)
                if not remaining:
                    observer.close()

        return observable.subscribe_callbacks(send, observer.throw, observer.close)
    return AnonymousObservable(subscribe)