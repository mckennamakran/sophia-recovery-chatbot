# relapse chatbot named Sophia helps addicts learn about relapse, predict whether they might relapse, and based on that percentage, give them advice
import csv
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

FILE_NAME = '../LinearRegression/sophia_dataset.csv'

# ---------------------User Info---------------------
def user_info():
    # ---------------------Basic Info---------------------
    print("First, let's start with some basic information so I can better understand your situation.")

    user_data = {}

    user_data['first_name'] = str(input("First Name: "))
    user_data['surname'] = str(input("Last Name: "))

    age = int(input("Age: "))
    while age <= 0 or age >= 120:
        print("Invalid input, please try again.")
        age = int(input("Age: "))
    user_data['age'] = age

    valid_options = ['male', 'female', 'm', 'f', 'other']
    gender = None

    while gender not in valid_options:
        gender_input = input("Enter your gender (Male/Female/M/F/Other): ").lower()
        if gender_input in valid_options:
            gender = user_data['gender'] = gender_input
        else:
            print("Invalid input, please try again.")


    # ---------------------Addiction Info---------------------
    print(f"Nice to meet you, {user_data['first_name']}. Let's dive straight into it.\n")
    print("-------------------------------------------\n")
    print("Section 1: Addiction Information:\n")

    print("What type of addiction do you have? Choose 1 from the list below:")
    note = "**Please note: This program focuses on one addiction at a time. If you want to work on another, you can rerun the program.\n"
    print(f"\x1B[3m{note}\x1B[0m")

    addiction_groups = {
        1: {
            'group_name': 'Cannabis',
            'drugs': {
                'a': 'Marijuana',
                'b': 'Hashish',
                'c': 'Other cannabis-containing substances'
            }
        },
        2: {
            'group_name': 'Synthetic cannabinoids',
            'drugs': {
                'a': 'K2',
                'b': 'Spice',
                'c': 'Bath salts'
            }
        },
        3: {
            'group_name': 'Sedatives',
            'drugs': {
                'a': 'Barbiturates',
                'b': 'Benzodiazepines',
                'c': 'Hypnotics'
            }
        },
        4: {
            'group_name': 'Stimulants',
            'drugs': {
                'a': 'Methamphetamine',
                'b': 'Cocaine',
                'c': 'Other stimulants'
            }
        },
        5: {
            'group_name': 'Club drugs',
            'drugs': {
                'a': 'MDMA (Ecstasy / Molly)',
                'b': 'GHB',
                'c': 'Ketamine',
                'd': 'Flunitrazepam (Rohypnol)'
            }
        },
        6: {
            'group_name': 'Hallucinogens',
            'drugs': {
                'a': 'LSD',
                'b': 'PCP',
                'c': 'Other hallucinogens'
            }
        },
        7: {
            'group_name': 'Inhalants',
            'drugs': {
                'a': 'Glue',
                'b': 'Paint thinners',
                'c': 'Correction fluid',
                'd': 'Marker fluid',
                'e': 'Gasoline',
                'f': 'Cleaning fluids',
                'g': 'Household aerosol products'
            }
        },
        8: {
            'group_name': 'Opioids',
            'drugs': {
                'a': 'Heroin',
                'b': 'Morphine',
                'c': 'Codeine',
                'd': 'Methadone',
                'e': 'Fentanyl',
                'f': 'Oxycodone'
            }
        }
    }

    for key, value in addiction_groups.items():
        print(f"{key}. {value['group_name']}") #print all group names

    group_choice = int(input("\nYour choice (1-8): "))
    while group_choice not in addiction_groups.keys(): #number must be a key
        print("Invalid number. Try again.")
        group_choice = int(input("Your choice (1-8): "))

    selected_group = addiction_groups[group_choice]

    print("\nPlease specify the drug:")
    for key, drug in selected_group['drugs'].items(): #set the key to 'drug'
        print(f"{key}. {drug}")

    drug_choice = input("\nYour choice (a-z): ").lower()
    while drug_choice not in selected_group['drugs']:
        print("Invalid choice. Try again.")
        drug_choice = input("Your choice (a-z): ").lower()

    selected_drug = selected_group['drugs'][drug_choice]

    user_data['addiction_type'] = f"{selected_group['group_name']} -> {selected_drug}" #store addiction type


    # ---------------------Trigger Info---------------------
    print('Thank you so much for sharing. Now lets talk about triggers\n')
    print("-------------------------------------------\n")
    print("Section 2: Triggers\n")
    print('Triggers are situations, emotions, or thoughts that can make you want to use or relapse. Understanding them helps you manage your recovery better.\n')
    print('Lets start with Emotional Triggers:')

    triggers = {
        'Emotional': {
            'a': 'Stress',
            'b': 'Anxiety',
            'c': 'Depression',
            'd': 'Loneliness',
            'e': 'Anger',
            'f': 'Boredom',
            'g': 'Guilt or shame',
            'h': 'Low self-esteem',
            'i': 'Grief or loss',
            'j': 'Feeling overwhelmed'
        },

        'Mental': {
            'a': 'Cravings',
            'b': 'Obsessive thoughts',
            'c': 'Rationalizing use',
            'd': 'Minimizing consequences',
            'e': 'Negative self-talk',
            'f': 'Hopelessness',
            'g': 'Overconfidence in control'
        },

        'Environmental': {
            'a': 'Being around substances',
            'b': 'Certain places',
            'c': 'Easy access to drugs',
            'd': 'Lack of structure',
            'e': 'Being alone too long',
            'f': 'Parties or social events'
        },

        'Social': {
            'a': 'Peer pressure',
            'b': 'Conflict with others',
            'c': 'Feeling judged',
            'd': 'Relationship problems',
            'e': 'Isolation',
            'f': 'Enabling friends or family'
        }
    }

    def collect_triggers(category_name, trigger_dict):
        print(f"\n{category_name} Triggers")
        print("Enter letters separated by commas (example: a,c,f)\n")

        #print all triggers
        for key, value in trigger_dict.items():
            print(f"{key}. {value}")

        while True:
            user_input = input("Your triggers: ").lower()
            if user_input == "":
                print("Please select at least one option.")
                continue

            user_choices = [c.strip() for c in user_input.split(',')]
            selected = []

            for choice in user_choices:
                if choice in trigger_dict:
                    selected.append(trigger_dict[choice])

            if len(selected) == 0:
                print("Invalid input, please try again.")
            else:
                break

        return selected

    # ---------------------Trigger Collection---------------------
    all_triggers = {}

    for category in ['Emotional', 'Mental', 'Environmental', 'Social']:
        selected = collect_triggers(category, triggers[category])
        all_triggers[category] = selected

    #empty list to hold all triggers
    combined_triggers = []

    for trigger_list in all_triggers.values():
        for trigger in trigger_list:
            combined_triggers.append(trigger)

    #join everything (comma separated string)
    user_data['triggers'] = ', '.join(combined_triggers)

    print("\nGreat job at identifying your triggers! Let's move n to cravings\n")

    # --------------------------- Cravings -------------------------------
    print("-------------------------------------------\n")
    print("Section 3: Cravings\n")
    print("Cravings are natural urges or desires related to your addiction. "
          "Acknowledging them is the first step to managing them.\n")

    craving_types = {
        'a': 'Physical urge',
        'b': 'Mental obsession',
        'c': 'Emotional craving',
        'd': 'Habit-based craving',
        'e': 'Stress-induced craving',
        'f': 'None'
    }

    print("\nDo you have any of the following cravings?")

    for key, value in craving_types.items():
        print(f"{key}. {value}")

    user_input = input("\nYour cravings: ").lower()
    choices = user_input.split(',')

    selected_cravings = []

    for choice in choices:
        choice = choice.strip()
        if choice in craving_types:
            selected_cravings.append(craving_types[choice])

    user_data['cravings'] = ', '.join(selected_cravings)  #store users cravings

    while True:
        intensity = input("\nRate your craving from 0–10: ")
        if intensity.isdigit() and 0 <= int(intensity) <= 10:
            user_data['craving_intensity'] = int(intensity)
            break
        else:
            print("Please enter a number between 0 and 10.")


    # --------------------- Accessibility / Exposure ---------------------

    print("\nI appreciate you letting me know!\n")
    print("-------------------------------------------\n")
    print("Section 4: Accessibility / Exposure\n")

    print("How easy is it for you to access substances right now?")
    print("0 = No access at all | 5 = Very easy access")

    while True:
        access = input("Enter a number (0–5): ")

        if access.isdigit() and 0 <= int(access) <= 5:
            user_data['accessibility_or_exposure'] = int(access)
            break
        else:
            print("Please enter a number between 0 and 5.")

    # --------------------- Medication ---------------------

    print("\nThanks for being honest.\n")
    print("-------------------------------------------\n")
    print("Section 5: Health Information\n")

    print("\nMedication")
    print("I'd like to go a bit deeper and talk about your general and mental health.\n")

    while True:
        on_medication = input("Are you currently taking any medication? (yes/y/no/n): ").lower()

        if on_medication == 'yes' or on_medication == 'y':
            medication_name = input("Please enter the medication name(s): ")
            user_data['medication'] = medication_name
            break

        elif on_medication == 'no' or on_medication == 'n':
            user_data['medication'] = 'None'
            break

        else:
            print("Please enter yes/y or no/n.")

    # --------------------- Stress Levels ---------------------
    print("\nStress Levels")
    print("\nOn a scale from 0–10, how stressed do you feel right now?")
    print("0 = No stress | 10 = Extremely stressed")

    while True:
        stress = input("Enter a number (0–10): ")

        if stress.isdigit() and 0 <= int(stress) <= 10:
            user_data['stress_levels'] = int(stress)
            break
        else:
            print("Please enter a number between 0 and 10.")

    # --------------------- Self Esteem ---------------------

    print("\nSelf-Esteem Assessment")
    print("Rate how much you agree with each statement:")
    print("0 = Strongly disagree | 1 = Disagree | 2 = Agree | 3 = Strongly agree\n")

    self_esteem_questions = [
        "I feel good about myself most of the time.",
        "I believe I have value as a person.",
        "I am confident in my abilities.",
        "I feel worthy of love and respect."
    ]

    self_esteem_score = 0

    for question in self_esteem_questions:
        print(question)

        while True:
            answer = input("Your rating (0–3): ")

            if answer.isdigit() and 0 <= int(answer) <= 3:
                self_esteem_score += int(answer)
                break
            else:
                print("Please enter a number between 0 and 3.")

    #store final score
    user_data['self_esteem'] = self_esteem_score

    # --------------------- Mental Health Conditions ---------------------

    print("\nMental Health Conditions")
    print("Have you ever been diagnosed with any of the following mental heath conditions?\n")

    mental_health_conditions = {
        'a': 'Depression',
        'b': 'Anxiety',
        'c': 'PTSD',
        'd': 'Bipolar disorder',
        'e': 'ADHD',
        'f': 'Personality Disorder',
        'g': 'Other',
        'h': 'None'
    }

    for key, value in mental_health_conditions.items():
        print(f"{key}. {value}")

    user_input = input("\nYour choices: ").lower()
    selected_conditions = []

    if user_input != "":
        choices = user_input.split(',')

        for choice in choices:
            choice = choice.strip()

            if choice in mental_health_conditions:
                #if user selects None, ignore all others
                if mental_health_conditions[choice] == 'None':
                    selected_conditions = ['None']
                    break
                elif mental_health_conditions[choice] == 'Other':
                    other_condition = input("Please specify the other condition: ")
                    selected_conditions.append(other_condition)
                else:
                    selected_conditions.append(mental_health_conditions[choice])


    user_data['mental_health_conditions'] = ', '.join(selected_conditions)

    # --------------------- Life Stressors ---------------------

    print("\nLife Stressors")
    print("Are you experiencing stress in any of the following areas of your life?\n")

    life_stressors = {
        'a': 'Financial problems',
        'b': 'Work or school stress',
        'c': 'Relationship issues',
        'd': 'Health problems',
        'e': 'Legal issues',
        'f': 'Recent loss or grief',
        'g': 'None'
    }

    for key, value in life_stressors.items():
        print(f"{key}. {value}")

    user_input = input("\nYour choices: ").lower()
    selected_stressors = []

    if user_input != "":
        choices = user_input.split(',')

        for choice in choices:
            choice = choice.strip()
            if choice in life_stressors:
                if life_stressors[choice] == 'None':
                    selected_stressors = ['None']
                    break
                else:
                    selected_stressors.append(life_stressors[choice])

    user_data['life_stressors'] = ', '.join(selected_stressors)



    print("\nI hear you. I’m glad you told me that.\n")

    # --------------------- Support System ---------------------

    print("-------------------------------------------\n")
    print("Section 6: Support System\n")
    print("Having a support system can make a big difference in your recovery. These are the "
          "people or groups you can turn to when you need understanding, encouragement, "
          "or just someone to listen.\n")


    support_options = {
        'a': 'Family',
        'b': 'Friends',
        'c': 'Support group',
        'd': 'Therapist',
        'e': 'None'
    }

    print("Who's in your support system?")

    for key, value in support_options.items():
        print(f"{key}. {value}")

    while True:
        choice = input("\nYour choice (a-e): ").lower().strip()
        if choice in support_options:
            user_data['support'] = support_options[choice]
            break
        else:
            print("Invalid choice. Please enter a letter from a to e corresponding to your support system.")
    return user_data

