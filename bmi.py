def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation."""
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")
    return bmr

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure (TDEE) based on activity level."""
    activity_levels = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }
    if activity_level.lower() not in activity_levels:
        raise ValueError("Invalid activity level.")
    return bmr * activity_levels[activity_level.lower()]
