from src.pyPkmHome import scapePkhHomeScreenCapture


def main():
    """
    Main function that calls the scapePkhHomeScreenCapture function from the pyPkmHome module.
    """
    print("=================================================================")
    user_input = input(
        """
Choose Program to execute:
[1] Scraping Pokemon HOME information from Nintendo Switch Capture pictures.

Enter number and press Enter:
"""
    )

    print("=================================================================\n")
    if user_input == "1":
        print("Executing scapePkhHomeScreenCapture")
        print("=================================================================\n")
        scapePkhHomeScreenCapture()

    else:
        print("No Program Available!")

    print("\n=================================================================")
    print("||                           Finished!                         ||")
    print("=================================================================")


if __name__ == "__main__":
    # If this script is run as the main program, call the main function.
    main()

################################################################################
#                                END OF FILE                                   #
################################################################################
