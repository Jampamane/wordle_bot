from multiprocessing import Process
from wordle import Wordle


def main(x=None, y=None, width=None, height=None):
    wordle = Wordle()
    wordle.browser.set_window_position(x=x, y=y)
    wordle.browser.set_window_size(width=width, height=height)
    wordle.solve()


def wordle_multiprocess():
    p1 = Process(
        target=main,
        args=(
            0,
            0,
            480,
            1080,
        ),
    )
    p2 = Process(
        target=main,
        args=(
            480,
            0,
            480,
            1080,
        ),
    )
    p3 = Process(
        target=main,
        args=(
            960,
            0,
            480,
            1080,
        ),
    )
    p4 = Process(
        target=main,
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


if __name__ == "__main__":
    wordle_multiprocess()
