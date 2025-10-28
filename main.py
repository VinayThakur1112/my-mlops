#!/usr/bin/env python3
"""
main.py - Unified CLI / Interactive entry point for:
  - Resource Service (create/delete resource groups)
  - Data Pipeline (placeholder)
  - Model Deployment (placeholder)

Behavior is controlled by config/config.json (interactive true/false).
"""

import sys
import time
import json
import os
from colorama import Fore, Style, init

# Import resource functions (assumes azure_resource_group.py exists in same folder)
from infra.resource_group import create_resource_group, delete_resource_group

# Initialize colorama
init(autoreset=True)


# -----------------------
# Config loader
# -----------------------
def load_app_config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return json.load(f)


# -----------------------
# UI / Printing helpers
# -----------------------
def print_divider(char="─"):
    print(f"{Fore.CYAN}{char * 60}{Style.RESET_ALL}")


def print_header_for(service_name):
    # Dynamic header depending on selected service
    title_map = {
        "resource": "Resource Management Service",
        "pipeline": "Data Pipeline Service",
        "model": "Model Deployment Service"
    }
    subtitle = title_map.get(service_name, "Azure Tooling")
    print()
    print_divider("═")
    print(f"{Fore.CYAN}{Style.BRIGHT}⚙️  {subtitle.center(46)}")
    print_divider("═")
    print()


def print_usage():
    print(f"{Fore.YELLOW}Usage (non-interactive):{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py resource create <env> <rg_name> [location]{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py resource delete <env> <rg_name>{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py pipeline run <env> <pipeline_name>{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}python main.py model deploy <env> <model_name>{Style.RESET_ALL}")
    print()
    print(f"{Fore.LIGHTBLACK_EX}Run without args when interactive mode is ON in config.{Style.RESET_ALL}\n")


def status(msg, kind="info"):
    icons = {
        "info": f"{Fore.CYAN}ℹ️ ",
        "action": f"{Fore.MAGENTA}🚀 ",
        "success": f"{Fore.GREEN}✅ ",
        "warn": f"{Fore.YELLOW}⚠️ ",
        "error": f"{Fore.RED}❌ ",
    }
    print(f"{icons.get(kind, '')}{msg}{Style.RESET_ALL}")


# -----------------------
# Placeholder functions for pipeline / model
# -----------------------
def run_pipeline(env_name, pipeline_name, cfg):
    """
    Placeholder: replace this with your actual pipeline invocation.
    """
    print_header_for("pipeline")
    status(f"Preparing to run pipeline '{pipeline_name}' in env '{env_name}'...", "action")
    # Example: access config values if needed
    contact = cfg.get("contact_email", "n/a")
    status(f"Contact: {contact}", "info")
    # Simulate long-running task
    time.sleep(1.0)
    status(f"Pipeline '{pipeline_name}' finished successfully.", "success")


def deploy_model(env_name, model_name, cfg):
    """
    Placeholder: replace this with your model deployment logic.
    """
    print_header_for("model")
    status(f"Preparing to deploy model '{model_name}' in env '{env_name}'...", "action")
    time.sleep(1.0)
    status(f"Model '{model_name}' deployed successfully.", "success")


# -----------------------
# Interactive flows
# -----------------------
def interactive_menu(cfg):
    print()
    status("Interactive mode enabled.", "info")
    # choose service
    print("Select service:")
    print(f"  1) Resource Service")
    print(f"  2) Data Pipeline")
    print(f"  3) Model Deployment")
    choice = input(f"\nEnter choice [1-3] (default 1): ").strip() or "1"

    if choice not in ("1", "2", "3"):
        status("Invalid choice. Exiting.", "error")
        return

    if choice == "1":
        interactive_resource_flow(cfg)
    elif choice == "2":
        interactive_pipeline_flow(cfg)
    else:
        interactive_model_flow(cfg)


def interactive_resource_flow(cfg):
    print_header_for("resource")
    env_name = input(f"Environment [{cfg.get('default_env', 'dev')}]: ").strip() or cfg.get("default_env", "dev")
    status(f"Selected env: {env_name}", "info")

    print("\nSelect action:")
    print("  1) Create Resource Group")
    print("  2) Delete Resource Group")
    a = input("Enter choice [1-2] (default 1): ").strip() or "1"

    if a == "1":
        rg_name = input("Resource group name: ").strip()
        if not rg_name:
            status("Resource group name is required. Aborting.", "error")
            return
        location = input(f"Location [{cfg.get('default_location', 'eastus')}]: ").strip() or cfg.get('default_location', 'eastus')
        status(f"Creating resource group '{rg_name}' in '{location}'...", "action")
        create_resource_group(env_name, rg_name, location)
        status("Create operation completed.", "success")
    elif a == "2":
        rg_name = input("Resource group name to delete: ").strip()
        if not rg_name:
            status("Resource group name is required. Aborting.", "error")
            return
        confirm = input(f"Are you sure you want to delete '{rg_name}'? Type 'yes' to confirm: ").strip().lower()
        if confirm == "yes":
            status(f"Deleting resource group '{rg_name}'...", "action")
            delete_resource_group(env_name, rg_name)
            status("Delete operation completed.", "success")
        else:
            status("Delete cancelled.", "warn")
    else:
        status("Invalid action selected.", "error")


