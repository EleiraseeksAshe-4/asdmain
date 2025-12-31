import glob
import os
import fitz
from langchain.chains.llm import LLMChain
from langchain.schema import Document
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts import PromptTemplate

## YOU NEED TO INSTALL pymupdf FOR THIS TO WORK
def read_document(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
    #return Document(title=os.path.basename(file_path), content=content)

def save_file(filepath, data):
    with open(filepath, 'w') as f:
        f.write(data)

def submit_query(client, query, documents):
    context = {
        'question': query,
        'documents': documents
    }
    response = client.run_chain(prompt='SimpleQA', initial_context=context)
    return response

def init_openai():
    api_key = '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'
    os.environ["OPENAI_API_KEY"] = api_key

    template = """
    # Define the prompt template
    Context: {context}
    Question: {question}
    Answer:
    """

    # Create a PromptTemplate instance
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    # Initialize the OpenAI LLM with LangChain
    llm = OpenAI(model="gpt-4")

    # Create an LLMChain with the prompt template and the LLM
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain

def main():

    chain = init_openai()

    fileroot = '/Users/johnbridges/Dropbox/NewHope Psychology/JoyConsulting/GateInc/ExpertReports/clients/active/'
    # List of file paths to be attached to the query
    search_pattern = os.path.join(fileroot, '**', '*Intake.pdf')
    intake_files = glob.glob(search_pattern, recursive=True)

    # Read the documents
    for filepath in intake_files:
        documents = []
        document = read_document(filepath)

        path = filepath.split('/')
        # naughty because we know there are only intake files on one level
        clientref = path[len(path) - 2]
        output_path = f"{fileroot}{clientref}/clientdata.json"
        # Define your query
        query = "Taking the data from the attached form, using the headings as keys format as json the information from the attached file. Utilise underscores to fill spaces in keys.The form has sectional headings - e.g. section 1 - Please enter the childs information - can you nest the data for each section using a summarised version of the question as a key - e.g. Please enter the child's information would become 'childs_information'"

        # Submit the query and get the response
        response = chain.run({"context": document, "question": query})

        save_file(output_path, response);

    # Print the response
    print(response)

if __name__ == "__main__":
    main()