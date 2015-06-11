# -*- coding: utf-8 -*-
#
# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from cloudpulseclient.openstack.common._i18n import _
from cloudpulseclient.openstack.common.apiclient import exceptions as exc


def common_filters(marker=None, limit=None, sort_key=None, sort_dir=None):
    """Generate common filters for any list request.

    :param marker: entity ID from which to start returning entities.
    :param limit: maximum number of entities to return.
    :param sort_key: field to use for sorting.
    :param sort_dir: direction of sorting: 'asc' or 'desc'.
    :returns: list of string filters.
    """
    filters = []
    if isinstance(limit, int) and limit > 0:
        filters.append('limit=%s' % limit)
    if marker is not None:
        filters.append('marker=%s' % marker)
    if sort_key is not None:
        filters.append('sort_key=%s' % sort_key)
    if sort_dir is not None:
        filters.append('sort_dir=%s' % sort_dir)
    return filters


def split_and_deserialize(string):
    """Split and try to JSON deserialize a string.

    Gets a string with the KEY=VALUE format, split it (using '=' as the
    separator) and try to JSON deserialize the VALUE.
    :returns: A tuple of (key, value).
    """
    try:
        key, value = string.split("=", 1)
    except ValueError:
        raise exc.CommandError(_('Attributes must be a list of '
                                 'PATH=VALUE not "%s"') % string)
    try:
        value = json.loads(value)
    except ValueError:
        pass

    return (key, value)


def args_array_to_patch(op, attributes):
    patch = []
    for attr in attributes:
        # Sanitize
        if not attr.startswith('/'):
            attr = '/' + attr
        if op in ['add', 'replace']:
            path, value = split_and_deserialize(attr)
            patch.append({'op': op, 'path': path, 'value': value})

        elif op == "remove":
            # For remove only the key is needed
            patch.append({'op': op, 'path': attr})
        else:
            raise exc.CommandError(_('Unknown PATCH operation: %s') % op)
    return patch
