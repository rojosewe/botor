"""
.. module: bobo.exceptions
    :platform: Unix
    :copyright: (c) 2015 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
.. moduleauthor:: Patrick Kelley <patrick@netflix.com>
"""
import functools
import botocore
import time
import boto


def rate_limited(max_attempts=None, max_delay=4):
    def decorator(f):
        metadata = {
            'count': 0,
            'delay': 0
        }

        @functools.wraps(f)
        def decorated_function(*args, **kwargs):

            def increase_delay(e):
                if metadata['delay'] == 0:
                    metadata['delay'] = 1
                elif metadata['delay'] < max_delay:
                    metadata['delay'] *= 2

                if max_attempts and metadata['count'] > max_attempts:
                    raise e

            metadata['count'] = 0
            while True:
                metadata['count'] += 1
                if metadata['delay'] > 0:
                    time.sleep(metadata['delay'])
                try:
                    retval = f(*args, **kwargs)
                    metadata['delay'] = 0
                    return retval
                except botocore.exceptions.ClientError as e:
                    if not e.response["Error"]["Code"] == "Throttling":
                        raise e
                    increase_delay(e)
                except boto.exception.BotoServerError as e:
                    if not e.error_code == 'Throttling':
                        raise e
                    increase_delay(e)

        return decorated_function
    return decorator























# def handle_aws_rate_limiting(func):
#     metadata = {
#         'count': 0,
#         'delay': 0
#     }
#
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         metadata['count'] = 0
#         while True:
#             metadata['count'] += 1
#             if metadata['delay'] > 0:
#                 time.sleep(metadata['delay'])
#
#             try:
#                 retval = func(*args, **kwargs)
#                 if metadata['delay'] > 0:
#                     # app.logger.warn("No longer being rate-limited {} -> {}".format(metadata['delay'], metadata['delay']/2))
#                     metadata['delay'] /= 2
#                 return retval
#             except botocore.exceptions.ClientError as e:
#                 if 'Throttling' in e.message:
#                     if metadata['delay'] == 0:
#                         metadata['delay'] = 1
#                         # app.logger.warn('Being rate-limited by AWS. Increasing delay from 0 to 1 second. Attempt {}'.format(metadata['count']))
#                     elif metadata['delay']< 16:
#                         metadata['delay'] *= 2
#                         # app.logger.warn('Still being rate-limited by AWS. Increasing delay to {} seconds. Attempt {}'.format(metadata['delay'], metadata['count']))
#                     else:
#                         raise e
#                 else:
#                     raise e
#             except boto.exception.BotoServerError as e:
#                 if  u'Rate exceeded' in e.message:
#                     if metadata['delay'] == 0:
#                         metadata['delay'] = 1
#                         # app.logger.warn('Being rate-limited by AWS. Increasing delay from 0 to 1 second. Attempt {}'.format(metadata['count']))
#                     else:
#                         metadata['delay'] *= 2
#                         # app.logger.warn('Still being rate-limited by AWS. Increasing delay to {} seconds. Attempt {}'.format(metadata['delay'], metadata['count']))
#                 else:
#                     raise e
#     return inner