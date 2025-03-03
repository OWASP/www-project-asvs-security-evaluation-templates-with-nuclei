import os
import re
import math

# Function to find .yaml files recursively
def find_yaml_files(root_dir):
    yaml_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.yaml') and re.match(r'(\d+\.)+\d+\.yaml', filename):
                yaml_files.append(os.path.join(dirpath, filename))
    return yaml_files

# Function to update README.md with an HTML table (5 columns, no .yaml extension)
def update_readme(yaml_files):
    readme_file = 'README.md'
    try:
        with open(readme_file, 'r', encoding='utf-8') as file:
            readme_content = file.read()

        # Remove .yaml extension and sort filenames
        yaml_filenames = sorted(set(os.path.splitext(os.path.basename(f))[0] for f in yaml_files))

        # Create a table with 5 columns
        table_rows = ""
        num_files = len(yaml_filenames)
        num_columns = 5
        num_rows = math.ceil(num_files / num_columns) 

        for i in range(num_rows):
            row_files = yaml_filenames[i * num_columns:(i + 1) * num_columns]
            table_rows += "<tr>" + "".join(f"<td>{file}</td>" for file in row_files) + "</tr>\n"

        table_html = f"""<h2 align="center">Available Templates</h2>
<table border="1" cellpadding="5" cellspacing="0" align="center">
        {table_rows}
</table>
</center>
"""

        if "<h2 align=\"center\">Available Templates</h2>" in readme_content:
            h2_index = readme_content.index("<h2 align=\"center\">Available Templates</h2>")

            readme_content = readme_content[:h2_index]

        readme_content += f'{table_html}'
        with open(readme_file, 'w', encoding='utf-8') as file:
            file.write(readme_content)

        print("README.md updated successfully.")

    except FileNotFoundError:
        print(f"{readme_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    root_dir = '../../'
    yaml_files = find_yaml_files(root_dir)
    if yaml_files:
        update_readme(yaml_files)
    else:
        print("No matching YAML files found.")