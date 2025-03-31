import os
import re
import math

# Function to find .yaml files recursively in all directories under templates
def find_yaml_files(root_dir):
    yaml_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.yaml') and re.match(r'(\d+\.)+\d+\.yaml', filename):
                yaml_files.append(os.path.join(dirpath, filename))
    return yaml_files

# Function to list all templates with a default ❌ mark
def initialize_template_status(yaml_files):
    template_status = {}
    for file in yaml_files:
        base_name = os.path.splitext(os.path.basename(file))[0]
        template_status[base_name] = "❌"  # Default to ❌
    return template_status

# Function to check if a related vulnerable page exists and update the status
def update_vulnerable_status(template_status, vuln_dir):
    for vuln_file in os.listdir(vuln_dir):
        if vuln_file.startswith("ASVS_"):
            base_name = vuln_file.replace("ASVS_", "").replace("_", ".")
            if base_name in template_status:
                template_status[base_name] = "✔️"  # Update to ✔️ if found

# Function to update README.md with a table (2 columns: Template Name, Vulnerable Page Exists)
def update_readme(template_status, root_dir):
    readme_file = 'README.md'
    github_base_url = "https://github.com/OWASP/www-project-asvs-security-evaluation-templates-with-nuclei/blob/dev/templates/"
    
    try:
        with open(readme_file, 'r', encoding='utf-8') as file:
            readme_content = file.read()

        # Sort templates based on the first two sections of the version number
        sorted_templates = sorted(template_status.items(), key=lambda x: tuple(map(int, x[0].split(".")[:2])))

        # Create table rows with 2 columns
        table_rows = ""
        for file_name, status in sorted_templates:
            file_link = '<a href="' + github_base_url + file_name + '.yaml">' + file_name + '</a>'
            table_rows += "<tr><td>" + file_link + "</td><td align='center'>" + status + "</td></tr>\n"

        table_html = f'''<h2 align="center">Available Templates</h2>
<table border="1" cellpadding="5" cellspacing="0" align="center">
<tr><th>Template Name</th><th>Vulnerable Page Exists</th></tr>
{table_rows}
</table>
</center>
'''

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
    root_dir = 'templates'
    vuln_dir = 'Vulnerable-Pages'
    yaml_files = find_yaml_files(root_dir)
    
    if yaml_files:
        template_status = initialize_template_status(yaml_files)
        update_vulnerable_status(template_status, vuln_dir)
        update_readme(template_status, root_dir)
    else:
        print("No matching YAML files found.")
