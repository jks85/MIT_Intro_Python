'''
Write a program to calculate how many months it will take you to save up enough money for a down
payment. You will want your main variables to be floats, so you should cast user inputs to floats.

'''


def house_hunting():

    # inputs
    annual_salary = float(input('Enter your annual salary:'))
    portion_saved = float(input('Enter the percent of your salary to save, as a decimal:'))
    total_cost = float(input('Enter the cost of your dream home:'))

    # house info
    total_down = 0.25 * total_cost  # % of home price to b e paid down (upfront)

    # salary info

    monthly_salary = annual_salary / 12

    # savings info
    current_savings = 0 # initial savings
    r = 0.04 # interest rate

    months = 0 # track number of months
    while current_savings < total_down:
        current_savings = portion_saved*monthly_salary + (r/12)*current_savings + current_savings
        months += 1
    print('Enter your annual salary:',annual_salary)
    print('Enter the percent of your salary to save, as a decimal:',portion_saved)
    print('Enter the cost of your dream home:',total_cost)
    return print('Number of months:',months)


house_hunting()