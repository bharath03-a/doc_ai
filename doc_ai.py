project_id = "manifest-craft-316206"
location = "us"  # Format is 'us' or 'eu'
processor_id = "ac2b1ccb698027af"  # Create processor in Cloud Console
#file_path = "inv_1.pdf" # Update to path of target document
file_path = "inv_2.pdf"

from google.cloud import documentai_v1 as documentai
import json

def process_document_sample(project_id: str, location: str, processor_id: str, file_path: str):
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Read the file into memory
    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    # Recognizes text entities in the PDF document
    result = client.process_document(request=request)
    document = result.document
    print("Document processing complete.")
    document_pages = document.pages

    # Read the text recognition output from the processor
#     print("The document contains the following paragraphs:")
#     for page in document_pages:
#         paragraphs = page.paragraphs
#         for paragraph in paragraphs:
#             paragraph_text = get_text(paragraph.layout, document)
#             print(f"Paragraph text: {paragraph_text}")
    
    fin = {}
    lis = []
    c = 1
    print("Printing as its key-value pairs:")
    for page in document_pages:
        
        print("Page number: {}".format(page.page_number))
        for field in page.form_fields:
            dic = {"fieldName" : "1", "fieldValue" : "2"}
            #print("Field Name: {}".format(get_text(field.field_name, document)))
            #print("Field Value: {}".format(get_text(field.field_value, document)))
            str1 = get_text(field.field_name, document)
            str2 = get_text(field.field_value, document)
            dic["fieldName"] =  str1[:-2]
            dic["fieldValue"] =  str2[:-2]
            lis.append(dic)
            fin[c] = dic
            c = c + 1
    
    jsonStr = json.dumps(fin,indent = 1)
    #print(fin)
    #print(lis)
    print(jsonStr)
    with open("inv_2.json", "w") as outfile:
        outfile.write(jsonStr)
            


# Extract shards from the text field
def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

# doc = process_document_sample(project_id, location, processor_id, file_path)
if __name__ == "__main__":
    process_document_sample(project_id, location, processor_id, file_path)
