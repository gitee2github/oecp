# -*- encoding=utf-8 -*-
"""
# **********************************************************************************
# Copyright (c) Huawei Technologies Co., Ltd. 2020-2020. All rights reserved.
# [oecp] is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# **********************************************************************************
"""

from oecp.executor.base import CompareExecutor


class NullExecutor(CompareExecutor):

    def __init__(self, base_dump, other_dump, config=None):
        super(NullExecutor, self).__init__(base_dump, other_dump, config)
        if hasattr(base_dump, 'run') and hasattr(other_dump, 'run'):
            base_dump.run()
            other_dump.run()

    def run(self):
        return []
