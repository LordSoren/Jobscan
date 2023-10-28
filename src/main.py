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

def save_mass_extractions(extraction_results, set_of_all_keywords):
    """
    In this function, we're going to save all keywords from job postings irrespective of whether they're in the resume.
    """
    list_of_all_keywords = list(set_of_all_keywords)
    # create a dataframe, initialize it to all zeros.
    results = pd.DataFrame(0, index=extraction_methods.keys(), columns=list_of_all_keywords)
    for key in extraction_methods.keys():
        posting_set = extraction_results[key + "_posting"]
        for keyword in posting_set:
            results[keyword][key] = 1

    # dump the results into a csv file so that we can look at them.
    results.to_csv('Mass_extraction.csv')


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
    #save_resultant_difference(extraction_results, set_of_all_keywords)
    save_mass_extractions(extraction_results, set_of_all_keywords)
    

    
    

# put the bulk of the code into a "main" function so that I could more easily separate out the parts of this that could be turned into discrete subroutines.
if __name__ == '__main__':
    " Step 1: Copy and paste the job posting into the triple quotes below "

    job_posting = """
    Software Engineer, Machine Learning
    Instabase

    Data Scientist
    Backbone

    Data Scientist
    Wealthfront


    Analytics Engineer
    Draftea


    At Instabase, we're passionate about building software to advance the state of the art in computing. We've built a fearlessly experimental, customer-obsessed team who are making discoveries to fundamentally change how people build and consume business applications. Today, we're partnering with the world's leading companies to transform how they use data and technology. If these challenges excite you, we'd love to hear from you!

    Our Engineering Team architects the underlying operating system, core services, platform infrastructure, dev toolkits, core algorithms, machine learning models, packaged end-user apps, and app store marketplace. Instabase engineers are excited to solve hard problems for complex organizations and are self-starters from day one.

    What you'll do:
    Work on a small team of ML engineers to apply Machine Learning techniques to challenging real world problems such as:
    Image Processing / Computer Vision
    Ocr
    Handwriting Recognition
    Visual Extraction (checkboxes, signatures, radio button, etc.)
    Object Detection
    Table Detection
    Document/Text Understanding
    Extraction from Documents
    Field Extraction from Document with Variable Structure (for example: paystubs, invoices, forms, etc.)
    Information Retrieval from Documents with Natural Language
    Finding relevant clause in legal contracts
    Extracting data (for example: effective date, duration, payment terms, etc.) from legal contracts
    Document Classification
    Document Clustering
    About you:
    2+ years industry / academia experience with Machine Learning
    Proficient with coding using Python
    Proven track record of excellence in applying Machine Learning techniques for solving difficult real world problems
    Knowledge of deep learning frameworks such as PyTorch and TensorFlow, computer vision, NLP, or related areas would be a plus
    MS in Computer Science, Engineering, Math, Science or related field. PhD preferred
    Instabase is an equal opportunity employer and values diversity in all forms. Instabase does not discriminate on the basis of race, religion, color, national origin, gender identity, sexual orientation, age, marital status, protected veteran status, disability, or any other unlawful factor. Instabase also complies with local laws, including the San Francisco Fair Chance Ordinance.

    Remote job description

    "Backbone feels as first-party as you could make something that is literally not first-party feel." - TechCrunch
    "The way that Backbone unifies gaming experiences across AAA iOS ports like Warzone or Minecraft, Xbox and Playstation Remote Play and now native xCloud games feels like the way of the future for mobile gaming in a way that none of the individual players... [have] managed to get right." - TechCrunch

    Backbone is growing the data team to help discover more insights and build better products from its wealth of gaming data. We are looking for a Data Scientist that has experience leading deep product analysis to uncover insights, crafting robust datasets, and building great data products based on ML/statistical applications.

    As one of the first members on the data team, you'll get to help shape the data team from the ground up, define best data science practices within the organization, and lead explorative analyses to influence the product roadmap.

    What you'll be doing
    Analyze our vast collection of gaming and product data to discover insights, build models to answer key business questions and address customer problems, and make business recommendations across the company from engineering teams to the CEO
    Use SQL and Python to prepare, clean, and transform data into robust datasets
    Collaborate with product and engineering to build data-powered features in the Backbone app
    Design, create, and maintain data dashboards to help the team make better data-driven decisions
    Work with our feature teams to design experiments, define success metrics, and analyze feature performance
    What we're looking for
    Passion for discovering data insights and high data quality
    1-2+ years experience as a Data Scientist, Data Engineer, Data Analyst, or Software Engineer in data
    Expert in SQL and Python
    Ability to perform data science/analytical investigations to drive business decisions
    Ability to communicate effectively to stakeholders of varying technical levels
    Ability to define and implement key metrics for both business level objectives as well as feature level goals
    Background in computer science and software engineering fundamentals
    Remote friendly
    Bonus points: See yourself as a Data Generalist with an emphasis on Data Science
    Bonus points: Familiarity with dbt, Mode Analytics, and/or Sisu Data
    Bonus points: Worked as a Data Scientist on a consumer/mobile product



    Summary
    Company name: Backbone
    Remote job title: Data Scientist
    Job tags: gaming

    Remote job description

    Data and its proper use is crucial to that vision and the data science team plays a fundamental role in understanding and interpreting those data sources.

    The Wealthfront data science team creates data products to deliver personalized financial product experiences, develops best in class investment algorithms, and analyzes our rich financial and behavioral data to make key business decisions. The team draws from a variety of backgrounds in Computer Science & Engineering, Statistics, Economics, Math, Operations Research, and Financial Engineering. We derive strength from this diversity and are constantly learning and teaching each other in a down-to-earth and dynamic environment. We are neither too big where you would be just another cog in the system, nor are we too small that none of our efforts can be realized.

    As a Data Scientist in Wealthfront's Data Science organization, you'll be responsible for improving the quality of our decisions using data and the scientific method. Your work will generate tools and insights that inform product and business decisions throughout the company and across the product lifecycle, from ideation and research to launch and iteration. You will mentor and collaborate with your data science colleagues with a focus on technical skills and career development. We are fortunate to work with experienced product managers and engineers that have worked on products at companies like Facebook, Google, Twitter and Apple. This is an opportunity to learn from some of the most experienced operators in the startup world and to further an important and meaningful mission. Our Data Science team focuses on product analytics (for the product areas of Investments and Banking), A/B Testing, growth/marketing analytics, and risk analytics (fraud, credit).

    What you'll do
    Work closely with cross-functional teams of product managers and engineers, translating open-ended business issues into data questions, identifying practical approaches including A/B testing to answer them, and carrying out timely and well-documented analyses that influence our product and company strategy
    Design and develop data products to assist consumers with decisions around investments, banking, and financial planning
    Continuously look for, and execute upon, opportunities to improve the quality of our data, infrastructure and products
    Understand and communicate a data-driven picture of our clients, product and business
    Promote automation of repetitive tasks and the creation of tools over ad hoc analyses, making your insights available to anyone that can benefit from them
    What we're looking for
    Knowledge of Python and SQL toolchain to access, transform, visualize, and model business data
    A firm foundation in data analysis basics including regression and classification models, experiment design, time series modeling and hypothesis testing
    Ability and empathy to explain technical and statistical work to business stakeholders
    Interest and ability to map business requirements and priorities to technical projects
    Interest in continuous learning and mentoring others
    BS, MS, or PhD in computer science, mathematics, statistics, economics or related field
    Everyone across the financial spectrum deserves to live secure and rewarding lives. In order to successfully serve clients across the United States, the Wealthfront team is focused on hiring team members with a diverse range of backgrounds, experiences and perspectives. We are an equal opportunity employer and value diversity at our company. We do not discriminate on the basis of race, religion, color, national origin, gender, sexual orientation, age, marital status, veteran status, or disability status.
    About Wealthfront
    Our first chapter was about transforming the investment advisory business. We focused on unlocking access to low cost investing for delegators - people who were underserved by high fee and human financial advisors. We built the first automated portfolio that allows you in seconds to invest in a personalized portfolio of thousands of companies for a remarkably low fee, which resulted in attracting more than $25 billion of our client's hard earned savings, created the robo-advisor category and transformed the broader industry.

    Now, we've embarked on expanding into an adjacent opportunity to transform the digital self-directed brokerage space. This focus enables us to empower a dramatically wider audience to build long-term wealth - people who are eager to learn about investing by making their own investment decisions, but need guidance. In the last few years, several financial technology companies have made it incredibly accessible and engaging to trade in individual stocks, but because of their transaction based business models, these apps keep people focused on the day-to-day gyrations of the market leading to short-term thinking and behaviors. As a result, millions of people are investing their hard earned savings in a handful of stocks which is inconsistent with building long-term wealth. We believe our vision serves their needs far better and that we can extend our core philosophy of embracing diversification, managing risk, minimizing fees and taxes and taking a long-term view, into self-directed investing. We believe this is an ideal opportunity to leverage our strength of building simple, easy-to-use products that offer a delightfully engaging experience to build long-term wealth.




    Summary
    Company name: Wealthfront
    Remote job title: Data Scientist
    Job tags: transaction fees, asset management, fintech

    Remote job description

    We are a product-led company with small, accountable squads. The engineering unit is based on customer-centric methodologies with a simple framework; security, performance, reliability.

    Your challenge
    Your first challenge will be to contribute in the creation of our platform from zero to one, creating beautiful software experiences with modern tools, and care deeply about creating the best possible products. We are currently a small team and you will be one of the first hires.

    Own the entire development process for our product analytics reporting. This includes meeting with internal customers to understand their needs, partnering with data engineering to centralize dispersed data and instrument our product, understanding the core data models, writing code to enrich and manipulate data, and designing and iterating dashboards.
    Design and develop the analytics layer and define complex business logic using SQL to help Draftees measure success across various departments & teams.
    Enable and scale self-serve analytics for all Draftees. You'll architect clean data sets by modeling data and metrics via tools like dbt to empower employees to make data-driven decisions with accurate information.
    Work with data scientists and other engineers to design our data models as inputs to metrics and machine learning models, and partner with infrastructure and product engineers to instrument our product. You will ensure that relevant data is centralized into an analytical warehouse, modeled for performant analytics, and meeting our high-quality standards
    Establish governance and enforce standards around our data infrastructure. Document best practices and coach/advise other data analysts, product managers, engineers, etc. on data modeling, SQL query optimization & reusability, etc. Keep our data warehouse tidy by managing roles and permissions and deprecating old projects.
    Help with hiring and mentoring analytics engineers. Provide technical leadership across the company for data modeling, metrics, visualization, etc.
    Requirements
    BS or MS degree in Computer Science, Engineering, or a related technical field.
    3+ years experience working in a data or analytics engineering role, working with instrumentation, data pipelines, data warehouses, and modeling, cataloging & documenting curated datasources.
    Strong understanding of modern ELT (eg Segment), data warehousing (eg Redshift), and data modeling concepts (e.g. Kimball, Star Schema)
    Expert-level SQL skills with experience transforming raw data into clean models, optimizing code, and troubleshooting & improving others' code
    Experience with business intelligence solutions (Metabase, Amplitude, Looker, Tableau, Periscope, Mode)
    Familiarity with software design principles, including test-driven development, and strong programming skills, preferably in Python
    Strong communication skills across stakeholders with varying business goals and levels of technical knowledge -- you're as comfortable talking to our API team about how they record events as you are brainstorming a new campaign with our Marketing team.
    Self-motivated and resourceful: you'll jump in to do whatever needs doing to get the job done.
    Deep interest in learning about and keeping up with quickly evolving industry trends around the modern data stack and data best practices
    Passionate about building the best version of whatever you're working on
    (nice to have) 1+ years experience with dbt and dbt Cloud - both as a user and administrator
    (nice to have) Experience in geospatial data management, analysis, and visualization with tools such as QGis, Postgres/PostGIS



    Summary
    Company name: Draftea
    Remote job title: Analytics Engineer
    Job tags: Database Arch/Design, Periscope, Python

    Remote job description

    We are NYC based, but remote friendly unless specified. (US & Canada based candidates only)
    Hello, World! Codecademy is on a mission to build inspiring careers in technology through engaging, accessible, and interactive online coding education.

    Our learners have gone on to start new jobs, launch new companies, and lead new lives thanks to their work with Codecademy, and our platform has transformed the way businesses develop and retain their teams.

    Since 2011, our team has grown to over 200 employees serving 50+ million learners from 190+ countries. We've raised over $82M in venture capital funding from top investors including Prosus, Owl Ventures, Union Square Ventures, Y Combinator, and more--which gives us the capital to get stuff done in an impactful way.

    Join us to help build a business that empowers tens of millions of people to lead better lives!

    What you'll do
    As a Data Scientist, you will work on an impactful team to analyze our millions of learners. We capture terabytes of data on how users engage with our platform. As Codecademy continues our rapid growth, we want to build a data-informed culture that uses hypothesis testing, experimentation, and exploratory analysis to guide our decision-making process.

    You will join a small but growing team of Data Scientists. Our work is in high-demand from all corners of Codecademy. We work on a variety of problems and have a real impact on the business and product. If you have a proven background in data and you are excited about making code education accessible, we want to hear from you!

    Apply exploratory data analysis and causal inference to answer complex questions about our users.
    Collaborate across teams to help scope out analyses, through a combination of experimentation (A/B testing) and quantitative user research.
    Design experiments and evaluate results to test and iterate on new product ideas.
    Perform deep dives into our data to build understanding around our business.
    Work with our data science and engineering teams to maintain data integrity.
    Mentor and consult with a cross-functional team of data scientists, engineers, and product managers.
    What you'll need
    3+ years of industry experience in a data science, analytics, or research role, with 1+ years of Machine Learning experience. You have strong data intuition and knowledge of using data science best practices to drive impact.
    Expert SQL. Able to write clean and efficient queries on massive datasets.
    Applied experience with statistical programming languages - R or Python preferred.
    Familiarity with multiple Machine Learning Frameworks
    Experience working with different algorithms (regressions, gradient boosting, random forest)
    Understanding of statistical methods and when to use them (hypothesis testing, experiment design, sampling).
    Strong written and verbal communicator. Comfortable working with loosely defined research problems.
    What will make you stand out
    Background in Advanced Machine Learning/Deep Learning.
    Knowledge of Scala and dbt.
    A workflow involving reproducible methods and version control - Github, Docker.
    Experience automating dashboards with business intelligence tools - Looker, Tableau.
    Passionate about teaching the world to code. Empathy for our learners, such as a background in education or past experience using our site.
    Interesting questions you might work on
    How can we estimate learning based on a user's journey?
    What are some different types of patterns in user behavior (i.e. predict churn, retention, LTV)?
    What do we do when we are unable to conduct an experiment?
    How do we improve the relevance of our course recommendations?
    How can we scale our existing processes? (experiment reporting framework, forecasting)
    Equal Employment Opportunity
    At Codecademy, we are committed to teaching people the skills they need to upgrade their careers. Codecademy aims to educate a richly diverse demographic of learners with our product and in order to accomplish this, we believe our team should reflect that rich diversity. Our company celebrates diversity in all of its forms-- race, gender, color, national origin, marital status, sexuality, religion, veteran status, age, ability, disability status-- and works to create an inclusive workplace where people of all backgrounds and beliefs are empowered to better their futures.


    ull Job Description
    Your Job
    If you are an engineer who's passionate about building impactful products that scale to tens of millions of page views a day, Indeed is looking for you. Indeed offers skilled developers like you a complex development ecosystem with short release cycles. Every week sees the new release of multiple products that meet the needs of jobseekers worldwide.

    Responsibilities:
    Write software to fulfill well-specified, small-scoped work requests for your team's product(s), escalating more complex or ambiguous issues to senior engineers.
    Write software to fix simple bugs.
    Assist in investigating problems and recommending fixes for products within your team.
    Utilize knowledge of programming languages and the software ecosystem to accomplish goals.
    Provide feedback within your team regarding code changes made by other engineers and regarding designs for new enhancements.
    Produce documentation for your team’s products, code, and work items. Grow your skills and knowledge learning from mentors, reading books or online resources, or by observing your co-workers applying their skills and knowledge.
    Who You Are
    Bachelor’s degree in Computer Science, Mathematics, Electrical Engineering, Computer Engineering or equivalent field required.
    1 year of work experience in software programming. Experience must include at least one of the following languages: Java, C, C++, C#, Python, Go, or Perl
    1 year of work experience building applications using at least one of the following:
    Web application technologies including: HTML, CSS, or JavaScript; or
    Databases, including MySQL, Mongo, or a similar program; or
    A collection of systems connected and communicating via a network connection.
    Who we are
    The Product Technology organization is responsible for Indeed’s foundational technology and platforms for job seeker and employer products. We help build and maintain analytics tools used weekly by most Indeedians, guide Indeed’s cloud infrastructure strategy and keep the website up and running, and finally offer secure login, payment, and communication systems for job seekers and employers.
    Our Mission
    As the world’s number 1 job site*, our mission is to help all people get jobs. We strive to cultivate an inclusive and accessible workplace where all people feel comfortable being themselves. We're looking to grow our teams with more people who share our enthusiasm for innovation and creating the best experience for job seekers.

    (*comScore Total Visits, September 2021)
    Salary Range Disclaimer
    The base salary range represents the low and high end of the Indeed salary range for this position. Actual salaries will vary depending on factors including but not limited to location, experience, and performance. The range listed is just one component of Indeed's total compensation package for employees. Other rewards may include quarterly bonuses, Restricted Stock Units (RSUs), an open Paid Time Off policy, and many region-specific benefits.
    Salary Range Transparency
    US Remote 86,000 - 124,000 USD per year
    Equal Opportunities and Accommodations Statement
    Indeed is deeply committed to building a workplace and global community where inclusion is not only valued, but prioritized. We’re proud to be an equal opportunity employer, seeking to create a welcoming and diverse environment. All qualified applicants will receive consideration for employment without regard to race, color, religion, gender, gender identity or expression, family status, marital status, sexual orientation, national origin, genetics, neuro-diversity, disability, age, or veteran status, or any other non-merit based or legally protected grounds.

    Indeed is committed to providing reasonable accommodations to qualified individuals with disabilities in the employment application process. To request an accommodation, please contact Talent Attraction Help at 1-855-567-7767, or by email at TAhelp@indeed.com at least one week in advance of your interview.

    Fair Chance Hiring
    We value diverse experiences, including those who have had prior contact with the criminal legal system. We are committed to providing individuals with criminal records, including formerly incarcerated individuals, a fair chance at employment.
    Our Policies and Benefits
    View Indeed's Applicant Privacy and Accessibility Policies - https://www.indeed.com/legal/indeed-jobs
    Learn about our global employee perks, programs and benefits - https://benefits.indeed.jobs/

    Where legally permitted, Indeed requires all individuals attending or working out of Indeed offices or visiting Indeed clients to be fully vaccinated against COVID-19. For positions that can only be performed at an Indeed office, candidates must be fully vaccinated against COVID-19 and present acceptable proof of vaccination by the date of hire as a condition of employment. Indeed will consider requests for reasonable accommodation as required under applicable law. To qualify as being fully vaccinated against COVID-19 there should have been a two week period after receiving the second dose (or any government recommended booster shot) in a 2-dose COVID-19 vaccine series, or a two week period after receiving a single-dose (or any government recommended booster shot) in a single dose COVID-19 vaccine.


    Full Job Description
    Your Job
    As a Software Development Engineer, you will design new software systems and enhancements to existing systems to support new software features and products. Work with Product Managers, Designers, Data Scientists, Test & Software Engineers and other stakeholders to clarify requirements and to decompose large requests into smaller ones that can be executed sequentially or in parallel. Contribute to the product roadmap, technology, and direction while supporting a culture of quality and operational excellence on the team. Investigate and resolve problems and fix bugs and balancing short-term and long-term results.
    This opportunity is for a software engineer working primarily on backend systems for the sourcing platform team in the Resume product group. This team is responsible for the backend systems, capabilities, and technologies to expose Indeed Sourcing capabilities to 3rd party integrators and tooling. This key new capability is unlocking new business opportunities and exciting new scenarios and capabilities for our customers. This team has only begun to unlock these capabilities and this is a great time to join the team and help us deliver on our ground-breaking vision for the future!
    Responsibilities:

    Design, develop, test, and deliver software and systems to solve technical problems and add new capabilities to the products you work on.
    Debug and fix issues and defects in software systems.
    Work with your team to improve processes, design and quality of software components.
    Collaborate with PMs, QA, and other stakeholders to ensure that our products provide the best possible customer experience
    Who You Are
    Bachelor’s Degree in Computer Science or a closely related field
    1+ years of work experience in software development. Experience must include at least one of the following languages: Java, Scala, Go, C#, or Python.
    1+ years work experience building web applications and/or services
    Solid understanding of Computer Science fundamentals and problem solving
    Good verbal and written communication skills
    Experience can be obtained concurrently.
    Who we are
    The Enterprise business organization is focused on delivering value for Indeed’s largest customers. We are driven by Indeed’s mission to help all people get jobs by helping enterprise employers make the best hires, at scale. Our work is very important to us as Enterprise employers are consistently rated among the top places to work globally. Our approach is multi-faceted with many dedicated product and engineering professionals driving innovation with our biggest clients in mind.
    Our Mission
    As the world’s number 1 job site*, our mission is to help all people get jobs. We strive to cultivate an inclusive and accessible workplace where all people feel comfortable being themselves. We're looking to grow our teams with more people who share our enthusiasm for innovation and creating the best experience for job seekers.

    (*comScore Total Visits, September 2021)
    Salary Range Disclaimer
    The base salary range represents the low and high end of the Indeed salary range for this position. Actual salaries will vary depending on factors including but not limited to location, experience, and performance. The range listed is just one component of Indeed's total compensation package for employees. Other rewards may include quarterly bonuses, Restricted Stock Units (RSUs), an open Paid Time Off policy, and many region-specific benefits.
    Salary Range Transparency
    Seattle 104,000 - 150,000 USD per year

    Equal Opportunities and Accommodations Statement
    Indeed is deeply committed to building a workplace and global community where inclusion is not only valued, but prioritized. We’re proud to be an equal opportunity employer, seeking to create a welcoming and diverse environment. All qualified applicants will receive consideration for employment without regard to race, color, religion, gender, gender identity or expression, family status, marital status, sexual orientation, national origin, genetics, neuro-diversity, disability, age, or veteran status, or any other non-merit based or legally protected grounds.

    Indeed is committed to providing reasonable accommodations to qualified individuals with disabilities in the employment application process. To request an accommodation, please contact Talent Attraction Help at 1-855-567-7767, or by email at TAhelp@indeed.com at least one week in advance of your interview.

    Fair Chance Hiring
    We value diverse experiences, including those who have had prior contact with the criminal legal system. We are committed to providing individuals with criminal records, including formerly incarcerated individuals, a fair chance at employment.
    Our Policies and Benefits
    View Indeed's Applicant Privacy and Accessibility Policies - https://www.indeed.com/legal/indeed-jobs
    Learn about our global employee perks, programs and benefits - https://benefits.indeed.jobs/

    Where legally permitted, Indeed requires all individuals attending or working out of Indeed offices or visiting Indeed clients to be fully vaccinated against COVID-19. For positions that can only be performed at an Indeed office, candidates must be fully vaccinated against COVID-19 and present acceptable proof of vaccination by the date of hire as a condition of employment. Indeed will consider requests for reasonable accommodation as required under applicable law. To qualify as being fully vaccinated against COVID-19 there should have been a two week period after receiving the second dose (or any government recommended booster shot) in a 2-dose COVID-19 vaccine series, or a two week period after receiving a single-dose (or any government recommended booster shot) in a single dose COVID-19 vaccine.

    Full Job Description
    Sun West Mortgage Company Inc. is a technology-driven mortgage company with over 40 years of experience. As one of the fastest growing fin-tech companies, we provide exceptional service, technology, and product innovation.

    Our team of brilliant engineers are continuously filing new patents and expanding the boundaries of the financial services industry through innovations in mobile applications, customer acquisition and retention algorithms, and AI based process automation. We need people like you to join in our mission to lower the cost of financial services so that we can reach new and underserved markets.

    Work in a highly collaborative and creative team of talented engineers. Use creativity and innovation to solve problems in ways that have never been imagined before. Build and architect large-scale, data driven systems.

    OUR REQUIREMENT:

    A highly skilled and disciplined software engineer. We believe in using the right tool for the job. Be prepared to work on a wide variety of technologies. Although most of our hard core development is in Java, our development stack is integrated across C/C++, Java, Node JS, Oracle, and Amazon Lambda.

    This position has no minimum education or experience requirements. We are looking for talented engineers and architects who have an innate passion for creating beautiful and elegant systems.

    If you fit this description, we would appreciate meeting with you to discuss a career at Sun West.

    You can work from the comfort of your home too!

    We've developed Empathetic Technology! Want to know more?

    Experience Technology that cares: https://youtu.be/pD4m75XaZlI
    Sun West launches Morgan - New empathetic technology for Loan Originators: https://youtu.be/c0Xq3QT7ORs
    Learn about our work culture by following us on Social Media:

    Facebook: https://www.facebook.com/SunWestMortgage
    Twitter: https://twitter.com/SunWestMortgage
    LinkedIn: https://www.linkedin.com/company/641035?trk=tyah&trkInfo=tarId%3A1404936420142%2Ctas%3Asun%20west%20%2Cidx%3A2-1-6
    Job Type: Full-time

    Pay: $71,813.00 - $164,405.00 per year

    Benefits:

    401(k)
    401(k) matching
    Dental insurance
    Health insurance
    Health savings account
    Paid time off
    Vision insurance
    Schedule:

    8 hour shift
    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Remote Software Engineer

    We are looking for passionate Software Engineers to design and develop software solutions for our Fortune 500 client working with the latest cloud technologies, development languages, and databases. Join our dynamic team and make your mark on the technology landscape of tomorrow.

    Skills We Are Looking For:

    Node JS and/or Python
    Web development with Angular or similar tools
    MongoDb and/or SQL Server
    AWS Services
    Design and Development Responsibilities

    Breakdown tickets to onshore or offshore team members. Applying the principles of engineering to the design, development, maintenance, and testing of components.
    Assisting team members and stakeholders in the understanding the big picture regarding development tasks.
    Perform code reviews and provide suggestions and guidance
    Work with engineering operations to assist with deployment, trouble shooting, repair defects and provide technical support.
    Work with QA to ensure complete testing with 90% code coverage.
    Documenting code and database designs.
    Develop robust, testable, and readable code with excellent error handling and logging to minimize maintenance costs.
    Work independently on assigned development tasks based on customer priorities.
    Fearless, but mindful of refactoring. Must have a passion for coding
    Provide level-of-effort estimates for epics and development tasks during project and sprint planning
    Recommend new technologies; showcase new technologies to the rest of the technology team.
    Job Types: Full-time, Part-time, Contract

    Pay: $70,000.00 - $150,000.00 per year

    Schedule:

    8 hour shift
    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    Javascript or Python: 1 year (Preferred)
    Document DB or SQL: 1 year (Preferred)

    Full Job Description
    We are looking for a Python Developer to join our engineering team and help us develop and maintain various software products. Python Developer responsibilities include writing and testing code, debugging programs and integrating applications with third-party web services. To be successful in this role, you should have experience using server-side logic and work well in a team. Ultimately, you’ll build highly responsive web applications that align with our business needs.

    Responsibilities

    Write effective, scalable code
    Develop back-end components to improve responsiveness and overall performance
    Integrate user-facing elements into applications
    Test and debug programs
    Improve functionality of existing systems
    Implement security and data protection solutions
    Assess and prioritize feature requests
    Coordinate with internal teams to understand user requirements and provide technical solutions
    Skills

    Work experience as a Python Developer
    Expertise in at least one popular Python framework (like Django, Flask or Pyramid)
    Knowledge of object-relational mapping (ORM)
    Familiarity with front-end technologies (like JavaScript and HTML5)
    Team spirit
    Good problem-solving skills
    BSc in Computer Science, Engineering or relevant field
    Job Types: Full-time, Part-time, Contract

    Salary: $60.00 - $80.00 per hour

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)

    Full Job Description
    Position: Software Engineer - Front End

    Who we are:

    Montera Health is clearing the path to quality healthcare. Montera delivers the best possible outcomes with the utmost convenience. We use kaizen to improve the patient journey and improve personalized care by applying AI and machine learning to optimize the treatment pathway.

    The first care vertical Montera improving is autism ABA therapy. Care is difficult to access and the delivery model must be reinvented to provide early access families. 1 in 44 children [CDC, 2021] are diagnosed to be on the autism spectrum. We are looking for driven, innovative, patient focused individuals to join our team as we reinvent the care and tools available to neurodiverse families.

    About the position:

    Full time, salary
    Remote
    Must be available and online during normal working hours
    What you’ll do:

    Developing and implementing front-end architecture to support user interface concepts
    Developing and implementing highly-responsive user interface components using React
    Building reusable components and front-end libraries for future use
    Working with internal and external business stakeholders to develop the overall look and design of a web application
    Optimizing components for maximum performance across a vast array of web-capable devices and browsers
    Monitoring and improving front-end performance.
    Documenting application changes and developing updates
    Identify, design, and implement internal process improvements, including CI/CD for automated testing and deployment
    Collaborate with fellow backend engineers and business strategy team to drive cross-product projects
    Learn new techniques in the worlds of software engineering and put them into practice to develop novel approaches in the domain of healthcare applications
    Keep our development environment secure and maintain compliance with the regulatory requirements
    What you bring: (requirements)

    Strong proficiency in JavaScript, including DOM manipulation and the JavaScript object model
    Thorough understanding of React and its core principles
    Preferred to have experience in Javascript, CSS, HTML, and wireframing tools
    Experience with data structure libraries
    Familiarity with RESTful APIs
    Knowledge of modern authorization mechanisms, such as JSON Web Token
    Familiarity with modern front-end build pipelines and tools
    Ability to understand business requirements and translate them into technical requirements
    Knowledge of SQL and NoSQL databases
    Experience in cloud native application development and deployment
    Understanding of security principles and compliance
    Strong communication skills with the ability to relay information across disciplines and to external partners
    Ability to operate in a fast-moving environment supporting a rapidly growing business
    What we offer:

    Competitive salary
    Engaging and Challenging Work
    Opportunity to Join a Fast Paced Startup
    If this sounds like your next career move, send us an email explaining your interest and experience with an attached resume. We will be interviewing as applications come in so, don’t wait to apply.

    Looking forward to working with you.

    -

    All qualified applicants will receive consideration for employment without regard to race, color, religion, sex, sexual orientation, gender identity, national origin, disability, protected veteran status. Montera Inc. is a Drug Free Workplace/ EO employer – M/F/Veteran/Disability.

    Job Type: Full-time

    Pay: $85,000.00 - $130,000.00 per year

    Benefits:

    401(k)
    Dental insurance
    Flexible schedule
    Health insurance
    Paid time off
    Vision insurance
    Schedule:

    Monday to Friday
    Weekend availability
    Education:

    High school or equivalent (Preferred)
    Experience:

    Front-end development: 1 year (Preferred)
    CSS: 1 year (Preferred)
    Angular: 1 year (Preferred)

    Your job
    Enterprise Candidates is focused on enabling Indeed’s enterprise customers to hire great talent efficiently at scale. To do so, we are reengineering a product suite from the ground up with that new customer base in mind, while building infrastructure that powers a seamless experience at scale and integrates with other Indeed products.

    

    On the Guided Discovery team within Enterprise Candidates, you will be creating an innovative new approach to managing large numbers of candidates, building a new backend to power a modern frontend. Based on years of behavioral science and economics research, our team has developed an approach that customers love.

    

    Once the groundwork has been laid, this team will be making fast iterative tests in order to move the product as a whole to a state that is more friendly to larger customers. 

    

    Responsibilities include:

    

    Collaborate closely with cross-functional stakeholders to identify, understand, and address common business needs. Ask the ‘what’ and the ‘why’ before the ‘how’.
    Design and develop simple, sustainable solutions to complex problems.
    Check for ways to reuse existing Indeed technologies before rolling your own.
    Who you are
    You are eager to solve business problems by applying engineering judgment and creative thinking rather than take orders and write code to spec. You respond positively to feedback and freely offer it to your peers in code reviews, design reviews, whiteboard sessions, and general meetings. You value robust unit and integration tests and recognize their increased importance in a CI/CD environment. You collaborate well with others, across disciplines, and beyond your immediate team.

    

    Requirements:

    Bachelor’s degree in Computer Science or similar major (or equivalent industry experience)
    Previous exposure to Java
    A willingness to participate in front end development given the team needs.
    General knowledge of AWS and running applications in the cloud is a plus
    Who we are
    The Enterprise business organization is focused on delivering value for Indeed’s largest customers. We are driven by Indeed’s mission to help all people get jobs by helping enterprise employers make the best hires, at scale. Our work is very important to us as Enterprise employers are consistently rated among the top places to work globally. Our approach is multi-faceted with many dedicated product and engineering professionals driving innovation with our biggest clients in mind.

    Our mission
    As the world’s number 1 job site*, our mission is to help all people get jobs. We strive to cultivate an inclusive and accessible workplace where all people feel comfortable being themselves. We're looking to grow our teams with more people who share our enthusiasm for innovation and creating the best experience for job seekers.

    

    (*comScore Total Visits, September 2021)

    Salary Range Disclaimer
    The base salary range represents the low and high end of the Indeed salary range for this position. Actual salaries will vary depending on factors including but not limited to location, experience, and performance. The range listed is just one component of Indeed's total compensation package for employees. Other rewards may include quarterly bonuses, Restricted Stock Units (RSUs), an open Paid Time Off policy, and many region-specific benefits.

    Salary Range Transparency
    SF Bay Area 140,000 - 204,000 USD per year

    EEO and Accommodations
    Indeed is deeply committed to building a workplace and global community where inclusion is not only valued, but prioritized. We’re proud to be an equal opportunity employer, seeking to create a welcoming and diverse environment. All qualified applicants will receive consideration for employment without regard to race, color, religion, gender, gender identity or expression, family status, marital status, sexual orientation, national origin, genetics, neuro-diversity, disability, age, or veteran status, or any other non-merit based or legally protected grounds.

    

    Indeed is committed to providing reasonable accommodations to qualified individuals with disabilities in the employment application process. To request an accommodation, please contact Talent Attraction Help at 1-855-567-7767, or by email at TAhelp@indeed.com at least one week in advance of your interview.

    

    Fair Chance Hiring

    We value diverse experiences, including those who have had prior contact with the criminal legal system. We are committed to providing individuals with criminal records, including formerly incarcerated individuals, a fair chance at employment.

    Privacy Policy
    View Indeed's Applicant Privacy and Accessibility Policies - https://www.indeed.com/legal/indeed-jobs 

    Learn about our global employee perks, programs and benefits - https://benefits.indeed.jobs/  

    

    Where legally permitted, Indeed requires all individuals attending or working out of Indeed offices or visiting Indeed clients to be fully vaccinated against COVID-19. For positions that can only be performed at an Indeed office, candidates must be fully vaccinated against COVID-19 and present acceptable proof of vaccination by the date of hire as a condition of employment.  Indeed will consider requests for reasonable accommodation as required under applicable law. To qualify as being fully vaccinated against COVID-19 there should have been a two week period after receiving the second dose (or any government recommended booster shot) in a 2-dose COVID-19 vaccine series, or a two week period after receiving a single-dose (or any government recommended booster shot) in a single dose COVID-19 vaccine.

    Full Job Description
    Job Description

    Front end (React JS )
    Should have good understanding about general web app development.
    Should be familiar with react application deployment on Azure.
    Proficiency in HTML5, CSS3 and JavaScript
    Backend (Node JS)
    Proficiency in Restful APIs and API communication.
    Good understanding about asynchronous programming and workarounds.
    Experienced with Express.
    Clear understanding about Node js event loop.
    Working knowledge in user authentication and authorization (OAuth workflow, experience with SSO implications using provider like Okta)
    Should be familiar with the general security protocols, data protection and best practices.
    Good error handling and debugging skill.
    Familiarity with the Node app deployment on Azure platform.
    SQL
    Should know basic SQL
    Database schema creation for business processes.
    Familiarity with the PostgreSQL
    PowerBI
    Basic understanding about PowerBI (dashboard, reports, pages, filters, slicers etc.)
    Proficiency in power bi embedded analytics.
    Cloud platform- Azure
    Familiarity with Azure portal and Azure app service.
    Familiarity with the CI/CD process.
    Good understanding about Azure Repos.
    Job Types: Full-time, Contract

    Pay: $140,000.00 - $180,000.00 per year

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Work Location: Remote

    Full Job Description
    Job Title: Java Developer
    Location: Irving, TX
    Duration: Long Term
    Contract: W2 full time

    Job Description

    Supporting EOGs real-time operation applications, the React Software Engineer will work with a team of mid to senior level software engineers on front-end, new application development, as well as enhancing and supporting existing in-house developed applications. The role will involve working with the Solutions Analysts, Solutions Engineers and end users to help identify requirements. Will also be responsible for analyzing requirements, and to architect, design and present solutions to the business problems.

    Experience & Skills:

    - Must have development experience with React/Redux/Material-UI.

    - Experience with building commercial and/or enterprise applications is preferred.

    - Oil and Gas exploration and production experience is a plus.

    - Individual should be flexible and able to adapt to a dynamic environment.

    - Individual should be self-motivated who can work independently with minimal supervision, and also work well as part of a team.

    - Should have good communication skills and the willingness and ability to jump into existing projects.

    Bachelor's degree in related field is preferred; High school diploma or GED required

    Job Types: Full-time, Contract, Internship

    Salary: $58,187.00 - $145,492.00 per year

    Benefits:

    401(k)
    Health insurance
    Paid time off
    Schedule:

    8 hour shift
    Supplemental Pay:

    Commission pay
    Signing bonus
    Education:

    High school or equivalent (Preferred)
    Experience:

    Front-end development: 1 year (Preferred)
    CSS: 1 year (Preferred)
    Angular: 1 year (Preferred)

    Full Job Description
    React Developer
    12+ Months
    Remote Role (Florida)

    Responsibilities:

    Candidates Must be Senior developers with experience with both React AND Node.
    Proficiency using MERN and MEAN Scaffolding tools
    Ability to adapt to a rapidly changing environment
    In-depth understanding of the systems development life cycle
    Proficiency programming in more than one object-oriented programming language; React.Js, Node.JS, JavaScript, and HTML
    Proficiency with HTML, CSS, SASS, JavaScript/jQuery, local storage, and cross-browser compatibility are required
    May include database knowledge in MongoBD

    Job Type: Full-time

    Pay: $65.00 - $70.00 per hour

    COVID-19 considerations:
    yes

    Education:

    High school or equivalent (Preferred)
    Experience:

    Full-stack development: 1 year (Preferred)
    React: 1 year (Preferred)
    react js: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Your Job
    If you are an engineer who's passionate about building impactful products that scale to tens of millions of page views a day, Indeed is looking for you. Indeed offers skilled developers like you a complex development ecosystem with short release cycles. Every week sees the new release of multiple products that meet the needs of jobseekers worldwide.

    Responsibilities:
    Work under team guidance to develop new features and improve current experience in the product
    Assist in investigating problems and recommending fixes for products within your team.
    Utilize knowledge of programming languages and the software ecosystem to accomplish goals.
    Provide feedback within your team regarding code changes made by other engineers and regarding designs for new enhancements.
    Produce documentation for your team’s products, code, and work items. Grow your skills and knowledge learning from mentors, reading books or online resources, or by observing your co-workers applying their skills and knowledge.
    Who You Are
    Bachelor’s degree required in Computer Science, Electrical Engineering, Computer Engineering or Mathematics or equivalent field required
    1 year of work experience in software programming. Experience must include at least one of the following languages: Java, C, C++, C#, Python, Go, or Perl
    1 year of work experience building applications using at least one of the following:
    Web application technologies including: HTML, CSS, or JavaScript; or
    Databases, including MySQL, Mongo, or a similar program; or
    A collection of systems connected and communicating via a network connection.
    Who we are
    In the Job Seeker organization, our promise is to deliver best in class service to our job seekers and teammates worldwide. We focus on collaboration, the ability to adapt to user needs, and a passionate approach to service to help job seekers navigate through the ever-changing recruitment landscape. Simply put, our vision is to help job seekers get better jobs.
    Our Mission
    As the world’s number 1 job site*, our mission is to help all people get jobs. We strive to cultivate an inclusive and accessible workplace where all people feel comfortable being themselves. We're looking to grow our teams with more people who share our enthusiasm for innovation and creating the best experience for job seekers.

    (*comScore Total Visits, September 2021)
    Salary Range Disclaimer
    The base salary range represents the low and high end of the Indeed salary range for this position. Actual salaries will vary depending on factors including but not limited to location, experience, and performance. The range listed is just one component of Indeed's total compensation package for employees. Other rewards may include quarterly bonuses, Restricted Stock Units (RSUs), an open Paid Time Off policy, and many region-specific benefits.
    Salary Range Transparency
    US Remote 90,000 - 130,000 USD per year

    Equal Opportunities and Accommodations Statement
    Indeed is deeply committed to building a workplace and global community where inclusion is not only valued, but prioritized. We’re proud to be an equal opportunity employer, seeking to create a welcoming and diverse environment. All qualified applicants will receive consideration for employment without regard to race, color, religion, gender, gender identity or expression, family status, marital status, sexual orientation, national origin, genetics, neuro-diversity, disability, age, or veteran status, or any other non-merit based or legally protected grounds.

    Indeed is committed to providing reasonable accommodations to qualified individuals with disabilities in the employment application process. To request an accommodation, please contact Talent Attraction Help at 1-855-567-7767, or by email at TAhelp@indeed.com at least one week in advance of your interview.

    Fair Chance Hiring
    We value diverse experiences, including those who have had prior contact with the criminal legal system. We are committed to providing individuals with criminal records, including formerly incarcerated individuals, a fair chance at employment.
    Our Policies and Benefits
    View Indeed's Applicant Privacy and Accessibility Policies - https://www.indeed.com/legal/indeed-jobs
    Learn about our global employee perks, programs and benefits - https://benefits.indeed.jobs/

    Where legally permitted, Indeed requires all individuals attending or working out of Indeed offices or visiting Indeed clients to be fully vaccinated against COVID-19. For positions that can only be performed at an Indeed office, candidates must be fully vaccinated against COVID-19 and present acceptable proof of vaccination by the date of hire as a condition of employment. For positions that require some in-office work or in-person client meetings, exceptions to these in-office or in-person job requirements may be made at the discretion of the business through June 2022, at which point full vaccination will be required. Indeed will consider requests for reasonable accommodation as required under applicable law. To qualify as being fully vaccinated against COVID-19 there should have been a two week period after receiving the second dose (or any government recommended booster shot) in a 2-dose COVID-19 vaccine series, or a two week period after receiving a single-dose (or any government recommended booster shot) in a single dose COVID-19 vaccine.

    Full Job Description
    EQ-Games (www.eq-games.com) is looking for a mid/senior level Unreal Engine videogame coder to join our team, either on-site or remotely.

    In addition to salary, the chosen candidate will earn permanent royalties for every year employed.

    We are currently working on a AAA online first person shooter, with very unique tactical elements.

    EQ-Games is a well-funded videogame development studio, with a commitment to high quality, technically excellent games that people are proud to put on their resumes!

    Responsibilities:

    Constructing gameplay systems from the ground up
    Debugging and optimizing existing gameplay systems
    Thinking creatively and critically
    Working closely with other coders, artists, and animators to contribute on game architecture and technical design
    Write extensible and easily maintained game code using a combination of blueprints, C++, and GPU-based shader code
    Contribute to the videogame design process, if so desired
    Desired Experience/Skills :

    A love for and knowledge of videogames
    Strong experience in Unreal Engine 4 (C++)
    Strong 2D/3D math and/or physics skills
    Ability to collaborate with team members to bring gameplay to life
    BS Computer Science or equivalent professional or hobby experience
    Proactive and motivated to learn and work well within team
    We Offer:

    Highly collaborative environment with wide range of expertise.
    An opportunity to work on highly visible, AAA-quality PC, PS4, and Xbox One games, such as Road Redemption
    An opportunity to gain experience in the new frontier of 3d, skill-based, hardcore, casino games
    Salary at increasing levels beyond $90,000, relative to skills and experience
    Job Type: Full-time

    Pay: $90,000.00 - $120,000.00 per year

    Benefits:

    Relocation assistance
    Schedule:

    Monday to Friday
    Supplemental Pay:

    Bonus pay
    COVID-19 considerations:
    We are happy to make whatever accommodations that would make you comfortable. Currently, all team members are seated considerable distance apart. Office environment is highly ventilated. Mask usage is left up to the individual.

    Experience:

    C++: 1 year (Preferred)
    Unreal Engine: 1 year (Required)
    Work Location: Remote

    Full Job Description
    Your Job
    The Enterprise Candidates team is focused on enabling our enterprise customers to hire great talent efficiently at a larger scale. To do so, we are reengineering a product suite from the ground up with that new customer base in mind, while building infrastructure that powers a seamless experience at scale and integrates with other Indeed products.

    On the Candidate Management team, you will be building a brand new suite of tools, using modern frontend architecture, for candidate organization and evaluation that provides specific feature sets catered to enterprise clients, while also utilizing previous work done at Indeed for small/medium businesses whenever possible.

    Once the groundwork has been laid, this team will be making fast iterative tests in order to move the product as a whole to a state that is more friendly to larger customers.

    Some responsibilities would include:

    Working closely with stakeholders to understand/identify critical business needs and problem areas. We ask the ‘what’ and the ‘why’ before the ‘how’
    Design and develop simple and sustainable solutions to complex problems
    Constantly be on the lookout for opportunities to reuse existing Indeed technologies before rolling your own
    Collaborating with teams across Indeed in order to solve common problems
    Who You Are
    You have a BS or BSA in Computer Science or similar major (equivalent industry experience will also be considered)
    You have previous experience with React
    A general knowledge of AWS and running applications in the cloud is a plus
    You are heavily interested in frontend development and are ready and willing to learn the latest technologies and patterns
    You react positively to feedback and freely give it to your peers in code reviews, design reviews, whiteboard sessions, and general meetings
    You value robust unit and integration tests and recognize their increased importance in a CI/CD environment
    You collaborate well with others, across disciplines and beyond the immediate team
    Who we are
    The Enterprise business organization is focused on delivering value for Indeed’s largest customers. We are driven by Indeed’s mission to help all people get jobs by helping enterprise employers make the best hires, at scale. Our work is very important to us as Enterprise employers are consistently rated among the top places to work globally. Our approach is multi-faceted with many dedicated product and engineering professionals driving innovation with our biggest clients in mind.
    Our Mission
    As the world’s number 1 job site*, our mission is to help all people get jobs. We strive to cultivate an inclusive and accessible workplace where all people feel comfortable being themselves. We're looking to grow our teams with more people who share our enthusiasm for innovation and creating the best experience for job seekers.

    (*comScore Total Visits, September 2021)
    Salary Range Disclaimer
    The base salary range represents the low and high end of the Indeed salary range for this position. Actual salaries will vary depending on factors including but not limited to location, experience, and performance. The range listed is just one component of Indeed's total compensation package for employees. Other rewards may include quarterly bonuses, Restricted Stock Units (RSUs), an open Paid Time Off policy, and many region-specific benefits.
    Salary Range Transparency
    Austin 143,000 - 207,000 USD per year

    Equal Opportunities and Accommodations Statement
    Indeed is deeply committed to building a workplace and global community where inclusion is not only valued, but prioritized. We’re proud to be an equal opportunity employer, seeking to create a welcoming and diverse environment. All qualified applicants will receive consideration for employment without regard to race, color, religion, gender, gender identity or expression, family status, marital status, sexual orientation, national origin, genetics, neuro-diversity, disability, age, or veteran status, or any other non-merit based or legally protected grounds.

    Indeed is committed to providing reasonable accommodations to qualified individuals with disabilities in the employment application process. To request an accommodation, please contact Talent Attraction Help at 1-855-567-7767, or by email at TAhelp@indeed.com at least one week in advance of your interview.

    Fair Chance Hiring
    We value diverse experiences, including those who have had prior contact with the criminal legal system. We are committed to providing individuals with criminal records, including formerly incarcerated individuals, a fair chance at employment.
    Our Policies and Benefits
    View Indeed's Applicant Privacy and Accessibility Policies - https://www.indeed.com/legal/indeed-jobs
    Learn about our global employee perks, programs and benefits - https://benefits.indeed.jobs/

    Where legally permitted, Indeed requires all individuals attending or working out of Indeed offices or visiting Indeed clients to be fully vaccinated against COVID-19. For positions that can only be performed at an Indeed office, candidates must be fully vaccinated against COVID-19 and present acceptable proof of vaccination by the date of hire as a condition of employment. Indeed will consider requests for reasonable accommodation as required under applicable law. To qualify as being fully vaccinated against COVID-19 there should have been a two week period after receiving the second dose (or any government recommended booster shot) in a 2-dose COVID-19 vaccine series, or a two week period after receiving a single-dose (or any government recommended booster shot) in a single dose COVID-19 vaccine.

    Full Job Description
    Boom Entertainment is a technology company that is fueling the biggest winners in sports betting, gaming, and casino products. Working with professional sports leagues, media companies, and leading casino operators, Boom provides technology and games to many of the biggest names in the industry - including NBC Sports, Barstool Sports, Penn National Gaming, MSG Networks, NASCAR, 8AM Golf, Yes Network, and many more.
    As a company, we are looking for driven dreamers who want to make an impact on this industry and the world. We want people of integrity who are both open to learning and willing to challenge the norm. We want people who are curious, reliable, empathetic, and obsessed with quality.
    Boom is known for its innovative, accessible, and truly fun products, operating world-class free-to-play games and technology for our partners and entertaining more than 3 million sports fans. In addition, we're hard at work creating casino and sports betting games for distribution to casino and sportsbook operators in the legal US and international iGaming markets.
    If you want to join our team as a Software Engineer and build (legal) sports gaming and casino products for the next generation, please apply!

    Responsibilities:

    Collaborate with other engineers, designers, and the leadership team to make technical decisions that solve real problems in a way that enhances our core capabilities
    Implement new game formats and social features by working across the presentation, server, event, and storage layers of our stack as necessary
    Optimize for performance and quality of end-user experience in the context of local execution, networked resources, and fully scaled operations
    Participate in roadmapping, daily stand ups, and ongoing discussions about best practices and the design patterns that are most appropriate for our use cases
    Develop an appreciation for the gaming vertical and participate in the design, testing, and evaluation of new products and features
    Qualifications:

    Demonstrated creative, critical thinking, and troubleshooting skills
    Highly professional work ethic and the ability to deliver well-vetted work on an ongoing basis
    Excellent collaborative skills, including written and verbal communication
    Experience with Game Development using Javascript, Unity, C++, or another game development framework and language
    Experience with networking and client-server communication (REST, websockets, server-sent events)
    Preferred Qualifications:

    Experience with ThreeJS, Typescript, WebGL, GLSL Shaders
    Professional experience as a game developer or engineer on a B2C Product
    B.S. or M.S. in Computer Science or a related technical discipline with solid academic performance.
    Boom Entertainment's positions are fully remote. This role will allow you to work from home for all of your working hours, with limited-to-no travel required.

    Job Type: Full-time

    Pay: $84,500.00 - $143,599.00 per year

    Benefits:

    401(k)
    401(k) matching
    Dental insurance
    Flexible schedule
    Flexible spending account
    Health insurance
    Life insurance
    Paid time off
    Parental leave
    Referral program
    Retirement plan
    Vision insurance
    Schedule:

    Monday to Friday
    COVID-19 considerations:
    Fully remote work.

    Work Location: Remote

    Full Job Description
    Role- Windchill/Thing Worx Developer
    Duration – Long Term
    Location – 100%Remote
    Job Type: Contract

    Only W2 Profiles

    Description:

    Windchill/Thing Worx Developer

    Job Types: Full-time, Contract

    Pay: $50.00 - $150.00 per hour

    Benefits:

    Health insurance
    Schedule:

    8 hour shift
    Education:

    High school or equivalent (Preferred)
    Experience:

    Java: 1 year (Preferred)
    Windchill: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    · Experience with Proven experience in full stack web development

    · software development Python, REST APIs, Azure or AWS

    · Git/GitHub or similar

    · Cloud-based architectures, development, and deployment

    · Scalability experience,

    · Experience with Flask Framework, Django REST framework, React Js, Angular.js, PostgreSQL

    · SQL Server

    · Apache Spar

    Job Type: Full-time

    Pay: $60.00 - $65.00 per hour

    Schedule:

    8 hour shift
    COVID-19 considerations:
    yes

    Education:

    Bachelor's (Preferred)
    Experience:

    , REST APIs: 1 year (Preferred)
    Python: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Skills:

    Must have experience programming with Python version 3.8+
    Any experience building mission-critical applications and supporting remote hardware, or even embedded software is a plus
    Experience building REST API’s using frameworks like Flask/FastAPI
    They use git for source management
    Experience with AWS or other cloud providers, or experience with Docker and Kubernetes is a plus
    Experience developing web UI’s with Angular or React.
    Duties:

    Develop software for our ground-station and satellite operation infrastructure with a strong focus on automating mission operations
    Help design new ground-station infrastructure to include building and testing client-server applications and designing REST APIs.
    Manually perform mission planning and mission operations while building out the automated system.
    Test and debug existing applications when issues arise.
    Develop unit tests, and full-system integration tests for entire ground-station infrastructure.
    entegee.com

    This message is intended only for the designated recipient(s). It may contain confidential or proprietary information and may be subject to other contractual or confidentiality protection. If you are not a designated recipient, you may not review, copy or distribute this message. If you receive this message in error, please notify the sender by reply email and delete this message.

    Job Types: Full-time, Contract

    Pay: $75.00 - $90.00 per hour

    Schedule:

    8 hour shift
    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    Software Development Occupations: 1 year (Preferred)
    REST: 1 year (Preferred)
    Java: 1 year (Preferred)

    FullStack Developer with AWS nodeJS
    Purple Drive Solution
    Remote
    Remote
    Full-time, Part-time, Contract
    Job details
    Job Type
    Full-time
    Part-time
    Contract
    Qualifications
    Bachelor's (Preferred)

    REST: 1 year (Preferred)

    Java: 1 year (Preferred)

    Indeed's salary guide
    Not provided by employer
    $97.6K to $124K per year is Indeed's estimated salary for full stack developer in Remote.
    Report inaccurate salary
    Full Job Description
    Role: FullStack Developer
    Location: US - Remote
    Type Of hire: Contract

    Skills: AWS, Node js and API background.

    Job Types: Full-time, Part-time, Contract

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Speak with the employer
    +91 9492293323

    Java Developer with node JS
    Tekspike LLC
    Remote
    Remote
    $68,828 - $152,823 a year - Full-time, Part-time, Contract
    Job details
    Salary
    $68,828 - $152,823 a year
    Job Type
    Full-time
    Part-time
    Contract
    Qualifications
    Bachelor's (Preferred)

    REST: 1 year (Preferred)

    Java: 1 year (Preferred)

    Full Job Description
    Hi Guys,

    We have an immediate requirement with one of our clients.

    Java Developer with node js
    Remote
    Long term project
    Any visa is fine

    Please share resumes to nataraj(@)tekspike.com or reach me at 469-305-7541

    Job Types: Full-time, Part-time

    Pay: $68,828.00 - $152,823.00 per year

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Software Engineer/Developer
    Astronomic Agency Company
    Remote
    Remote
    $120,000 - $140,000 a year - Full-time, Contract
    Job details
    Salary
    $120,000 - $140,000 a year
    Job Type
    Full-time
    Contract
    Qualifications
    Bachelor's (Preferred)

    Node.js: 1 year (Preferred)

    Java: 1 year (Preferred)

    Benefits
    Pulled from the full job description
    Health insurance
    Full Job Description
    Job Overview

    We are looking for a Software Engineer to join our growing Engineering team and build out the next generation of our platform. The ideal candidate is a hands-on platform builder with significant experience in developing scalable data platforms. We’re looking for someone with experience in business intelligence, analytics, data science and data products.

    Responsibilities for Software Developer

    Collaborate with team members to determine best practices and client requirements for software
    Develop intuitive software that meets and exceeds the needs of the company
    Professionally maintain all software and create updates regularly to address customer and company concerns
    Analyze and test programs and products before formal launch
    Troubleshoot coding problems quickly and efficiently to ensure a productive workplace
    Collaborate with team members to determine best practices and client requirements for software
    Develop intuitive software that meets and exceeds the needs of the company
    Professionally maintain all software and create updates regularly to address customer and company concerns
    Skills

    1-2 years of experience developing and implementing software applications
    Experience working on large-scale software projects
    Experience developing software utilizing various coding languages including Node.js and Javascript.
    Outstanding collaboration and communication skills are essential
    Job Type: Full-time

    Salary: $120,000.00 - $140,000.00 per year

    Benefits:

    Health insurance
    Schedule:

    8 hour shift
    Day shift
    Education:

    Bachelor's (Preferred)
    Experience:

    Node.js: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Oracle ADF Developer
    Sunera Technologies
    Remote
    Remote
    $60,631 - $145,582 a year - Full-time, Contract
    Sunera Technologies
    14 reviews
    Read what people are saying about working here.
    Job details
    Salary
    $60,631 - $145,582 a year
    Job Type
    Full-time
    Contract
    Qualifications
    Bachelor's (Preferred)

    Full Job Description
    Required Skills & Experience:

    Interpret requirements and design solution that satisfy the customer’s needs and also satisfied the need for standardization, usability and maintainability of the different Agent facing applications.
    Breakdown solution into components that could be assigned and tracked in pursue of a fast and cost effective solution.
    Implement ADF Business Components / Web Services / Oracle Objects Calls that would provide the data access layer for the Agent Applications processes.
    Implement the ADF View Controller components, including Tasks Flows, Beans and JSF pages that would allow the successful interaction between the agents and the applications.
    Supervise tasks performed by other members of the solution team in order to ensure a cohesive approach that satisfies the external (customer) requirements and internal (technology) requirements.
    Publish and maintain Coding and UI standards
    Job Type: Full-time

    Pay: $60,631.00 - $145,582.00 per year

    Schedule:

    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Work Location: Remote

    This open position is for an individual contributor role as a software engineer on a stream-aligned team that specializes in the interpretation of business requirements, design, implementation, maintenance, and documentation of software applications owned by the team. This role is expected to efficiently deliver high quality, sustainable software solutions to the problems identified by the stakeholders. Candidates will be expected to participate in: team problem solving exercises, Agile sprint ceremonies, implementation of the Product Backlog Items, peer code reviews.

    This will be an Angular 7+ and Typescript heavy role with an emphasis on strong problem solving skills in an enterprise environment. The applicant is expected to participate in all phases of the SDLC. The candidate must have experience with Angular 7+, including a practical knowledge of Angular constructs, RXJS operators, and unit testing. Some experience with NPM package management, Azure pipelines, AngularJS, C#, and general micro-frontend concepts would be a plus.

    Job Types: Full-time, Contract

    Pay: $71,783.00 - $164,047.00 per year

    Benefits:

    401(k) matching
    Dental insurance
    Health insurance
    Life insurance
    Paid time off
    Vision insurance
    Schedule:

    8 hour shift
    Day shift
    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)

    Full Job Description
    No C2C

    C++ is the only REQUIRED skill

    You will get to learn mobile development

    What You Will Do:

    Work with a team of highly performing engineers.
    Design and implement efficient and maintainable code.
    Design and deliver software for a cross platform C++ SDK on iOS, Android, and Linux.
    Design and implement software for iOS and Android.
    Follow a test driven development process where unit tests are included in reviews and code merges.
    Actively participate in the design and code review process across the team.
    Execute functional/integration tests to prove the feature from a user perspective.
    Support production code and new feature development.
    Investigate and resolve issues with the code.
    Improve our development processes as ideas are raised during sprint retrospectives.
    Decipher agriculture equipment CAN data (ISO 11783 based on J1939).
    Work well in a team atmosphere and be able to take direction from a technical lead.
    Build your knowledge and contribute your ideas through interactive product design sessions, hackathons, and on-farm opportunities.

    Job Types: Full-time, Contract

    Pay: $50.00 - $75.00 per hour

    Benefits:

    401(k)
    Dental insurance
    Health insurance
    Paid time off
    Referral program
    Schedule:

    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    C++: 3 years (Required)
    mobile platform: 1 year (Preferred)
    controller area network: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    * Only W2 Candidates will be considered *

    CEIs Fortune 50 Client in Media and Telecommunications is adding a QA to their team. Interested candidates should have hands-on Java and JavaScript experience reflected on their resume

    100% Remote (within the US)
    Long term contract with potential for permanent conversion
    Responsibilities:

    70% Java Automation + 30% Manual Testing
    Develop microservices for Client/Platform environments in a middleware capacity
    Required and Desired Skills:

    Hands-on Java and JavaScript experience
    Automation experience
    As a trusted technology partner, CEI delivers solutions that help our customers transform their business and achieve meaningful results. From strategy and custom application development through application management - our technology and digital experience services are tailored to meet each unique need of our customers. Our staffing solutions bring specialized skills to complement our customers' workforce and project requirements.

    Job Types: Full-time, Contract

    Pay: $45.00 - $50.00 per hour

    Benefits:

    401(k)
    Dental insurance
    Health insurance
    Vision insurance
    Schedule:

    8 hour shift
    Day shift
    Monday to Friday
    Application Question(s):

    I appreciate your interest in the position. Are you able to work W2? (Yes/No)
    Education:

    Bachelor's (Required)
    Experience:

    Java automation: 2 years (Preferred)
    JavaScript development: 1 year (Required)
    Work Location: Remote

    Full Job Description
    I am currently recruiting for a Java engineer for one of the biggest telecommunications companies in the US. This global leader in communications and technology is looking for back-end engineers to grow one of their cutting-edge teams.

    You would be working on a dynamic scrum team modernizing their Video On-Demand feature!

    The ideal developer is a Java engineer with some experience or exposure to Golang. As you will be working to migrate their legacy Java backend systems to Golang. Commercial experience is preferred but not essential.

    Required Skills

    - Java

    - Golang

    - AWS

    - Microservices

    Beneficial skills

    - Commercial Golang experience

    - Kubernetes

    - AWS RDS

    - AWS Neptune (or any other graph database)

    My client is offering a 12-month contract on a fully remote basis. The rate is $75-$85 on a C2C basis and is open to US citizens or green card holders.
    If this role sounds like a fit for your next career move, please reach

    Job Types: Full-time, Contract

    Schedule:

    8 hour shift
    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    Software Development Occupations: 1 year (Preferred)
    Go: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Strong development skills with C#
    Strong experience with Dynamics 365 lifecycle management
    Proficiency in automating Dynamics 365 through various environments
    Track record of automated testing with Dynamics 365
    Experience with automated Quality Assurance methodologies
    Experience with Azure, Power Platform, and Azure DevOps
    Ability to collaborate with remote team members to ensure automation is built to meet business needs
    Ability to quickly ramp up on new technology areas
    Analytical mind with problem-solving aptitude
    Ability to work independently and with excellent communications and leadership skills
    BSc/BA in Computer Science or a related degree, or sufficient certifications from accredited institutions to demonstrate reasonable equivalent knowledge
    Job Types: Full-time, Contract

    Pay: $140,000.00 - $190,000.00 per year

    Benefits:

    401(k)
    Dental insurance
    Health insurance
    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    We are looking for a specialized Game developer to turn a game idea into code on a fast moving environment. You will be involved in various aspects of game’s creation from concept to finished product including coding, programming, audio, design, production and visual arts.

    Responsibilities

    Translate requirements into complicated but clean and efficient code
    Construct the base or the engine on which the game will run
    Produce prototypes of gameplay ideas and features
    Develop schedules and determine milestones
    Generate game scripts and storyboards
    Animate characters and objects
    Contribute to the design and audio features of the game
    Create unit tests and validation procedures to assure quality
    Detect identification and resolution and document technical specifications
    “Polish” the game, maintain code, fix bugs and iron out occurring problems
    Skills

    Proven working experience in full lifecycle game development
    Hands on experience primarily with C++ or other programming languages (Java, C, etc)
    High level knowledge of APIs and libraries
    Expert in one or more programming specialties (artificial intelligence, 3D Rendering, 3D animation, physics, multiplayer/networking, or audio)
    Up-to-date with the latest gaming trends, techniques, best practices and technologies
    Ability to solve problems creatively and effectively
    BS degree in Computer Science or Games Technology
    Job Type: Full-time

    Pay: $80,187.00 - $145,492.00 per year

    Benefits:

    Health insurance
    Schedule:

    8 hour shift
    Education:

    High school or equivalent (Preferred)
    Experience:

    Front-end development: 1 year (Preferred)
    CSS: 1 year (Preferred)
    Angular: 1 year (Preferred)

    Full Job Description
    Java Developer #java
    Full Time
    Exp: 3-6 years - $95k + Benefits
    Exp: 7-9 Years - $100-110k + Benefits
    Exp: 10+ Years - $115 + Benefits

    Job Type: Full-time

    Pay: $90,000.00 - $115,000.00 per year

    Benefits:

    401(k)
    Dental insurance
    Health insurance
    Life insurance
    Paid time off
    Vision insurance
    Schedule:

    8 hour shift
    Supplemental Pay:

    Bonus pay
    Commission pay
    Signing bonus
    Tips
    Education:

    Bachelor's (Preferred)
    Experience:

    Software Development Occupations: 1 year (Preferred)
    REST: 1 year (Preferred)
    Java: 1 year (Preferred)

    Full Job Description
    Join Filteroff as Software Engineer #1 at the company!

    This is an opportunity to join a newly funded startup, set the Engineering direction, and work closely with Product & Marketing to create an experience that brings humans together.

    Filteroff is the app for human connection.

    We are looking for a Fullstack Software Engineer that is eager to contribute at both a Product and Engineering level. Our team is small, and will rely on your creativity to implement new features, dream up new ones, and execute.

    What makes this exciting?
    Every night, in cities across the world, thousands of users open up Filteroff to go on back-to-back 3-minute video speed dates. If you have experience with "thundering herd" type problems, real-time dating algorithms, want to work with cutting-edge video protocols, and build all types of interesting scam detection systems, you'll love the challenges of Filteroff.

    You will work closely with our co-founder, a fellow Product / Software Engineer.

    Perks:
    - Remote! (or come to our NYC office)
    - Flexible schedule
    - Stock options
    - Health Insurance
    - Employee #2 at a startup

    Responsibilities
    - Write well-designed, testable code
    - Document, discuss, and execute on new features
    - Troubleshoot, debug and upgrade existing systems
    - Help us recruit new engineers
    - Work with Product & Marketing for brand alignment

    Skills
    - Enjoy the quick iteration of dev at a startup
    - Can take a feature from idea to production
    - Backend: Ruby on Rails (or equivalent)
    - Frontend: React Native
    - Experience designing mobile applications
    - Strong knowledge of relational databases (Postgres)
    - Strong knowledge of websockets
    - Proficiency in software dev/deploy tools (Git, Trello, Heroku)
    - Ability to document requirements and specifications

    Job Type: Full-time

    Pay: $71,699.00 - $166,858.00 per year

    Benefits:

    401(k)
    Dental insurance
    Flexible schedule
    Health insurance
    Paid time off
    Schedule:

    8 hour shift
    COVID-19 considerations:
    We work at a WeWork, so you would need to abide by their policy when in office.

    Education:

    Bachelor's (Required)
    Experience:

    Ruby on Rails: 2 years (Preferred)
    React Native: 2 years (Preferred)
    Work Location: Remote

    Full Job Description
    Your Job
    If you are an engineer who's passionate about building impactful products that scale to tens of millions of page views a day, Indeed is looking for you. Indeed offers skilled developers like you a complex development ecosystem with short release cycles. Every week sees the new release of multiple products that meet the needs of jobseekers worldwide.

    Responsibilities:
    Write software to fulfill well-specified, small-scoped work requests for your team's product(s), escalating more complex or ambiguous issues to senior engineers.
    Write software to fix simple bugs.
    Assist in investigating problems and recommending fixes for products within your team.
    Utilize knowledge of programming languages and the software ecosystem to accomplish goals.
    Provide feedback within your team regarding code changes made by other engineers and regarding designs for new enhancements.
    Produce documentation for your team’s products, code, and work items. Grow your skills and knowledge learning from mentors, reading books or online resources, or by observing your co-workers applying their skills and knowledge.
    Who You Are
    Bachelor’s degree in Computer Science, Mathematics, Electrical Engineering, Computer Engineering or equivalent field required.
    1 year of work experience in software programming. Experience must include at least one of the following languages: Java, C, C++, C#, Python, Go, or Perl
    1 year of work experience building applications using at least one of the following:
    Web application technologies including: HTML, CSS, or JavaScript; or
    Databases, including MySQL, Mongo, or a similar program; or
    A collection of systems connected and communicating via a network connection.
    Who we are
    The Product Technology organization is responsible for Indeed’s foundational technology and platforms for job seeker and employer products. We help build and maintain analytics tools used weekly by most Indeedians, guide Indeed’s cloud infrastructure strategy and keep the website up and running, and finally offer secure login, payment, and communication systems for job seekers and employers.
    Our Mission
    As the world’s number 1 job site*, our mission is to help all people get jobs. We strive to cultivate an inclusive and accessible workplace where all people feel comfortable being themselves. We're looking to grow our teams with more people who share our enthusiasm for innovation and creating the best experience for job seekers.

    (*comScore Total Visits, September 2021)
    Salary Range Disclaimer
    The base salary range represents the low and high end of the Indeed salary range for this position. Actual salaries will vary depending on factors including but not limited to location, experience, and performance. The range listed is just one component of Indeed's total compensation package for employees. Other rewards may include quarterly bonuses, Restricted Stock Units (RSUs), an open Paid Time Off policy, and many region-specific benefits.
    Salary Range Transparency
    US Remote 86,000 - 124,000 USD per year
    Equal Opportunities and Accommodations Statement
    Indeed is deeply committed to building a workplace and global community where inclusion is not only valued, but prioritized. We’re proud to be an equal opportunity employer, seeking to create a welcoming and diverse environment. All qualified applicants will receive consideration for employment without regard to race, color, religion, gender, gender identity or expression, family status, marital status, sexual orientation, national origin, genetics, neuro-diversity, disability, age, or veteran status, or any other non-merit based or legally protected grounds.

    Indeed is committed to providing reasonable accommodations to qualified individuals with disabilities in the employment application process. To request an accommodation, please contact Talent Attraction Help at 1-855-567-7767, or by email at TAhelp@indeed.com at least one week in advance of your interview.

    Fair Chance Hiring
    We value diverse experiences, including those who have had prior contact with the criminal legal system. We are committed to providing individuals with criminal records, including formerly incarcerated individuals, a fair chance at employment.
    Our Policies and Benefits
    View Indeed's Applicant Privacy and Accessibility Policies - https://www.indeed.com/legal/indeed-jobs
    Learn about our global employee perks, programs and benefits - https://benefits.indeed.jobs/

    Where legally permitted, Indeed requires all individuals attending or working out of Indeed offices or visiting Indeed clients to be fully vaccinated against COVID-19. For positions that can only be performed at an Indeed office, candidates must be fully vaccinated against COVID-19 and present acceptable proof of vaccination by the date of hire as a condition of employment. Indeed will consider requests for reasonable accommodation as required under applicable law. To qualify as being fully vaccinated against COVID-19 there should have been a two week period after receiving the second dose (or any government recommended booster shot) in a 2-dose COVID-19 vaccine series, or a two week period after receiving a single-dose (or any government recommended booster shot) in a single dose COVID-19 vaccine.

    Full Job Description
    We are looking for a Java Developer with experience in building high-performing, scalable, enterprise-grade applications. You will be part of a talented software team that works on mission-critical applications. Java developer roles and responsibilities include managing Java/Java EE application development while providing expertise in the full software development lifecycle, from concept and design to testing. Java developer responsibilities include designing, developing and delivering high-volume, low-latency applications for mission-critical systems.

    Responsibilities

    Contribute in all phases of the development lifecycle
    Write well designed, testable, efficient code
    Ensure designs are in compliance with specifications
    Prepare and produce releases of software components
    Support continuous improvement by investigating alternatives and technologies and presenting these for architectural review
    Skills

    BS/MS degree in Computer Science, Engineering or a related subject
    Proven hands-on Software Development experience
    Proven working experience in Java development
    Hands on experience in designing and developing applications using Java EE platforms
    Object Oriented analysis and design using common design patterns.
    Profound insight of Java and JEE internals (Classloading, Memory Management, Transaction management etc)
    Excellent knowledge of Relational Databases, SQL and ORM technologies (JPA2, Hibernate)
    Experience in the Spring Framework
    Experience as a Sun Certified Java Developer
    Experience in developing web applications using at least one popular web framework (JSF, Wicket, GWT, Spring MVC)
    Experience with test-driven development
    Job Type: Full-time

    Pay: $80,805.00 - $152,855.00 per year

    Benefits:

    Health insurance
    Schedule:

    8 hour shift
    Education:

    Bachelor's (Required)
    Experience:

    Front-end development: 1 year (Preferred)
    CSS: 1 year (Preferred)
    Angular: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Doozer Software has been providing custom software development solutions, database/BI consulting, and IT staffing services for the past 24 years to companies across the Southeast. Our IT staffing division is currently assisting one of our customers in a search for 3 .NET Developers that will work as contractors until 12/31/2022 and could have option for renewal into 2023 on the project. We are looking for developers that have experience with .NET Core and Microservices. You will create applications from scratch, configure existing systems and provide user support. In this role, you should be able to write functional code with a sharp eye for spotting defects. You should be a team player and excellent communicator. If you are passionate about the .NET framework and software design/architecture, we’d like to talk with you.

    Responsibilities

    Participate in requirements analysis
    Collaborate with internal teams to produce software design and architecture
    Write clean, scalable code using .NET programming languages
    Test and deploy applications and systems
    Revise, update, refactor and debug code
    Improve existing software
    Develop documentation throughout the software development life cycle (SDLC)
    Serve as an expert on applications and provide technical support
    Skills

    Proven experience as a Developer working with .NET Core and Microservices
    Familiarity with the ASP.NET framework, SQL Server and design/architectural patterns (e.g. Model-View-Controller (MVC))
    Knowledge of at least one of the .NET languages (e.g. C#, Visual Basic .NET) and HTML5/CSS3
    Familiarity with architecture styles/APIs (REST, RPC)
    Understanding of Agile methodologies
    Excellent troubleshooting and communication skills
    Attention to detail
    Experience with Kubernetes, Docker, Containers, Bamboo, CI CD, are all a major plus on this engagement but not required
    Job Types: Full-time, Contract

    Pay: $60.00 - $85.00 per hour

    Benefits:

    401(k)
    Dental insurance
    Health insurance
    Vision insurance
    Schedule:

    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    .NET Development: 4 years (Preferred)
    .NET Core: 1 year (Preferred)
    Microservices: 1 year (Preferred)
    Docker, Kubernetes, Bamboo, CI/CD, Containers(Not Required): 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    We are looking for a specialized Game developer to turn a game idea into code on a fast moving environment. You will be involved in various aspects of game’s creation from concept to finished product including coding, programming, audio, design, production and visual arts.

    Responsibilities

    Translate requirements into complicated but clean and efficient code
    Construct the base or the engine on which the game will run
    Produce prototypes of gameplay ideas and features
    Develop schedules and determine milestones
    Generate game scripts and storyboards
    Animate characters and objects
    Contribute to the design and audio features of the game
    Create unit tests and validation procedures to assure quality
    Detect identification and resolution and document technical specifications
    “Polish” the game, maintain code, fix bugs and iron out occurring problems
    Skills

    Proven working experience in full lifecycle game development
    Hands on experience primarily with C++ or other programming languages (Java, C, etc)
    High level knowledge of APIs and libraries
    Expert in one or more programming specialties (artificial intelligence, 3D Rendering, 3D animation, physics, multiplayer/networking, or audio)
    Up-to-date with the latest gaming trends, techniques, best practices and technologies
    Ability to solve problems creatively and effectively
    BS degree in Computer Science or Games Technology
    Job Type: Full-time

    Pay: $78,187.00 - $145,492.00 per year

    Benefits:

    Health insurance
    Schedule:

    8 hour shift
    Monday to Friday
    Education:

    High school or equivalent (Preferred)
    Experience:

    Front-end development: 1 year (Preferred)
    CSS: 1 year (Preferred)
    Angular: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    JOB DESCRITION

    Design, build and configure applications to meet business process and application requirements.
    Provide functional and/or technical expertise to plan, analyze, define and support the delivery of future functional and technical capabilities for an application or group of applications.
    Assist in facilitating impact assessment efforts and in producing and reviewing estimates for client work requests.
    Candidates with Scala experience & AWS certification are desired.
    Job Type: Full-time

    Salary: From $50.00 per hour

    Schedule:

    8 hour shift
    Ability to commute/relocate:

    Reston, VA 20191: Reliably commute or planning to relocate before starting work (Preferred)
    Education:

    High school or equivalent (Preferred)
    Experience:

    Front-end development: 1 year (Preferred)
    Scala: 1 year (Preferred)
    AWS: 1 year (Preferred)
    Work Location: Remote

    Speak with the employer
    +91 8770750390

    Full Job Description
    Software Engineer for a contract position with our client in Richfield, MN.

    Tell us about your department:

    The Space & Visual Merchandising team support the Client design and implementations of retail store layouts (retail floor plans & planograms), recommendations for retail merchandise locations for optimal customer experience and performance of sales and delivering solutions surrounding implementation within the stores.
    This is a growing area with a strategic focus on providing the best shopping experience for our customers.
    Project Description:

    This Engineer will be a member of the application delivery team and will be responsible for designing and building technology solutions that meet our Product and Engineering requirements and deliver the associated benefit.
    This role will be required to apply knowledge and experience to understand business challenges and opportunities, while driving new and innovative approaches to resolving them using a combination of open and closed source technologies.
    Position Summary/Job Description:

    Apply architecture and design principals consistently and holistically to enable target end-to-end usage scenarios
    Adhere to processes around development methodologies including continuous integration, static code analysis, test coverage, etc.
    Perform peer code reviews to ensure quality
    Participate in grooming sessions to ensure sound technical design and story pointing
    Collaborate and create technical specification artifacts required for the epic and/or story
    Work closely with the Engineering Manager and Architect/Lead for design of the application and its nonfunctional requirements for scalability, performance, stability, and supportability.
    Work closely with Product Owner to implement functional requirements to meet business outcome
    Keep up to date on industry technology trends and modern software delivery techniques.
    Developing and maintaining long term business domain knowledge
    Subject matter expert on system behavior of domain features
    How much time will the resource spend pair programming?

    None
    Skills Overview:

    Utilize established development tools, guidelines and conventions using C#/VB.NET,VBScript, ASP.NET, SQL Server, HTML, CSS, JavaScript, PL/SQL.
    Design, code and test new Windows and web software applications.
    Enhance existing systems by analyzing business objectives, preparing an action plan and identifying areas for modification and improvement.
    Maintain existing software systems by identifying and correcting software defects
    Preferred Skills:

    Strong knowledge Database - Access, Oracle, Teradata
    Reporting tool experience- BOBJ, SharePoint
    Experience with Space Management tools, e.g. AutoCAD, Blue Yonder (formally JDA) Space Planning Suite (Space Planning, Floor Planning, IKB, Open Access, Assortment Optimization, Space Automation)
    Experience with Cloud Computing platforms, e.g. Amazon AWS, Microsoft Azure, Google Computing Platform, OpenShift and OpenStack
    If you have the described qualifications and are interested in this exciting opportunity, apply ASAP!

    Genesis10 has been providing staffing services since 1999 and is recognized by Gartner as a Top IT Staffing firm in the U.S. and by Staffing Industry Analysts as an organization that “stands out for its sizeable operation, impressive achievements and as an industry leader in today’s competitive and dynamic ecosystem. Whether you are looking for contract, contract-to-hire, or permanent positions, let's connect today!

    Benefits of Working with Genesis10:

    Medical, Dental, HSA, 401k, etc are available.
    Bi-weekly payroll.
    Established consultant re-marketing program that provides meaningful and challenging on-going opportunities.
    Downtown parking allowance.
    Delivery Director for employee success and support.
    $1000 referral program with the opportunity to earn additional income.
    About Genesis10:
    Genesis10 is a Professional Technology Services Firm providing Staffing, Workforce Optimization and Domestic Outsourcing Solutions. If you are a high performing business or IT professional with solid, referenced experience, we want to meet you. Genesis10 recruiters and delivery professionals are highly accomplished career advocates, who get to know you beyond your resume to position you with the opportunities that fit your skills, experience and aspirations. We have benefit options to fit your needs and a support staff that works with you from placement throughout your engagement – project after project. To learn more about Genesis10 and to view all our available career opportunities, please visit us at www.genesis10.com “Genesis10 is an Equal Opportunity Employer, M/F/D/V”

    Job Types: Full-time, Contract

    Pay: Up to $78.00 per hour

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    Cloud Computing platform: 1 year (Preferred)
    Access, Oracle, Teradata: 1 year (Preferred)
    Reporting tool- BOBJ, SharePoint: 1 year (Preferred)
    Space Management tools: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Position Details:
    Job title: C/C++ Developer
    Location: REMOTE
    Duration: 18 Months

    Interview : C++ programing testing remotely.

    Job Description:
    Complete Description:
    *candidate will work remotely.

    Title: C/C++ Developer
    Description: Candidate will be heavily involved in c/C++ development program.
    We believe that the ideal candidate will have the following skills and abilities:

    C++/C development extensive programing logic
    Education: Bachelors

    Work Authorization : H1b/EAD/GC/Citizen/Any Work Authorization

    Work Type : C2C/W2

    Job Types: Full-time, Part-time, Contract

    Pay: $50.00 per hour

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    C++ Development: 5 years (Preferred)
    C Programming Development: 1 year (Preferred)

    Full Job Description
    New York-based, fully remote digital agency is looking for a creative-technologist with a strong background in software development to provide support of an existing hardware/software project to help push it to MVP launch with the project team.

    A strong candidate will have experience using C-based languages to build and maintain audio/video installations, native app development, WebRTC/WebSockets, and computer vision. Familiarity with Git workflows. We use Jira and Slack for communication.

    Job Types: Full-time, Part-time, Contract

    Pay: $90.00 - $100.00 per hour

    Schedule:

    Monday to Friday
    Education:

    Bachelor's (Preferred)
    Experience:

    C-Based Languages: 7 years (Preferred)
    Native App Development: 7 years (Preferred)
    WebRTC / WebSockets: 7 years (Preferred)
    Work Location: Remote

    Full Job Description
    We are looking for a passionate Software Engineer to design, develop and install software solutions. Software Engineer responsibilities include gathering user requirements, defining system functionality and writing code in various languages, like Java, Python, Angular or .NET programming languages (e.g. C++ or JScript.NET.). Our ideal candidates are familiar with the software development life cycle (SDLC) from preliminary system analysis to tests and deployment. Ultimately, the role of the Software Engineer is to build high-quality, innovative and fully performing software that complies with coding standards and technical design.

    Responsibilities

    Execute full software development life cycle (SDLC)
    Develop flowcharts, layouts and documentation to identify requirements and solutions
    Write well-designed, testable code
    Produce specifications and determine operational feasibility
    Integrate software components into a fully functional software system
    Develop software verification plans and quality assurance procedures
    Document and maintain software functionality
    Troubleshoot, debug and upgrade existing systems
    Deploy programs and evaluate user feedback
    Comply with project plans and industry standards
    Ensure software is updated with latest features
    Skills

    Proven work experience as a Software Engineer or Software Developer
    Experience designing interactive applications
    Ability to develop software in Java, Python, C# or other programming languages
    Excellent knowledge of relational databases, SQL and ORM technologies (JPA2, Hibernate)
    Experience developing web applications using at least one popular web framework (Spring, Django, etc)
    Experience with test-driven development
    Proficiency in software engineering tools
    Ability to document requirements and specifications
    BSc degree in Computer Science, Engineering or relevant field
    Job Types: Full-time, Contract

    Pay: $80,000.00 - $120,000.00 per year

    Schedule:

    8 hour shift
    Monday to Friday
    Application Question(s):

    Do you now or in the future require sponsorship to be employed in the United States?
    Education:

    Bachelor's (Preferred)
    Experience:

    REST: 1 year (Preferred)
    Java: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Design and implement Java applications that fulfill employer requirements
    Create well-written code that runs efficiently and optimally
    Communicate with end-users to determine their needs
    Test completed software and debug as necessary
    Examine existing code and recommend patches, design overhauls or fixes for broken code
    Job Types: Full-time, Contract

    Pay: From $75.00 per hour

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    Experience:

    AWS: 1 year (Preferred)
    ASP.NET: 1 year (Preferred)
    APIs: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Please apply here: https://app.dover.io/apply/netomi/0bcfd174-f3d0-47db-8da3-ff1271f21cf2?rs=55634680

    Netomi is an AI-first customer service platform that enables companies to deliver the highest quality customer experiences while significantly reducing cost. Netomi's Relationship Operating System automatically resolves up to 80% of routine customer service inquiries, decreasing resolution time, and increasing customer satisfaction and support quality. The patented, no-code platform works across messaging, chat, email and voice, and understands 100+ languages. Netomi is based in San Francisco and has offices in New York and India.

    Want to have a direct impact in solving the top challenges businesses face today? Join us!

    Job Description:
    We're looking for a technically savvy & strategically oriented Marketing Analyst based in the US or Canada to help us identify and understand our opportunities for growth and how to best leverage them.

    Job Responsiblities

    Owner of monthly digital marketing & e-commerce reporting, KPI & target tracking with the main objective of automating the reporting process as much as possible
    Leverage data to understand and identify areas of growth for in-depth paid marketing channel performance across different regions and countries
    Develop regional view by markets & channels to measure performance and optimize investment across digital marketing & e-commerce activity.
    Work with engineering leadership to develop tools to help us define our TAM
    Integrate multiple 1st and 3rd party APIs & data sources into structured datasets to generate automated performance tracking dashboards, liaising closely with other key stakeholders and business partners throughout the region.
    Create reports/dashboards by compiling data from different platforms (Salesforce, Hubspot, Google Analytics, etc.).
    Ensure data cleanliness, aligning data sets to stakeholder objectives for reporting & analysis.
    Document key findings for growth opportunities.
    Conduct ad-hoc analyses on key areas of the business.
    Requirements

    Working knowledge of analysis tools like Python and R
    Knowledge of statistical techniques and machine learning algorithms
    Passion for delivering actionable insights
    Strong interpersonal and communication skills
    Prior work or academic experience with MS Excel, PowerPoint
    Analytically inclined, exceptional organizational skills, with rigorous attention to detail
    Ability to learn and adapt on the go : )
    Netomi is an equal opportunity employer committed to diversity in the workplace. We evaluate qualified applicants without regard to race, color, religion, sex, sexual orientation, disability, veteran status, and other protected characteristics.

    Job Type: Full-time

    Pay: $70,000.00 - $110,000.00 per year

    Benefits:

    Dental insurance
    Health insurance
    Paid time off
    Vision insurance
    Schedule:

    Monday to Friday

    Full Job Description
    Worksite location: 100% remote from a home office!

    Position Title: QNXT Data/Business Analysts - FTE/Perm - 5 positions!

    Targeted Salary Range: $90-$115K DOE

    Interview Process: Web interview

    Work Site Location: 100% remote. They will provide computer.

    Top 4 Skills:

    QNXT/Schema knowledge
    Healthcare/business knowledge in member, eligibility, TPL, claims processing, provider, pharmacy claims
    Good/Excellent SQL skills
    Good Oral/Written communication skills
    The candidate are expected to be able to develop program specifications and mapping documents. Perform analysis on data to understand transformation requirements, work with ETL staff to ensure code has been developed that meet the business requirements documented, test the interface/report to ensure requirements are met and work with other team member members.

    Data Analyst Job Description:

    Responsible for performing research and requirement analysis, creation and design of mapping documents, and presents findings to appropriate team members, clients and vendors. Determines best practices and provides suggestions on how to improve current practices.

    · Duties and Responsibilities (List all essential duties and responsibilities in order of importance)

    Creates accurate mapping documents according to the mapping process.
    Works toward delivering a first draft solution to ETL for coding, by rapidly understanding which details about the mapping can be deferred.
    Supports DSD creation and response.
    Presents analysis and design recommendations to lead MITA teams, customer and/or vendors into the acceptance of the design.
    Supports the ETL developers based on the mappings created.
    Works closely with configuration team and DBAs to ensure synchronicity of configuration to interfaces and mappings.
    Refines mapping documents, adding more detail and filling out deferred material as questions are resolved.
    Uses SQL, data models, data element dictionary and schema to perform data and business analysis.
    Creates unit test cases for area of responsibility.
    Validates test plan results that satisfy the detailed design goals.
    Updates technical specifications and mappings.
    Supports Unit Testing, System Integration Testing, System Testing, and User Acceptance Testing.
    · Knowledge, Skills and Abilities ( List all knowledge, skills and abilities that are necessary to perform the job satisfactorily)

    o Analytical and data analysis skills within a technical environment preferably SQL

    o Healthcare knowledge within a claims processing environment preferably in Medicaid

    o Excellent verbal and written communication skills

    o Maintain confidentiality and comply with Health Insurance Portability and Accountability Act (HIPAA)

    o Ability to establish and maintain positive and effective work relationships with coworkers, clients, members, providers and customers

    Job Types: Full-time, Contract

    Pay: $90,000.00 - $115,000.00 per year

    Schedule:

    8 hour shift
    Experience:

    QNXT: 1 year (Required)
    SQL: 5 years (Required)
    ETL: 5 years (Required)
    Mapping: 5 years (Required)
    UAT: 5 years (Preferred)

    Full Job Description
    We are looking for a passionate Data Analyst. The successful candidate will turn data into information, information into insight and insight into business decisions. Data analyst responsibilities include conducting full lifecycle analysis to include requirements, activities and design. Data analysts will develop analysis and reporting capabilities. They will monitor performance and quality control plans to identify improvements.

    Responsibilities

    Interpret data, analyze results using statistical techniques and provide ongoing reports
    Develop and implement databases, data collection systems, data analytics and other strategies that optimize statistical efficiency and quality
    Acquire data from primary or secondary data sources and maintain databases/data systems
    Identify, analyze, and interpret trends or patterns in complex data sets
    Filter and “clean” data by reviewing computer reports, printouts, and performance indicators to locate and correct code problems
    Work with management to prioritize business and information needs
    Locate and define new process improvement opportunities
    Skills

    Proven working experience as a data analyst or business data analyst
    Technical expertise regarding data models, database design development, data mining and segmentation techniques
    Strong knowledge of and experience with reporting packages (Business Objects etc), databases (SQL etc), programming (XML, Javascript, or ETL frameworks)
    Knowledge of statistics and experience using statistical packages for analyzing datasets (Excel, SPSS, SAS etc)
    Strong analytical skills with the ability to collect, organize, analyze, and disseminate significant amounts of information with attention to detail and accuracy
    Adept at queries, report writing and presenting findings
    BS in Mathematics, Economics, Computer Science, Information Management or Statistics
    Job Type: Full-time

    Pay: $80,000.00 - $100,000.00 per year

    Benefits:

    401(k)
    Dental insurance
    Health insurance
    Life insurance
    Paid time off
    Vision insurance
    Schedule:

    Monday to Friday
    Experience:

    SQL: 1 year (Preferred)

    Full Job Description
    DSM is in search of qualified applicants for its Business Analyst position. In this role you work will directly with DSM’s clients to identify and solve challenging business problems using data, analytics and technology. Successful team members are excellent communicators, able to learn new technologies and business concepts quickly, and work well in team settings.

    Responsibilities

    Data Preparation: Validate, cleanse, and integrate data from various sources to support reporting and analysis objectives
    Reporting: Build and maintain reports for clients in various formats; including web-based dashboards, MS Excel, and MS PowerPoint
    Analysis: Conduct analysis on data to answer important business questions
    Reporting and Analysis Design: Create reports, data visualizations, analyses, and/or decision models to answer important business questions. Design measurement frameworks to evaluate operational performance.
    Quality Assurance Testing: Test applications, databases, and reports to ensure data accuracy and proper function
    Workstream Management: Support one or more workstreams of a client project, collaborate with internal and external stakeholders
    Requirements

    Bachelor’s degree in Business, Economics, Information Systems, or similar field of study
    Excellent written and verbal communication skills
    Preferences

    Experience with relational database management systems (e.g., Microsoft SQL Server)
    Experience with data visualization software (e.g., Tableau, Microsoft Power BI)
    Background in data science, machine learning, data mining, and/or statistics
    Job Type: Full-time

    Pay: $80,000.00 - $110,000.00 per year

    Benefits:

    401(k)
    401(k) matching
    Dental insurance
    Health insurance
    Paid time off
    Parental leave
    Referral program
    Vision insurance
    Schedule:

    Monday to Friday
    Supplemental Pay:

    Bonus pay
    Signing bonus
    Work Location: Remote

    Full Job Description
    Required Skills:

    Strong communication skills - the role requires engagement with senior business stakeholders
    Excellent problem solving
    Senior, self-starter
    Independent, proactive
    Analytical, Excel spreadsheet savvy
    Very curious
    Insurance experience
    Employee Benefits experience a plus
    FINEOS exposure a plus
    Job Type: Full-time

    Salary: Up to $68.00 per hour

    Work Location: Remote

    Full Job Description
    Position: Business Data Analyst

    Location: Remote

    duration: 12 months +

    Business Data Analyst with experience in Retail Banking business.

    Good understanding of the data models in the domains-Customer, Products ( Deposits, Loans, Cards, Payments) & related services). Experience in the data analysis work : source to target, target to source - data mapping , business rules , data validation.

    Nice to have : Core banking project - rollover, data migration experience, basic understanding of canonical models, APIs.

    Unable to consider consultants who require sponsorship now or in future

    Job Types: Full-time, Contract

    Pay: $60.00 - $65.00 per hour

    Schedule:

    8 hour shift
    Work Location: Remote

    YOUR LIFE'S MISSION: POSSIBLE

    You have goals, dreams, hobbies and things you’re passionate about.


    What’s Important to You Is Important to Us
    We’re looking for people who not only want to do meaningful, challenging work, keep their skills sharp and move ahead, but who also take time for the things that matter to them—friends, family and passions. And we're looking for team members who are passionate about our mission—making a difference in military members' and their families' lives. Together, we can make it happen.


    Don’t take our word for it.

    FORTUNE 100 Best Companies to Work For®
    Computerworld® Best Places to Work in IT
    FORTUNE® Best Workplaces for Millennials
    Forbes® America’s Best Employers
    Basic Purpose

    Data Analysts document data requirements, analyze data in source systems and its suitability for usage, create data mappings with derivation rules as integration specifications, create data models, perform root causes analysis, develop queries and notebooks, develop dashboards and reports, load and manage metadata.

    Responsibilities:

    Document source data requirements and create mappings between business terms, source system tables/columns, and target database schemas, including derivation rules and transformations as ETL specifications
    Conduct analysis of data contained in source systems and its suitability for usage through data profiling, and data quality assessment
    Create and maintain conceptual, logical, and physical data models; create and publish data element definitions for use in metadata repositories
    Perform root cause and impact analyses in support of business data stewards, Data Engineers, SQA and user acceptance testers
    Create advanced SQL queries; develop Databricks notebooks using Python
    Conduct basic statistical analyses
    Visualize data metrics and trends using dashboards and reports
    Collaborate well with a range of roles from business customers to IT partners, service providers, and vendors
    Create and deliver end-user training and documentation and provides second-line support to power users
    Provide coaching and mentorship to junior data analysts.
    Provide direction and leadership for a team of data analysts.

    Qualifications and Education Requirements:

    Experience translating user needs into data requirements, estimating work effort and duration
    Experience in data profiling, data mapping with derivation rules, and data quality assessments
    Experience in data modeling
    Experience conducting root cause analysis and impact assessments
    Advanced SQL query programming experience
    Experience in Python programming
    Experience using Jupyter and/or Databricks Notebooks
    Working knowledge of relational, NoSQL and columnar databases
    Bachelor’s degree in MIS, computer science, statistics, marketing, management, finance, related fields or equivalent experience
    Experience creating reports and dashboards
    Ability to interpret and update complex technical documentation
    Excellent written and oral communication skills
    Desired: Prior experience in the Financial Industry

    Desired Qualifications and Education Requirements:

    Ability to interpret complex mainframe copybooks, and XML data feeds
    Master’s degree in computer science, statistics, or related field
    Prior experience in the Financial Industry
    Experience in the MS Azure technology stack
    Experience with data mining, pattern matching, forecasting, sentiment analysis, cluster analysis or similar
    Knowledge of Navy Federal Credit Union instructions, standards, and procedures

    Hours: Monday - Friday, 8:00am - 4:30pm

    Location: 820 Follin Lane, Vienna, VA 22180 | 5550 Heritage Oaks Dr Pensacola, FL 32526 | 141 Security Dr. Winchester, VA 22602 | Remote

    Due to COVID-19 and social distancing, this position will be temporarily working from home with plans to return to campus at the desired location listed once Navy Federal is back to normal operations. The specific logistics for returning to campus will be determined at a future date by individual leadership.

    Salary: Navy Federal Credit Union assesses market data to establish salary ranges that enable us to remain
    competitive. You are paid within the salary range, based on your experience, location and market position.

    The salary range for this position is: $72,300 to $142,000
    #LI-Remote
    Equal Employment Opportunity

    Navy Federal values, celebrates, and enacts diversity in the workplace. Navy Federal takes affirmative action to employ and advance in employment qualified individuals with disabilities, disabled veterans, Armed Forces service medal veterans, recently separated veterans, and other protected veterans. EOE/AA/M/F/Veteran/Disability

    COVID-19 Vaccine Information

    As a COVID-19 safety measure, our employees must either provide proof of COVID-19 vaccination or follow additional safety protocols, including testing.

    Disclaimer

    Navy Federal reserves the right to fill this role at a higher/lower grade level based on business need. An assessment may be required to compete for this position.

    Bank Secrecy Act

    Remains cognizant of and adheres to Navy Federal policies and procedures, and regulations pertaining to the Bank Secrecy Act.

    Employee Referrals

    This position is eligible for the TalentQuest employee referral program. If an employee referred you for this job, please apply using the system-generated link that was sent to you.

    Full Job Description
    Octave is a national behavioral health practice creating a new standard for care delivery that’s both high-quality and accessible to more people. With in-person and virtual clinics in California and New York, we offer personalized care plans that can include individual therapy, couples therapy, and groups, while pioneering relationships with payers to make care more affordable through insurance. Grounded in science, Octave enables clients to experience profound change that is as measurable as it is meaningful. Learn more at www.findoctave.com

    Job Type: Full-time

    Position: Business Data Analyst

    Location: Remote

    Duration: 12 months

    Description:

    Business Data Analyst with experience in Retail Banking business.

    Good understanding of the data models in the domains-Customer, Products ( Deposits, Loans, Cards, Payments) & related services). Experience in the data analysis work : source to target, target to source - data mapping , business rules , data validation.

    Nice to have : Core banking project - rollover, data migration experience, basic understanding of canonical models, APIs.

    not accepting consultants who need sponsorship now or in future

    Job Types: Full-time, Contract

    Pay: $60.00 - $65.00 per hour

    Full Job Description
    Remote Business Analyst
    24+ Months
    Office of Child Support Enforcement
    Skills:

    Knowledge or experience with Software Engineering (IEEE) Capability Maturity Model (CMM) standards. Knowledge or experience with Full Development Life-Cycle (FDLC) methodologies.
    Familiar with SQL tools. Experience with 508 compliancy. Knowledge of object oriented programming analysis methods.
    Experience with or knowledge of data modeling and modeling tools.
    Experience with building customer relationships to prioritize and analyze system issues.
    Provide subject matter expertise on how State Disbursement Units (SDU) work and have knowledge of system capabilities of different payment systems in the child support enforcement domain.
    Provide expert guidance on different file formats – ACH/NACHA/SPS etc., and bringing up any nuances associated with their usage that needs to be well understood by all the groups involved
    Document the interfacing needs with all of the stakeholder systems involved with international payment processing system.
    Help with high level UI mockups/prototypes.
    Help with system validation once the software has been developed.
    Work closely work with the Project Manager, technical architect and the other development staff.
    Job Types: Full-time, Contract

    Pay: $50.00 - $60.00 per hour

    Schedule:

    8 hour shift
    COVID-19 considerations:
    yes

    Experience:

    SQL: 1 year (Preferred)

    Full Job Description
    Contract Type: W2 Only
    This is a Fully Remote position

    REQUIRED SKILLS:

    Bachelor’s Degree in a quantitative discipline (e.g. Statistics, Math, Computer Science, Data Science, Analytics, or similar)
    2+ years of experience in Business Intelligence, Data Analytics, or related quantitative functions
    2+ years of experience in performing data analysis on Microsoft Excel using various functions (VLOOKUP, Pivot table, dashboards, Slicers, etc.)
    Knowledge and direct experience using business intelligence reporting tools (such as Tableau, Power BI etc.)
    Job Types: Full-time, Contract

    Pay: $35.00 - $55.00 per hour

    Experience:

    SQL: 1 year (Preferred)

    Full Job Description
    Post1

    Job Title: Business Analyst
    Location: Bowie, MD
    Duration: 12+ Months

    Job Description:

    The Business Analyst is the liaison between the design and development teams and the client to define the objectives and requirements of the client.
    Finalizes the implementation process by implementing development plans
    Job Requirements:

    Minimum of 4 years of experience as a software business analyst
    Minimum of 1 year of experience in a healthcare/specialty pharmacy related environment.
    Must be familiar with healthcare/pharmacy system designs and concepts
    Possesses excellent communication, organizational and observational skills
    Proficient problem solving skills with good judgment and decision making
    Must be goal-oriented and focused
    Work well as a member of a team
    Possess SQL and Crystal Reports skills.
    Job Types: Full-time, Contract

    Salary: $45.00 - $54.00 per hour

    Schedule:

    8 hour shift
    Day shift
    Monday to Friday
    Work Location: Remote

    Full Job Description
    Position: Business Analyst with Insurance

    Location: Remote Intial/Piscataway, New Jersey

    Duration: 6+ Months

    Required Skills:

    Strong communication skills - the role requires engagement with senior business stakeholders
    Excellent problem solving
    Senior, self-starter
    Independent, proactive
    Analytical, Excel spreadsheet savvy
    Very curious
    Insurance experience
    Employee Benefits experience a plus
    FINEOS exposure a plus
    Job Types: Full-time, Contract

    Salary: $55.00 - $60.00 per hour

    Schedule:

    8 hour shift
    Experience:

    SQL: 1 year (Preferred)
    Work Location: Remote

    Full Job Description
    Title: Data Visualization Expert / UI design
    Location: Remote, may need to come to Herndon periodically
    Clearance: PT required, or Secret Preferred

    Key Requirements:
    someone with Grafana is a plus

    Mandatory Skills/Experience:

    Experience architecting, analyzing, modeling and orchestrating performance management initiatives, develop and implement IT Balanced Scorecard concepts for a large organization.

    Knowledge of industry standard key performance indicators (FCR, MTTR, ASA, etc.) and specific charts associated with Six Sigma and IT Service Management.

    Experience with data visualization design, relational database principles, demonstrated experience with performance and process improvement, demonstrated experience in developing and implementing IT Balanced Scorecard concepts for large organizations, experience with enterprise tool not limited to Enterprise Service Management Tool (ESMT), JIRA, Primavera, experience with Tableau

    Desired Skills/Experience: ITIL; Desired Certifications: ITIL.

    Job Type: Full-time

    Pay: $150,000.00 - $160,000.00 per year

    Benefits:

    401(k) matching
    Education:

    Bachelor's (Preferred)
    Experience:

    Data Visualization: 1 year (Required)
    UI: 1 year (Preferred)
    Grafana: 1 year (Preferred)
    Public Trust: 1 year (Required)
    Work Location: Remote

    Full Job Description
    The Business Analyst role is to complement and support the Product Owner.

    PRIMARY ACCOUNTABILITIES

    Lead the analysis and thorough documentation of current and future state business processes that require improvements
    Design and develop requirements including writing basic functional and non-functional specifications, user interface mock-ups, process and data flow diagrams, dashboards, reports
    Participate in daily scrum sessions, writing stories and identifying Acceptance Criteria or gathering and composing other on-demand documentation.
    Develop, improve and oversee the review and validation of written specifications with the subject matter experts, development team members, and other partners to ensure on-time completion with all necessary sign offs.
    Responsible for acting as a liaison between Product Owner and development team
    Together with the Product Owner they are responsible for making recommendations about products and features that would support a positive, secure and efficient customer experience
    Analyze the 3rd party/ product integration aspects of business requirements and be able to effectively work with vendors to implement such requirements
    Assist the Product Owner in the testing of new product features: design test cases to monitor system functionality and support system enhancements
    Partner with Product Owner to monitor and evaluate processes and KPIs in order to improve the customer experience
    QUALIFICATIONS

    Education

    Master’s degree in Computer or Science, Information Systems, or a related discipline (Highly Desired).
    Experience

    4+ experience in either a consulting environment, focused on store technology capabilities, or in similar roles in diversified, multi-brand businesses.
    Previous experience in Business Analyst role
    Exposure to retail and fashion industry
    Essential an understanding of digital capabilities in store
    Skills

    team-oriented, excellent communication skills and is highly organized
    Skilled in Agile.
    Knowledge and experience of business analysis tools such as Use Cases, Activity Diagrams, User Stories, etc.
    Language Skills: English fluency

    Job Types: Full-time, Contract

    Pay: $65.00 per hour

    Schedule:

    8 hour shift
    Education:

    Bachelor's (Preferred)
    License/Certification:

    PMP (Preferred)
    Work Location: Remote

    Full Job Description
    Title: Security Analyst

    Location: Remote

    Duration: 12 Months+

    Description:

    Demonstrated experience working in a SOC triaging, investigating, and responding to security events and data breach incidents.
    Experience with forensic analysis of multiple forms of digital files and media from a diverse array of operating systems (Windows, Linux, BSD), application and data platforms
    Experience in developing services or scripts for automation of data analysis, incident response, and/or digital forensics
    Experience in reverse engineering and debugging basic malware and malicious actor techniques
    Experience with threat hunting and the application of appropriate behavior-based models
    One or more of the following information security-related qualifications or demonstrable equivalent experience/certifications: CFCE, GCFA, GNFA, GCIH, GCFE, OSCP, CISSP

    Job Types: Full-time, Part-time, Contract

    Schedule:

    Monday to Friday
    Work Location: Remote


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