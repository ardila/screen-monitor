import os
import time
import random



save_in_folder = os.path.expanduser('~/Desktop/ScreenMonitor/')
# Create the directory if it doesn't exist
os.makedirs(save_in_folder, exist_ok=True)

def schedule_screenshot(mean_minutes):

    while True:
        filename = """$(date +%Y-%m-%d-%H-%M-%S).png"""
        path_to_save = os.path.join(save_in_folder, filename)
        os.system(f"screencapture {path_to_save}")
        # Equivalent to a poisson distribution with mean mean_minutes
        wait_time_in_minutes = random.expovariate(1.0 / mean_minutes)
        wait_time_in_seconds = wait_time_in_minutes * 60
        time.sleep(wait_time_in_seconds)

if __name__ == "__main__":
    schedule_screenshot(mean_minutes=5)