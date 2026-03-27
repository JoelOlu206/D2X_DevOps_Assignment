import requests 
import pandas
import json
import argparse



#Pulls data from API, converts JSON, creates data frame.
def Get_NYC_Baby_Names():
    
    #increased limit for more data
    rq = requests.get("https://data.cityofnewyork.us/resource/25th-nujf.json?$limit=50000") 

    URL_data = rq.json()
    data_frame = pandas.DataFrame(URL_data)
    return data_frame


#handles any gender over any single or range of given years.
def top_names_by_gender(gender, start_year, end_year):
    df = Get_NYC_Baby_Names()
    gender_df = df[df['gndr'] == gender.upper()]
    
    gender_yr = gender_df[gender_df['brth_yr'].isin([str(year) for year in range(start_year, end_year + 1)])]
    gender_yr = gender_yr.copy()
    gender_yr['cnt'] = gender_yr['cnt'].astype(int)
    
    gender_yr = gender_yr.groupby('nm')['cnt'].sum().reset_index()
    top_5 = gender_yr.nlargest(5, 'cnt')
    
    return top_5['nm'].tolist()


#Returns top 5 male names for single or given year.
def top_5_male_names(year):
    return top_names_by_gender('MALE', year, year)

#Returns top 5 female names between two given years
def top_female_names(start_year, end_year):
    return top_names_by_gender('FEMALE', start_year, end_year)


#Returns the most popular name overall
def top_name_overall():
    df = Get_NYC_Baby_Names()
    df['cnt'] = df['cnt'].astype(int)

    overall_name = df.groupby('nm')['cnt'].sum().reset_index()
    top_overall = overall_name.nlargest(1, 'cnt')

    return top_overall['nm'].tolist()


#Test Cases with JSON output and CLI arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NYC Baby Names")
    parser.add_argument("--function", type=str, help="function to run: male, female, overall")
    parser.add_argument("--year", type=int, help="year for top male names")
    parser.add_argument("--start_year", type=int, help="start year for top female names")
    parser.add_argument("--end_year", type=int, help="end year for top female names")
    
    args = parser.parse_args()

    if args.function == "male":
       year = args.year or args.start_year
       end = args.end_year or args.year
       print(json.dumps(top_names_by_gender('MALE', year, end), indent=5))

    elif args.function == "female":
        print(json.dumps(top_female_names(args.start_year, args.end_year), indent=5))

    elif args.function == "overall":
        print(json.dumps(top_name_overall(), indent=5))
    
    
    
    
    
    



