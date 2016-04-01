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

Then you can set gitzicht to use you newly created file, `input.log`. 

Using as CLI
-------------

Using in your code
-------------------

There are 5 main classes in 5 files that you can use:

    * logparser.py
    * commitparser.py
    * transformations.py
    * pivot.py
    * exporter.py

** LogParser: ** This one is used to read your log file, parse it, and return a list of all parsed commits there. Here is how to use it:

    from gitzicht import LogParser
    parser = LogParser('your-file-name.log')
    commits = parser.get_commits()

Sometimes, you may need to do you analysis based on the files edited in each commit. In that case, setting `per_file=True` in `get_commits()` means that for a commit with multiple files edited, it will be returned as if it is multiple commits, each with one of the edited files:

    commits = parser.get_commits(per_file=True)

** CommitParser: ** Most likely, you will not need to use this yourself. It is used by LogParser to parse each commit. Some thing for the ** Commits ** class, forget about it for now.

Running Tests
--------------

If you are willing to contribute to _gitzicht_ development, all tests are in the `/tests` folder. We use Python `unittest` here. 

To run all tests:

    python -m unittest discover

And to run a specific test:

    python -m unittest tests.test_logparser

