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

from cloudpulseclient import exceptions
from cloudpulseclient.openstack.common import cliutils as utils


def _print_list_field(field):
    return lambda obj: ', '.join(getattr(obj, field))


@utils.arg('--failed',
           dest='failed',
           action="store_true",
           default=False,
           help='Display only test results that have failed.')
@utils.arg('--period',
           metavar='<period>',
           help='List tests results that have been run in the last x minutes.')
def do_result(cs, args):
    """List all the test results"""
    search_opts = {
        'failed': args.failed,
        'period': args.period,
    }
    healtchecks = cs.healthcheck.list(search_opts=search_opts)
    columns = ('uuid', 'id', 'name', 'testtype', 'state')
    utils.print_list(healtchecks, columns,
                     {'versions': _print_list_field('versions')},
                     sortby_index=1)


@utils.arg('--name',
           metavar='<name>',
           help='Name of the test to run')
@utils.arg('--all-tests',
           metavar='<all_tests>',
           action='store_const',
           const='all_tests',
           help="Run all tests")
@utils.arg('--all-endpoint-tests',
           metavar='<all_endpoint_tests>',
           action='store_const',
           const='all_endpoint_tests',
           help="Run all endpoint tests")
@utils.arg('--all-operator-tests',
           metavar='<all_operator_tests>',
           action='store_const',
           const='all_operator_tests',
           help="Run all operator tests")
def do_run(cs, args):
    """Run a new manual test"""
    if not any([args.name, args.all_operator_tests,
                args.all_tests, args.all_endpoint_tests]):
        raise exceptions.CommandError(
            ("Usage: cloudpulse --name <testname>."
             "See 'cloudpulse help run' for details"))
    opts = {}
    opts['name'] = args.name or args.all_operator_tests or \
        args.all_tests or args.all_endpoint_tests
    healtcheck = cs.healthcheck.create(**opts)
    utils.print_dict(healtcheck._info)


@utils.arg('cpulse',
           metavar='<cpulse>',
           nargs='+',
           help='Id of the test result to show.')
def do_show(cs, args):
    """Show the detailed result of a test"""
    for id in args.cpulse:
        healthcheck = cs.healthcheck.get(id)
        utils.print_dict(healthcheck._info)


def do_test_list(cs, args):
    """Show a list of scenarios and tests in each scenario"""
    healthcheck = cs.healthcheck.get_test_list()
    utils.print_dict(
        healthcheck[0]._info, dict_property="Scenarios", dict_value="Tests")


@utils.arg('cpulse',
           metavar='<cpulse>',
           nargs='+',
           help='Id of the test result to delete.')
def do_delete(cs, args):
    """Delete the test result"""
    for id in args.cpulse:
        try:
            cs.healthcheck.delete(id)
        except Exception as e:
            print("Delete for cpulse %(cpulse)s failed: %(e)s" %
                  {'cpulse': id, 'e': e})
