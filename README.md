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
XenoCore is a cross-platform (Linux&Windows) designed to manage all the possible options for Vagrant and generate customized Vagrantfiles via GUI. You can configure up to 50 environments with various parameters (network interfaces, provisioners, synchronized folders, disk size, and more).

## Dependencies

Ensure the following are installed:

1. **Vagrant**: Available from [hashicorp.com](https://developer.hashicorp.com/vagrant)
2. **VirtualBox**: Available from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads)
3. **Python Modules**: Installed via `requirements.txt`


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akhos09/XenoCore.git
   cd XenoCore/
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

    _You could use a virtual environment:_
    
     ```bash
     python -m venv venv
     #Linux: source venv/bin/activate  
     #Windows: venv\Scripts\activate
     ```


## Usage

1. **Navigate to the source directory**:

   ```bash
   cd src
   ```

2. **Run the application**:

   ```bash
   python app.py
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
│   └── app.pyw                   
├── vagrantfiles/
│   ├── ansible/
│   ├── dhcp/
│   ├── grafana&prometheus/
│   ├── openldap/
│   ├── php/
│   ├── webserver/
│   └── wordpress/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Troubleshooting

* Make sure Python is added to your system's PATH.
* If modules are missing, ensure `pip install -r requirements.txt` completed without errors.
* Use `python --version` to verify you're using the correct Python version.
* Activate your virtual environment before running the script.


## Development
 - Enhance Linux support
 - Add more advanced parameters to the VgFileGenerator
 - Implement more fonts and themes
 - Create a customized theme creator

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
