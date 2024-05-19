import time

class TimedApplication:
    def __init__(self):
        self.start_hour = 0
        self.start_minute = 0
        self.end_hour = 0
        self.end_minute = 0
        self.schedule_set = False
        self.delay_time = 10  # Default delay time in seconds
        self.settings_applied = False
        self.apply_time = None

    def set_congestion_schedule(self, start_hour, start_minute, end_hour, end_minute):
        try:
            start_hour = int(start_hour)
            start_minute = int(start_minute)
            end_hour = int(end_hour)
            end_minute = int(end_minute)
            if 0 <= start_hour < 24 and 0 <= start_minute < 60 and 0 <= end_hour < 24 and 0 <= end_minute < 60:
                self.start_hour = start_hour
                self.start_minute = start_minute
                self.end_hour = end_hour
                self.end_minute = end_minute
                self.schedule_set = True
                print(f"Congestion pricing schedule set from {start_hour}:{start_minute:02} to {end_hour}:{end_minute:02}")
            else:
                print("Invalid hours or minutes. Hours must be between 0 and 23, and minutes between 0 and 59.")
        except ValueError:
            print("Invalid input. Please enter valid hours and minutes.")

    def check_congestion_pricing(self):
        if self.schedule_set:
            current_time = time.localtime()
            current_hour = current_time.tm_hour
            current_minute = current_time.tm_min
            if (self.start_hour < current_hour or (self.start_hour == current_hour and self.start_minute <= current_minute)) and \
               (current_hour < self.end_hour or (current_hour == self.end_hour and current_minute < self.end_minute)):
                print("Congestion pricing is in effect.")
            else:
                print("Congestion pricing is not in effect.")
        else:
            print("Please set the congestion pricing schedule first.")

    def wait_for_congestion_start(self):
        if self.schedule_set:
            current_time = time.localtime()
            current_hour = current_time.tm_hour
            current_minute = current_time.tm_min
            while (current_hour, current_minute) != (self.start_hour, self.start_minute):
                print(f"Waiting for congestion pricing to start at {self.start_hour}:{self.start_minute:02}...")
                time.sleep(60)  # Sleep for 1 minute before checking again
                current_time = time.localtime()
                current_hour = current_time.tm_hour
                current_minute = current_time.tm_min
            print("Congestion pricing is now in effect!")
        else:
            print("Please set the congestion pricing schedule first.")

    def apply_settings(self):
        self.settings_applied = True
        self.apply_time = time.strftime("%H:%M:%S")

    def check_apply_settings(self):
        current_time = time.strftime("%H:%M:%S")
        if self.settings_applied and self.apply_time == current_time:
            print("Settings applied successfully.")
            self.settings_applied = False

    def set_delay_time(self, delay):
        self.delay_time = delay

    def apply_settings_with_delay(self):
        self.apply_settings()
        print(f"Settings will be applied after {self.delay_time} seconds.")
        time.sleep(self.delay_time)
        self.check_apply_settings()

    def apply_settings_immediately(self):
        self.apply_settings()
        self.check_apply_settings()

# Example usage:
pricing_system = TimedApplication()
while True:
    start_hour = input("Enter the start hour for congestion pricing (0-23): ")
    start_minute = input("Enter the start minute for congestion pricing (0-59): ")
    end_hour = input("Enter the end hour for congestion pricing (0-23): ")
    end_minute = input("Enter the end minute for congestion pricing (0-59): ")
    pricing_system.set_congestion_schedule(start_hour, start_minute, end_hour, end_minute)
    if pricing_system.schedule_set:
        break

# Set delay time if needed
pricing_system.set_delay_time(10)  # Example delay time in seconds

# Apply settings with delay
pricing_system.apply_settings_with_delay()

# Or apply settings immediately
# pricing_system.apply_settings_immediately()

# Wait for congestion pricing to start
pricing_system.wait_for_congestion_start()

# Check if congestion pricing is in effect
pricing_system.check_congestion_pricing()
