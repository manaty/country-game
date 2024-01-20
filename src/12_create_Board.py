import os
from PIL import Image

def create_image_with_flags_and_map(flags_path, output_path):
    # Define dimensions for the base image (inside the border)
    width, height = 5339, 5339  # Example dimensions

    # Create a new image with the specified background color
    base_image = Image.new('RGB', (width, height), '#011b43')


    # Add flags to the sides
    # itereate over all files in the flags_path folder
    flagPosition = (0, 0)  # Initial position
    flagSize = (356, 232)
    count=0
    flag_path_list = os.listdir(flags_path)
    #filter only png files
    flag_path_list = [x for x in flag_path_list if x.endswith(".png")]
    #sort the list of flags
    flag_path_list.sort()

    for flag_path in flag_path_list:
        flag = Image.open(os.path.join(flags_path, flag_path))
        
        print(f"Adding {flag_path} at {flagPosition}")
        # draw the flag on the base image
        base_image.paste(flag, (flagPosition[0], flagPosition[1], flagPosition[0] + flagSize[0], flagPosition[1] + flagSize[1]))
        if count == 0:
            positionIncrement = (flagSize[0], 0)
        elif count == 14:
            positionIncrement = (0, flagSize[1])
        elif count == 36:
            positionIncrement = (flagSize[0]*(-1), 0)
        elif count == 50:
            positionIncrement = (0, flagSize[1]*(-1))
        flagPosition = (flagPosition[0] + positionIncrement[0], flagPosition[1] + positionIncrement[1])
        count += 1

    # Add a border
    border_color = (0, 0, 0)  # Black border, for example
    border_width = 30
    board_image = Image.new('RGB', (width + 2*border_width, height + 2*border_width), border_color)
    board_image.paste(base_image, (border_width, border_width))

    # Save the final image
    board_image.save(output_path)

    
flags_path = "../files/flag/"
output_path = '../files/board/country_game_board.png'
create_image_with_flags_and_map(flags_path, output_path)
