
# Wye Streaming Framework

## Introduction

Wye is a streaming framework in early stages of development.  Written in C++,
it is very simple to get started with.  To use the framework requires writing
elements
in Python, and instantiation of stream elements is possible using Python.

Currently, the framework is limited in that:
* Framework really only usefully makes use of a single machine.
* Framework supports streaming components written in Python only.
* Framework doesn't support multi-machine, nor resilience.

Lots of ambitions to expand the framework into:
* Distributed stream processing, with automatic election of master.
* Checkpointing stream results for resilience.
* Stream modules written in other languages (C++, Lua, Java).
* Failure recovery in event of node loss.

## Getting started

Compile the framework:

```
make
```
Run the service daemon.  This starts a service on port 8080:

```
./service
```

In a separate terminal, invoke a stream processing job:

```
./run_test
```

This submits a job consisting of a set of workers.  There is a source job
which creates a random tuple.  Two transformation elements perform
multiplication and division on the tuple.  Sinks take the elements and
output them.

The service terminal should generate lots of output, and a set of numbers once
per second.

## Utilities

```
delete-job <job>
delete-worker <worker>
get-job <job>
get-jobs
get-worker <worker>
get-workers
```

## JSON interface

```
wget -q -O- --post-data='{
  "operation":"create-worker",
  "model":"python",
  "file":"sink.py",
  "job_id":"asd"
}' \
http://localhost:8080/
```

```
wget -q -O- --post-data='{
  "operation":"create-worker",
  "name": "source",
  "model":"python",
  "file":"source.py",
  "job_id":"asd",
  "outputs": {
      "o1": [ [ "one", "two" ], ["three", "four"] ]
  }
}' \
http://localhost:8080/
```

