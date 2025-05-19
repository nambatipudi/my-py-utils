import os
import argparse

def collect_files_as_markdown(root_folder, extensions, output_file):
    extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# 📦 Collected Source Files\n\n")

        for foldername, _, filenames in os.walk(root_folder):
            for filename in filenames:
                if os.path.splitext(filename)[1].lower() in extensions:
                    file_path = os.path.join(foldername, filename)
                    language = os.path.splitext(filename)[1].lstrip('.')

                    out.write(f"## 📄 `{file_path}`\n\n")
                    out.write(f"```{language}\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"// Error reading file: {e}")
                    out.write("\n```\n\n")

def main():
    parser = argparse.ArgumentParser(description='Collect code files and write them to a Markdown (.md) file.')
    parser.add_argument('root_folder', help='Root directory to search files in')
    parser.add_argument('--ext', nargs='+', required=True, help='List of file extensions (e.g., java py js)')
    parser.add_argument('--out', required=True, help='Output Markdown file path (e.g., code_prompt.md)')

    args = parser.parse_args()
    collect_files_as_markdown(args.root_folder, args.ext, args.out)

if __name__ == "__main__":
    main()
