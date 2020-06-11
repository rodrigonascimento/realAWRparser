#!/usr/bin/env python3

import argparse
import json
from os import path
from awr_file import AWRFile


def cli_args():
    ap = argparse.ArgumentParser(description='*** Oracle AWR text file parser ***')
    ap.add_argument('--metric-file', type=str, default='metrics.json', required=True,
                    help='JSON file with metrics to be parsed')
    ap.add_argument('--awr-file', nargs='+', dest='awr_files', required=True, help='List of AWR files to be parsed')
    return vars(ap.parse_args())


def get_awr_basedir(awr_file=None):
    basedir = path.dirname(path.abspath(awr_file))
    return basedir


def csv_header(awr=None):
    header = ''
    for metric in awr.load_profile:
        header += metric + ','

    for metric in awr.top10:
        header += metric + ','

    header += 'run,' + 'num_threads,' + 'filename'
    return header


def output_csv(output_fn=None):
    pass


def main():
    cmd_args = cli_args()
    try:
        with open(cmd_args['metric_file'], 'r') as fd_metrics:
            metrics = json.load(fd_metrics)
    except FileNotFoundError:
        print('Could not find file %s.' % cmd_args['metric_file'])

    header = False
    for awr_file in cmd_args['awr_files']:
        csv_filename = path.abspath(awr_file).split('/')[len(path.abspath(awr_file).split('/'))-2] + '.csv'
        awr = AWRFile(file_name=awr_file, perf_metrics=metrics)
        awr.read_file()
        p = awr.parse_to_csv()
        with open(csv_filename, 'a') as outf:
            if not header:
                outf.write(csv_header(awr=awr) + '\n')
                header = True
            outf.write(p + '\n')


if __name__ == '__main__':
    main()
