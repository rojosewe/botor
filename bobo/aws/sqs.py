"""
.. module: bobo.aws.sqs
    :platform: Unix
    :copyright: (c) 2015 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>
.. moduleauthor:: Patrick Kelley <patrick@netflix.com>
"""

from bobo.aws.sts import sts_conn


@sts_conn('sqs', service_type='resource')
def get_queue(**kwargs):
    return kwargs.pop('resource').get_queue_by_name(QueueName=kwargs.pop('queue_name'))


def get_messages(**kwargs):
    return kwargs.pop('queue').receive_messages(**kwargs)
