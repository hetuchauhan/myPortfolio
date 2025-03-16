import pypdf, pandas
import os
import json 

def extract_pdf(pdf_path):
    
    try:
        with open(pdf_path, "rb") as file:
            print("file opened")
            reader = pypdf.PdfReader(file)
            fields = reader.get_fields()
            print(fields)
                                                                    #actually getting the fields
            if fields:
                print("retrieved")
                return {key: fields[key].get('/v','N/A') for key in fields}
                
            else:
                return None
            
    except Exception as exp:
        print(f"Error Processing {pdf_path}: {exp}")
        return None
    
def process_pdfs_in_folder(folder_path, output_json):                           #getting all files in the dir
    
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    all_data = []
    skipped_files = []
    os.path.dirname(folder_path)
    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        form_data = extract_pdf(pdf_path)

        if form_data:
            form_data["Pre-filled PDFs"] = pdf  # Add filename for reference
            all_data.append(form_data)
        else:
            skipped_files.append(pdf)

    # Save extracted data to JSON
    if all_data:
        with open(output_json, "w", encoding="utf-8") as json_file:
            json.dump(all_data, json_file, indent=4)
        print(f"JSON file saved at: {output_json}")
    else:
        print(" No fillable PDFs found or no data extracted.")

process_pdfs_in_folder(r"D:\pdf files for code", r"D:\pdf files for code\output.json") #1. directory, 2. output