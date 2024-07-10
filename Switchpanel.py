import shutil
import os
import sys
import subprocess
import winreg
import curses
import random
import time
import ctypes
import win32com.client
import win32pipe, win32file, pywintypes
# Backup Functionality
def backup_data(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
    try:
        shutil.copytree(source, destination)
        print(f"Backup of {source} completed successfully at {destination}")
    except Exception as e:
        print(f"Error during backup: {e}")

def create_vm_named_pipes():
    pipes = [
        r'\\.\pipe\vmware-authdpipe',
        r'\\.\pipe\vmware-vmx',
        r'\\.\pipe\vmware-usb',
        r'\\.\pipe\vmware-toolbox-cmd',
        r'\\.\pipe\VBoxMiniRdrDN',
        r'\\.\pipe\VBoxTrayIPC',
        r'\\.\pipe\VBoxGuest'
    ]
    created_pipes = []
    for pipe in pipes:
        try:
            handle = win32pipe.CreateNamedPipe(
                pipe,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, 65536, 65536,
                0,
                None
            )
            created_pipes.append(handle)
            print(f"Created named pipe: {pipe}")
        except pywintypes.error as e:
            print(f"Failed to create named pipe {pipe}: {e}")
    return created_pipes

def delete_vm_named_pipes(handles):
    for handle in handles:
        try:
            win32file.CloseHandle(handle)
            print(f"Deleted named pipe handle: {handle}")
        except pywintypes.error as e:
            print(f"Failed to delete named pipe handle {handle}: {e}")

def verify_vm_named_pipes_created():
    pipes = [
        r'\\.\pipe\vmware-authdpipe',
        r'\\.\pipe\vmware-vmx',
        r'\\.\pipe\vmware-usb',
        r'\\.\pipe\vmware-toolbox-cmd',
        r'\\.\pipe\VBoxMiniRdrDN',
        r'\\.\pipe\VBoxTrayIPC',
        r'\\.\pipe\VBoxGuest'
    ]
    return all(os.path.exists(pipe) for pipe in pipes)

def verify_vm_named_pipes_deleted():
    pipes = [
        r'\\.\pipe\vmware-authdpipe',
        r'\\.\pipe\vmware-vmx',
        r'\\.\pipe\vmware-usb',
        r'\\.\pipe\vmware-toolbox-cmd',
        r'\\.\pipe\VBoxMiniRdrDN',
        r'\\.\pipe\VBoxTrayIPC',
        r'\\.\pipe\VBoxGuest'
    ]
    return all(not os.path.exists(pipe) for pipe in pipes)

# VM Techniques Implementation
import os

def create_vm_files():
    system32 = os.getenv('WINDIR') + r"\System32"
    vm_files = [
        os.path.join(system32, "drivers", "vmhgfs.sys"),
        os.path.join(system32, "drivers", "VBoxMouse.sys"),
        os.path.join(system32, "drivers", "VBoxGuest.sys"),
        os.path.join(system32, "drivers", "vmci.sys"),
        os.path.join(system32, "drivers", "VBoxSF.sys"),
        os.path.join(system32, "drivers", "VBoxVideo.sys"),
        os.path.join(system32, "vboxdisp.dll"),
        os.path.join(system32, "vboxhook.dll"),
        os.path.join(system32, "vboxmrxnp.dll"),
        os.path.join(system32, "vboxogl.dll"),
        os.path.join(system32, "vboxoglarrayspu.dll"),
        os.path.join(system32, "vboxoglcrutil.dll"),
        os.path.join(system32, "vboxoglerrorspu.dll"),
        os.path.join(system32, "vboxoglfeedbackspu.dll"),
        os.path.join(system32, "vboxoglpackspu.dll"),
        os.path.join(system32, "vboxoglpassthroughspu.dll"),
        os.path.join(system32, "vboxservice.exe"),
        os.path.join(system32, "vboxtray.exe"),
        os.path.join(system32, "VBoxControl.exe"),
        os.path.join(system32, "drivers", "vmmouse.sys"),
        os.path.join(system32, "drivers", "vmusbmouse.sys"),
        os.path.join(system32, "drivers", "vmkdb.sys"),
        os.path.join(system32, "drivers", "vmrawdsk.sys"),
        os.path.join(system32, "drivers", "vmmemctl.sys"),
        os.path.join(system32, "drivers", "vm3dmp.sys")
    ]
    for file in vm_files:
        try:
            with open(file, 'w') as f:
                f.write("This is a dummy VM file.")
            print(f"Created VM file: {file}")
        except Exception as e:
            print(f"Failed to create VM file {file}: {e}")

def delete_vm_files():
    system32 = os.getenv('WINDIR') + r"\System32"
    vm_files = [
        os.path.join(system32, "drivers", "vmhgfs.sys"),
        os.path.join(system32, "drivers", "VBoxMouse.sys"),
        os.path.join(system32, "drivers", "VBoxGuest.sys"),
        os.path.join(system32, "drivers", "vmci.sys"),
        os.path.join(system32, "drivers", "VBoxSF.sys"),
        os.path.join(system32, "drivers", "VBoxVideo.sys"),
        os.path.join(system32, "vboxdisp.dll"),
        os.path.join(system32, "vboxhook.dll"),
        os.path.join(system32, "vboxmrxnp.dll"),
        os.path.join(system32, "vboxogl.dll"),
        os.path.join(system32, "vboxoglarrayspu.dll"),
        os.path.join(system32, "vboxoglcrutil.dll"),
        os.path.join(system32, "vboxoglerrorspu.dll"),
        os.path.join(system32, "vboxoglfeedbackspu.dll"),
        os.path.join(system32, "vboxoglpackspu.dll"),
        os.path.join(system32, "vboxoglpassthroughspu.dll"),
        os.path.join(system32, "vboxservice.exe"),
        os.path.join(system32, "vboxtray.exe"),
        os.path.join(system32, "VBoxControl.exe"),
        os.path.join(system32, "drivers", "vmmouse.sys"),
        os.path.join(system32, "drivers", "vmusbmouse.sys"),
        os.path.join(system32, "drivers", "vmkdb.sys"),
        os.path.join(system32, "drivers", "vmrawdsk.sys"),
        os.path.join(system32, "drivers", "vmmemctl.sys"),
        os.path.join(system32, "drivers", "vm3dmp.sys")
    ]
    for file in vm_files:
        try:
            if os.path.exists(file):
                os.remove(file)
            print(f"Deleted VM file: {file}")
        except Exception as e:
            print(f"Failed to delete VM file {file}: {e}")

def verify_vm_files_created():
    system32 = os.getenv('WINDIR') + r"\System32"
    vm_files = [
        os.path.join(system32, "drivers", "vmhgfs.sys"),
        os.path.join(system32, "drivers", "VBoxMouse.sys"),
        os.path.join(system32, "drivers", "VBoxGuest.sys"),
        os.path.join(system32, "drivers", "vmci.sys"),
        os.path.join(system32, "drivers", "VBoxSF.sys"),
        os.path.join(system32, "drivers", "VBoxVideo.sys"),
        os.path.join(system32, "vboxdisp.dll"),
        os.path.join(system32, "vboxhook.dll"),
        os.path.join(system32, "vboxmrxnp.dll"),
        os.path.join(system32, "vboxogl.dll"),
        os.path.join(system32, "vboxoglarrayspu.dll"),
        os.path.join(system32, "vboxoglcrutil.dll"),
        os.path.join(system32, "vboxoglerrorspu.dll"),
        os.path.join(system32, "vboxoglfeedbackspu.dll"),
        os.path.join(system32, "vboxoglpackspu.dll"),
        os.path.join(system32, "vboxoglpassthroughspu.dll"),
        os.path.join(system32, "vboxservice.exe"),
        os.path.join(system32, "vboxtray.exe"),
        os.path.join(system32, "VBoxControl.exe"),
        os.path.join(system32, "drivers", "vmmouse.sys"),
        os.path.join(system32, "drivers", "vmusbmouse.sys"),
        os.path.join(system32, "drivers", "vmkdb.sys"),
        os.path.join(system32, "drivers", "vmrawdsk.sys"),
        os.path.join(system32, "drivers", "vmmemctl.sys"),
        os.path.join(system32, "drivers", "vm3dmp.sys")
    ]
    return all(os.path.exists(file) for file in vm_files)

def verify_vm_files_deleted():
    system32 = os.getenv('WINDIR') + r"\System32"
    vm_files = [
        os.path.join(system32, "drivers", "vmhgfs.sys"),
        os.path.join(system32, "drivers", "VBoxMouse.sys"),
        os.path.join(system32, "drivers", "VBoxGuest.sys"),
        os.path.join(system32, "drivers", "vmci.sys"),
        os.path.join(system32, "drivers", "VBoxSF.sys"),
        os.path.join(system32, "drivers", "VBoxVideo.sys"),
        os.path.join(system32, "vboxdisp.dll"),
        os.path.join(system32, "vboxhook.dll"),
        os.path.join(system32, "vboxmrxnp.dll"),
        os.path.join(system32, "vboxogl.dll"),
        os.path.join(system32, "vboxoglarrayspu.dll"),
        os.path.join(system32, "vboxoglcrutil.dll"),
        os.path.join(system32, "vboxoglerrorspu.dll"),
        os.path.join(system32, "vboxoglfeedbackspu.dll"),
        os.path.join(system32, "vboxoglpackspu.dll"),
        os.path.join(system32, "vboxoglpassthroughspu.dll"),
        os.path.join(system32, "vboxservice.exe"),
        os.path.join(system32, "vboxtray.exe"),
        os.path.join(system32, "VBoxControl.exe"),
        os.path.join(system32, "drivers", "vmmouse.sys"),
        os.path.join(system32, "drivers", "vmusbmouse.sys"),
        os.path.join(system32, "drivers", "vmkdb.sys"),
        os.path.join(system32, "drivers", "vmrawdsk.sys"),
        os.path.join(system32, "drivers", "vmmemctl.sys"),
        os.path.join(system32, "drivers", "vm3dmp.sys")
    ]
    return all(not os.path.exists(file) for file in vm_files)


def delete_registry_tree(key, sub_key):
    try:
        open_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_ALL_ACCESS)
        info_key = winreg.QueryInfoKey(open_key)
        for x in range(0, info_key[0]):
            subkey = winreg.EnumKey(open_key, 0)
            delete_registry_tree(open_key, subkey)
        winreg.DeleteKey(open_key, '')
        open_key.Close()
        return True
    except Exception as e:
        print(f"Failed to delete registry key {sub_key}: {e}")
        return False