# ---------------------Store Data---------------------
def store_data(user_data):
    column_names = [
        'first_name', 'surname', 'age', 'gender', 'addiction_type', 'triggers',
        'cravings', 'craving_intensity', 'accessibility_or_exposure', 'medication',
        'stress_levels', 'self_esteem', 'mental_health_conditions', 'life_stressors',
        'support', 'relapse_phase', 'prob_of_relapse'
    ]

    file_exists = os.path.exists(FILE_NAME)

    if not file_exists:
        empty_df = pd.DataFrame(columns=column_names)
        empty_df.to_csv(FILE_NAME, index=False)

    #add new user data
    with open(FILE_NAME, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writerow(user_data)




# ---------------------Models ---------------------

#load dataset
df = pd.read_csv(FILE_NAME)

#features and targets
features = ['age', 'gender', 'addiction_type', 'triggers', 'cravings', 'craving_intensity',
            'accessibility_or_exposure', 'medication', 'stress_levels', 'self_esteem',
            'mental_health_conditions', 'life_stressors', 'support']

target_class = 'relapse_phase'
target_reg = 'prob_of_relapse'

X = df[features]
y_class = df[target_class]
y_reg = df[target_reg]


categorical_cols = ['gender', 'addiction_type', 'triggers', 'cravings',
                    'medication', 'mental_health_conditions', 'life_stressors', 'support']

#fit OneHotEncoder on categorical columns
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoder.fit(X[categorical_cols])

#keep numerical columns as they are
numerical_cols = ['age', 'accessibility_or_exposure', 'craving_intensity', 'stress_levels', 'self_esteem']

#prepare X for training
X_encoded = encoder.transform(X[categorical_cols])
X_final = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(categorical_cols))
X_final[numerical_cols] = X[numerical_cols].reset_index(drop=True)

