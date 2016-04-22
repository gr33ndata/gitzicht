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

Basically, you can:

    python gogitzicht.py -i input.log -o output.csv

This uses the default pivots to analyze logs in `input.log` and dump output CSV data into `output.csv`. Omitting output parameter dumps data to your screen. Additionally, you can omit input parameter and use CLI pipe to get log from `git log --numstat --no-merges` into `gogitzicht.py` right away. 

Using in your code
-------------------

There are 5 main classes in 5 files that you can use:

    * logparser.py
    * commitparser.py
    * transformations.py
    * pivot.py
    * exporter.py

**LogParser:** This one is used to read your log file, parse it, and return a list of all parsed commits there. Here is how to use it:

    from gitzicht import LogParser
    parser = LogParser('your-file-name.log')
    commits = parser.get_commits()

Sometimes, you may need to do you analysis based on the files edited in each commit. In that case, setting `per_file=True` in `get_commits()` means that for a commit with multiple files edited, it will be returned as if it is multiple commits, each with one of the edited files:

    commits = parser.get_commits(per_file=True)


**CommitParser:** Most likely, you will not need to use this yourself. It is used by LogParser to parse each commit. Some thing for the *Commits* class, forget about it for now.

**Pivot:** Here comes the fun part. This class allows you to transform the list of commits into matrix. Rows and columns are to be called dimensions, and values inside cells are to be called metrics here. The pivoting works as follows:

    pivot = Pivot(dim1, dim2, metric)
    pivoted = pivot.calculate(commits)

You first initialize the Pivot class by passing 3 functions (callback functions) to it. One to extract values to be put in the first dimension. One of extracting values for the second dimension. The third callback function is for extracting values to be put in cells. All 3 functions are called with the commit being processed passed to them. Then you apply its `calculate()` method, passing to it the list of parsed commits you got from `parser.get_commits()`.  

Maybe an example is needed to make things clears. Say, you want to list number of commits by years, and month. You will have years as one dimension, month is the second dimension, and the total number of commits during that period as values for their intersections. 

First, we define our callback functions:

    def extract_year(commit): 
        return str(commit['date'].year)

    def extract_month(commit): 
        return str(commit['date'].month)

    def just_return_one_for_each_commit(commit):
        return 1

Then we initialize the pivot with the callback function:

    pivot = Pivot(extract_year, extract_month, just_return_one_for_each_commit)

Finally, we apply the pivot to get the pivoted data in the form of a [Pandas](http://pandas.pydata.org/) DataFrame:

    pivot.calculate(commits)

To have your output as a Python list of lists:
    
    pivot.calculate(commits, as_dataframe=False):

Gitzicht comes with some predefined callback functions that you can use. They are defined as class methods of the Pivot class. To list available callback functions for extracting dimensions use `Pivot.list_dims()`, and for available metrics use `Pivot.list_metrics()`.

**Transformations:** Currently, the only transformations you can apply on the matrices produced by the _Pivot_ is to filter out some dimensions based on regular expressions.

Running Tests
--------------

If you are willing to contribute to _gitzicht_ development, all tests are in the `/tests` folder. We use Python `unittest` here. 

To run all tests:

    python -m unittest discover

And to run a specific test:

    python -m unittest tests.test_logparser


Contacts
--------
 
+ Name: [Tarek Amr](http://tarekamr.appspot.com/)
+ Twitter: [@gr33ndata](https://twitter.com/gr33ndata)
