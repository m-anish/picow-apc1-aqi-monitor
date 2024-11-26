# Wi-Fi and Sensor Data Web Server for Raspberry Pi Pico W

This project enables the Raspberry Pi Pico W to:
1. Connect to a Wi-Fi network using stored credentials.
2. Start an Access Point (AP) if the connection fails, allowing the user to input new credentials via a web form.
3. Retrieve and display weather sensor data from the APC1 sensor on a dynamically updating webpage styled with Bootstrap.

---

## Features

- **Wi-Fi Connectivity**: Automatically connects to a saved Wi-Fi network on boot.
- **Access Point Mode**: Starts an AP for entering Wi-Fi credentials if the connection fails.
- **Web Interface**: Displays real-time sensor data from the APC1 on a web page.
- **Automatic Reboot**: Saves credentials, stops AP mode, and reboots the device after submission.

---

## Prerequisites

### Hardware:
- Raspberry Pi Pico W
- APC1 weather sensor connected via I2C

### Software:
- MicroPython firmware installed on the Pico W
- Required Python libraries: 
  - `Microdot`
  - `Microdot.utemplate`
  - `APC1`

---

## Installation

1. Upload all files to the Raspberry Pi Pico W using a tool like [Thonny](https://thonny.org/).
2. After rebooting, code should run automatically

---

## Usage

### 1. Automatic Wi-Fi Connection
On boot, the script attempts to connect to the Wi-Fi network using credentials stored in `wifi_config.py`. 

- **Stored Credentials**: The file `wifi_config.py` should define the following:
  ```python
  SSID = 'YourSSID'
  PASSWORD = 'YourPassword'
  ```

### 2. Access Point Mode
If the Wi-Fi connection fails:
- The device creates an AP named `AQISetup`.
- Users can connect to this AP and visit `http://192.168.4.1` to input Wi-Fi credentials.
- The device reboots after saving the credentials.

### 3. Sensor Data Webpage
Once connected to Wi-Fi:
- Visit the device's IP address (shown in the console) to view the sensor data.
- The webpage updates every 2 seconds with live sensor readings styled using Bootstrap.

---

## Web Interface

### **Wi-Fi Credentials Form**
- Accessible at `http://192.168.4.1` in AP mode.
- Allows entering SSID and Password for Wi-Fi connection.

### **Sensor Data Page**
- Displays live weather data retrieved from the APC1 sensor.
- Dynamically updates using the Bootstrap theme.

---

## Functions

### `connect_wifi()`
- Connects to a Wi-Fi network using saved credentials.
- Raises a `WifiConnectionError` if the connection fails after 10 attempts.

### `start_ap_mode()`
- Activates AP mode with the SSID `AQISetup`.
- Serves a web form to input Wi-Fi credentials.
- Stops AP mode and reboots after saving credentials.

### `save_wifi_credentials(ssid, password)`
- Writes the given Wi-Fi credentials to `wifi_config.py`.

---

## Dependencies

Listed in the `requirements.txt` file:
- `microdot`
- `microdot-utemplate`
-   apc1 (https://github.com/m-anish/APC1)  

---

## License

This project is licensed under the **GNU GPL v3**.

---

## Credits

- Built using the [Microdot](https://github.com/miguelgrinberg/microdot) framework.
- Utilizes the APC1 sensor class for real-time weather data.
