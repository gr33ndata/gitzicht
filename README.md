GitZicht (Analyze and summarize your git commits history)
==========================================================

Exporting git logs
-------------------

This library works on analyzing git logs. We use the following format:

    git log --numstat --no-merges > input.log

Then you can set gitzicht to use `input.log`. 

Running Tests
--------------

We use Python `unittest` here. To run all tests:

    python -m unittest discover

To run specific test:

    python -m unittest tests.test_logparser

