import os
import subprocess
import re


# Set these variables to your desired values
PYTHON_SCRIPT_PATH = "screenshot.py"
BASE_EXECUTABLE_NAME = "screenshot"
PLIST_NAME = "com.screenmonitor.screenshot"
PLIST_TEMPLATE_PATH = "screenshot_plist_template.plist"

# Get the directory of the current script, convert it to a full path
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, 'dist')
os.makedirs(OUTPUT_PATH, exist_ok=True)


# Install PyInstaller if not already installed
subprocess.run(['pip3', 'install', 'pyinstaller'])

# Determine the version number for the new executable
version = 1
regex = re.compile(rf'{BASE_EXECUTABLE_NAME}_v(\d+)')
existing_executables = [f for f in os.listdir(OUTPUT_PATH) if regex.match(f)]
if existing_executables:
    # Get the version number from the existing executable's filename and increment it
    version = max(int(regex.match(f).group(1)) for f in existing_executables) + 1

    # Remove the existing executables
    for f in existing_executables:
        os.remove(os.path.join(OUTPUT_PATH, f))

executable_name = f"{BASE_EXECUTABLE_NAME}_v{version}"

# Build the standalone executable with PyInstaller and directly output to the desired directory
subprocess.run(['pyinstaller', '--onefile', '--name', executable_name, '--distpath', OUTPUT_PATH, PYTHON_SCRIPT_PATH])

# Create the .plist file for the launchd job
with open(os.path.join(os.path.expanduser('~'), 'Library', 'LaunchAgents', f'{PLIST_NAME}.plist'), 'w') as plist_file:
    plist_file.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{os.path.join(OUTPUT_PATH, executable_name)}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
""")

# Unload the existing launchd job, if any
subprocess.run(['launchctl', 'unload', os.path.join(os.path.expanduser('~'), 'Library', 'LaunchAgents', f'{PLIST_NAME}.plist')], stderr=subprocess.DEVNULL)

# Load the launchd job
subprocess.run(['launchctl', 'load', os.path.join(os.path.expanduser('~'), 'Library', 'LaunchAgents', f'{PLIST_NAME}.plist')])

# Done
print(f"Build process completed successfully. New version of {executable_name} is now running as a background service.")