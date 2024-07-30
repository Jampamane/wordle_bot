from multiprocessing import Process
from wordle import Wordle


def wordle_child(x: str=None, y: str=None, width: str=None, height: str=None) -> None:
    """
    A multiprocess child object that will create a chrome instance and play wordle.

    Args:
        x (str, optional): X pos of window. Defaults to None.
        y (str, optional): Y pos of window. Defaults to None.
        width (str, optional): Width of window. Defaults to None.
        height (str, optional): Height of window. Defaults to None.
    """
    wordle = Wordle()
    wordle.browser.set_window_position(x=x, y=y)
    wordle.browser.set_window_size(width=width, height=height)
    wordle.solve()


def wordle_multiprocess() -> None:
    """Will create 4 child objects. Assumes the monitor is 1920x1080."""
    p1 = Process(
        target=wordle_child,
        args=(
            0,
            0,
            480,
            1080,
        ),
    )
    p2 = Process(
        target=wordle_child,
        args=(
            480,
            0,
            480,
            1080,
        ),
    )
    p3 = Process(
        target=wordle_child,
        args=(
            960,
            0,
            480,
            1080,
        ),
    )
    p4 = Process(
        target=wordle_child,
        args=(
            1440,
            0,
            480,
            1080,
        ),
    )
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