def add_vm_device_entries():
    devices = {
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_15AD&DEV_0405": None,  # VMware SVGA II
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_80EE&DEV_CAFE": None,  # VirtualBox Graphics Adapter
    }
    for key, value in devices.items():
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
                if value is not None:
                    winreg.SetValueEx(reg_key, "", 0, winreg.REG_SZ, value)
            print(f"Added dummy device entry: {key}")
        except Exception as e:
            print(f"Failed to add dummy device entry {key}: {e}")

def delete_vm_device_entries():
    devices = [
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_15AD&DEV_0405",  # VMware SVGA II
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_80EE&DEV_CAFE",  # VirtualBox Graphics Adapter
    ]
    for key in devices:
        success = delete_registry_tree(winreg.HKEY_LOCAL_MACHINE, key)
        if success:
            print(f"Deleted dummy device entry: {key}")
        else:
            print(f"Failed to delete dummy device entry {key}")

def verify_vm_device_entries_added():
    devices = [
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_15AD&DEV_0405",  # VMware SVGA II
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_80EE&DEV_CAFE",  # VirtualBox Graphics Adapter
    ]
    for key in devices:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key):
                pass
        except FileNotFoundError:
            return False
    return True

def verify_vm_device_entries_deleted():
    devices = [
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_15AD&DEV_0405",  # VMware SVGA II
        r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_80EE&DEV_CAFE",  # VirtualBox Graphics Adapter
    ]
    keys_remaining = []
    for key in devices:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key):
                keys_remaining.append(key)
        except FileNotFoundError:
            pass
    return keys_remaining



