'''
Going to try doing this in multiple libraries.
This will let me see which results best match the results from the original Jobscan tool.
Then I can decide which library to use for the rest of the project.
'''

import spacy

'''
Alternative function to do the same basic thing, but more differently.
'''
def main_using_spacy(job_posting, resume):
    # Extract named entities from the job posting and resume
    nlp = spacy.load("en_core_web_sm")
    job_posting_doc = nlp(job_posting)
    resume_doc = nlp(resume)
    # Print the named entities in the job posting that are not in the resume
    print("USING SPACY")
    print("Job posting entities")
    print("--------------------")
    print(job_posting_doc.ents)
    print("Resume entities")
    print("---------------")
    print(resume_doc.ents)
    print("Resume entities missing")
    print("-----------------------")
    for entity in job_posting_doc.ents:
        if entity not in resume_doc.ents:
            print(entity)
    #print(resume_doc.ents)
    '''
    for entity in job_posting_doc.ents:
        if entity.text not in resume_doc.ents:
            print(entity.text, entity.label_)
    '''

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
    #main(job_posting, resume)
    #main_using_spacy(job_posting, resume)