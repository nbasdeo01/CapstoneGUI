from Bill_detect import detect_cash
from Coin_detect import update_total_price
from calc import calculate_change, display_images, load_bill_and_coin_images
import open_cash_box

def main():
    target_amount = float(input("Please enter price in $00.00 format $").replace('$', ''))
    total_amount = detect_cash(target_amount)
    print("Total amount after bills detection: ${:.2f}".format(total_amount))

    # Check if total_amount is equal to or greater than target_amount after Bill_detect
    if total_amount >= target_amount:
        print("Skipping coins detection.")
        updated_total_amount = total_amount
    else:
        # Run Coin_detect
        updated_total_amount, _ = update_total_price(total_amount, target_amount)
        print("Total amount after coins detection: ${:.2f}".format(updated_total_amount))

    # Run change_calculator
    change_dict = calculate_change(updated_total_amount, target_amount)

    # Check if there is any change due
    if sum(change_dict.values()) > 0:
        # Load bill and coin images
        bill_and_coin_images = load_bill_and_coin_images()

        # Display images
        display_images(change_dict, bill_and_coin_images)

        # Call the function to open the cash register box
        open_cash_box.open_cash_register()
    else:
        print("No change due. Not opening cash register box.")


if __name__ == "__main__":
    main()

