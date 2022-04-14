# -*- encoding=utf-8 -*-
"""
# **********************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.
# [oecp] is licensed under the Mulan PSL v1.
# You can use this software according to the terms and conditions of the Mulan PSL v1.
# You may obtain a copy of Mulan PSL v1 at:
#     http://license.coscl.org.cn/MulanPSL
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v1 for more details.
# **********************************************************************************
"""
import os
import re
from abc import ABC, abstractmethod
from oecp.result.compare_result import CMP_RESULT_MORE, CMP_RESULT_LESS, CMP_RESULT_SAME, CMP_RESULT_DIFF, \
    CMP_RESULT_CHANGE

# 两者category指定的级别不同或者未指定

CPM_CATEGORY_DIFF = 4


class CompareExecutor(ABC):

    def __init__(self, dump_a, dump_b, config):
        self.dump_a = dump_a
        self.dump_b = dump_b
        self.config = config

    @staticmethod
    def format_dump(data_a, data_b):
        dump_set_a, dump_set_b = set(data_a), set(data_b)
        common_dump = dump_set_a & dump_set_b
        only_dump_a = dump_set_a - dump_set_b
        only_dump_b = dump_set_b - dump_set_a
        change_dump = []
        for side_a_file in list(only_dump_a):
            for side_b_file in list(only_dump_b):
                if os.path.basename(side_a_file) == os.path.basename(side_b_file):
                    side_a_floders = side_a_file.split('/')
                    side_b_floders = side_b_file.split('/')
                    if len(side_a_floders) > 1 and len(side_b_floders) == len(side_a_floders):
                        diff = list(set(side_a_floders).difference(set(side_b_floders)))
                        if len(diff) == 1 and re.search('\d+', diff[0]):
                            change_dump.append([side_a_file, side_b_file])
                            only_dump_a.discard(side_a_file)
                            only_dump_b.discard(side_b_file)

        all_dump = [
            [[x, x, CMP_RESULT_SAME] for x in common_dump],
            [[x[0], x[1], CMP_RESULT_CHANGE] for x in change_dump],
            [[x, '', CMP_RESULT_LESS] for x in only_dump_a],
            [['', x, CMP_RESULT_MORE] for x in only_dump_b]
        ]
        return all_dump

    @staticmethod
    def split_common_files(files_a, files_b):
        common_file_pairs = []
        for file_a in files_a:
            for file_b in files_b:
                if file_a.split('__rpm__')[-1] == file_b.split('__rpm__')[-1]:
                    common_file_pairs.append([file_a, file_b])
        return common_file_pairs

    @staticmethod
    def format_dump_kv(data_a, data_b, kind):
        list_a = list(data_a)
        list_b = list(data_b)
        h_a = {}
        h_b = {}
        same = []
        diff = []
        less = []
        all_dump = []

        for a in list_a:
            t = a.split(" = ")
            h_a[t[0]] = t[0] + " " + t[1]

        for b in list_b:
            t = b.split(" = ")
            h_b[t[0]] = t[0] + " " + t[1]

        for k, va in h_a.items():
            vb = h_b.get(k, None)
            if vb == None:
                less.append([va, '', 'less'])
            elif va == vb:
                same.append([va, vb, 'same'])
            else:
                diff.append([va, vb, 'diff'])

        all_dump.append(same)
        all_dump.append(diff)
        all_dump.append(less)

        if kind == 'kconfig':
            more = []
            for k, vb, in h_b.items():
                va = h_a.get(k, None)
                if va == None:
                    more.append(['', vb, 'more'])

            if more:
                all_dump.append(more)

        return all_dump

    @staticmethod
    def format_service_detail(data_a, data_b):
        same = []
        changed = []
        losted = []
        all_dump = []
        file_result = CMP_RESULT_SAME
        for k, va in data_a.items():
            vb = data_b.get(k, None)
            if vb == None:
                losted.append([' '.join([k, "=", va]), '', 'losted'])
            elif va == vb:
                same.append([' '.join([k, "=", va]), ' '.join([k, "=", vb]), 'same'])
            else:
                changed.append([' '.join([k, "=", va]), ' '.join([k, "=", vb]), 'changed'])
        all_dump.append(same)
        all_dump.append(changed)
        all_dump.append(losted)
        if changed or losted:
            file_result = CMP_RESULT_DIFF
        return file_result, all_dump

    @abstractmethod
    def run(self):
        pass
