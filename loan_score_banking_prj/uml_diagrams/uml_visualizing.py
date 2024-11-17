from plantuml import PlantUML
import os

uml_file_path = 'uml_diagrams/uml1.txt' #!!!!!!!!!!!CHANGE THE NAME!!!!!!!!!!!!!!

#let it be, used after encounter an error
print("Current working directory:", os.getcwd())

if not os.path.isfile(uml_file_path):
    print(f"Error: The file {uml_file_path} does not exist.")
    exit(1)

with open(uml_file_path, 'r') as file:
    plantuml_code = file.read()

plantuml_server = PlantUML(url='http://www.plantuml.com/plantuml/img/')

output_directory = 'uml_diagrams/output_pngs/'
output_filename = 'uml_diagram1.png' #!!!!!!!!!!!CHANGE THE NAME!!!!!!!!!!!!!!
output_file = os.path.join(output_directory, output_filename)

os.makedirs(output_directory, exist_ok=True)

temp_file = 'uml_temp.puml'
with open(temp_file, 'w') as file:
    file.write(plantuml_code)

plantuml_server.processes_file(temp_file, outfile=output_file)
print(f'UML diagram has been saved to {output_file}')