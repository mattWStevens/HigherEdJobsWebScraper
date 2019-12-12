# web_scraper.py
# author: Matthew Stevens

from bs4 import BeautifulSoup
import re
import sys

cs_or_ce = sys.argv[1]  # Flag to indicate whether mining CS or CE

csv_array = []  # We will store all job information here.

num_pages = 13 if cs_or_ce == "CS" else 5

# Iterate over each result page.
for i in range(1, num_pages):
    if cs_or_ce == "CS":
        job_file = "comp_sci/results_page" + str(i) + ".html"

    else:
        job_file = "comp_eng/results_page" + str(i) + ".html"

    # Check current results page.
    with open(job_file, "r") as f:
        contents = f.read()

        page_content = BeautifulSoup(contents, "html.parser")

        # Obtain all job postings for current page.
        results = page_content.find_all("div", class_="row record")

        # Gather relevant data for each job.
        for result in results:
            job_details = result.find("div", class_="col-sm-7")

            job_title = job_details.find("a").getText().strip()
            # Get rid of comma if present, can cause problems with csv.
            job_title = job_title.replace(",", " ")
            university = ""

            # We already have the job title, this will make it easier
            # to parse out the rest of the info.
            job_details.a.extract()

            # This span element, if it exists
            # does not contain useful information.
            if job_details.find("span"):
                job_details.span.extract()

            # Convert HTML to string representation
            # to make it easier to gather the job
            # information that is spaced out throughout
            # the div element.
            job_string = job_details.prettify()
            job_array = job_string.split("<br/>")
            university = job_array[1].strip()
            # Get rid of comma if present, can cause problems with csv.
            university = university.replace(",", " ")

            location = job_array[2]
            location = job_array[2].replace("</div>", "").strip()
            # Get rid of comma in location, can cause problems with csv.
            location = location.replace(",", " ")

            application_details = result.find("div", class_="col-sm-5 text-sm-right")

            application_string = application_details.prettify()
            application_array = application_string.split("<br/>")

            # Gather the date and job type of the posting.
            job_type = application_array[0][application_array[0].find(">") + 1:].strip()
            # Get rid of comma if present, can cause problems with csv.
            job_type = job_type.replace(",", " ")
            date = re.search("[0-9]{2}/[0-9]{2}/[0-9]{2}", application_array[1]).group(0)

            # Save job information for use in writing csv later on.
            row = [job_title, university, location, job_type, date]

            csv_array.append(row)


# Write the csv file.
file_name = "comp_sci.csv" if cs_or_ce == "CS" else "comp_eng.csv"
csv = open(file_name, "w+")

# Put headers into csv.
csv.write("job_title,university,location,job_type,date\n")

# Put each job information row in the csv.
for line in csv_array:
    for i in range(len(line)):
        if i != len(line) - 1:
            csv.write(line[i] + ",")

        else:
            csv.write(line[i] + "\n")

csv.close()