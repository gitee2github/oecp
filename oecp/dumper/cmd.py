# -*- encoding=utf-8 -*-
"""
# **********************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2021-2021. All rights reserved.
# [oecp] is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v1.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# **********************************************************************************
"""


import os
import logging
logger = logging.getLogger('oecp')

from oecp.dumper.base import AbstractDumper

class CmdDumper(AbstractDumper):
    def __init__(self, repository, cache=None, config=None):
        super(CmdDumper, self).__init__(repository, cache, config)
        cache_require_key = 'extract'
        self.cache_dumper = self.get_cache_dumper(cache_require_key)
        self.extract_info = self.cache_dumper.get_extract_info()
        self._component_key = 'cmd'

    def _get_cmd_files(self, rpm_extract_dir):
        cmd_files = self.cache_dumper.get_cmd_files(rpm_extract_dir)
        return cmd_files

    def dump(self, repository):
        rpm_path = repository['path']
        category = repository['category'].value
        verbose_path = os.path.basename(rpm_path)
        rpm_extract_dir = self.extract_info.get(verbose_path)
        rpm_extract_name = rpm_extract_dir.name
        if not rpm_extract_name:
            logger.exception('RPM decompression path not found')
            raise
        cmd_files = self._get_cmd_files(rpm_extract_name)
        item = {'rpm': verbose_path, 'category': category, 'kind': self._component_key, 'data': cmd_files}
        return item

    def run(self):
        dumper_list = []
        for _, repository in self.repository.items():
            dumper = self.dump(repository)
            dumper_list.append(dumper)
        return dumper_list
