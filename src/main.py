'''
Going to try doing this in multiple libraries.
This will let me see which results best match the results from the original Jobscan tool.
Then I can decide which library to use for the rest of the project.
'''

from KeyBERT_extraction import keybert_keyword_extraction
from NLTK_extraction import nltk_keyword_extraction
from summa_extraction import summa_keyword_extraction
from RAKE_extraction import RAKE_keyword_extraction
from spacy_extraction import spacy_keyword_extraction
from spacy_extraction import pyTextRank_keyword_extraction
from textblob_extraction import textblob_keyword_extraction
from YAKE_extraction import YAKE_keyword_extraction

import pandas as pd
import numpy as np


# this is a dictionary of all the extraction methods that I want to use.
# the keys are the names of the files that contain the extraction methods.
# the values are the names of the extraction methods.
# I'm using this so that I can loop through all the extraction methods while also being able to call them by name.
extraction_methods = {
    'KeyBERT_extraction': keybert_keyword_extraction,
    #'NLTK_extraction': nltk_keyword_extraction,
    'summa_extraction': summa_keyword_extraction,
    'RAKE_extraction': RAKE_keyword_extraction,
    'spacy_extraction': spacy_keyword_extraction,
    'pyTextRank_extraction': pyTextRank_keyword_extraction,
    'textblob_extraction': textblob_keyword_extraction,
    'YAKE_extraction': YAKE_keyword_extraction
}

def save_verbose_results(extraction_results, set_of_all_keywords):
    # to make it easier to compare the results, we'll create a pandas dataframe.
    # the rows will be the words in the set of all keywords.
    # the columns will be the sets of keywords from each extraction method for both the resume and the posting.
    # the cells will be True or False, depending on whether the word is in the set of keywords for that extraction method.
    list_of_all_keywords = list(set_of_all_keywords)
    results = pd.DataFrame(index=list_of_all_keywords, columns=extraction_results.keys())
    for column_name, set_of_keywords in extraction_results.items():
        for keyword in list_of_all_keywords:
            if keyword in set_of_keywords:
                results[column_name][keyword] = 1
            else:
                results[column_name][keyword] = 0

    # now we'll add a column that shows the number of extraction methods that found each keyword.
    results['number_of_methods'] = results.sum(axis=1)
    # dump the results into a csv file so that we can look at them.
    results.to_csv('results.csv')

def save_resultant_difference(extraction_results, set_of_all_keywords):
    """
    In this function, we're going to have a single column per method that shows the keywords in the posting that aren't in the resume.
    """
    list_of_all_keywords = list(set_of_all_keywords)
    # create a dataframe, initialize it to all zeros.
    results = pd.DataFrame(0, index=extraction_methods.keys(), columns=list_of_all_keywords)
    for key in extraction_methods.keys():
        resume_set = extraction_results[key + "_resume"]
        posting_set = extraction_results[key + "_posting"]
        # difference is everything in posting_set that isn't in resume_set
        difference = posting_set.difference(resume_set)
        # now we'll put the difference into the results dataframe.
        for keyword in difference:
            results[keyword][key] = 1

    # dump the results into a csv file so that we can look at them.
    results.to_csv('differences.csv')


def main(resume, posting):
    '''
    For each of the extraction methods, run an extraction on the posting and the resume.
    Save the results (lists of words) so that we can compare all methods and their outcomes.
    I need to figure out how to format the output so that it's easy to compare.

    The extraction methods are in files that end with '_extraction.py'.
    the extraction methods have names that end with '_keyword_extraction(text)'.
    '''
    set_of_all_keywords = set()
    extraction_results = {}
    for filename, method_name in extraction_methods.items():
        resume_set = method_name(resume)
        posting_set = method_name(posting)
        extraction_results[filename + "_resume"] = resume_set
        extraction_results[filename + "_posting"] = posting_set
        set_of_all_keywords = set_of_all_keywords.union(resume_set)
        set_of_all_keywords = set_of_all_keywords.union(posting_set)

    #save_verbose_results(extraction_results, set_of_all_keywords)
    save_resultant_difference(extraction_results, set_of_all_keywords)
    

    
    

