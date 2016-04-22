import sys 
import re

from gitzicht import *


def main(args):

    input_filename = args.input_file
    output_filename = args.output_file

    parser = LogParser(input_filename)
    
    if args.debug:
        parser.print_debug_message()

    commits = parser.get_commits(per_file=args.per_file)

    dim1 = getattr(Pivot, args.dim1)
    dim2 = getattr(Pivot, args.dim2)
    metric = getattr(Pivot, args.metric)

    if args.debug:
        print 'Pivoting on {}, {} using {}'.format(dim1, dim2, metric)

    pivot = Pivot(dim1, dim2, metric)
    
    pivoted = pivot.calculate(commits)

    exporter = Exporter(pivoted)
    exporter.to_csv(output_filename,'date')

if __name__ == '__main__':

    args = parse_cli()
    main(args)
