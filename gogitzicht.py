import sys 
import re

from argparse import ArgumentParser

from gitzicht import *

def parse_cli():

    '''
    argparser = ArgumentParser(description='Do you speak London? A library for Natural Language Identification.')
    argparser.add_argument('--version', action='store_true', help='Show version')
    argparser.add_argument('--list-langs', action='store_true', help='List supported languages in training data')
    argparser.add_argument('--unk', choices=['y','n'], default='n', help='Input text to classify')
    argparser.add_argument('--corpus', default='', help='Specify path to custom training-set')
    argparser.add_argument('--lang', help='Add training sample for the language specified')
    argparser.add_argument('input', nargs='*', help='Input text to classify')
    args = argparser.parse_args()
    '''

    argparser = ArgumentParser(description='Gogitzicht, git log analyzer')
    argparser.add_argument(
        '-d', '--debug', 
        action='store_true', 
        help='Print debug messages'
    )
    argparser.add_argument(
        '-i', '--input-file', 
        default='input.txt', 
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

    def dim_file_about(commit):
        filename = commit['files'][0].split('/')[-1]
        if re.findall('[Aa]uthor',filename):
            return 'Authorization'
        if re.findall('[Ee]ntity',filename):
            return 'Entity'
        if re.findall('[Mm]ember',filename):
            return 'Member'
        if re.findall('[Ss]earch',filename):
            return 'Search'
        if re.findall('[Gg]roup',filename):
            return 'Group'
        if re.findall('[Uu]ser',filename):
            return 'User'
        if re.findall('[Tt]emplate',filename):
            return 'Template'
        if re.findall('[Cc]ompetition',filename):
            return 'Competition'
        if re.findall('[Cc]omplete',filename):
            return 'Completion'
        if re.findall('[Cc]ontact',filename):
            return 'Contact'
        if re.findall('[Nn]otif',filename):
            return 'Notification'
        return 'Others'

    dim1 = getattr(Pivot, args.dim1)
    dim2 = getattr(Pivot, args.dim2)
    metric = getattr(Pivot, args.metric)
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
