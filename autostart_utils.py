import sys
import os
import winreg

def add_to_startup_registry():
    """Add application to Windows startup registry"""
    try:
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
            work_dir = os.path.dirname(app_path)

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )

            command = f'cmd /c "cd /d \"{work_dir}\" && start \"\" \"{app_path}\""'

            winreg.SetValueEx(
                key,
                "DailyWidget",
                0,
                winreg.REG_SZ,
                command
            )

            winreg.CloseKey(key)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error adding to startup: {e}")
        return False

def remove_from_startup_registry():
    """Remove application from Windows startup registry"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        try:
            winreg.DeleteValue(key, "DailyWidget")
        except:
            pass

        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error removing from startup: {e}")
        return False

def is_in_startup_registry():
    """Check if application is in Windows startup registry"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        try:
            value, _ = winreg.QueryValueEx(key, "DailyWidget")
            winreg.CloseKey(key)
            return True
        except:
            winreg.CloseKey(key)
            return False
    except:
        return False