import sys
from azure_resource_group import create_resource_group, delete_resource_group

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py create <resource_group_name> <location>")
        print("  python main.py delete <resource_group_name>")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "create":
        if len(sys.argv) != 4:
            print("Usage: python main.py create <resource_group_name> <location>")
            sys.exit(1)
        rg_name = sys.argv[2]
        location = sys.argv[3]
        create_resource_group(rg_name, location)

    elif action == "delete":
        if len(sys.argv) != 3:
            print("Usage: python main.py delete <resource_group_name>")
            sys.exit(1)
        rg_name = sys.argv[2]
        delete_resource_group(rg_name)

    else:
        print("Invalid action. Use 'create' or 'delete'.")

if __name__ == "__main__":
    main()