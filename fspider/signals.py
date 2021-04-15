import asyncio
import functools
import logging

from pydispatch import dispatcher
from pydispatch.dispatcher import liveReceivers, getAllReceivers, disconnect, Any

from fspider import context

logger = logging.getLogger(__name__)

spider_opened = object()
spider_closed = object()
crawler_closed = object()


def disconnect_all(signal=Any, sender=Any):
    """Disconnect all signal handlers. Useful for cleaning up after running
    tests
    """
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        disconnect(receiver, signal=signal, sender=sender)


def connect(receiver, signal, sender=None, **kwargs):
    if not sender:
        sender = context.spider.get()
    return dispatcher.connect(receiver, signal, sender, **kwargs)


async def send(signal, sender=None, *args, **kwargs):
    if not sender:
        sender = context.spider.get()
    return await _send_catch_log(signal, sender, *args, **kwargs)


async def _send_catch_log(signal, sender, *args, **kwargs):
    responses = []
    _dont_log = False
    loop = asyncio.get_running_loop()
    for receiver in liveReceivers(getAllReceivers(sender, signal)):
        func = functools.partial(
            receiver,
            *args,
            **kwargs
        )
        try:
            if asyncio.iscoroutinefunction(receiver):
                response = await func()
            else:
                response = await loop.run_in_executor(None, func)
        except Exception as e:
            response = e
            logger.error(f'Caught an error on {receiver}', exc_info=True)
        responses.append((receiver, response))

    return responses
