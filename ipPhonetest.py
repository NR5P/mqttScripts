import subprocess
import time

def make_call(ip_address):
    try:
        # Start linphone in terminal
        process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait for linphone to initialize
        time.sleep(2)

        # Command to call the IP address
        call_command = f"call sip:{ip_address}\n"
        process.stdin.write(call_command)
        process.stdin.flush()

        # Wait for some duration for call - adjust as needed
        time.sleep(5)

        # Command to terminate the call
        terminate_command = "terminate\n"
        process.stdin.write(terminate_command)
        process.stdin.flush()

        # Close linphone
        quit_command = "quit\n"
        process.stdin.write(quit_command)
        process.stdin.flush()

        # Wait for process to end
        process.wait()

    except Exception as e:
        print(f"An error occurred: {e}")

def make_call_sip(extension):
    try:
        # Start linphone in terminal
        process = subprocess.Popen(['linphonec'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait for linphone to initialize
        time.sleep(2)

        # Command to call the IP address
        call_command = f"call sip:{extension}@192.168.10.24\n"
        process.stdin.write(call_command)
        process.stdin.flush()

        # Wait for some duration for call - adjust as needed
        time.sleep(5)

        # Command to terminate the call
        terminate_command = "terminate\n"
        process.stdin.write(terminate_command)
        process.stdin.flush()

        # Close linphone
        quit_command = "quit\n"
        process.stdin.write(quit_command)
        process.stdin.flush()

        # Wait for process to end
        process.wait()

    except Exception as e:
        print(f"An error occurred: {e}")





# Example usage
#make_call("192.168.1.22")

#make_call_sip("12345")


