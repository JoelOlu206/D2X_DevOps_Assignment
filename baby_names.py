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


#Returns top 5 male names for given year.
def top_5_male_names(year):
    df = Get_NYC_Baby_Names()
    male = df[df['gndr'] == 'MALE']
    
    #converts to int
    male_yr = male[male['brth_yr'] == str(year)]
    male_yr['cnt'] = male_yr['cnt'].astype(int)    

    #removes duplicates
    male_yr = male_yr.groupby('nm')['cnt'].sum().reset_index()
    top_5_male = male_yr.nlargest(5, 'cnt')
    
    #tolist() for cleaner output
    return top_5_male['nm'].tolist()


#Returns top 5 female names between two given years
def top_female_names(start_year, end_year):
    df = Get_NYC_Baby_Names()
    female = df[df['gndr'] == 'FEMALE'] 



    female_yr = female[female['brth_yr'].isin ([str(year) for year in range(start_year, end_year + 1)])]
    female_yr['cnt'] = female_yr['cnt'].astype(int)


    female_yr = female_yr.groupby('nm')['cnt'].sum().reset_index()
    top_5_female = female_yr.nlargest(5, 'cnt')
    
    
    return top_5_female['nm'].tolist()


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
        print(json.dumps(top_5_male_names(args.year), indent=5))
    elif args.function == "female":
        print(json.dumps(top_female_names(args.start_year, args.end_year), indent=5))
    elif args.function == "overall":
        print(json.dumps(top_name_overall(), indent=5))
    
    
    
    
    
    



