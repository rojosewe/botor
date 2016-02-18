"""
.. module: bobo.aws.sts
    :platform: Unix
    :copyright: (c) 2015 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
.. moduleauthor:: Patrick Kelley <patrick@netflix.com>
"""
from functools import wraps
import boto3


def _client(service, region, role):
    return boto3.client(
        service,
        region_name=region,
        aws_access_key_id=role['Credentials']['AccessKeyId'],
        aws_secret_access_key=role['Credentials']['SecretAccessKey'],
        aws_session_token=role['Credentials']['SessionToken']
    )


def _resource(service, region, role):
    return boto3.resource(
        service,
        region_name=region,
        aws_access_key_id=role['Credentials']['AccessKeyId'],
        aws_secret_access_key=role['Credentials']['SecretAccessKey'],
        aws_session_token=role['Credentials']['SessionToken']
    )


def sts_conn(service, service_type='client'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            sts = boto3.client('sts')
            arn = 'arn:aws:iam::{0}:role/{1}'.format(
                kwargs.pop('account_number'),
                kwargs.pop('assume_role')
            )
            role = sts.assume_role(RoleArn=arn, RoleSessionName=kwargs.pop('session_name', 'bobo'))

            if service_type == 'client':
                kwargs[service_type] = _client(service, kwargs.pop('region'), role)
            elif service_type == 'resource':
                kwargs[service_type] = _resource(service, kwargs.pop('region'), role)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
