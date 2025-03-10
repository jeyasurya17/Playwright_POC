import yaml
import os
from dotenv import load_dotenv
import subprocess
import sys
import webbrowser

def run_tests():
# Load Environment Variables
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of run_suite.py
    env_path = os.path.join(script_dir, ".env")  # Path to env file

    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment variables from: {env_path}")
    else:
        print(f"Warning: .env not found at {env_path}. Ensure it exists.")

    # Read Environment Variables
    suites_to_run = os.getenv("SUITE", "").split(",") if os.getenv("SUITE") else []
    specs_to_run = os.getenv("SPEC", "").split(",") if os.getenv("SPEC") else []
    tags_to_run = os.getenv("TAGS", "").split(",") if os.getenv("TAGS") else []
    workers = os.getenv("WORKERS", "2")  # Default workers is 2

    # Locate and Load `suite.yaml`
    suite_yaml_path = os.path.join(script_dir, "suite.yaml")
    if not os.path.exists(suite_yaml_path):
        print(f"Error: suite.yaml not found at {suite_yaml_path}. Exiting...")
        exit(1)

    with open(suite_yaml_path, "r") as file:
        suite_data = yaml.safe_load(file)
        print(f"Loaded suite.yaml from: {suite_yaml_path}")
        print(f"Suite Data: {suite_data}")

    # Collect Test Paths Based on ENV Variables
    test_paths = []

    if specs_to_run:
        test_paths.extend(specs_to_run)
    elif suites_to_run:
        for suite in suites_to_run:
            if suite in suite_data:
                test_paths.extend(suite_data[suite])

    #Tags to run

    if tags_to_run:
        tags = " or ".join(tags_to_run)
    else:
        tags =""

    # Convert Relative Paths to Absolute Paths
    test_paths = [os.path.abspath(os.path.join(script_dir, "..", path)) for path in test_paths]

    # Debugging Prints
    print("\n=== Debugging Information ===")
    print(f"SUITE env variable: {suites_to_run}")
    print(f"SPEC env variable: {specs_to_run}")
    print(f"TAGS env variable: {tags_to_run}")
    print(f"Tags = {tags}")

    print(f"Workers: {workers}")
    print(f"Test paths collected: {test_paths}")
    print("============================\n")

    # Run tests in parallel at the **suite level**
    if test_paths:
        command = [
            "pytest",
            "--alluredir=allure-results",
            "-n", workers,                # Run with parallel workers
            "-m",tags,
           "--dist=loadgroup",            # Groups tests by custom group marks to ensure they run in the same worker.
            "--verbose",
            "--capture=no",
        ] + test_paths

        print(f"Running tests: {test_paths} with {workers} workers...\n")
        subprocess.run(command)
    else:
        print("No valid test paths found for execution.")

  # Generate Allure report after tests
    generate_allure_report()


def generate_allure_report():
    """Generate and open Allure report automatically."""

    try:
        subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean","--single-file"], check=True)
        print("Allure report generated successfully!")

        # Open the report automatically
        report_index = os.path.join("allure-report", "index.html")
        if os.path.exists(report_index):
            webbrowser.open(f"file://{os.path.abspath(report_index)}")
            print(f"Allure report opened: {report_index}")
        else:
            print(" Failed to open Allure report.")

    except FileNotFoundError:
        print(" Allure CLI not found. Please install Allure manually.")


def install_dependencies():
    """Automatically install missing dependencies, including Allure CLI."""
    print("🔍 Checking and installing required dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    # Install Allure if not available
    try:
        subprocess.run(["allure", "--version"], check=True)
    except FileNotFoundError:
        print(" Allure CLI not found. Installing allure-pytest...")
        subprocess.run([sys.executable, "-m", "pip", "install", "allure-pytest"], check=True)

if __name__ == "__main__":
    install_dependencies()  #This ensures dependencies are installed before tests run
    run_tests()