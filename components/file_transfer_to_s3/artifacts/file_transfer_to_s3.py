import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3


class MyHandler(FileSystemEventHandler):
    def process(self, event):
        file_path = event.src_path
        print(f"Detected event_type: {event.event_type}")
        # Only process file created events
        if event.event_type == 'created' and os.path.isfile(file_path):
            print(f"Detected new file: {file_path}")

            s3 = boto3.client('s3')
            bucket_name = os.environ.get("uploadBucketName")
            file_name = os.path.basename(file_path)
            folder_name = "inbox"
            key = f'{folder_name}/{file_name}'

            # Upload the file to S3
            try:
                with open(file_path, 'rb') as data:
                    s3.upload_fileobj(data, bucket_name, key, ExtraArgs={
                                      'ContentType': 'application/pdf'})
                print(f"Uploaded {file_name} to {bucket_name}/{key}")

                # Delete the local file
                os.remove(file_path)
                print(f"Deleted local file: {file_path}")
            except Exception as e:
                print(f"Error occurred: {e}")

    def on_created(self, event):
        self.process(event)


message = "Path: %s!" % sys.argv[1]
print(message)
path = sys.argv[1]
observer = Observer()
observer.schedule(MyHandler(), path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()

# if __name__ == "__main__":
# main()
