#!/usr/bin/env python2.7
# -*- coding: utf-8

import sys
import Tkinter
import random


class RectArray:
    def __init__(self, rt, arr, x0, y0, wight, height, bord):
        self.array = arr
        self.canvas = Tkinter.Canvas(
            rt, width=wight + 2 * bord, height=height + 2 * bord, bg='white')
        self.canvas.focus_set()
        self.canvas.pack()

        self.x0 = x0
        self.y0 = y0
        self.x1 = self.x0 + wight
        self.y1 = self.y0 - height
        self.length = len(self.array)
        self.dx = 1. * (self.x1 - self.x0) / self.length
        self.m = max(self.array)
        self.y = lambda n: (1. * n / self.m * (self.y1 - self.y0) + self.y0) \
            if(n != 0) else self.y0 - 1

        self.rgb = lambda n: (int(255. * n / self.m),
                              int(255. * (self.m - n) / self.m), 0)
        self.rgb_str = lambda n:\
            '#{0[0]:02x}{0[1]:02x}{0[2]:02x}'.format(self.rgb(n))

        self.rect_array = self.create_array()

        self.out_steps = arr
        self.played = False

        self.sort_str = sys.argv[1] if len(sys.argv) > 2 else "quicksort"
        self.sort = dict(
            zip(["quicksort", "shaker_sort"],
                [quicksort, shaker_sort]))[self.sort_str]

    def create_array(self):
        return [self.canvas.create_rectangle(
            self.x0 + 1. * i * self.dx, 1. * self.y0,
            self.x0 + 1. * (i + 1) * self.dx, self.y(self.array[i]),
            fill=self.rgb_str(self.array[i]))
            for i in range(len(self.array))]

    def update_array(self):
        for i in range(len(self.rect_array)):
            self.canvas.coords(self.rect_array[i],
                               self.x0 + 1. * i * self.dx, 1. * self.y0,
                               self.x0 + 1. * (i + 1) * self.dx,
                               self.y(self.array[i]))
            self.canvas.itemconfig(self.rect_array[i],
                                   fill=self.rgb_str(self.array[i]))
        self.canvas.focus_set()
        self.canvas.pack()
        self.canvas.update_idletasks()
        root.update()

    def shuffle(self):
        random.shuffle(self.array)

    def sort_play(self):
        self.played = True
        dt = int(7000. / len(self.out_steps)) if len(self.out_steps) > 0 else 1
        for i in range(len(self.out_steps)):
            self.array = self.out_steps[i][:]
            try:
                root.after(dt, self.update_array())
            except Tkinter.TclError:
                break
        self.played = False


# Sorts

# For qsort
class Stack (list):
    ''' push() to add an item to the top of the stack '''
    push = list.append


def quicksort(items):
    """
    Sort a sequence using the quick-sort algorithm.

    :param items: the sequence to be sorted
    :return: out, sorted steps
    """
    nItems = len(items)
    if nItems < 2:
        return []
    todo = Stack([(0, nItems - 1)])
    out = []
    while todo:
        elem_idx, pivot_idx = low, high = todo.pop()
        elem = items[elem_idx]
        pivot = items[pivot_idx]
        while pivot_idx > elem_idx:
            if elem > pivot:
                items[pivot_idx] = elem
                pivot_idx -= 1
                items[elem_idx] = elem = items[pivot_idx]
            else:
                elem_idx += 1
                elem = items[elem_idx]
        items[pivot_idx] = pivot
        out.append(items[:])
        rects.array = items[:]
        lsize = pivot_idx - low
        hsize = high - pivot_idx
        if lsize <= hsize:
            if 1 < lsize:
                todo.push((pivot_idx + 1, high))
                todo.push((low, pivot_idx - 1))
        else:
            todo.push((low, pivot_idx - 1))
        if 1 < hsize:
            todo.push((pivot_idx + 1, high))
    return out


def shaker_sort(a):
    """
    Sort a sequence using the shaker-sort algorithm.

    :param a: the sequence to be sorted
    :return: out, sorted steps
    """
    out = []

    i = 0
    j = len(a) - 1

    if j < 1:
        return out

    while i + 1 < j:
        b = a[:]
        s = j
        k = i
        while k < j:
            if a[k] > a[k + 1]:
                a[k], a[k + 1] = a[k + 1], a[k]
                out.append(a[:])
                s = k
            k = k + 1
        j = s
        s = i
        k = j
        while k > i:
            if a[k - 1] > a[k]:
                a[k], a[k - 1] = a[k - 1], a[k]
                out.append(a[:])
                s = k
            k = k - 1
        i = s
        if a == b:
            break
    return out
# /Sorts


# Callbacks
def sort_callback(event):
    out = rects.sort(rects.array)
    out1 = [out[0]] if (len(out) > 1) else []
    # !!! deletes copy iterations
    for i in out[1:]:
        if i != out1[-1]:
            out1 = out1 + [i]
    rects.out_steps = out1
    rects.sort_play()


def shuffle_callback(event):
    if not rects.played:
        rects.shuffle()
        rects.update_array()


def update_callback():
    rects.update_array()


def close_callback(event):
    # quit = True
    # root.withdraw ()  # if you want to bring it back
    root.destroy()
    # sys.exit ()  # if you want to exit the entire thing
# /Callbacks


if __name__ == "__main__":
    # ./main [sorttype=quicksort|shaker_sort length]
    #    sorttype:    quicksort (default)
    #                 shaker_sort
    #   length:       100..1000 for quicksort (default 350)
    #                 10 ..300  for shaker_sort
    # In program:
    #    q - exit
    #    w - shuffle array
    #    e - sort array

    if len(sys.argv) > 2:
        num = int(sys.argv[2])
    else:
        num = 350
    a = [i for i in range(num)]

    root = Tkinter.Tk()

    w = 800  # width for the Tk root
    h = 600  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('+{}+{}'.format(x, y))
    root.resizable(False, False)

    border = 50
    rects = RectArray(
        root, a, border, h - border, w - 2 * border, h - 2 * border, border)

    # root.bind('<Escape>', close_callback) #Need focus root
    root.bind('q', close_callback)
    rects.canvas.bind('w', shuffle_callback)
    rects.canvas.bind('e', sort_callback)
    root.mainloop()
