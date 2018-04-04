# -*- coding: utf-8 -*-
import gevent
import multiprocessing

def compute(x, y):
    print "Compute %s + %s..." %(x, y)
    # gevent.sleep(1.0)
    return x + y

def print_sum(x, y):
    result = compute(x, y)
    print "%s + %s = %s" % (x, y, result)

print multiprocessing.cpu_count()
import pdb; pdb.set_trace()
print_sum(1,2)
