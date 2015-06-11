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


class HealthCheck(base.Resource):
    def __repr__(self):
        return "<Cpulse %s>" % self._info


class HealthCheckManager(base.Manager):
    resource_class = HealthCheck

    @staticmethod
    def _path(id=None):
        return '/v1/cpulse/%s' % id if id else '/v1/cpulse'

    def list(self, marker=None, limit=None, sort_key=None,
             sort_dir=None, detail=False):
        return self._list(self._path(''), "cpulses")

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
