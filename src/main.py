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
    subprocess.run(["docker", "build", "-t", image_name, "."], check=True)

def run_docker_container(image_name, host_dir):
    # Run the Docker container and capture its ID
    result = subprocess.run(["docker", "run", "-d","-t", image_name], stdout=subprocess.PIPE, check=True, text=True)
    container_id = result.stdout.strip()
    subprocess.run(["docker", "exec", container_id, "ls"])
    # Execute your application inside the Docker container (Replace 'your-application-command' accordingly)
    try:
        subprocess.run(["docker", "exec", container_id, "python", "/app/cli.py", "-d", "-g", "-s", "-p"], check=True)

        # Copy the Data directory from the Docker container to the host machine
        subprocess.run(["docker", "cp", f"{container_id}:/app/Data", host_dir], check=True)
    except:
        print("ERROR: ")

    # Stop and remove the container
    subprocess.run(["docker", "container", "rm", "-f", container_id], check=True)


def main():
    parser = argparse.ArgumentParser(description="Manage my Dockerized app.")
    parser.add_argument("--path", required=True, help="Path to store data on the host machine")

    args = parser.parse_args()
    host_dir = args.path
    image_name = "latex-printed"

    if not docker_image_exists(image_name):
        print("Docker image does not exist, building...")
        build_docker_image(image_name)

    print("Running Docker container...")
    run_docker_container(image_name, host_dir)

if __name__ == "__main__":
    main()