# --------------------- Train Models ---------------------
clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
clf_model.fit(X_final, y_class)

reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
reg_model.fit(X_final, y_reg)


def prepare_user_data(user_data):
    df_user = pd.DataFrame([user_data])

    #categorical columns
    cat_encoded = encoder.transform(df_user[categorical_cols])
    df_encoded = pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out(categorical_cols))

    #numerical columns
    df_encoded[numerical_cols] = df_user[numerical_cols].reset_index(drop=True)

    return df_encoded


def classify_relapse(user_data):
    #predict relapse phase - classification
    df_input = prepare_user_data(user_data)
    return clf_model.predict(df_input)[0]


def predict_relapse_probability(user_data):
    #predict probability of relapse - regression
    df_input = prepare_user_data(user_data)
    return round(float(reg_model.predict(df_input)[0]), 2)


# ---------------------MAIN FUNCTION---------------------

print("\nHi, I'm Sophia. I'm here to support you on your recovery journey.")
print("I'm going to walk you through a few questions about your experiences and feelings, so I can "
      "give you more personalized guidance.\n")


user_data = user_info()

#update &nd store
user_data['relapse_phase'] = classify_relapse(user_data)
user_data['prob_of_relapse'] = predict_relapse_probability(user_data)

store_data(user_data)

