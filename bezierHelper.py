import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print "Warining: Fonts Disabled!"
if not pygame.mixer: print "Warning: Sound Disabled!"

class BezierHelper():

    #linear interpolate between 2 values
    def Bezier2(self, v1, v2, t, duration=1):
        self.duration = duration
        self.v1 = v1
        self.v2 = v2
        self.t = self.Clamp01(t/duration)
        return v1 + v2 * self.t

    #quadratic interpolate between 3 values
    def Bezier3(self, v1, v2, v3, t, duration=1):
        self.duration = duration
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.t = self.Clamp01(t/duration)
        oneMinusT = 1 - self.t
        return (oneMinusT * oneMinusT * v1 + \
        2 * oneMinusT * self.t * v2 + \
        self.t * self.t * v3)

    #cubic interpolate between 4 values
    def Bezier4(self, v1, v2, v3, v4, t, duration=1):
        self.duration = duration
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.t = self.Clamp01(t/duration)
        oneMinusT = 1 - self.t
        return (oneMinusT * oneMinusT * oneMinusT * v1 + \
        3 * oneMinusT * oneMinusT * self.t * v2 + \
        3 * oneMinusT * self.t * self.t * v3 + \
        self.t * self.t * self.t * v4)

    #returns smaller of two values
    def Min(self, a, b):
        if a < b:
            return a
        else:
            return b

    #returns larger of two values
    def Max(self, a, b):
        if a > b:
            return a
        else:
            return b

    #clamp value between 0 and 1
    def Clamp01(self, value):
        return self.Max(self.Min(value, 1), 0)

    #clamp value between min and max
    def Clamp(self, value, min, max):
        return self.Max(self.Min(value, max), min)

    def NextBezier2(self, deltaT):
        return self.Bezier2(self.v1, self.v2, self.t * self.duration + deltaT, self.duration)

    def NextBezier3(self, deltaT):
        return self.Bezier3(self.v1, self.v2, self.v3, self.t * self.duration + deltaT, self.duration)

    def NextBezier4(self, deltaT):
        return self.Bezier4(self.v1, self.v2, self.v3, self.v4, self.t * self.duration + deltaT, self.duration)

if __name__ == "__main__":
    move = BezierHelper()
    print "Bezier2(0,10,.5): "
    print move.Bezier2(0, 10, .5)
    print "Bezier3(0,10,0,.8): "
    print move.Bezier3(0, 10, 0, 0)
    for i in range(0,15):
        print move.NextBezier3(.1)
