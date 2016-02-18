# bobo
A thin wrapper around boto3

## features

 - intelligent connection caching.
 - rate limit handling, with exponential backoff.
 - multi-account sts:assumerole abstraction.

## Example

    from bobo.aws.sqs import get_queue, get_messages
    queue = get_queue(queue_name='MyQueue', account_number='111111111111', assume_role='MyRole', region='us-east-1')
    messages = get_messages(queue=queue)