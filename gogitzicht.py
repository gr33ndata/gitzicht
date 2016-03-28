import sys 
import re

from argparse import ArgumentParser

from gitzicht import *

def parse_cli():

    argparser = ArgumentParser(description='Gogitzicht, git log analyzer')
    argparser.add_argument(
        '-v', '--version', 
        action='version', 
        version='{}, version {}'.format(NAME, VERSION)
    )
    argparser.add_argument(
        '-d', '--debug', 
        action='store_true', 
        help='Print debug messages'
    )
    argparser.add_argument(
        '-i', '--input-file', 
        default='input.log', 
        help='Input file for git logs'
    )
    argparser.add_argument(
        '-o', '--output-file', 
        default='output.csv', 
        help='Output file for git logs'
    )

    pivot_argparser = argparser.add_argument_group('Pivot')
    pivot_argparser.add_argument(
        '-p', '--pivot', 
        action='store_true', 
        help='Pivot on 2 dimensions using metric'
    )
    pivot_argparser.add_argument(
        '--dim1', 
        choices=Pivot.list_dims(), 
        default='_dim1', 
        help='Set pivot\'s First dimension'
    )
    pivot_argparser.add_argument(
        '--dim2', 
        choices=Pivot.list_dims(), 
        default='_dim2', 
        help='Set pivot\'s second dimension'
    )
    pivot_argparser.add_argument(
        '--metric', 
        choices=Pivot.list_metrics(), 
        default='_metric', 
        help='Set pivot\'s metric'
    )

    return argparser.parse_args()

def main(args):

    input_filename = args.input_file
    output_filename = args.output_file

    parser = LogParser(input_filename)
    
    if args.debug:
        parser.print_debug_message()

    commits = parser.get_commits(per_file=True)

    dim1 = getattr(Pivot, args.dim1)
    dim2 = getattr(Pivot, args.dim2)
    metric = getattr(Pivot, args.metric)
    if args.debug:
        print 'Pivoting on {}, {} using {}'.format(dim1, dim2, metric)
    pivot = Pivot(dim1, dim2, metric)
    
    #pivot = Pivot(dim_file_about, Pivot.dim_year_month, Pivot.metric_changes)
    pivoted = pivot.calculate(commits)

    #pivoted = Transformations.dim1_filter_regex(pivoted, regex='.*\.java')
    #pivoted = Transformations.dim2_filter_regex(pivoted, regex='201[456].*')
    #pivoted = Transformations.dim1_top_n(pivoted, n=10)

    exporter = Exporter(pivoted)
    exporter.to_csv(output_filename,'date')

if __name__ == '__main__':

    args = parse_cli()
    main(args)
