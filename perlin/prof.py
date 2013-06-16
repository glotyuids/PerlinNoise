#!/usr/bin/env python
# $Id: prof.py,v 1.5 2001/05/31 04:57:05 kevint Exp $
# This file is to serve as example code.  Do whatever you like with it!
#  -- Kevin Turner <acapnotic@users.sourceforge.net>

"""Profiling PerlinNoise"""

import perlin
from Numeric import *
import profile, pstats
import pygame

import peterlin

TRUE = 1==1
FALSE = not TRUE

def f8_i(x):
    """using an integer clock, so cut out the floating-point"""

    return string.rjust(`x`,8)

pstats.f8 = f8_i

class PygameProfile(profile.Profile):
    def __init__(self):
	profile.Profile.__init__(self, pygame.time.get_ticks)

    def trace_dispatch_i(self, frame, event, arg):
	t = self.timer() - self.t # - 0 # Calibration constant
	# (but this needs to calibration constant on my machine)

	if self.dispatch[event](frame,t):
	    self.t = self.timer()
	else:
	    self.t = self.timer() - t # put back unrecorded delta
	return


def prof():
    if 0:
	callers_prof()
    else:
	comparitive_prof()


def callers_prof():
    pr = do_prof((3,3), 6, runs=3)

    stats = pstats.Stats(pr).strip_dirs()

    stats.sort_stats('time')
    stats.print_stats()
    stats.print_callers()


def comparitive_prof():
    do_prof((9,),6,runs=6)

    do_prof((9,),6,dynamic=FALSE,runs=6)

    do_prof((3,3), 6, runs=3)

    do_prof((3,3), 6, dynamic=FALSE, runs=3)

    do_prof((3,3), 6, None, optimize=FALSE, runs=3)

    do_prof((3,3), 6, perlin.ease_interpolation, runs=3)

    do_prof((3,3), 6, perlin.ease_interpolation,
	    optimize=FALSE, runs=3)


def do_prof(size, frequency, interp_func=None,
	    optimize=TRUE, dynamic=TRUE, runs=1):

    pr=PygameProfile()

    dimensions = len(size)

    try:
	funcname = interp_func.__name__
    except:
	funcname = `None`

    print "%dD %sx%s ifunc=%s %s %s" % (len(size),size,frequency,funcname,
				       optimize and 'Optimized' or 'general',
				       dynamic and 'Dynamic' or 'static')

    if optimize:
	perlin._FORCE_GENERIC_CASE = FALSE
    else:
	perlin._FORCE_GENERIC_CASE = TRUE

    if dynamic:
	perlin._DISABLE_DYNAMIC_CODE = FALSE
    else:
	perlin._DISABLE_DYNAMIC_CODE = TRUE

    build_func = globals()['build_%dD' % dimensions]

    old_t = 0
    for i in range(1,runs+1):
	pr.runcall(build_func, size, frequency, interp_func)

	t = pstats.Stats(pr).total_tt
	print "Run %2d:" % i,t - old_t
	old_t = t

    print "Average:", t / runs
    # XXX: add stats_dumping

    return pr


def build_1D((width,), frequency, interp_func=None):

    resolution = frequency

    noise = perlin.PerlinNoise((width,),interp_func)

    surfarray = zeros((width*resolution,), Int)

    histogram = {}
    for x in range(width * resolution):
	nx = x / float(resolution)
	value = noise.value_at((nx,))

	#if histogram.has_key(int(value * 10)):
	#histogram[int(value * 10)] += 1
	#else:
	#histogram[int(value * 10)] = 1

	value = int(value * 128 + 128.5)
	if value < 0:
	    value = 0
	elif value > 255:
	    value = 255
	surfarray[x] = value

    # draw_histogram(histogram, surface)

def build_2D((width, height), frequency, interp_func=None):

    resolution = frequency

    noise = perlin.PerlinNoise((width,height),interp_func)

    surfarray = zeros((width*resolution, height*resolution),Int)

    histogram = {}
    for x in range(width * resolution):
	for y in range(height * resolution):
	    nx = x / float(resolution)
	    ny = y / float(resolution)
	    value = noise.value_at((nx,ny))

	    #if histogram.has_key(int(value * 10)):
	    #histogram[int(value * 10)] += 1
	    #else:
	    #histogram[int(value * 10)] = 1

	    value = int(value * 128 + 128.5)
	    if value < 0:
		value = 0
	    elif value > 255:
		value = 255
	    surfarray[x,y] = value

    # draw_histogram(histogram, surface)


def build_petelin_prof(size, frequency, runs=1):
    print "2D %sx%s petelin" % (size,frequency)

    pr=PygameProfile()

    old_t = 0
    for i in range(1,runs+1):
	pr.runcall(build_petelin, size, frequency)

	t = pstats.Stats(pr).total_tt
	print "Run %2d:" % i,t - old_t
	old_t = t

    print "Average:", t / runs
    # XXX: add stats_dumping

    return pr


def build_pet*�������Fc�M�v`�� �^��ԩ�9:�F�u!6%�9��N8��V�ݖ}:F��Z��'���)�5�G%�X�UFF�	*�&\^@� ��~���PE�=)`�I�m(m^w}�,y�_$��4���tK,�B�mt�!�C���O���������Mu���u e�t5$* d����VC��K����}�'lƿ»W̤㎑#o�НT��f66p��L�?^	���%�]G22̸��msn/8�'MX��͌^��}P�gq*f̽<���(af՟���], �׉������[X��Ι���b�7ٺ�Q�Oq���۴Mv�w[Z ;�]���]���n�=lWЋ���>jf�]#�a�7�{��	]�Z&�h���!<c�$!q��F"�	Eb�x�Ǣ���*l��AX�h�anã�U?)���XO�O�oN�ݵ`�����/�|O�I�����ǝ��@��`H`��YT��)k3��� �v��֯��p��Α�4��l8���@L�D&�㱖��g�I�t��jHT�B��^t������ԦK<d� |3����﹯��x6������[6_ȯρXS���j���>��G=#!�jD��3~����<M$�
�� [�6�&5j=�.���?mDg��� g��n�T�k�&�������q#p��;�����y�(�i���muE�&���WEk<�/]f΄��b�_���};c�r4؃����"����t�Р���<�M�-n��=XA����B;����0#�l�O9r1�%�H�t3��[����܋��'l��i6�IepO���;<�m�o��z�@�� 	�������": �x�"8e<�b}�tx$�WL�d��!,T��
I�K Y��<���<#�U����՗$��T9�4�E�R��l���ZwN%����ĵO)]?ZF�!�4�5%���]�M�- t"x�-��in�T���ŧ���g�J'D2OX��m����p��ɝO�D���OE�u0Hχ�qA��G���N��Q�C냳��!M��F�K��3�i'$���#�~���9E �iXo�#M埧A�,|�6��Eu�쑼�ɹ���E��$]�{�&֭�;�}�=y��=��q-���Y����{'������� y
�bt��8gmL�ːNt�Ǌa3�g��/��#�R��+�^�U�W_���>��9�GUS� g+�c5S
���<�ξ��0ak�G/5�3瞨��_1<o2\u|�#������6��7_� Ts6MӪ�����â��M�%j��4����0�]��ل^�7����Hsb&f���~RfB�(���I\U�E�ν��r!m�;��%�T�wBQ"o����z*]@-(