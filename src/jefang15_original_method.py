# TODO: figure out if there's a more efficient way of doing this procedure. I'm not familiar with the string.replace() function's efficiency.
def remove_punctuation(split_text_list):
    clean_split_text_list = [  # Remove punctuation from list of words in job description
        word.replace('•', "")
            .replace(",", "")
            .replace("""""", "")
            .replace("-", "")
            .replace("'", "")
            .replace("''", "")
            .replace(":", "")
            .replace(";", "")
            .replace("*", "")
            .replace("!", "")
            .replace("&", "")
            .replace("/n", "")
            .replace("/", "")
            .replace("?", "")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
            .replace("…", "")
        for line in split_text_list for word in line.lower().split()
        ]
    return clean_split_text_list

def Jefang15_comparison(job_posting, resume):
    # we're taking job_posting and resume as arguments so that we can use this code for multiple job postings and resumes.

    " Step 2: Remove punctuation from job posting "

    job_posting_list = job_posting.split()  # Creates a list of words in the job description

    clean_job_posting = remove_punctuation(job_posting_list)

    job_count = dict()
    for i in clean_job_posting:
        job_count[i] = job_count.get(i, 0) + 1

    " Step 6: Remove punctuation from resume "

    resume_list = resume.split()  # Creates a list of words in your resume

    clean_resume = remove_punctuation(resume_list)

    resume_count = dict()

    for i in clean_resume:
        resume_count[i] = resume_count.get(i, 0) + 1


    " Step 3: Remove common filler words in job posting "
    # Feel free to add additional words to the list below that appear frequently in job posts (e.g. task, qualification, etc.)

    common_job_words = [

        'a', 'ability', 'about', 'added', 'against', 'an', 'and', 'any' 'are', 'as', 'assist', 'assisting', 'at',

        'be', 'both', 'but', 'by',

        'can',

        'demonstrate', 'demonstrated', 'duties'

        'employee', 'every', 'existing', 'experience',

        'following', 'for', 'from',

        'gpa',

        'have',

        'in', 'including', 'identify', 'into', 'is', 'it',

        'make', 'members', 'more', 'must',

        'not',

        'obtain', 'of', 'on', 'opportunity', 'or', 'other', 'our',

        'preferred',

        'qualifications',

        'reach', 'require', 'required',

        'skill', 'skills', 'strong', 'such', 'support', 'supporting',

        'that', 'the', 'their', 'this', 'to',

        'upon', 'us', 'use', 'using',

        'we', 'will', 'with', 'work', 'working',

        'you', 'your',

        ]


    " Step 4: Show top keywords in the job posting and count their frequency "

    for key in list(job_count.keys()):
        if key in common_job_words:
            del job_count[key]

    job_keywords_count = sorted(job_count.items(), key=lambda x: x[1], reverse=True)
    print(job_keywords_count)

    " Step 7: Remove common filler words in resume "
    # Feel free to add words to the list that appear frequently in your resume (e.g. cities you have worked in, your name, etc.)

    common_resume_words = [
        '2018', '2019', '2020', '2021', '2022', '2023',

        'a', 'an', 'and', 'as',

        'be', 'bloomington',

        'dc', 'december',

        'every', 'existing', 'experience',

        'from', 'for',

        'have',

        'in', 'into', 'is', 'it',

        'may',

        'obtain', 'of', 'on', 'opportunity', 'or', 'our',

        'portland',

        'spea', 'strong', 'support', 'supporting',

        'that', 'the', 'their', 'to',

        'university', 'us', 'use',

        'washington', 'we', 'will', 'work', 'with',

        'you', 'your',

        ]

    for key in list(resume_count.keys()):
        if key in common_resume_words:
            del resume_count[key]


    " Step 8: Show top keywords in your resume and count their frequency "

    resume_keywords_count = sorted(resume_count.items(), key=lambda x: x[1], reverse=True)
    #print(resume_keywords_count)


    " Step 9: Identify key words in job posting that are not in your resume "

    # TODO: can improve by using the job_keywords_count and resume_keywords_count variables, which are lists not dictionary.
    missing = {k: v for k, v in job_count.items() if k not in resume_count}
    missing_keywords = sorted(missing.items(), key=lambda x: x[1], reverse=True)
    print("Missing keywords")
    print("----------------")
    for i in missing_keywords:
        print(i[0], i[1])

    " Step 10: Identify key words in your resume that are not in the job posting "