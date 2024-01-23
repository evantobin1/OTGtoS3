import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from greengrasssdk import IPCClient


class MyHandler(FileSystemEventHandler):
    def process(self, event):
        file_path = event.src_path
        print(f"Detected event_type: {event.event_type}")
        # Only process file created events
        if event.event_type == 'created' and os.path.isfile(file_path):
            print(f"Detected new file: {file_path}")

            file_name = os.path.basename(file_path)
            folder_name = "inbox"
            key = f'{folder_name}/{file_name}'

            # Upload the file to S3
            try:
                s3_upload_request = {
                    "localFilePath": file_path,
                    "bucket": bucket_name,
                    "key": key
                }
                response = ipc_client.send_request(
                    "aws.greengrass.S3Uploader", s3_upload_request)
                print(f"Uploaded {file_name} to {bucket_name}/{key}")
                print(f"Upload response: {response}")

                # Delete the local file
                os.remove(file_path)
                print(f"Deleted local file: {file_path}")
            except Exception as e:
                print(f"IPC request error: {e}")

    def on_created(self, event):
        self.process(event)


if __name__ == "__main__":
    path = sys.argv[1]
    bucket_name = sys.argv[2]
    print("Path: %s!" % sys.argv[1])
    print("Bucket Name: %s!" % sys.argv[2])

    ipc_client = IPCClient()

    observer = Observer()
    observer.schedule(MyHandler(), path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
