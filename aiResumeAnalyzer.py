import openai
import PyPDF2
import docx2pdf
from dotenv import load_dotenv
import os

def convert_to_pdf(file_path):
    # Convert the DOCX file to PDF
    pdf_file_path = file_path.replace(".docx", ".pdf")
    docx2pdf.convert(file_path, pdf_file_path)
    return pdf_file_path


def read_resume_pdf(file_path):
    # Read the resume PDF file
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        resume_text = ""
        for page in range(len(pdf_reader.pages)):
            resume_text += pdf_reader.pages[page].extract_text()
    return resume_text

def analyze_resume_job_match(resume_text, job_description):
    # Set up your OpenAI API credentials
    openai.api_key =os.environ["OPENAI_API_KEY"]

    # Define the prompt for the ChatGPT API
    prompt =  f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n\n Analyze how well the resume matches the job description, \
        then Analyze the resume and provide an estimate percentage of how well it matches the job description\
        Additionally, provide critiques on the resume:"


    # Call the ChatGPT API to analyze the resume and job description
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000,
        temperature=0.7
    )

    # Extract the analysis response from the API response
    analysis_response = response.choices[0].text.strip()
    return analysis_response

def main():
    # Load the API key from .env file
    load_dotenv()
    # Specify the file path to your resume PDF
    resume_file_path = '/Users/a.cube/Downloads/afolabi technical resume.pdf'

    # Specify the job description
    job_description = """
    The Back End Software Engineer is responsible for the following:
    • Develop server-side logic, definition and maintenance of the central database, and ensure high performance and responsiveness to requests from the front-end developers.
    • Integrate user-facing elements developed by front-end developers with server-side applications.
    • Collaborate with front-end developers, customers, users and Product Managers to establish objectives and design functional, cohesive codes to enhance the user experience.
    • Keep abreast of novel technical concepts and markets.
    • Provide technical leadership and documentation to developers and stakeholders.
    • Apply usability procedures and principles as defined at the project or Product Line level or through customer input.
    • Build prototypes, products and systems that meet the project quality standards and requirements.
    • Contribute to and support re-use through common components that are well documented and tested
    """
    if resume_file_path.endswith('.docx'):
        pdf_file_path = convert_to_pdf(resume_file_path)
    else:
        pdf_file_path = resume_file_path

    # Read the resume PDF file
    resume_text = read_resume_pdf(pdf_file_path)

    # Analyze the resume and job description match
    match_analysis = analyze_resume_job_match(resume_text, job_description)

    # Print the analysis result
    print(f"Resume-Job Description Analysis:\n{match_analysis}")

if __name__ == "__main__":
    main()
