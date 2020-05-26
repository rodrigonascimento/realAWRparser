#!/usr/bin/env python3


class AWRFile:
    def __init__(self, file_name=None, perf_metrics=None):
        self.file_name = file_name
        self.load_profile = {}
        self.top10 = {}
        self.content = []
        self.perf_metrics = perf_metrics

    def read_file(self):
        try:
            with open(self.file_name, 'r') as fd_awr:
                awr_content = fd_awr.read().splitlines()

            for line in awr_content:
                self.content.append(line.strip())
        except FileNotFoundError:
            print('Could not open file %s ' % self.file_name)

    def _get_section_offset(self, section_header=None):
        for line in self.content:
            if line[:len(section_header)] == section_header:
                return self.content.index(line)

    def parse_load_profile(self):
        pos = self._get_section_offset(section_header='Load Profile')
        if pos is None:
            return None

        for pm in self.perf_metrics['Load Profile']:
            line = pos
            while line < len(self.content):
                if self.content[line][:len(pm)] == pm:
                    awr_line = self.content[line].split(':')
                    raw_metric = awr_line[1].split()[0]
                    if ',' in raw_metric:
                        metric_v = float(raw_metric.replace(',', ''))
                    else:
                        metric_v = float(raw_metric)
                    self.load_profile[awr_line[0]] = metric_v
                    break
                else:
                    line += 1

    def parse_top_foreground(self):
        pos = self._get_section_offset(section_header='Top 10 Foreground Events')
        if pos is None:
            return None

        for pm in self.perf_metrics['Top 10 Foreground Events']:
            line = pos
            while line < len(self.content):
                if self.content[line][:len(pm)] == pm:
                    awr_line = self.content[line].split()
                    raw_metric_v = awr_line[len(pm.split()) + 2]

                    if raw_metric_v[-2:] == 'ms':
                        metric_v = float(raw_metric_v[:-2]) * 1000
                    elif raw_metric_v[-2:] == 'us':
                        metric_v = float(raw_metric_v[:-2])

                    self.top10[pm] = metric_v
                    break
                else:
                    line += 1