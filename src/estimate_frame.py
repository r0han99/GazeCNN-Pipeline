def get_valid_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def estimation(start_time, end_time):

    SAMLING_RATE = 200
    starting_frame_number = 200 * start_time
    end_frame_number = 200 * end_time

    return starting_frame_number, end_frame_number



if __name__ == "__main__":
    while True:
        start_time = get_valid_input("Enter the start time in seconds: ")
        end_time = get_valid_input("Enter the end time in seconds: ")

        if start_time < end_time:
            break
        else:
            print("Start time must be greater than end time. Please try again.")

    print(f"Start time: {start_time} seconds")
    print(f"End time: {end_time} seconds")

    confirm = input("Confirm the input (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("Input confirmed.")
        start_frame_number, end_frame_number = estimation(start_time, end_time)

        start_frame_number = int(start_frame_number)
        end_frame_number = int(end_frame_number)
        
    
        print(f"Trial Starts at Frame Number: {start_frame_number}")
        print(f"Trial Ends at Frame Number: {end_frame_number}")

        print('--'*50)
        print(f'In frames decomposed, Start from frames_{start_frame_number} to frames_{end_frame_number} for a complete trial')
        print()

    else:
        print("Input not confirmed or Invalid. Please run the script again to re-enter values.")


    
        
        

