from PIL import Image
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def display_images(change_dict, bill_and_coin_images):
    # Set the size of the final image and create a white background
    output_image_width = 800
    output_image_height = 500
    output_image = Image.new("RGB", (output_image_width, output_image_height), "white")

    # Set the initial position for pasting images
    x_offset, y_offset = 10, 10

    # Load a font for displaying the quantity text
    font_path = "Cash_Detection/LiberationSerif-Regular.ttf"  # Update the path accordingly
    font_size = 36
    font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(output_image)

    for key, value in change_dict.items():
        if key in bill_and_coin_images:
            # Resize the bill/coin image
            img = bill_and_coin_images[key].copy()
            img.thumbnail((300, 300), Image.ANTIALIAS)

            # Paste the bill/coin image onto the output image
            output_image.paste(img, (x_offset, y_offset))

            # Draw the quantity text next to the image
            draw.text((x_offset + img.width + 10, y_offset + img.height // 2 - 10), "{} x {}".format(value, key), font=font, fill="black")


            # Update the y_offset for the next image
            y_offset += img.height + 20

            # Reset the x_offset and update the y_offset if the images reach the bottom of the output image
            if y_offset + img.height > output_image_height:
                y_offset = 10
                x_offset += img.width + 150

    # Show the output image with all the change images and quantities
    output_image_np = cv2.cvtColor(np.array(output_image), cv2.COLOR_RGB2BGR)
    cv2.imshow("Change", output_image_np)
    key = cv2.waitKey(20000)
    if key == ord('q'):
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()


def calculate_change(current_amount, target_amount):
    if current_amount < target_amount:
        print("Error: Current amount is less than the target amount.")
        return

    change = current_amount - target_amount
    print("Change to give back: ${:.2f}".format(change))


    bills_and_coins = [100, 50, 20, 10, 5, 1, 0.25, 0.10, 0.05, 0.01]
    bill_and_coin_names = ["$100 bill", "$50 bill", "$20 bill", "$10 bill", "$5 bill", "$1 bill",
                           "quarter", "dime", "nickel", "penny"]

    change_dict = {}

    for i, value in enumerate(bills_and_coins):
        count = int(change // value)
        if count > 0:
            change_dict[bill_and_coin_names[i]] = count
            change -= count * value

    print("Best combination of coins and bills to give back:")
    for key, value in change_dict.items():
        print("{} x {}".format(value, key))


    return change_dict

def main():
    current_amount = float(input("Please enter the current amount in $00.00 format: ").replace('$', ''))
    target_amount = float(input("Please enter the target amount in $00.00 format: ").replace('$', ''))
    change_dict = calculate_change(current_amount, target_amount)

    bill_and_coin_images = {
       
    }

    display_images(change_dict, bill_and_coin_images)

def load_bill_and_coin_images():
    return {
        "$100 bill": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/100.jpg"),
        "$50 bill": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/50.jpg"),
        "$20 bill": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/20.jpg"),
        "$10 bill": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/10.jpg"),
        "$5 bill": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/5.jpg"),
        "$1 bill": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/1.jpg"),
        "quarter": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/.25.jpg"),
        "dime": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/.10.jpg"),
        "nickel": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/.5.jpg"),
        "penny": Image.open("/home/jetson/CapstoneGUI/Cash_Detection/images/.1.jpg"),
    }

if __name__ == "__main__":
    main()
