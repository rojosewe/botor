"""
.. module: botor.decorators
    :platform: Unix
    :copyright: (c) 2015 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
.. moduleauthor:: Patrick Kelley <patrick@netflix.com>
.. moduleauthor:: Mike Grima <mgrima@netflix.com>
"""
import functools
from itertools import product
from botor.aws.sts import boto3_cached_conn

from botor import Botor


def iter_account_region(service, service_type='client', accounts=None, regions=None, assume_role=None, session_name='botor', conn_type='botor'):
    def decorator(func):
        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            threads = []
            for account, region in product(accounts, regions):
                conn_dict = {
                    'tech': service,
                    'account_number': account,
                    'region': region,
                    'session_name': session_name,
                    'assume_role': assume_role,
                    'service_type': service_type
                }
                if conn_type == 'botor':
                    kwargs['botor'] = Botor(**conn_dict)
                elif conn_type == 'dict':
                    kwargs['conn_dict'] = conn_dict
                elif conn_type == 'boto3':
                    del conn_dict['tech']
                    kwargs['conn'] = boto3_cached_conn(service, **conn_dict)
                result = func(*args, **kwargs)
                if result:
                    threads.append(result)

            result = []
            for thread in threads:
                result.append(thread)
            return result
        return decorated_function
    return decorator
