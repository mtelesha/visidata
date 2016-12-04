# Copyright (C) 2016 Saul Pwanson
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import curses
from curses.ascii import DEL

class EscapeException(Exception):
    pass

class CtrlKey:
    def __getattr__(self, k):  # Ctrl.a or Ctrl.A -> ^A keycode
        return ord(k) & 31
    def __call__(self, k):   # Ctrl('^') -> Ctrl-^ keycode
        return ord(k) & 31
Ctrl = CtrlKey()

class ShiftKey:
    def __getattr__(self, k):  # Ctrl.a or Ctrl.A -> ^A keycode
        assert curses.ascii.isupper(k)
        return ord(k)
Shift = ShiftKey()

class PlainKey(object):
    TAB = Ctrl.I
    ENTER = Ctrl.J
    ESC = 27
    def __getattr__(self, k):
        if len(k) == 1 and ord(k) < 127:
            return ord(k)
        return getattr(curses, 'KEY_' + k)
    def __call__(self, k):
        assert len(k) == 1 and ord(k) < 127
        return ord(k)
Key = PlainKey()

def keyname(ch):
    return curses.keyname(ch).decode('utf-8')


def editText(scr, y, x, w, attr=curses.A_NORMAL, value='', fillchar=' ', unprintablechar='.'):
    def splice(v, i, s):  # splices s into the string v at i (v[i] = s[0])
        return v if i < 0 else v[:i] + s + v[i:]
    def clean(s):
        return ''.join(c if c.isprintable() else unprintablechar for c in str(s))
    def delchar(s, i, remove=1):
        return s[:i] + s[i+remove:]

    insert_mode = False
    v = str(value) # value under edit
    i = 0          # index into v
    while True:
        dispval = clean(v)
        dispi = i
        if len(dispval) < w:
            dispval += fillchar*(w-len(dispval))
        elif i >= w:
            dispi = w-1
            dispval = dispval[i-w:]

        scr.addstr(y, x, dispval, attr)
        scr.move(y, x+dispi)
        ch = scr.getch()
        if ch == Key.IC:                             insert_mode = not insert_mode
        elif ch == Ctrl.A or ch == Key.HOME:         i = 0
        elif ch == Ctrl.B or ch == Key.LEFT:         i -= 1
        elif ch == Ctrl.C or ch == Key.ESC:          raise EscapeException(keyname(ch))
        elif ch == Ctrl.D or ch == Key.DC:           v = delchar(v, i)
        elif ch == Ctrl.E or ch == Key.END:          i = len(v)
        elif ch == Ctrl.F or ch == Key.RIGHT:        i += 1
        elif ch in (Ctrl.H, Key.BACKSPACE, DEL):     i -= 1 if i > 0 else 0; v = delchar(v, i)
        elif ch == Ctrl.J or ch == Key.ENTER:        break
        elif ch == Ctrl.K:                           v = v[:i]
        elif ch == Ctrl.R:                           v = value
        elif ch == Ctrl.T:                           v = delchar(splice(v, i-2, v[i-1]), i)
        elif ch == Ctrl.U:                           v = v[i:]; i = 0
        elif ch == Ctrl.V:                           v = splice(v, i, chr(scr.getch())); i += 1
        else:
            if insert_mode:
                v = splice(v, i, chr(ch))
            else:
                v = v[:i] + chr(ch) + v[i+1:]

            i += 1

        if i < 0: i = 0
        if i > len(v): i = len(v)

    return v
