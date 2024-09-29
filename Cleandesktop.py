import os
import shutil
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directories
source_dir = '' # Add your Source Directory
dest_dir_doc = '' # Add your Document Directory
dest_dir_music = '' # Add your Music Directory
dest_dir_video = '' # Add your Video Directory
dest_dir_image = '' # Add your Image Directory

# Supported file types
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".ico"]
video_extensions = [".webm", ".mpg", ".mpeg", ".mp4", ".avi", ".mov", ".wmv", ".flv"]
audio_extensions = [".mp3", ".wav", ".flac", ".aac", ".m4a", ".wma"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# Temporary file extensions
temporary_extensions = [".crdownload", ".part", ".tmp"]

# Configuration for waiting and retrying
RETRY_LIMIT = 10
MAX_WAIT_TIME = 60
RETRY_INTERVAL = 1

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class MoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.handle_new_file(event.src_path)

    def handle_new_file(self, file_path):
        """Handle the new file creation."""
        name = os.path.basename(file_path)
        logging.info(f"Detected new file: {name}")

        # Wait a bit to allow renaming to occur
        time.sleep(1)

        # Check if the file exists
        if not os.path.exists(file_path):
            logging.info(f"File no longer exists immediately after detection: {name}, exiting...")
            return

        # Wait for the file to finish downloading
        for _ in range(RETRY_LIMIT):
            if not is_downloading(file_path):
                break
            logging.info(f"File still downloading: {name}, waiting...")
            time.sleep(RETRY_INTERVAL)

        # After waiting, check for renamed file
        final_name = self.get_final_name(file_path)
        if final_name is None:
            logging.info(f"No final name detected for file: {name}, exiting...")
            return

        # Determine destination directory based on final file extension
        dest = self.get_destination(final_name)
        if not dest:
            logging.info(f"File type not supported for moving: {final_name}")
            return

        # Ensure the destination directory exists
        if not os.path.exists(dest):
            os.makedirs(dest)
            logging.info(f"Created destination directory: {dest}")

        # Prepare the destination file path
        dest_file_path = os.path.join(dest, final_name)

        # Move the file
        try:
            shutil.move(final_name, dest_file_path)
            logging.info(f"Moved file: {final_name} to {dest}")
        except Exception as e:
            logging.exception(f"Error moving file {final_name}: {e}")

    def get_final_name(self, file_path):
        """Check for renamed files after download."""
        for _ in range(RETRY_LIMIT):
            time.sleep(RETRY_INTERVAL)  # Allow time for the renaming
            if os.path.exists(file_path[:-4]):  # Check if the non-tmp file exists
                return os.path.basename(file_path[:-4])  # Return the new name without the tmp extension
        return None

    def get_destination(self, name):
        """Determine the destination directory based on file extension."""
        if name.endswith(tuple(document_extensions)):
            return dest_dir_doc
        elif name.endswith(tuple(audio_extensions)):
            return dest_dir_music
        elif name.endswith(tuple(video_extensions)):
            return dest_dir_video
        elif name.endswith(tuple(image_extensions)):
            return dest_dir_image
        return None

def is_downloading(file_path):
    """Check if the file is still downloading based on size."""
    try:
        initial_size = os.path.getsize(file_path)
        time.sleep(RETRY_INTERVAL)
        current_size = os.path.getsize(file_path)
        return initial_size == current_size
    except FileNotFoundError:
        return True  # Treat as still downloading if the file isn't found

if __name__ == "__main__":
    # Start the observer to monitor file changes
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()

    logging.info("Watching for new files in Downloads folder...")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
