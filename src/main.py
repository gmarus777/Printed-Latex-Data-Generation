# cli.py
import argparse
import subprocess

def docker_image_exists(image_name):
    try:
        subprocess.run(["docker", "inspect", image_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except:
        return False

def build_docker_image(image_name):
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["docker", "build", "-t", image_name, current_dir], check=True)


def run_docker_container(image_name, host_dir, args):
    
    
    # Run the Docker container and capture its ID
    result = subprocess.run(["docker", "run", "-d","-t", image_name], stdout=subprocess.PIPE, check=True, text=True)
    container_id = result.stdout.strip()
    try: 
        subprocess.run(["docker", "exec", container_id, "ls"])
    except:
        cleanup_container(container_id)
    
    # Execute your application inside the Docker container (Replace 'your-application-command' accordingly)
    try:
        command = get_main_command(ApplicationParameters(args))
        print(command)
        subprocess.run(["docker", "exec", container_id, *command], check=True)

        # Copy the Data directory from the Docker container to the host machine
        subprocess.run(["docker", "cp", f"{container_id}:/app/Data", host_dir], check=True)
    except Exception as e:
        print("ERROR: " , e)    
        cleanup_container(container_id)

    # Stop and remove the container
    subprocess.run(["docker", "container", "rm", "-f", container_id], check=True)




def cleanup_container(container_id):
    subprocess.run(["docker", "container", "rm", "-f", container_id], check=True)
    raise Exception("Error occured, container removed")

def cleanup_image():
    subprocess.run(["docker", "image", "rm", "-f", "latex-printed"], check=True)

class ApplicationParameters: 
    def __init__(self, args):
        self.bool_flags ={
            "d": args.download, 
            "g": args.generate,
            "s": args.svg,
            "p": args.png,
        }

        self.str_flags = {
            "urls_file": args.urls_file,
            "filter_words_file": args.filter_words_file,        
        }

        self.int_flags  ={
            "max_formula_size": args.max_formula_size,
            "minimum_formula_size": args.minimum_formula_size,
            "dpi_x": args.dpi_x,
            "dpi_y": args.dpi_y,
            "width": args.width,
            "height": args.height,
        }


class Command: 
    def __init__(self):
        self.command_list = [] 


    def add(self, value):
        self.command_list.append(value)

    def add_bool_flags(self, flags):
        for flag, value in flags.items():
            if value:
                self.add(f"-{flag}")

    def add_int_flags(self, flags):
        for flag, value in flags.items():
            if value:
                self.add(f"--{flag}")
                self.add(str(value))

    def add_str_flags(self, flags):
        for flag, value in flags.items():
            if value:
                self.add(f"--{flag}")
                self.add(str(value))


    def to_list(self):
        return self.command_list




def get_main_command(params: ApplicationParameters):
    command = Command() 

    command.add("python")
    command.add("/app/cli.py")
    command.add_bool_flags(params.bool_flags)
    command.add_str_flags(params.str_flags)
    command.add_int_flags(params.int_flags)

    return command.to_list() 






def main():
    parser = argparse.ArgumentParser(description="Manage my Dockerized app.")
    parser.add_argument("--path", required=True, help="Path to store data on the host machine")
    
    parser.add_argument("-d", "--download", action="store_true", help="Download the dataset")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate the dataset")
    parser.add_argument("-s", "--svg", action="store_true", help="Generate the svg images")
    parser.add_argument("-p", "--png", action="store_true", help="Generate the png images")

    parser.add_argument("--max_formula_size", type=int, help="Max size of formulas to include in bytes")
    parser.add_argument("--minimum_formula_size", type=int, help="Min size of formulas to include in bytes")

    parser.add_argument("--urls-file", type=str, help="File containing urls to download, otherwise use default")
    parser.add_argument("--filter_words_file", type=str, help="File containing words to filter out to add, otherwise use default")
    parser.add_argument("--dpi_x", type=int, help="x-DPI to use for png images")
    parser.add_argument("--dpi_y", type=int, help="y-DPI to use for png images")
    parser.add_argument("--width", type=int, help="Width of png images")
    parser.add_argument("--height", type=int, help="Height of png images")

    
    args = parser.parse_args()
    host_dir = args.path
    image_name = "latex-printed"

    if not docker_image_exists(image_name):
        print("Docker image does not exist, building...")
        build_docker_image(image_name)

    print("Running Docker container...")
    run_docker_container(image_name, host_dir, args)

if __name__ == "__main__":
    main()
