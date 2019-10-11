# Copyright (c) 2011-2019 Eric Froemling
"""Defines Actor(s)."""
from __future__ import annotations

from typing import TYPE_CHECKING

import ba

if TYPE_CHECKING:
    from typing import Optional, Union, Any


class OnScreenTimer(ba.Actor):
    """A handy on-screen timer.

    category: Gameplay Classes

    Useful for time-based games where time increases.
    """

    def __init__(self) -> None:
        super().__init__()
        self._starttime: Optional[int] = None
        self.node = ba.newnode('text',
                               attrs={
                                   'v_attach': 'top',
                                   'h_attach': 'center',
                                   'h_align': 'center',
                                   'color': (1, 1, 0.5, 1),
                                   'flatness': 0.5,
                                   'shadow': 0.5,
                                   'position': (0, -70),
                                   'scale': 1.4,
                                   'text': ''
                               })
        self.inputnode = ba.newnode('timedisplay',
                                    attrs={
                                        'timemin': 0,
                                        'showsubseconds': True
                                    })
        self.inputnode.connectattr('output', self.node, 'text')

    def start(self) -> None:
        """Start the timer."""
        tval = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(tval, int)
        self._starttime = tval
        self.inputnode.time1 = self._starttime
        ba.sharedobj('globals').connectattr('time', self.inputnode, 'time2')

    def hasstarted(self) -> bool:
        """Return whether this timer has started yet."""
        return self._starttime is not None

    def stop(self,
             endtime: Union[int, float] = None,
             timeformat: ba.TimeFormat = ba.TimeFormat.SECONDS) -> None:
        """End the timer.

        If 'endtime' is not None, it is used when calculating
        the final display time; otherwise the current time is used.

        'timeformat' applies to endtime and can be SECONDS or MILLISECONDS
        """
        if endtime is None:
            endtime = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
            timeformat = ba.TimeFormat.MILLISECONDS

        if self._starttime is None:
            print('Warning: OnScreenTimer.stop() called without start() first')
        else:
            endtime_ms: int
            if timeformat is ba.TimeFormat.SECONDS:
                endtime_ms = int(endtime * 1000)
            elif timeformat is ba.TimeFormat.MILLISECONDS:
                assert isinstance(endtime, int)
                endtime_ms = endtime
            else:
                raise Exception(f'invalid timeformat: {timeformat}')

            self.inputnode.timemax = endtime_ms - self._starttime

    def getstarttime(self, timeformat: ba.TimeFormat = ba.TimeFormat.SECONDS
                     ) -> Union[int, float]:
        """Return the sim-time when start() was called.

        Time will be returned in seconds if timeformat is SECONDS or
        milliseconds if it is MILLISECONDS.
        """
        val_ms: Any
        if self._starttime is None:
            print('WARNING: getstarttime() called on un-started timer')
            val_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        else:
            val_ms = self._starttime
        assert isinstance(val_ms, int)
        if timeformat is ba.TimeFormat.SECONDS:
            return 0.001 * val_ms
        if timeformat is ba.TimeFormat.MILLISECONDS:
            return val_ms
        raise Exception(f'invalid timeformat: {timeformat}')

    def handlemessage(self, msg: Any) -> Any:
        # if we're asked to die, just kill our node/timer
        if isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()
