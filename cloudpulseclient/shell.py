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


###
# This code is taken from python-novaclient. Goal is minimal modification.
###

"""
Command-line interface to the OpenStack Cloudpulse API.
"""

from __future__ import print_function
import logging
import sys

from oslo_utils import encodeutils
import six


logger = logging.getLogger(__name__)


def main():
    try:
        # NOTE : To implement cloudpulse client
        logger.debug("Calling cloudpulseclient")
    except Exception as e:
        logger.debug(e, exc_info=1)
        print("ERROR: %s" % encodeutils.safe_encode(six.text_type(e)),
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