# ---------------------Patient Overview---------------------
#figure a way to print this in a better format
def print_patient_overview(user_data):
    print("\n==================== Patient Overview ====================")
    print(f"Name: {user_data['first_name']} {user_data['surname']}")
    print(f"Age: {user_data['age']} | Gender: {user_data['gender'].title()}")
    print(f"Addiction Type: {user_data['addiction_type']}")
    print(f"Triggers: {user_data['triggers']}")
    print(f"Cravings: {user_data['cravings']} (Intensity: {user_data['craving_intensity']})")
    print(f"Support System: {user_data['support']}")
    print(f"Stress Levels: {user_data['stress_levels']} | Self-Esteem: {user_data['self_esteem']}")
    print(f"Mental Health Conditions: {user_data['mental_health_conditions']}")
    print(f"Life Stressors: {user_data['life_stressors']}")
    print(f"Predicted Relapse Phase: {user_data['relapse_phase'].capitalize()}")
    print(f"Probability of Relapse: {user_data['prob_of_relapse']*100:.1f}%")
    print("===========================================================\n")


def therapeutic_advice(user_data):
    phase = user_data['relapse_phase'].lower()
    print("===== Supportive Guidance =====\n")

    if phase == 'low':
        print("You're currently at a low risk of relapse. This is a great place to be!")
        print(
            "Keep using your coping strategies and leaning on your support system. Celebrate your progress—you’re doing amazing.\n")

    elif phase == 'medium':
        print(
            "Your relapse risk is moderate right now. It's okay, this is just a sign to stay mindful of your triggers.")
        print(
            "Try checking in with a trusted friend, journaling your feelings, or practicing a calming activity. You have the strength to navigate this.\n")

    elif phase == 'high':
        print(
            "It looks like your risk of relapse is high at the moment. I want you to know that this is not a failure.")
        print(
            "Reach out to your support system, use your coping skills, and remember it's okay to ask for help. You are not alone, and taking small steps now can help you regain control.\n")

    else:
        print(
            "We couldn't determine your relapse risk at this time, but remember, self-awareness is already a powerful step in your recovery journey.\n")

    print("\nRemember: Recovery is a journey, not a race. Every step you take towards self-care matters. You got this!")


# --------------------- MAIN ---------------------

print_patient_overview(user_data)
therapeutic_advice(user_data)