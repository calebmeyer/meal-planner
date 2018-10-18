
# coding: utf-8

# # Running me!
# To run this notebook, click the Cell menu item above, then click Run All

# # Read in Data
# First we have to read in the meal data from the csv file. We're using pandas since it has better support for working with the data than a simple python list of lists.

# In[1]:


import pandas as pd

df = pd.read_csv("meals.csv")


# In[2]:


df.loc[df['category'] == 'Pasta'] # just to see the data


# # Setup Days List
# Next we have to get a list of the days we're planning for.

# In[3]:


days = [
    "Friday1", "Saturday1", "Sunday1", "Monday1", "Tuesday1", "Wednesday1", "Thursday1",
    "Friday2", "Saturday2", "Sunday2", "Monday2", "Tuesday2", "Wednesday2", "Thursday2",
]


# # Add Validations
# There's quite a few things we need to check for a given meal. Eventually we may extend this to work for breakfast and lunch, and you don't want to have a dinnery food selected for breakfast. For now we just want to make sure that any meal selected for Tuesday feeds a crowd, and that we don't have the same category twice in a row.

# In[4]:


def valid(day, meal):
    """ A meal is valid if it feeds enough people """
    if "Tuesday" not in day:
        return True # Today is not Tuesday, so any meal will work
    else:
        if meal.feeds_a_crowd.item() == "Yes":
            return True # today is Tuesday and the meal feeds a crowd
        return False # today is Tuesday and the meal does not feed a crowd


# # Pick the Meals
# Now we need to go through and choose a meal for each day. We'll add a column `already_used` to the dataframe, initialized to False, then begin picking meals.

# In[5]:


df["already_used"] = False


# In[6]:


df.head(5)


# In[7]:


days_meals = {} # we'll use a dictionary storing the name of the day mapped to the name of the meal
for day in days:
    found_valid_meal = False
    previous_meal = None
    while not found_valid_meal:
        # choose a random meal
        meal = df.sample()
        if meal.already_used.bool():
            continue # start over at the while loop
        if not valid(day, meal):
            continue
        if previous_meal is not None:
            if str(previous_meal.category.item()) == str(meal.category.item()):
                continue

        # if we passed all the above checks, then this meal is perfect
        days_meals[day] = meal
        df.at[meal.index, 'already_used'] = True
        previous_meal = meal
        found_valid_meal = True


# # Display our choices
# Now we just need a nice format for display

# In[8]:


for day, meal in days_meals.items():
    dayname = day[:-1]
    daynum = int(day[-1])
    ordinal = 'first' if daynum == 1 else 'second'

    print("We'll be having {} on the {} {}".format(meal.name.item(), ordinal, dayname))
