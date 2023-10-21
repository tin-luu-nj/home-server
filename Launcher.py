from src import executeApplication, executeGenerator

def main():
    print("=================================================================")
    user_input = input(
        """
Choose Program to execute:
[1] Execute Application.
[2] Execute Generator.

Enter number and press Enter:
"""
    )

    print("=================================================================\n")
    if user_input == "1":
        print("Executing Application")
        print("=================================================================\n")
        executeApplication()
        return

    if user_input == "2":
        print("Executing Generator")
        print("=================================================================\n")
        executeGenerator()
        return

    print("No Program Available!")


if __name__ == "__main__":
    main()
# end main