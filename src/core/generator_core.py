import jinja2 as ji
import threading
import subprocess
import sys
from tkinter import Tk, filedialog as fd, messagebox
from contextlib import contextmanager
import os

@contextmanager
def change_directory(path):
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)
class VgFileGenerator:
    def __init__(self, machine_data: dict):
        self.env = ji.Environment(
            loader=ji.FileSystemLoader("./core/templates"),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.template = self.env.get_template("vgfile.j2")

        self.params = {
            "multi_machine": True,
            "machines": self.reformat_data(machine_data)
        }
        self.output = self.template.render(**self.params)
        
#Format data function------------------------------------------------------------------------------
    def reformat_data(self, data: dict):
        machines = []
        for key, env in data.items():
            name = (env.get("name") or key).lower()
            hostname = (env.get("hostname") or name).lower()

            network_interfaces = []
            for iface in env.get("network_interfaces", []):
                network_interfaces.append({
                    "type": iface.get("type", "Host Only/Private Interface"),
                    "ip": iface.get("ip", ""),
                    "subnet_mask": iface.get("subnet_mask", "255.255.255.0"),
                    "gateway": iface.get("gateway", "")
                })

            sync_folders = []
            for folder in env.get("sync_folders", []):
                if folder.get("host_folder") and folder.get("vm_destination"):
                    sync_folders.append({
                        "host_folder": folder.get("host_folder", ""),
                        "vm_destination": folder.get("vm_destination", "")
                    })

            provisioners = []
            for prov in env.get("provisioners", []):
                if prov.get("type") == "shell":
                    provisioners.append({
                        "type": "shell",
                        "path": prov.get("path", "")
                    })
                elif prov.get("type") == "file":
                    provisioners.append({
                        "type": "file",
                        "source": prov.get("path", ""),
                        "destination": prov.get("destination", "")
                    })

            machines.append({
                "name": name,
                "hostname": hostname,
                "box": env.get("box", "hashicorp/bionic64"),
                "box_version": env.get("box_version", ""),
                "cpu": int(env.get("cpu") or 1),
                "ram": int(env.get("ram") or 1024),
                "disk_size": env.get("disk_size", "20GB"),
                "network_interfaces": network_interfaces,
                "sync_folders": sync_folders,
                "provisioners": provisioners,
            })
        return machines


    
#Render template function------------------------------------------------------------------------------
    def render_template(self, default_name="Vagrantfile"):
        # --- Select folder in thread ---
        folder_selected = None

        def folder_dialog():
            nonlocal folder_selected
            try:
                root = Tk()
                root.withdraw()
                root.wm_attributes("-topmost", 1)
                folder_selected = fd.askdirectory(title="Select folder to save Vagrantfile")
            finally:
                try:
                    root.destroy()
                except:
                    pass

        thread = threading.Thread(target=folder_dialog)
        thread.start()
        thread.join()

        if not folder_selected:
            return

        # --- Write the Vagrantfile ---
        try:
            file_path = os.path.join(folder_selected, default_name)
            with open(file_path, "w") as f:
                f.write(self.output)
        except Exception as e:
            self._show_messagebox("ERROR", f"Failed to write Vagrantfile: {e}", error=True)
            return

        # --- Ask if user wants to run vagrant up ---
        confirmed = False

        def confirm_dialog():
            nonlocal confirmed
            try:
                root = Tk()
                root.withdraw()
                root.wm_attributes("-topmost", 1)
                confirmed = messagebox.askyesno("Run Vagrant", "Do you want to run create the environment?")
            finally:
                try:
                    root.destroy()
                except:
                    pass

        thread = threading.Thread(target=confirm_dialog)
        thread.start()
        thread.join()

        if not confirmed:
            return

        # --- Run vagrant up ---
        with change_directory(folder_selected):
            cmd = 'start /wait cmd /c "vagrant up & pause"' if sys.platform == "win32" else "vagrant up"
            subprocess.run(cmd, shell=True, check=True)
        # except subprocess.CalledProcessError as e:
        #     self("ERROR", f"Vagrant error: {e}", error=True)
        # except Exception as e:
        #     self._show_messagebox("ERROR", f"Unexpected error: {e}", error=True)