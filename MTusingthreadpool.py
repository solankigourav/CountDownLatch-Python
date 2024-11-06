import time,boto3,mysql.connector
from concurrent.futures import ThreadPoolExecutor,as_completed
from botocore.exceptions import BotoCoreError, ClientError
from mysql.connector import Error as MySQLError

# Initialize SQS client
sqs_client = boto3.client('sqs', region_name='us-east-2')
queue_url = "https://sqs.us-east-2.amazonaws.com/337225672478/GouravSQS"

# Configure MySQL connection
db_config = {
    'user': 'root',
    'password': '2000',
    'host': 'localhost',
    'database': 'example_db'
}


def connect_to_mysql():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        return connection, cursor
    except MySQLError as e:
        print(f"Error connecting to MySQL: {e}")



def process_message(message, cursor, connection):
    #Process a single SQS message and insert it into MySQL
    try:
        # Extract message body
        body = message['Body']

        # Insert data into MySQL database
        query = "INSERT INTO messages (message_body) VALUES (%s)"
        cursor.execute(query, (body,))
        connection.commit()

        # Print message for debugging or logging purpose
        print(f"Processed message: {body}")

        # Delete message from  queue
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )

    except MySQLError as e:
        print(f"Error processing message in MySQL: {e}")
    except BotoCoreError as e:
        print(f"Error with SQS operation: {e}")
    except ClientError as e:
        print(f"Error with SQS client: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    connection, cursor = connect_to_mysql()

    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                try:
                    #receive message from sqs
                    response = sqs_client.receive_message(
                        QueueUrl=queue_url,
                        MaxNumberOfMessages=10,
                        WaitTimeSeconds=2
                    )

                    messages = response.get('Messages', [])

                    if messages:
                        futures = [executor.submit(process_message, message, cursor, connection) for message in
                                   messages]
                        try:
                            future.result()  # Retrieve result
                        except Exception as e:
                            print(f"An error occurred during message processing: {e}")
                    else:
                         print("No messages received")

                except (BotoCoreError, ClientError) as e:
                    print(f"Error receiving messages from SQS: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred during polling: {e}")

                time.sleep(5)


    finally:
        # Close MySQL connection and cursor
        cursor.close()
        connection.close()
        print("MySQL connection closed.")


if __name__ == "__main__":
    main()