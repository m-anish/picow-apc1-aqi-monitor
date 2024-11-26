import network
import time
import machine
from machine import Timer
from microdot import Microdot, Response
from microdot.utemplate import Template
from apc1 import APC1  # Using APC1 class directly
from wifi_config import SSID, PASSWORD
import ujson  # Import ujson for JSON handling in MicroPython

# Set default content type to 'text/html' for all Microdot responses
Response.default_content_type = 'text/html'

# Path to the file storing Wi-Fi credentials
CREDENTIALS_FILE = 'wifi_config.py'


class WifiConnectionError(Exception):
    """Custom exception raised when Wi-Fi connection fails after multiple attempts."""
    pass


def save_wifi_credentials(ssid, password):
    """
    Save Wi-Fi credentials to the CREDENTIALS_FILE.

    Args:
        ssid (str): The SSID of the Wi-Fi network.
        password (str): The password of the Wi-Fi network.
    """
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f"SSID = '{ssid}'\n")
        f.write(f"PASSWORD = '{password}'\n")


def connect_wifi():
    """
    Attempt to connect to a Wi-Fi network using stored credentials.

    Raises:
        WifiConnectionError: If the connection fails after 10 attempts.
    """
    max_attempts = 10
    curr_attempt = 0
    wlan = network.WLAN(network.STA_IF)  # Set up the Wi-Fi interface in station mode
    wlan.active(True)  # Activate the Wi-Fi interface
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print(".", end="")
            curr_attempt += 1
            if curr_attempt >= max_attempts:
                wlan.active(False)
                raise WifiConnectionError("Unable to connect to Wi-Fi after 10 attempts.")
    print("\nConnected to WiFi!")
    print("IP Address:", wlan.ifconfig()[0])  # Display the assigned IP address


def start_ap_mode():
    """
    Start an Access Point (AP) mode to allow the user to enter Wi-Fi credentials.
    The AP broadcasts the SSID 'AQISetup' and serves a form for credential submission.
    """
    ap = network.WLAN(network.AP_IF)  # Configure the device as an Access Point
    ap.active(False)
    ap.active(True)  # Activate the AP
    ap.config(essid='AQISetup')  # Set the AP SSID
    ap.config(security=0)  # Open security (no password)

    # Wait for AP to become active
    while not ap.active():
        time.sleep(1)

    print(ap.ifconfig())  # Display the AP's IP address
    print('Access Point started, connect to "AQI-Setup"')

    app = Microdot()

    @app.route('/')
    def form(request):
        """Serve the Wi-Fi credentials input form."""
        return '''
            <html>
                <body>
                    <h1>Enter Wi-Fi Credentials</h1>
                    <form method="POST" action="/submit">
                        <label>SSID:</label>
                        <input type="text" name="ssid" required><br><br>
                        <label>Password:</label>
                        <input type="password" name="password" required><br><br>
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>
        '''

    @app.route('/submit', methods=['POST'])
    def submit(request):
        """
        Handle the submission of Wi-Fi credentials.

        Args:
            request: HTTP POST request containing SSID and password.

        Returns:
            HTML response indicating that credentials were saved.
        """
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        save_wifi_credentials(ssid, password)
        time.sleep(0.1)  # Allow any pending operations to complete
        ap.active(False)  # Deactivate the AP

        # Reboot the device after a short delay
        Timer(-1).init(period=5000, mode=Timer.ONE_SHOT, callback=lambda t: machine.reset())
        return '''
            <html>
                <body>
                    <h1>Credentials Saved!</h1>
                    <p>The Wi-Fi credentials have been saved. The device will reboot now.</p>
                </body>
            </html>
        '''

    # Start the Microdot server in AP mode
    app.run(debug=True, host='0.0.0.0', port=80)


# Main program logic
try:
    # Attempt to connect to Wi-Fi
    connect_wifi()
except WifiConnectionError:
    # If Wi-Fi connection fails, start AP mode to allow the user to enter new credentials
    start_ap_mode()

# Initialize the Microdot app
app = Microdot()

# Initialize the APC1 sensor
sensor = APC1(id=0, scl=1, sda=0)  # Use APC1 sensor on specific I2C pins


@app.route('/')
def index(request):
    """
    Serve the main sensor data page.

    Args:
        request: HTTP GET request.

    Returns:
        Rendered HTML template containing sensor data.
    """
    # Get all sensor data from the APC1 sensor
    sensor_data = sensor.get_all_sensor_data()

    # Render the template with the sensor data
    return Template('index.html').render(data=sensor_data)


# Start the Microdot web server
if __name__ == '__main__':
    # Listen on all interfaces (for Raspberry Pi Pico W)
    app.run(debug=True, host='0.0.0.0', port=80)
