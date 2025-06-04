import os
import json
import sys

def load_settings(settings_file, enable_logging=False):
    if enable_logging:
        print(f"[Settings] Attempting to load settings from: {settings_file} (File {'exists' if os.path.exists(settings_file) else 'does not exist'})")
    if not os.path.exists(settings_file):
        if enable_logging:
            print("[Settings] Settings file not found")
        return {}
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            try:
                loaded_settings = json.load(f)
            except json.JSONDecodeError as json_error:
                if enable_logging:
                    print(f"[Settings] JSON decoding error: {json_error}")
                return {}
    except Exception as e:
        if enable_logging:
            print(f"[Settings] Error reading settings file: {e}")
        return {}
    try:
        if 'position' in loaded_settings:
            pos = loaded_settings['position']
            if not isinstance(pos, dict) or 'x' not in pos or 'y' not in pos:
                if enable_logging:
                    print("[Settings] Invalid position format in settings")
                loaded_settings.pop('position')
            else:
                loaded_settings['position'] = {
                    'x': int(pos['x']),
                    'y': int(pos['y'])
                }
        if 'scale' in loaded_settings:
            scale = int(loaded_settings['scale'])
            if scale < 100 or scale > 500:
                if enable_logging:
                    print(f"[Settings] Invalid scale value '{loaded_settings.get('scale', None)}', resetting to 100")
                loaded_settings['scale'] = 100
            else:
                loaded_settings['scale'] = scale
    except Exception as e:
        if enable_logging:
            print(f"[Settings] Error processing scale data. Invalid value: '{loaded_settings.get('scale', None)}'. Expected an integer between 100 and 500. Error details: {e}")
        loaded_settings['scale'] = 100
    if enable_logging:
        print(f"Settings loaded successfully: {loaded_settings}")
    return loaded_settings

def save_settings(settings_file, data, enable_logging=False):
    try:
        settings_dir = os.path.dirname(settings_file)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        temp_file = settings_file + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        if sys.platform == 'win32':
            if os.path.exists(settings_file):
                os.replace(temp_file, settings_file)
            else:
                os.rename(temp_file, settings_file)
        else:
            os.replace(temp_file, settings_file)
    except Exception as e:
        if enable_logging:
            print(f"[Settings] Error saving settings: {e}")
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as e:
            if enable_logging:
                print(f"[Settings] Fatal error saving settings: {e}")