def add_vm_registry_keys():
    vmware_keys = {
        r"SYSTEM\CurrentControlSet\Services\vmhgfs": None,
        r"SYSTEM\CurrentControlSet\Services\VBoxSF": None,
        r"SYSTEM\CurrentControlSet\Services\VMware\Unity": None,
        r"SOFTWARE\Oracle\VirtualBox Guest Additions": None,
        r"HARDWARE\ACPI\DSDT\VBOX__": None,
        r"HARDWARE\ACPI\FADT\VBOX__": None,
        r"HARDWARE\ACPI\RSDT\VBOX__": None,
        r"SYSTEM\ControlSet001\Services\VBoxGuest": None,
        r"SYSTEM\ControlSet001\Services\VBoxMouse": None,
        r"SYSTEM\ControlSet001\Services\VBoxService": None,
        r"SYSTEM\ControlSet001\Services\VBoxSF": None,
        r"SYSTEM\ControlSet001\Services\VBoxVideo": None,
        r"SOFTWARE\VMware, Inc.\VMware Tools": None
    }
    for key, value in vmware_keys.items():
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
                if value is not None:
                    winreg.SetValueEx(reg_key, "", 0, winreg.REG_SZ, value)
            print(f"Added registry key: {key}")
        except Exception as e:
            print(f"Failed to add registry key {key}: {e}")

