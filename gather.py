import os

def main():
    root_directory = './'  # Update this path to the directory containing your Python scripts
    output_filename = 'gather_output.txt'
    prefix_filename = 'gather_prefix.txt'
    postfix_filename = 'gather_postfix.txt'
    
    # Prepare to concatenate Python files
    concatenated_content = ''
    
    # Exclude the script itself by name
    script_name = 'gather.py'
    
    # Walk through each file in the directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.py') and filename != script_name:
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, start=root_directory)
                with open(full_path, 'r') as file:
                    # Adding relative path as a comment at the start of its content
                    file_content = f"# {relative_path}\n" + file.read() + "\n\n" + "-"*80 + "\n\n"
                    concatenated_content += file_content
    
    # Combine prefix, all Python files content, and potentially postfix
    final_content = "<CODE>\n"+concatenated_content+"/n</CODE>"
    
    # Check if postfix.txt exists and append its content if it does
    
    #  Check if prefix_filename exists and append its content if it does
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
    main()
