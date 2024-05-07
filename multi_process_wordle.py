from multiprocessing import Process
from typing import Any
from wordle import Wordle

class PlaySixteen():

    def __new__(self, number_of_times) -> None:
        for _ in range(number_of_times):
            a = Process(target=self._play_wordle, args=(self, 3360, 417, 510, 480),)
            b = Process(target=self._play_wordle, args=(self, 2880, 417, 510, 480),)
            c = Process(target=self._play_wordle, args=(self, 2400, 417, 510, 480),)
            d = Process(target=self._play_wordle, args=(self, 1920, 417, 510, 480),)
            e = Process(target=self._play_wordle, args=(self, 1440, 0, 510, 480),)
            f = Process(target=self._play_wordle, args=(self, 960, 0, 510, 480),)
            g = Process(target=self._play_wordle, args=(self, 480, 0, 510, 480),)
            h = Process(target=self._play_wordle, args=(self, 0, 0, 510, 480),)
            i = Process(target=self._play_wordle, args=(self, 3360, 927, 510, 480),)
            j = Process(target=self._play_wordle, args=(self, 2880, 927, 510, 480),)
            k = Process(target=self._play_wordle, args=(self, 2400, 927, 510, 480),)
            l = Process(target=self._play_wordle, args=(self, 1920, 927, 510, 480),)
            m = Process(target=self._play_wordle, args=(self, 1440, 510, 510, 480),)
            n = Process(target=self._play_wordle, args=(self, 960, 510, 510, 480),)
            o = Process(target=self._play_wordle, args=(self, 480, 510, 510, 480),)
            p = Process(target=self._play_wordle, args=(self, 0, 510, 510, 480),)

            a.start()
            b.start()
            c.start()
            d.start()
            e.start()
            f.start()
            g.start()
            h.start()
            i.start()
            j.start()
            k.start()
            l.start()
            m.start()
            n.start()
            o.start()
            p.start()

            a.join()
            b.join()
            c.join()
            d.join()
            e.join()
            f.join()
            g.join()
            h.join()
            i.join()
            j.join()
            k.join()
            l.join()
            m.join()
            n.join()
            o.join()
            p.join()

    def _play_wordle(self, x, y, height, width):
        wordle = Wordle(x, y, height, width)
        wordle.solve()
