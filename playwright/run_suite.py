import yaml
import os
from dotenv import load_dotenv
import subprocess

# Load Environment Variables
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of run_suite.py
env_path = os.path.join(script_dir, "env.env")  # Path to env file

if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"Loaded environment variables from: {env_path}")
else:
    print(f"Warning: env.env not found at {env_path}. Ensure it exists.")

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
    # "--dist=loadgroup",            # Groups tests by custom group marks to ensure they run in the same worker.
        "--verbose",
        "--capture=no",
    ] + test_paths

    print(f"Running tests: {test_paths} with {workers} workers...\n")
    subprocess.run(command)
else:
    print("No valid test paths found for execution.")