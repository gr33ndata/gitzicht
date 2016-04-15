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
    

    parse_argparser = argparser.add_argument_group('Parser')
    parse_argparser.add_argument(
        '-i', '--input-file', 
        default='input.log', 
        help='Input file for git logs'
    )
    parse_argparser.add_argument(
        '-o', '--output-file', 
        default='output.csv', 
        help='Output file for git logs'
    )
    parse_argparser.add_argument(
        '--per-file', 
        default=True, 
        action='store_true', 
        help='Convert commits with multiple file changes into multiple commits.'
    )

    pivot_argparser = argparser.add_argument_group('Pivot')
    pivot_argparser.add_argument(
        '-p', '--pivot', 
        default=True, 
        action='store_true', 
        help='Pivot on 2 dimensions using metric [default: True]'
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
