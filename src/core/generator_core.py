import jinja2 as ji
import tkinter as tk
from tkinter import filedialog

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
    def render_template(self, output_path=None):
        if not output_path:
            root = tk.Tk()
            root.withdraw()
            output_path = filedialog.asksaveasfilename(
                title="Save Vagrantfile as...",
                filetypes=[("All files", "*.*")],
                initialfile="Vagrantfile"
            )
            if not output_path:
                print("Cancelled. No file saved.")
                return

        with open(output_path, "w") as f:
            f.write(self.output)
