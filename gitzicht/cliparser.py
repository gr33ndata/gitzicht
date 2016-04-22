from argparse import ArgumentParser

from gitzicht import NAME, VERSION
from gitzicht import Pivot

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
        default='STDIN', 
        help='Input file for git logs'
    )
    parse_argparser.add_argument(
        '-o', '--output-file', 
        default='STDOUT', 
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