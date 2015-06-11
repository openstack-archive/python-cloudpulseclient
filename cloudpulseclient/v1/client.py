# Copyright 2014
# The Cloudscaling Group, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from keystoneclient.v2_0 import client as keystone_client_v2
from keystoneclient.v3 import client as keystone_client_v3

from cloudpulseclient.common import httpclient
from cloudpulseclient.v1 import cloudpulseservices as healthcheck


class Client(object):
    def __init__(self, username=None, api_key=None, project_id=None,
                 project_name=None, auth_url=None, cloudpulse_url=None,
                 endpoint_type='publicURL', service_type='container',
                 region_name=None, input_auth_token=None):

        keystone = None
        if not input_auth_token:
            keystone = self.get_keystone_client(username=username,
                                                api_key=api_key,
                                                auth_url=auth_url,
                                                project_id=project_id,
                                                project_name=project_name)
            input_auth_token = keystone.auth_token
        if not input_auth_token:
            raise RuntimeError("Not Authorized")

        if not cloudpulse_url:
            keystone = keystone or self.get_keystone_client(
                username=username,
                api_key=api_key,
                auth_url=auth_url,
                token=input_auth_token,
                project_id=project_id,
                project_name=project_name)
            cloudpulse_url = keystone.service_catalog.url_for(
                service_type=service_type,
                endpoint_type=endpoint_type,
                region_name=region_name)

        http_cli_kwargs = {
            'token': input_auth_token,
            # TODO(yuanying): - use insecure
            # 'insecure': kwargs.get('insecure'),
            # TODO(yuanying): - use timeout
            # 'timeout': kwargs.get('timeout'),
            # TODO(yuanying): - use ca_file
            # 'ca_file': kwargs.get('ca_file'),
            # TODO(yuanying): - use cert_file
            # 'cert_file': kwargs.get('cert_file'),
            # TODO(yuanying): - use key_file
            # 'key_file': kwargs.get('key_file'),
            'auth_ref': None,
        }
        self.http_client = httpclient.HTTPClient(cloudpulse_url,
                                                 **http_cli_kwargs)
        self.healthcheck = healthcheck.HealthCheckManager(self.http_client)

    @staticmethod
    def get_keystone_client(username=None, api_key=None, auth_url=None,
                            token=None, project_id=None, project_name=None):
        if not auth_url:
                raise RuntimeError("No auth url specified")
        imported_client = (keystone_client_v2 if "v2.0" in auth_url
                           else keystone_client_v3)

        client = imported_client.Client(
            username=username,
            password=api_key,
            token=token,
            tenant_id=project_id,
            tenant_name=project_name,
            auth_url=auth_url,
            endpoint=auth_url)
        client.authenticate()

        return client
