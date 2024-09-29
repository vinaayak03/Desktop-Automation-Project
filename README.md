Overview
This Python project automates the process of sorting and organizing files on your desktop by monitoring for newly added files and moving them to designated folders based on their file type (e.g., images, documents, videos). This ensures your desktop stays organized with minimal manual intervention.

The script uses Python's os, shutil, and time libraries to monitor the Desktop folder and classify files by extension. It supports common file types like images (.png, .jpg), documents (.pdf, .docx, .txt), videos (.mp4, .mkv), and executables (.exe), but can be easily customized to include more types.

Features
Automatic File Sorting: Files are automatically moved to pre-defined folders based on their file type.
Real-Time Monitoring: The script continuously monitors the Desktop folder for any new files.
Completion Check: The script waits until file downloads are complete to prevent errors related to incomplete files.
Customizable: You can customize the folder paths and file types to suit your needs.
No External Dependencies: Uses only Python's built-in libraries.
How It Works
Monitoring the Desktop Folder: The script monitors your Desktop for any new files.
File Type Detection: Once a new file is detected, the script checks its extension to determine the type.
File Movement: The file is then moved to its designated folder. For example, images go into the "Pictures" folder, documents into "Documents," etc.
Completion Handling: The script ensures that files are fully transferred (or downloaded) before moving them to their respective folders, avoiding issues with temporary or incomplete files.
Installation
Clone this repository:
bash
Copy code
git clone https://github.com/yourusername/Desktop-Automation.git
cd Desktop-Automation
Ensure you have Python 3 installed. You can check this by running:
bash
Copy code
python --version
No external libraries are required, as the script uses Python's built-in modules.
Usage
Modify the folder paths if needed in the Python script. By default, it monitors the Desktop and moves files into the following folders:
Images: Pictures/
Documents: Documents/
Videos: Videos/
Executables: Programs/
Run the script:
bash
Copy code
python file_mover.py
The script will continue running in the background, organizing your files as they appear.
Example
python
Copy code
# Example structure for file types and folders
file_destinations = {
    'Images': ['.png', '.jpg', '.jpeg', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Programs': ['.exe', '.bat']
}
You can add more file types and their corresponding folders by modifying the dictionary in the script.

Customization
Add more file types: Modify the file_destinations dictionary to include new file types or change the folder paths.
Change monitoring folder: If you'd like to monitor a different folder (e.g., Downloads), you can easily update the desktop_path in the script.
Contributions
Feel free to contribute by opening a pull request or submitting issues.

License
This project is licensed under the MIT License - see the LICENSE file for details.
