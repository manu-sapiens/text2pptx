import os
import argparse

def main(include_subdirs):
    root_directory = './'  # Update this path to the directory containing your Python scripts
    output_filename = 'gather_output.txt'
    prefix_filename = 'gather_prefix.txt'
    postfix_filename = 'gather_postfix.txt'
    
    # Prepare to concatenate Python files
    concatenated_content = ''
    
    # Exclude the script itself by name
    script_name = 'gather.py'
    
    if include_subdirs:
        walk = os.walk
    else:
        # Mimic os.walk behavior for just the root directory
        walk = lambda x: [(x, next(os.walk(x))[1], next(os.walk(x))[2])]
    
    # Walk through each file in the directory
    for dirpath, dirnames, filenames in walk(root_directory):
        for filename in filenames:
            if filename.endswith('.py') and filename != script_name:
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, start=root_directory)
                with open(full_path, 'r') as file:
                    # Adding relative path as a comment at the start of its content
                    file_content = f"# {relative_path}\n" + file.read() + "\n\n" + "-"*80 + "\n\n"
                    concatenated_content += file_content
    
    # Combine prefix, all Python files content, and potentially postfix
    final_content = "<CODE>\n" + concatenated_content + "/n</CODE>"
    
    # Check if prefix_filename exists and append its content if it does
    if os.path.exists(prefix_filename):
        with open(prefix_filename, 'r') as file:
            prefix_content = file.read()
        final_content = prefix_content + "\n" + final_content
            
    # Check if postfix_filename exists and append its content if it does
    if os.path.exists(postfix_filename):
        with open(postfix_filename, 'r') as file:
            postfix_content = file.read()
        final_content = final_content + "\n" + postfix_content
    
    # Write everything to the output file
    with open(output_filename, 'w') as file:
        file.write(final_content)

    print(f"All python files have been concatenated and prefixed. Output is in {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate Python scripts with optional subdirectory inclusion.')
    parser.add_argument('--include-subdirs', action='store_true', help='Include subdirectories in the search for Python files.')
    args = parser.parse_args()

    main(args.include_subdirs)