def delete_vm_registry_keys():
    vmware_keys = [
        r"SYSTEM\CurrentControlSet\Services\vmhgfs",
        r"SYSTEM\CurrentControlSet\Services\VBoxSF",
        r"SYSTEM\CurrentControlSet\Services\VMware\Unity",
        r"SOFTWARE\Oracle\VirtualBox Guest Additions",
        r"HARDWARE\ACPI\DSDT\VBOX__",
        r"HARDWARE\ACPI\FADT\VBOX__",
        r"HARDWARE\ACPI\RSDT\VBOX__",
        r"SYSTEM\ControlSet001\Services\VBoxGuest",
        r"SYSTEM\ControlSet001\Services\VBoxMouse",
        r"SYSTEM\ControlSet001\Services\VBoxService",
        r"SYSTEM\ControlSet001\Services\VBoxSF",
        r"SYSTEM\ControlSet001\Services\VBoxVideo",
        r"SOFTWARE\VMware, Inc.\VMware Tools"
    ]
    for key in vmware_keys:
        success = delete_registry_tree(winreg.HKEY_LOCAL_MACHINE, key)
        if success:
            print(f"Deleted registry key: {key}")
        else:
            print(f"Failed to delete registry key {key}")

def verify_vm_registry_keys_added():
    vmware_keys = [
        r"SYSTEM\CurrentControlSet\Services\vmhgfs",
        r"SYSTEM\CurrentControlSet\Services\VBoxSF",
        r"SYSTEM\CurrentControlSet\Services\VMware\Unity",
        r"SOFTWARE\Oracle\VirtualBox Guest Additions",
        r"HARDWARE\ACPI\DSDT\VBOX__",
        r"HARDWARE\ACPI\FADT\VBOX__",
        r"HARDWARE\ACPI\RSDT\VBOX__",
        r"SYSTEM\ControlSet001\Services\VBoxGuest",
        r"SYSTEM\ControlSet001\Services\VBoxMouse",
        r"SYSTEM\ControlSet001\Services\VBoxService",
        r"SYSTEM\ControlSet001\Services\VBoxSF",
        r"SYSTEM\ControlSet001\Services\VBoxVideo",
        r"SOFTWARE\VMware, Inc.\VMware Tools"
    ]
    for key in vmware_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key):
                pass
        except FileNotFoundError:
            return False
    return True

def verify_vm_registry_keys_deleted():
    vmware_keys = [
        r"SYSTEM\CurrentControlSet\Services\vmhgfs",
        r"SYSTEM\CurrentControlSet\Services\VBoxSF",
        r"SYSTEM\CurrentControlSet\Services\VMware\Unity",
        r"SOFTWARE\Oracle\VirtualBox Guest Additions",
        r"HARDWARE\ACPI\DSDT\VBOX__",
        r"HARDWARE\ACPI\FADT\VBOX__",
        r"HARDWARE\ACPI\RSDT\VBOX__",
        r"SYSTEM\ControlSet001\Services\VBoxGuest",
        r"SYSTEM\ControlSet001\Services\VBoxMouse",
        r"SYSTEM\ControlSet001\Services\VBoxService",
        r"SYSTEM\ControlSet001\Services\VBoxSF",
        r"SYSTEM\ControlSet001\Services\VBoxVideo",
        r"SOFTWARE\VMware, Inc.\VMware Tools"
    ]
    for key in vmware_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key):
                return False
        except FileNotFoundError:
            pass
    return True


def run_dummy_processes():
    dummy_processes = ["dist/VBoxService.exe", "dist/vmtoolsd.exe", "dist/vmwaretray.exe", "dist/vmwareuser.exe", "dist/vmacthlp.exe", "dist/VBoxTray.exe", "dist/VBoxControl.exe"]
    for process in dummy_processes:
        try:
            subprocess.Popen([process], creationflags=subprocess.CREATE_NEW_CONSOLE)
            print(f"Started dummy process: {os.path.basename(process)}")
        except Exception as e:
            print(f"Failed to start dummy process {os.path.basename(process)}: {e}")

def kill_dummy_processes():
    dummy_processes = ["VBoxService.exe", "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe", "VBoxTray.exe", "VBoxControl.exe"]
    for process in dummy_processes:
        try:
            subprocess.call(["taskkill", "/IM", process, "/F"], shell=True)
            print(f"Killed dummy process: {process}")
        except Exception as e:
            print(f"Failed to kill dummy process {process}: {e}")

