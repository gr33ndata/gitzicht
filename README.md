Gitzicht
=========

Analyze and summarize your git commits history
----------------------------------------------

This is both python library and command line tool. 

You can either import gitzicht library into your own code:

    import gitzicht

Or run the CLI tool, `gogitzicht.py` as follows:

    python gogitzicht.py --help


P.S. Still under development

Exporting git logs
-------------------

This library works on analyzing git logs. We use the following format:

    git log --numstat --no-merges > input.log

Then you can set gitzicht to use `input.log`. 

Running Tests
--------------

If you are willing to contribute in developing _gitzicht_, all tests are in the tests folder. We use Python `unittest` here. 

To run all tests:

    python -m unittest discover

To run specific test:

    python -m unittest tests.test_logparser

