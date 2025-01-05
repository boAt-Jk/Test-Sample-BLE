import csv
import re
from datetime import datetime

def convert_log_to_csv_with_time_diff(input_file, output_file):
    """
    Convert a log text file to a structured CSV file with a time difference column 
    and include only rows where the time difference is greater than 2 minutes.
    
    Args:
        input_file (str): Path to the input log file.
        output_file (str): Path to the output CSV file.
    """
    try:
        # Open the input log file for reading
        with open(input_file, 'r') as txt_file:
            lines = txt_file.readlines()

        # Open the CSV file for writing
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write header row
            writer.writerow(['Date', 'Time', 'Time Difference (minutes)', 'Device', 'Address', 'RSSI'])

            previous_time = None  # To store the previous timestamp for comparison

            # Parse each line and extract data
            for line in lines:
                # Use regex to extract information
                match = re.match(
                    r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) - Device: (.+?), Address: (.+?), RSSI: ([-\d]+)",
                    line.strip()
                )
                if match:
                    date, time, device, address, rssi = match.groups()

                    # Calculate the time difference
                    current_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
                    if previous_time is None:
                        # For the first row, add it without a time difference check
                        time_difference = "N/A"
                        writer.writerow([date, time, time_difference, device, address, rssi])
                    else:
                        diff_in_minutes = (current_time - previous_time).total_seconds() / 60
                        if diff_in_minutes > 2:
                            time_difference = f"{diff_in_minutes:.2f} minutes"
                            # Write the row if the time difference is greater than 2 minutes
                            writer.writerow([date, time, time_difference, device, address, rssi])

                    # Update the previous time
                    previous_time = current_time

        print(f"File converted successfully and saved as '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
input_file = 'ble_devices_800.txt'  # Replace with the path to your log text file
output_file = 'output_with_time_diff.csv'  # Replace with the desired CSV file name
convert_log_to_csv_with_time_diff(input_file, output_file)
