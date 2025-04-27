#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Print enhanced ASCII art banner"""
    print(r"""
███████╗██████╗ ███████╗ █████╗ ██╗      ██╗  ██╗ █████╗ ███████╗██╗  ██╗
╚══███╔╝██╔══██╗██╔════╝██╔══██╗██║      ██║  ██║██╔══██╗██╔════╝██║  ██║
  ███╔╝ ██████╔╝█████╗  ███████║██║      ███████║███████║███████╗███████║
 ███╔╝  ██╔══██╗██╔══╝  ██╔══██║██║      ██╔══██║██╔══██║╚════██║██╔══██║
███████╗██║  ██║███████╗██║  ██║███████╗ ██║  ██║██║  ██║███████║██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """)
    print("Advanced Archive Hash Extractor for John the Ripper\n")
    print("Supported formats: RAR, ZIP, 7z\n")

def clean_file_path(input_path):
    """Clean and normalize file path"""
    return str(Path(input_path.strip().strip("'\"").strip()).expanduser().resolve())

def find_john_tool(file_ext):
    """Locate appropriate john tool for file type with better detection"""
    tools = {
        '.rar': ['rar2john', 'rar2john'],
        '.zip': ['zip2john', 'keepass2john'],
        '.7z': ['7z2john', 'keepass2john']
    }
    
    tool_names = tools.get(file_ext.lower(), [])
    
    # Search in common paths
    search_paths = [
        '/usr/bin',
        '/usr/local/bin',
        '/usr/sbin',
        '/opt/john/run',
        '/usr/share/john',
        '/usr/local/share/john',
        str(Path.home() / 'john' / 'run')
    ]
    
    for tool_name in tool_names:
        for path in search_paths:
            tool_path = os.path.join(path, tool_name)
            if os.path.exists(tool_path):
                return tool_path
    
    return None

def extract_archive_hash(file_path):
    """Extract archive hash with better error handling"""
    file_ext = os.path.splitext(file_path)[1].lower()
    john_tool = find_john_tool(file_ext)
    
    if not john_tool:
        supported_formats = ", ".join([".rar", ".zip", ".7z"])
        print(f"\n❌ Error: No extractor found for {file_ext or 'unknown'} files!")
        print(f"Supported formats: {supported_formats}")
        print("\nPlease install John the Ripper with all components:")
        print("  Debian/Ubuntu: sudo apt install john")
        print("  RHEL/CentOS: sudo yum install john")
        print("  Arch: sudo pacman -S john")
        print("Or build from source: https://github.com/openwall/john")
        return None
    
    try:
        result = subprocess.run(
            [john_tool, file_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=300  # 5 minutes timeout for large files
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  Timeout: {os.path.basename(john_tool)} took too long (file may be too large)")
        return None
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {os.path.basename(john_tool)}:")
        print(f"Exit code: {e.returncode}")
        if e.stderr:
            print(f"Error message: {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return None

def get_john_format(file_path):
    """Determine John format with better detection"""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.rar':
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                if b'Rar!\x1a\x07\x01\x00' in header:
                    return 'rar5'
                elif b'Rar!\x1a\x07\x00' in header:
                    return 'rar'
        except:
            return 'rar'  # fallback
    
    format_map = {
        '.zip': 'zip',
        '.7z': '7z'
    }
    
    return format_map.get(file_ext, 'unknown')

def main():
    print_banner()

    # Get file path from user
    while True:
        file_input = input("📁 Masukkan path file archive (atau 'q' untuk keluar): ").strip()
        if file_input.lower() == 'q':
            return
        
        file_path = clean_file_path(file_input)
        
        # Verify file exists
        print(f"\n🔍 Memverifikasi file: {file_path}")
        if not os.path.exists(file_path):
            print("\n❌ File tidak ditemukan!")
            print("Pastikan:")
            print(f"1. Path benar: {file_path}")
            print("2. Gunakan tab autocomplete untuk menghindari typo")
            print("3. File memiliki permission yang tepat")
            continue
        
        if not os.path.isfile(file_path):
            print("\n❌ Path yang dimasukkan bukan file!")
            continue

        # Check file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in ['.rar', '.zip', '.7z']:
            print("\n❌ Format file tidak didukung!")
            print("Hanya mendukung: .rar, .zip, .7z")
            continue

        # Extract the hash
        print(f"\n⏳ Mengekstrak hash {file_ext.upper()} (mungkin butuh waktu untuk file besar)...")
        archive_hash = extract_archive_hash(file_path)
        
        if not archive_hash:
            print("\n❌ Gagal mengekstrak hash archive")
            continue
            
        print("\n✅ Hash archive yang kompatibel dengan John:")
        print("-" * 60)
        print(archive_hash)
        print("-" * 60)

        # Save to file option
        save = input("\n💾 Simpan hash ke file? (y/n): ").strip().lower()
        if save == 'y':
            default_out = f"{os.path.basename(file_path)}.hash"
            output_file = input(f"Masukkan nama file output [{default_out}]: ").strip()
            output_file = output_file if output_file else default_out
            
            try:
                with open(output_file, 'w') as f:
                    f.write(archive_hash)
                print(f"\n✅ Hash disimpan di: {os.path.abspath(output_file)}")
                
                # Show appropriate john command
                john_format = get_john_format(file_path)
                print(f"\n🔧 Contoh perintah John:")
                print(f"john --format={john_format} --wordlist=rockyou.txt {output_file}")
                print(f"john --format={john_format} --show {output_file}")
                print("\n💡 Tips: Gunakan '--fork=4' untuk multi-core processing")
            except Exception as e:
                print(f"\n❌ Gagal menyimpan file: {str(e)}")
        
        print("\n🎉 Selesai! Anda bisa menggunakan hash di atas dengan John the Ripper")
        print("Tekan Enter untuk melanjutkan atau 'q' untuk keluar...")
        if input().strip().lower() == 'q':
            break

if __name__ == "__main__":
    try:
        # Command line mode
        if len(sys.argv) > 1:
            file_path = clean_file_path(sys.argv[1])
            if os.path.exists(file_path):
                hash_result = extract_archive_hash(file_path)
                if hash_result:
                    print(hash_result)
                    sys.exit(0)
                else:
                    sys.exit(1)
            else:
                print(f"File not found: {file_path}")
                sys.exit(1)
        else:
            # Interactive mode
            main()
    except KeyboardInterrupt:
        print("\n🛑 Program dihentikan oleh pengguna")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)