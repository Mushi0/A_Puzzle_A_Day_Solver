import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

def main():
    with open("result.txt", "r") as file:
        result_data = file.readlines()
    
    # use regular expressions to find all dates: 
    date_pattern = re.compile(r'Date:\s*(\d{1,2})/(\d{1,2})')
    date_counts = {}
    for line in result_data:
        match = date_pattern.search(line)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            date_key = (day, month)
            if date_key in date_counts:
                date_counts[date_key] += 1
            else:
                date_counts[date_key] = 1
    # change date_counts to a dataframe and order it
    df_date_counts = pd.DataFrame(columns = ['Month', 'Date', 'Count'])
    for date_key, count in date_counts.items():
        day, month = map(int, date_key)
        df_date_counts = pd.concat([df_date_counts, 
                                    pd.DataFrame({'Month': [month], 
                                                  'Date': [day], 
                                                  'Count': [count]})], 
                                    ignore_index=True)
    df_date_counts = df_date_counts.sort_values(by = ['Month', 'Date']).reset_index(drop = True)
    df_date_counts['Month_Name'] = df_date_counts['Month'].map(month_names)

    # print summary statistics and save as excel
    print(df_date_counts[['Count']].astype(int).describe())
    if not os.path.exists('images'):
        os.makedirs('images')
    df_date_counts.to_excel(os.path.join('images', 'solutions_per_date.xlsx'), index = False)

    sns.set_style("darkgrid")

    # plot the results in bar plot
    plt.figure(figsize = (40, 6))
    plt.bar(range(len(df_date_counts)), df_date_counts['Count'], color = 'darkgreen')
    plt.xticks(range(len(df_date_counts)), 
               [row['Month_Name'] if row['Date'] == 15 else '' 
                for _, row in df_date_counts.iterrows()], 
               rotation = 90)
    plt.margins(x = 0, tight = True)
    plt.xlabel('Date')
    plt.ylabel('Number of Solutions')
    plt.title('Number of Solutions per Date')
    plt.tight_layout()
    plt.savefig(os.path.join('images', 'solutions_per_date.png'))
    plt.close()

    # plot the average value for every month
    plt.figure(figsize = (8, 6))
    df_monthly_avg = df_date_counts.groupby('Month')['Count'].mean().reset_index()
    plt.bar(df_monthly_avg['Month'].map(month_names), df_monthly_avg['Count'], color = 'darkgreen')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Solutions')
    plt.title('Average Number of Solutions per Month')
    plt.tight_layout()
    plt.savefig(os.path.join('images', 'average_solutions_per_month.png'))
    plt.close()

    # plot the distribution of solutions per date
    plt.figure(figsize = (8, 6))
    sns.histplot(df_date_counts['Count'], bins = 30, color = 'darkgreen', kde = True)
    plt.xlabel('Number of Solutions')
    plt.ylabel('Frequency')
    plt.title('Distribution of Solutions per Date')
    plt.tight_layout()
    plt.savefig(os.path.join('images', 'distribution_solutions_per_date.png'))
    plt.close()

if __name__ == "__main__":
    main()