import time

class TimedApplication:
    def __init__(self):
        self.settings_applied = False
        self.apply_time = None
        self.delay_time = 10  # Default delay time in seconds

    def apply_settings(self):
        self.settings_applied = True
        self.apply_time = time.time() + self.delay_time  # Set the time when settings will be applied

    def check_apply_settings(self):
        if self.settings_applied and time.time() >= self.apply_time:
            # Apply settings here
            print("Settings applied successfully.")
            self.settings_applied = False

    def set_delay_time(self, delay):
        self.delay_time = delay

    def apply_settings_with_delay(self):
        self.apply_settings()
        print(f"Settings will be applied after {self.delay_time} seconds.")
        
    def apply_settings_immediately(self):
        self.apply_settings()
        self.check_apply_settings()

# Example usage
if __name__ == "__main__":
    app = TimedApplication()
    # Applying settings with delay
    app.apply_settings_with_delay()
    # Applying settings immediately
    app.apply_settings_immediately()
