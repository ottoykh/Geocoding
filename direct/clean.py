def clean_data(input_file_path, output_file_path):
    """
    Cleans the data in the input file and saves the cleaned data to the output file.
    
    Args:
        input_file_path (str): The path to the input file.
        output_file_path (str): The path to the output file.
    """
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: {input_file_path} not found.")
        return

    cleaned_lines = [line.replace("N/A,", "") for line in lines]

    try:
        with open(output_file_path, 'w') as file:
            file.writelines(cleaned_lines)
    except IOError:
        print(f"Error: Unable to write to {output_file_path}.")
        return

    print(f"Cleaned data has been saved to {output_file_path}")