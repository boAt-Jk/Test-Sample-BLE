import asyncio
from bleak import BleakScanner
import time
from datetime import datetime

# Define a function that will continuously scan for a customized time duration
async def run():
    start_time = time.time()  # Record the start time
    duration = 63000  # Duration in seconds

    # Open a file to store the results
    with open("BLE_devices_AD800.txt", "w") as file:
        def detection_callback(device, advertisement_data):
            # Filter and log device information if RSSI > -50 and "300_BLE" is in the device name
            if advertisement_data.rssi > -50 and device.name and "800_BLE" in device.name:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = f"{current_time} - Device: {device.name}, Address: {device.address}, RSSI: {advertisement_data.rssi}"
                print(result)
                file.write(result + "\n")  # Write the result to the text file
                file.flush()  # Ensure data is written to the file immediately

        # Use BleakScanner with a detection callback
        scanner = BleakScanner(detection_callback)

        try:
            await scanner.start()
            print(f"Scanning for {duration} seconds...")
            await asyncio.sleep(duration)  # Scan for the specified duration
        except asyncio.CancelledError:
            print("Scan was cancelled.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await scanner.stop()
            print("Scanner stopped.")

# Run the scanner using asyncio.run()
if __name__ == "__main__":
    asyncio.run(run())
