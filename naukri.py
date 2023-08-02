from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time
import pandas as pd
#from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#import time

# timing for the entire process
start = time.time()

def parse_jobs (search_keyword, num_of_jobs, path):
    
    # initializing the chromedriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path+"/chromedriver.exe", options=options)
    
    # setting the URL
    driver.get("https://www.naukri.com/data-scientist-jobs?k=data%20scientist")
    
    # getting the main window handle id (some of the code below is used to close the unwanted popups)
    Main_Window = driver.current_window_handle
    
    time.sleep(5)
    
    #getting all the open window handle id's to close additional popups that are appearing
    popup_windows = driver.window_handles

    #looping through all the open  windows and closing ones that are not needed
    for winId in popup_windows:
        if winId != Main_Window: 
            driver.switch_to.window(winId)
            driver.close()
    
    # switching to the main window
    driver.switch_to.window(Main_Window)
    
    time.sleep(5)
    
    # getting the current url which has a specific format which will be used later
    get_url = driver.current_url
    
    # getting the twoparts of the url by splitting with ?
    first_part = get_url.split("?")[0]
    second_part = get_url.split("?")[-1]
    
    # defining empty lists to store the parsed values
    Title =      []
    Company =    []
    Experience = []
    Salary =     []
    Location =   []
    Tags =       []
    Reviews =    []
    Ratings =    []
    Job_Type =   []
    Posted =     []

    
    # this is where parsing begins
    for i in range(1,int(num_of_jobs/20)+1):
        
        # printing the number of pages parsed
        print ("Page {} of {}".format(i,int(num_of_jobs/20)))
        
        # forming the new url with the help of two parts we defined earlier
        url = first_part+"-"+str(i)+"?"+second_part
    
        # opening the url
        driver.get(url)
        
        # giving some time so that all elements are loaded
        time.sleep(5)

        # getting job listing details
        job_list = driver.find_elements(By.CLASS_NAME,"jobTuple")

        
        # looping through all the job listings we have found in the above line of code.
        for element in job_list:
            
        
            # getting the Title of the Job
            try:
                title = driver.find_elements(By.CLASS_NAME,"title.ellipsis")
                for titles in title:
                    print(titles.text) 
                    Title.append(title)
            except NoSuchElementException:
                Title.append(None)
            
            # getting the Company name
            try:
                company = element.find_elements(By.CLASS_NAME,"subTitle.ellipsis.fleft")
                Company.append(company)
            except NoSuchElementException:
                Company.append(None)
            
            # getting the Experience needed for the job
            try:
                experience = element.find_elements(By.CLASS_NAME,"ellipsis.fleft.fs12.lh16")
                Experience.append(experience)
            except NoSuchElementException:
                Experience.append(None)
            
            # getting the Salary details if any
            try:
                salary = element.find_elements(By.CLASS_NAME,"fleft.grey-text.br2.placeHolderLi.salary")
                Salary.append(salary)
            except NoSuchElementException:
                Salary.append(None)
            
            # getting the Location 
            try:
                location = element.find_elements(By.CLASS_NAME,"fleft.grey-text.br2.placeHolderLi.location")
                Location.append(location)
            except NoSuchElementException:
                Location.append(None)
            
            # getting the Tags
            try:
                tags = element.find_elements(By.CLASS_NAME,"tags.has-description")
                Tags.append(tags)
            except NoSuchElementException:
                Tags.append(None)
            
            # getting the number of Reviews of the company
            try: 
                review = element.find_elements(By.CSS_SELECTOR,'a.reviewsCount.ml-5.fleft.blue-text')
                Reviews.append(review)
            except NoSuchElementException:
                Reviews.append(None)
            
            # getting the Rating of the company
            try:
                rating = element.find_elements(By.CSS_SELECTOR,"span.starRating.fleft.dot")
                Ratings.append(rating)
            except NoSuchElementException:
                Ratings.append(None)
            
            # getting the Job Type, eg: Hotness, Preferred etc
            try: 
                job_type = element.find_elements(By.CSS_SELECTOR,'div.jobType.type.fleft.br2.mr-8')
                Job_Type.append(job_type)
            except NoSuchElementException:
                Job_Type.append(None)
            
            # getting the number of days before which the job was posted
            try: 
                days = element.find_elements(By.CSS_SELECTOR,'div.type.br2.fleft.grey')
                Posted.append(days)
            except NoSuchElementException:
                try:
                    days = element.find_elements(By.CLASS_NAME,'div.type.br2.fleft.green')
                    Posted.append(days)
                except NoSuchElementException:
                    Posted.append(None)
    
    # initializing empty dataframe 
    df = pd.DataFrame()
    
    # assigning values to dataframe columns
    df['Title'] =      Title
    df['Company'] =    Company
    
    df['Experience'] = Experience
    df['Location'] =   Location
    df['Tags'] =       Tags
    df['Ratings'] =    Ratings
    df['Reviews'] =    Reviews
    df['Salary'] =     Salary
    df['Job_Type'] =   Job_Type
    df['Posted'] =     Posted
    
    # end time to complete the process
    end = time.time()
    
    print(df)
    print ("Time Taken to Parse {} jobs is:{} seconds".format(num_of_jobs,(end-start)))
    
    # quitting the driver (browser)
    driver.quit()
    
    # returning the dataframe formed
    return df
df = parse_jobs("Data Science", 20, "C:/Users/jai/Desktop")
df.to_csv('Job List.csv',index=None)




    

    