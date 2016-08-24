#!/usr/bin/env python

import sys
import wye

url = "http://localhost:8080"

context = wye.StreamingContext(url)

job = context.define_job(name="pi", description="Calculates PI")

def pi(x):

    global total

    if not "total" in globals():
        total = 0.0

    total = total + (x[1] / (16.0 ** x[0]))
    
    sys.stderr.write("%2.20f\n" % total)
    return None

sink = job.define_lambda_worker("sink", pi)

def digit(k):

    global total

    if not "total" in globals():
        globals()["total"] = 0.0

    f1 = 4.0 / (8.0 * k + 1)
    f2 = - (2.0 / (8.0 * k + 4.0))
    f3 = - (1.0 / (8.0 * k + 5.0))
    f4 = - (1.0 / (8.0 * k + 6.0))
    
    f = (f1 + f2 + f3 + f4)

    total = total + f

    digit = (k, int(total))

    total = total - int(total)
    total = total * 16
    
    return digit

digit = job.define_lambda_worker("digit", digit,
                                 outputs={ "output": [(sink,"input")] })

src = job.define_python_worker("source", "source_nums.py",
                               outputs={ "output": [ (digit,"input") ] })

job_id = job.implement()

sys.stderr.write("Job %s is running.\n" % job_id)

