from diagnostic import Inspector


def DDX_normal_usecase():
    # Create an instance of the Inspector class
    inspector = Inspector()

    # Define an event
    events = [
        (10, 1, 1, "This is a debug event"),
        (20, 1, 1, "This is a info event"),
        (30, 1, 1, "This is a warning event"),
        (40, 1, 1, "This is a error event"),
        (50, 1, 1, "This is a critical event"),
    ]

    # Set the event status
    for event in events:
        inspector.set_event_status(event)

        # Check if the event is in the events list
        if inspector.look_up(event):
            print("Event found in the events list")

        # Remove the event from the events list
        if inspector.clean_up(event):
            print("Event removed from the events list")

    # Dump the Diagnostic Trouble Codes (DTCs) to a file
    inspector.dump_DTC()


DDX_normal_usecase()
