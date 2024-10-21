import pandas as pd
import pycountry_convert as pc

schema_df = pd.read_csv('survey_results_schema.csv')
result_df = pd.read_csv('survey_results_public.csv')


# print(result_df.head(5))
# print(sorted(result_df.columns.tolist()))  

print('----------------------------------QUESTION 1----------------------------------------------\n')

result_df['Age1stCode'] = pd.to_numeric(result_df['Age1stCode'], errors='coerce').fillna(0)

avarage_age = result_df['Age1stCode'].mean()

print(f'{avarage_age} is the avarage age \n')

print('----------------------------------QUESTION 2----------------------------------------------\n')


second_result_df = result_df
# print(second_result_df['LanguageWorkedWith'].head(3))

python_devs = second_result_df[second_result_df['LanguageWorkedWith'].str.contains('Python', na=False)]

total_devs_per_country = second_result_df.groupby('Country').size()
# print(total_devs_per_country)

python_devs_per_country = python_devs.groupby('Country').size()
# print(python_devs_per_country)

python_percentage = (python_devs_per_country / total_devs_per_country * 100).fillna(0)
print(python_percentage,'\n')
# print(python_percentage['India'])

print('----------------------------------QUESTION 3----------------------------------------------\n')

third_result_df = result_df

def get_continent(country_name):
    
    try:
        
        # getting the alfa code for the country
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format='default')
        
        # map the country code to continent code
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        
        # convert the continent code to readable continent name
        continent_name = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "OC": "Australia",
            "SA": "South America",
        }.get(continent_code, 'Others')
        
        return continent_name
    except :
        return 'unknown'


third_result_df['Continent'] = third_result_df["Country"].apply(get_continent)
average_salary_by_continent = third_result_df.groupby("Continent")["ConvertedComp"].mean()
print(average_salary_by_continent,'is the avarage salary of each continent \n')


print('----------------------------------QUESTION 4----------------------------------------------\n')

fourth_result_df = result_df

desired_languages = fourth_result_df['LanguageDesireNextYear'].dropna().str.split(';').explode()

# print(max(desired_languages.value_counts()))
# print(desired_languages[max(desired_languages.value_counts())])

most_desired_language = desired_languages.value_counts().idxmax()
print(most_desired_language , 'is most deisred language \n')


print('----------------------------------QUESTION 5----------------------------------------------\n')

fifth_result_df = result_df

def standardize_gender(gender):
    if pd.isna(gender):
        return 'OTHERS'

    
    gender_list = [g.strip().lower() for g in gender.split(';')]

    
    if 'man' in gender_list and 'woman' not in gender_list:
        return 'MAN'
    elif 'woman' in gender_list and 'man' not in gender_list:
        return 'WOMAN'
    else:
        return 'OTHERS'  
        
    
# print(fifth_result_df['Gender'].unique())

filtered_df = fifth_result_df[~fifth_result_df['Gender'].isin(['Man', 'Others'])]
# print(filtered_df[['Respondent', 'Gender']].head())

fifth_result_df['Continent'] = fifth_result_df["Country"].apply(get_continent)

hobbyists_df = fifth_result_df[fifth_result_df['Hobbyist'] == 'Yes']

hobbyists_df['Gender'] = hobbyists_df["Gender"].apply(standardize_gender)

report = hobbyists_df.groupby(['Continent', 'Gender']).size()

print(report,'\n')

print('----------------------------------QUESTION 6----------------------------------------------\n')

sixth_result_df = result_df

satisfaction_mapping = {
    'Very dissatisfied': 1,
    'Slightly dissatisfied': 2,
    'Neither satisfied nor dissatisfied': 3,
    'Slightly satisfied': 4,
    'Very satisfied': 5
}

satisfaction_re_mapping = {
    1: 'Very dissatisfied',
    2: 'Slightly dissatisfied',
    3: 'Neither satisfied nor dissatisfied',
    4: 'Slightly satisfied',
    5: 'Very satisfied'
}

sixth_result_df['Continent'] = sixth_result_df["Country"].apply(get_continent)

sixth_result_df['CareerSat'] = sixth_result_df['CareerSat'].map(satisfaction_mapping)

sixth_result_df['JobSat'] = sixth_result_df['JobSat'].map(satisfaction_mapping)

sixth_result_df['Gender'] = sixth_result_df['Gender'].apply(standardize_gender)

sixth_result_df = sixth_result_df.dropna(subset=['CareerSat', 'JobSat'])

report = sixth_result_df.groupby(['Gender', 'Continent'])[['CareerSat', 'JobSat']].mean()

report['CareerSat'] = report['CareerSat'].round().replace(satisfaction_re_mapping)

report['JobSat'] = report['JobSat'].round().replace(satisfaction_re_mapping)

print(report,'\n')


print('-------------------------------------------------------------------------------------\n')

# print(sixth_result_df['CareerSat'])
# print(sixth_result_df['CareerSat'].unique())
# print(sixth_result_df['JobSat'].unique())
# print(sixth_result_df['JobSat'])



