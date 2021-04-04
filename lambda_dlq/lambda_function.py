import boto3

lamb = boto3.client('lambda')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='Events_DLQ')


def handler(event, context):
    for _ in range(100):
        messages_to_delete = []
        for message in queue.receive_messages(MaxNumberOfMessages=10):
            payload_bytes_array = bytes(message.body, encoding='utf8')
            # print(payload_bytes_array)
            lamb.invoke(
                FunctionName='ETL_job_func',
                InvocationType="Event",  # Event = Invoke the function asynchronously.
                Payload=payload_bytes_array
            )

            # Add message to delete
            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

        # If you don't receive any notifications the messages_to_delete list will be empty
        if len(messages_to_delete) == 0:
            break
        # Delete messages to remove them from SQS queue handle any errors
        else:
            deleted = queue.delete_messages(Entries=messages_to_delete)
            print(deleted)