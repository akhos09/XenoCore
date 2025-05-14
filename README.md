# 🛡️ XenoCore

An app that manages all posible options for Vagrant and generates customized Vagrantfiles

## Table of Contents

* [Dependencies](#dependencies)
* [Installation](#installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Troubleshooting](#troubleshooting)
* [Development](#development)
* [License](#license)

---

## Dependencies

Ensure the following are installed:

1. **Vagrant**: Available from [hashicorp.com](https://developer.hashicorp.com/vagrant).
2. **Python Modules**: Installed via `requirements.txt`.

---

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

   You could use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

---

## Usage

1. **Navigate to the source directory**:

   ```bash
   cd src
   ```

2. **Run the application**:

   ```bash
   python app.py
   ```

---

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
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

```

---

## Troubleshooting

* Make sure Python is added to your system's PATH.
* If modules are missing, ensure `pip install -r requirements.txt` completed without errors.
* Use `python --version` to verify you're using the correct Python version.
* Activate your virtual environment before running the script.

---

## Development

Planned features:

...
---

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.
