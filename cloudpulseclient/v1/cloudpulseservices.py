# Copyright 2014
# Cisco, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cloudpulseclient.common import base
import six
from six.moves.urllib import parse


class HealthCheckTest(base.Resource):

    def __repr__(self):
        return str(self._info)


class HealthCheck(base.Resource):

    def __repr__(self):
        return "<Cpulse %s>" % self._info


class HealthCheckManager(base.Manager):
    resource_class = HealthCheck

    @staticmethod
    def _path(id=None):
        return '/v1/cpulse/%s' % id if id else '/v1/cpulse'

    def list(self, search_opts=None, marker=None, limit=None,
             sort_key=None, sort_dir=None, detail=False):
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in six.iteritems(search_opts):
            if val:
                if isinstance(val, six.text_type):
                    val = val.encode('utf-8')
                qparams[opt] = val
        if qparams:
            items = list(qparams.items())
            new_qparams = sorted(items, key=lambda x: x[0])
            query_string = "?%s" % parse.urlencode(new_qparams)
        else:
            query_string = ""
        return self._list("%s%s" % (self._path(''), query_string), "cpulses")

    def create(self, **kwargs):
        new = {}
        for (key, value) in kwargs.items():
            new[key] = value
        return self._create(self._path(), new)

    def delete(self, id):
        return self._delete(self._path(id))

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None

    def get_test_list(self):
        return self._list(self._path('list_tests'), obj_class=HealthCheckTest)
