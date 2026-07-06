<p align="center">
  <img src="https://github.com/akhos09/XenoCore/blob/main/src/assets/img/app_icon.png" alt="XenoCore UI" width="190"/>
</p>
<h1 align="center">🛡️ XenoCore</h1>
<p align="center">
  <img src="https://github.com/akhos09/XenoCore/blob/main/src/assets/img/mainphoto_readme.png" alt="XenoCore UI" width="1920"/>
</p>

## Table of Contents

* [About](#about)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Troubleshooting](#troubleshooting)
* [Development](#development)
* [License](#license)



## About
XenoCore is a multi-platform (Linux&Windows) application designed to manage all the possible options for Vagrant and generate customized Vagrantfiles via GUI. You can configure up to 50 environments with various parameters (network interfaces, provisioners, synchronized folders, disk size, and more).

## Dependencies

Ensure the following are installed:

1. **Vagrant**: Available from [hashicorp.com](https://developer.hashicorp.com/vagrant)
2. **VirtualBox**: Available from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)
3. **uv**: Installed with`curl -LsSf https://astral.sh/uv/install.sh | sh` [docs](https://docs.astral.sh/uv/)


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akhos09/XenoCore.git
   cd XenoCore/
   ```

2. **Install Python dependencies using UV**:

   ```bash
   uv sync
   ```

## Usage

1. **Run the application**:

   ```bash
   uv run python src/app.py
   ```


## Project Structure

```
XenoCore/
├── src/
│   ├── assets/
│   │   ├── fonts/
│   │   └── img/
│   ├── core/                     
│   │   ├── templates/
│   │   ├── env_core.py
│   │   ├── generator_core.py
│   │   └── plg_core.py
│   ├── gui/
│   │   ├── components/
│   │   │   ├── constants.py
│   │   │   ├── fonts.py
│   │   │   ├── gui_core.py
│   │   │   ├── menu.py
│   │   │   └── themes.py
│   │   └── gui.py
│   └── app.py           
├── vagrantfiles/
│   ├── ansible/
│   ├── dhcp/
│   ├── grafana&prometheus/
│   ├── openldap/
│   ├── php/
│   ├── webserver/
│   └── wordpress/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── LICENSE
├── README.md
```

## Troubleshooting

* Make sure uv ins installed correctly `uv --version`.
* If dependencies fail, run `uv sync --resinstall`.
* Use `uv python list` to verify you're using the correct Python version (3.12.5 minimum).
* If you are in Windows disable Hyper-V, WSL, and Virtual Machine Platform. It could cause some trouble with VirtualBox.


## Development
 - Enhance Linux support
 - Add more advanced parameters to the VgFileGenerator
 - Implement more fonts and themes
 - Create a customized theme creator
 - Add a multiplier to create X times the same environment with the same options
 - Add metrics checkbox option (to collect data from the virtual machines and redirect it into a Grafana installed on the native system)

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