def interactive_pipeline_flow(cfg):
    print_header_for("pipeline")
    env_name = input(f"Environment [{cfg.get('default_env', 'dev')}]: ").strip() or cfg.get("default_env", "dev")
    pipeline_name = input("Pipeline name to run: ").strip()
    if not pipeline_name:
        status("Pipeline name is required. Aborting.", "error")
        return
    status(f"Running pipeline '{pipeline_name}' in env '{env_name}'...", "action")
    run_pipeline(env_name, pipeline_name, cfg)


def interactive_model_flow(cfg):
    print_header_for("model")
    env_name = input(f"Environment [{cfg.get('default_env', 'dev')}]: ").strip() or cfg.get("default_env", "dev")
    model_name = input("Model name to deploy: ").strip()
    if not model_name:
        status("Model name is required. Aborting.", "error")
        return
    status(f"Deploying model '{model_name}' in env '{env_name}'...", "action")
    deploy_model(env_name, model_name, cfg)


# -----------------------
# Non-interactive (CLI) flows
# -----------------------
def cli_dispatch(args, cfg):
    # args[0] = service (resource|pipeline|model)
    # args[1] = action
    service = args[0].lower()
    action = args[1].lower() if len(args) > 1 else None

    if service == "resource":
        print_header_for("resource")
        if action == "create":
            # expected: resource create <env> <rg_name> [location]
            if len(args) < 4:
                status("Insufficient args for resource create.", "error")
                print_usage()
                return
            env_name = args[2]
            rg_name = args[3]
            location = args[4] if len(args) > 4 else cfg.get("default_location")
            status(f"Creating resource group '{rg_name}' in env '{env_name}' (location: {location})...", "action")
            create_resource_group(env_name, rg_name, location)
            status("Create operation completed.", "success")

        elif action == "delete":
            # expected: resource delete <env> <rg_name>
            if len(args) != 4:
                status("Insufficient args for resource delete.", "error")
                print_usage()
                return
            env_name = args[2]
            rg_name = args[3]
            status(f"Deleting resource group '{rg_name}' in env '{env_name}'...", "action")
            delete_resource_group(env_name, rg_name)
            status("Delete operation completed.", "success")
        else:
            status("Unknown resource action. Use create or delete.", "error")
            print_usage()

    elif service == "pipeline":
        print_header_for("pipeline")
        # expected: pipeline run <env> <pipeline_name>
        if action == "run":
            if len(args) < 4:
                status("Insufficient args for pipeline run.", "error")
                print_usage()
                return
            env_name = args[2]
            pipeline_name = args[3]
            run_pipeline(env_name, pipeline_name, cfg)
        else:
            status("Unknown pipeline action. Use run.", "error")
            print_usage()

    elif service == "model":
        print_header_for("model")
        # expected: model deploy <env> <model_name>
        if action == "deploy":
            if len(args) < 4:
                status("Insufficient args for model deploy.", "error")
                print_usage()
                return
            env_name = args[2]
            model_name = args[3]
            deploy_model(env_name, model_name, cfg)
        else:
            status("Unknown model action. Use deploy.", "error")
            print_usage()
    else:
        status("Unknown service. Choose resource|pipeline|model.", "error")
        print_usage()


# -----------------------
# Entry point
# -----------------------
def main():
    try:
        cfg = load_app_config()
    except Exception as e:
        print(f"{Fore.RED}Failed to load config: {e}{Style.RESET_ALL}")
        sys.exit(1)

    is_interactive = bool(cfg.get("interactive", False))

    # If interactive mode enabled and no CLI args, run interactive menu
    if is_interactive and len(sys.argv) == 1:
        interactive_menu(cfg)
        return

    # Non-interactive: expect CLI args (service action ...)
    if len(sys.argv) == 1:
        # No args provided and interactive is off
        print_header_for("resource")
        status("No arguments provided and interactive mode is disabled.", "error")
        print_usage()
        return

    # Parse CLI args (skip script name)
    cli_args = sys.argv[1:]
    # expected: <service> <action> ...
    cli_dispatch(cli_args, cfg)


if __name__ == "__main__":
    main()