# put the bulk of the code into a "main" function so that I could more easily separate out the parts of this that could be turned into discrete subroutines.
if __name__ == '__main__':
    " Step 1: Copy and paste the job posting into the triple quotes below "

    job_posting = """
    We are looking for a talented Developer to join our experienced development team. In this role, you will be responsible for designing, coding, testing, modifying, and implementing new or existing software products. Your duties will include liaising with the Development Managers, writing clean, scalable code, creating testing protocols, fixing bugs, and deploying programs.

    To ensure success as a Developer, you should have advanced knowledge of programming languages, excellent problem-solving skills, and the ability to work to a deadline. A top-class Developer works together with the development team to create high-level programs that perfectly meet the needs of the company.

    Developer Responsibilities:
    Meeting with Development Managers to discuss the scope of software projects.
    Analyzing existing programs for modification purposes.
    Researching and designing new software systems, websites, programs, and applications.
    Writing and implementing, clean, scalable code.
    Troubleshooting and debugging code.
    Verifying and deploying software systems.
    Evaluating user feedback.
    Recommending and executing program improvements.
    Maintaining software code and security systems.
    Creating technical documents and training staff.
    Developer Requirements:
    Bachelor\'s degree in Computer Science, Computer Engineering or Information Technology.
    Advanced knowledge of programming languages including JavaScript, HTML5, Java, C++, and PHP.
    Knowledge of software systems and frameworks including AnglularJS, Git, GitHub, and .NET.
    Experience with object-Relational Mapping (ORM) frameworks.
    Familiarity with Agile development technologies.
    Ability to learn new languages and technologies quickly.
    Good communication skills.
    Ability to work as part of a team or individually on a project.
    Ability to work well under pressure.


    """
    " Step 5: Copy your resume below within the triple quotes "

    resume = """

    Victoria, BC
    (250) 701-1556
    sorenchilds@gmail.com
    https://www.linkedin.com/in/soren-childs/
    Soren Childs 
    CAREER PROFILE

    Junior Developer and Analyst with hands-on experience of relational databases, extract-transform-insert programs on customer information databases, network monitoring applications, and low-level programmatic backups of production data in both the energy and retail sectors.

    Core competencies include: Agile workflow, multiple integrate development environments, programming, multiple programming languages, relational database design, database administration, software design, software development, version control systems, data cleaning, data extraction, data analysis, data visualization, machine learning tools, software quality assurance, unit testing, integration testing, end-to-end testing, web development, user interface design, front end development.
    EDUCATION
    University of Victoria, Victoria, BC  
    Bachelor\'s Degree – BSc in Computer Science.
    Camosun College, Victoria, BC  
    Diploma – Two-year Computer Systems Technology program.

    EXPERIENCE
    IT Helpdesk Technician and Junior Developer, Andrew Sheret Ltd.  — Victoria, BC
    May 2021 - December 2022 (co-op placement transitioning to contract)
    ●	Developed and deployed:
    ○	Email notification and multithreading for network monitoring software with Java and PostgreSQL.
    ○	Containerized versions of database systems using Docker and Kubernetes.
    ○	ETI Java applications for migrating customer data between PostgreSQL databases
    ●	Collaborated with teammates using agile methodologies, Jira, and version control software.
    ●	Provided remote and deskside MacOS and Linux support to employees at 32 branches.
    ●	Upgraded hardware in servers, networking equipment, printers, workstations, digital signage, and music-on-hold devices.
    IS Co-op Technician, Fortis BC  — Trail, BC
    January 2019 - December 2019 (three consecutive co-op placements)
    ●	Created Oracle SQL database schemas for a machine learning and data analysis project.
    ●	Analyzed and wrote recommendations for the network security technology roadmap.
    ●	Supported employees with Windows workstations at more than five critical power-generating sites and more than 10 additional locations.
    IT Co-op, Mosaic IT  — Nanaimo, BC
    June 2016 - September 2016 (co-op placement)
    ●	Performed systems discovery survey and documentation of the company’s network infrastructure
    Certifications
    SQL (BASIC), HackerRank, May 2023
    Python (BASIC), HackerRank, May 2023
    JavaScript (BASIC), HackerRank, May 2023
    Java (BASIC), HackerRank, May 2023

    SKILLS

    C, C++, Python, Java, JavaScript, SQL, MySQL, Oracle SQL, PostgreSQL, ETI applications, Extract-Transform-Insert/Extract-Transform-Load, JetBrains IDEs, PyCharm, IntelliJ, Visual Studio Code, Eclipse, NetBeans, Scikit-learn, NumPy, SciPy, Pandas, Keras, TensorFlow, TensorFlow GPU, Docker, Kubernetes, Windows, OSX, MacOS, Linux, Ubuntu, Ubuntu Server, Nano, Vim, BASH scripting, Jira, Confluence, SVN, Apache Subversion, Git, GitHub, Orange, Sublime Text, multithreaded application development, Pytest, Jest, playwright, React Framework, Electron


    """
    main(resume, job_posting)
    #main_using_spacy(job_posting, resume)