
import math



# main function
def main():
    # Menu options for the user to choose from
    print('''
            Investment - To calculate theamount of interest you'll earn on your investment
            Bond       - To calculate the amount you'll have to pay on the home loan.
          ''')

    user_choice = input("Enter either 'Investment' or 'Bond' from the menu to proceed: ").strip().lower()

    # if the user selects to invest, the investment() function is run
    if user_choice == 'investment':
        # run investment()
        investment() 
    # if the user seects to bond, the bond() function is run
    elif user_choice == 'bond':
        # run bon()
        bond()
    else: 
        print("Invalid choice. Please enter 'investment' or 'bond'.")


# function for the investment plan
def investment():
    # User inputs the deposit amount, interest rate, and investment duration
    deposit_amount = float(input("please enter the amount you want to deposit: "))
    interest_rate = float(input("Please enter the interest rate: "))/100
    num_year_invest = int(input("Please enter the amount of years you want to invest: "))

    #uses must choose how they want to invest
    interest = input("Would you like to calculate your investment using simple or compound interest?: ")

    if interest == 'simple':
        #calculation for simple interest
        investment_return = deposit_amount * (1 + interest_rate  * num_year_invest)
        print(f"Your total invesment will be: R{investment_return}")
    elif interest == 'compound':
        #calculation for compound interest
        investment_return = deposit_amount * math.pow(1 + (interest_rate), num_year_invest) 
        print(f"Your total invesment will be: R{investment_return}")
    else: 
        print("Invalid choice. Please enter 'simple' or 'compound'.")
        ## Exit the function if input is invalid
    
        

# function for the bond planin
def bond():
    # User inputs the present house value, interest rate, and repayment duration in months
    present_house_value = float(input("Please enter the present house value: "))
    interest_rate = float(input("Please enter the interest rate: ")) / 100 / 12
    num_months = int(input("Please enter the number of months you want to pay the bond over: "))
    # Calculation for bond repayments
    monthly_payments = (interest_rate * present_house_value) / (1 - math.pow((1 + interest_rate),-(num_months)))

    print(f"Your monthly payments are: R{monthly_payments}")

# run main()
main()