def verify_dummy_processes_running():
    dummy_processes = ["VBoxService.exe", "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe", "VBoxTray.exe", "VBoxControl.exe"]
    for process in dummy_processes:
        result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {process}"], capture_output=True, text=True)
        if process not in result.stdout:
            return False
    return True

def verify_dummy_processes_killed():
    dummy_processes = ["VBoxService.exe", "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe", "VBoxTray.exe", "VBoxControl.exe"]
    for process in dummy_processes:
        result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {process}"], capture_output=True, text=True)
        if process in result.stdout:
            return False
    return True


# Curses-based Menu
def print_menu(stdscr, selected_row_idx, toggles, status_message):
    menu = ["Create VM Files", "Add VM Devices", "Add VM Registry Keys", "Run Dummy Processes", "Create VM Named Pipes", "Exit"]
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = "Switchpanel"
    subtitle = "A VM Impersonation Tool"
    stdscr.addstr(1, w//2 - len(title)//2, title, curses.A_BOLD)
    stdscr.addstr(2, w//2 - len(subtitle)//2, subtitle)
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
        if idx < len(toggles) and toggles[idx]:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x + len(row) + 2, "[ON]")
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(y, x + len(row) + 2, "[OFF]")
            stdscr.attroff(curses.color_pair(3))
    stdscr.addstr(h-2, w//2 - len(status_message)//2, status_message, curses.A_BOLD)
    stdscr.refresh()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin_privileges():
    if not is_admin():
        print("Requesting administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    current_row = 0
    menu = ["Create VM Files", "Add VM Devices", "Add VM Registry Keys", "Run Dummy Processes", "Create VM Named Pipes", "Exit"]
    toggles = [False] * (len(menu) - 1)
    status_message = ""

    print_menu(stdscr, current_row, toggles, status_message)

    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(menu) - 1:
                break
            else:
                toggles[current_row] = not toggles[current_row]
                if toggles[current_row]:
                    status_message = backup_and_execute(current_row, True)
                else:
                    status_message = backup_and_execute(current_row, False)
                print_menu(stdscr, current_row, toggles, status_message)
                time.sleep(2)
                status_message = ""
        print_menu(stdscr, current_row, toggles, status_message)


def backup_and_execute(option, enable):
    source = os.getcwd()
    destination = os.path.join(source, "backup")
    backup_data(source, destination)
    try:
        if enable:
            if option == 0:
                create_vm_files()
                if verify_vm_files_created():
                    return "VM files created successfully."
                else:
                    return "Failed to create VM files."
            elif option == 1:
                add_vm_device_entries()
                if verify_vm_device_entries_added():
                    return "VM devices spoofed successfully."
                else:
                    return "Failed to spoof VM devices."
            elif option == 2:
                add_vm_registry_keys()
                if verify_vm_registry_keys_added():
                    return "Registry keys added successfully."
                else:
                    return "Failed to add registry keys."
            elif option == 3:
                run_dummy_processes()
                if verify_dummy_processes_running():
                    return "Dummy processes started successfully."
                else:
                    return "Failed to start dummy processes."
            elif option == 4:
                global created_pipes
                created_pipes = create_vm_named_pipes()
                if verify_vm_named_pipes_created():
                    return "VM named pipes created successfully."
                else:
                    return "Failed to create VM named pipes."
        else:
            if option == 0:
                delete_vm_files()
                if verify_vm_files_deleted():
                    return "VM files deleted successfully."
                else:
                    return "Failed to delete VM files."
            elif option == 1:
                delete_vm_device_entries()
                if not verify_vm_device_entries_deleted():
                    return "VM devices deleted successfully."
                else:
                    return "Failed to delete VM devices."
            elif option == 2:
                delete_vm_registry_keys()
                if verify_vm_registry_keys_deleted():
                    return "Registry keys deleted successfully."
                else:
                    return "Failed to delete registry keys."
            elif option == 3:
                kill_dummy_processes()
                if verify_dummy_processes_killed():
                    return "Dummy processes killed successfully."
                else:
                    return "Failed to kill dummy processes."
            elif option == 4:
                delete_vm_named_pipes(created_pipes)
                if verify_vm_named_pipes_deleted():
                    return "VM named pipes deleted successfully."
                else:
                    return "Failed to delete VM named pipes."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    request_admin_privileges()
    try:
        import windows_curses
    except ImportError:
        pass
    curses.wrapper(main)
