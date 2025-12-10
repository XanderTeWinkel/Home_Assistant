import subprocess
import os
import sys
import platform
import shutil

# Paths
project_root = os.path.abspath("")
frontend_path = os.path.join(project_root, "Frontend")
backend_path = os.path.join(project_root, "Backend")

print(f"Project root: {project_root}")
print(f"Frontend path: {frontend_path}")
print(f"Backend path: {backend_path}")


# Function to open a new terminal and run a command
def run_in_new_terminal(command, cwd):
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["start", "cmd", "/k", command], cwd=cwd, shell=True)
    elif system == "Darwin":  # macOS
        subprocess.Popen(
            [
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "cd {cwd} && {command}"',
            ]
        )
    else:  # Linux
        # Try to find a terminal emulator
        terminals = ["gnome-terminal", "konsole", "xfce4-terminal", "tilix", "xterm"]
        terminal_cmd = None
        for term in terminals:
            if shutil.which(term):
                terminal_cmd = term
                break

        if not terminal_cmd:
            print(
                "No supported terminal emulator found. Please install one (gnome-terminal, konsole, xfce4-terminal, tilix, xterm)."
            )
            sys.exit(1)

        if terminal_cmd in {"gnome-terminal", "tilix"}:
            subprocess.Popen(
                [terminal_cmd, "--", "bash", "-c", f"cd {cwd} && {command}; exec bash"]
            )
        elif terminal_cmd == "konsole" or terminal_cmd == "xfce4-terminal" or terminal_cmd == "xterm":
            subprocess.Popen(
                [terminal_cmd, "-e", f"bash -c 'cd {cwd} && {command}; exec bash'"]
            )


# Step 1: Install new poetry packages
print("Installing new poetry packages...")
subprocess.run(["poetry", "install", "--no-root"], cwd=backend_path, check=False)

# Step 2: Run backend
print("Starting backend...")
run_in_new_terminal("poetry run python app.py", backend_path)

# Step 3: Run frontend
print("Starting frontend...")
run_in_new_terminal("npm run dev", frontend_path)

print("Both frontend and backend should now be running in separate terminals.")
