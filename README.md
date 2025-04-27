Here's a comprehensive README.md for your ZREAL HASH tool:

```markdown
# ZREAL HASH - Advanced Archive Hash Extractor

███████╗██████╗ ███████╗ █████╗ ██╗      ██╗  ██╗ █████╗ ███████╗██╗  ██╗
╚══███╔╝██╔══██╗██╔════╝██╔══██╗██║      ██║  ██║██╔══██╗██╔════╝██║  ██║
  ███╔╝ ██████╔╝█████╗  ███████║██║      ███████║███████║███████╗███████║
 ███╔╝  ██╔══██╗██╔══╝  ██╔══██║██║      ██╔══██║██╔══██║╚════██║██╔══██║
███████╗██║  ██║███████╗██║  ██║███████╗ ██║  ██║██║  ██║███████║██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

## 🔍 Overview
ZREAL HASH is a Python-based tool that extracts password hashes from encrypted archive files (RAR, ZIP, 7z) in a format compatible with John the Ripper. It provides both interactive and command-line interfaces for easy integration into your security workflows.

## ✨ Features
- Supports multiple archive formats: RAR, ZIP, 7z
- Automatic detection of RAR versions (RAR3/RAR5)
- Interactive mode with user-friendly prompts
- Command-line mode for scripting/automation
- Timeout handling for large files
- Detailed error reporting
- Generates ready-to-use John the Ripper commands

## 📦 Installation
### Prerequisites
- Python 3.6+
- John the Ripper (with rar2john, zip2john, 7z2john utilities)

### Setup
```bash
git clone https://github.com/RestuWibisonoo/zreal-hash.git
cd zreal-hash
chmod +x zreal_hash.py
```

### Install John the Ripper
```bash
# Debian/Ubuntu
sudo apt install john

# RHEL/CentOS
sudo yum install john

# Arch Linux
sudo pacman -S john
```

## 🚀 Usage
### Interactive Mode
```bash
./zreal_hash.py
```
Follow the on-screen prompts to:
1. Enter archive file path
2. View extracted hash
3. Save hash to file
4. Get John the Ripper cracking commands

### Command-line Mode
```bash
./zreal_hash.py /path/to/archive.rar
```
Outputs the hash directly to stdout for piping to other tools

## 🛠️ Examples
### Basic Usage
```bash
$ ./zreal_hash.py secret.zip
$zip2$*0*3*0*b5d6431f4c9b234a*50*4e*8*0*b5d6*5534*...
```

### Full Cracking Workflow
```bash
# Extract hash
./zreal_hash.py documents.rar > doc.hash

# Crack with John
john --format=rar5 --wordlist=rockyou.txt doc.hash

# Show results
john --show doc.hash
```

## 📝 Output Format
The tool generates hashes in John the Ripper compatible format:
- `$rar5$` for RAR5 archives
- `$rar$` for RAR3 archives
- `$zip$` for ZIP archives
- `$7z$` for 7-Zip archives

## 🧩 Technical Details
### Supported Formats
| Format | John Format | Tested Versions |
|--------|-------------|-----------------|
| RAR    | rar/rar5    | RAR3, RAR5      |
| ZIP    | zip         | PKZIP, WinZIP   |
| 7z     | 7z          | 7-Zip 19.00+    |

### Dependencies
- Python Standard Library
- John the Ripper utilities:
  - rar2john
  - zip2john
  - 7z2john

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

## 📜 License
MIT

---

💻 **Happy Hashing!** Let's crack those archives responsibly!
```

## Key Sections Explained:

1. **Overview**: Brief description of what the tool does
2. **Features**: Highlighted capabilities in bullet points
3. **Installation**: Clear setup instructions with OS-specific commands
4. **Usage**: Both interactive and command-line modes explained
5. **Examples**: Practical usage scenarios
6. **Output Format**: Technical details about hash formats
7. **Technical Details**: Table of supported formats and dependencies
8. **Contributing & License**: Standard open-source info

You should:
1. Replace the placeholder banner URL with an actual image
2. Update the git clone URL with your repository
3. Add any additional credits/acknowledgments if needed
4. Consider adding a "Security Note" section if needed for responsible disclosure

Would you like me to add any additional sections or modify any part of this documentation?