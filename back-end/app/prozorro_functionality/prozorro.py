import requests
import pandas as pd
from fastapi import HTTPException
import camelot.io as camelot
from dotenv import load_dotenv
import fitz
import ocrmypdf
import os

BASE_URL = 'https://public.api.openprocurement.org/api/2.5'

def get_contract(contract_id):
    url = f'{BASE_URL}/contracts/{contract_id}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.HTTPError as err:
        raise HTTPException(status_code=response.status_code, detail=f"Error: {err}")

def get_pdf_url(documents):
    url = []

    for doc in documents:
        if doc.get('confidentiality') == 'public' and doc.get('format') == 'application/pdf':
            url.append(doc.get('url'))
    if not url:
        raise Exception("There are not pinned files connected to tender!")
    return url


def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as ex:
            print(f"Error while deleting {file_path}: {ex}")


def get_splited_pdf_by_pages(input_pdf):
    """This func return list of paths with splited pdf by pages"""
    doc = fitz.open(input_pdf)
    splited_pdf = []
    for i in range(len(doc)):
        page = fitz.open()
        path_to_page = f"app/prozorro_functionality/temp_pdf/page_{i}.pdf"
        page.insert_pdf(doc, from_page=i, to_page=i)
        page.save(path_to_page)
        splited_pdf.append(path_to_page)
    return splited_pdf


def ocr_pdf(inputFile, num_of_page, lang = "ukr+eng", pagesegmode = 3, ocr_engine_mode = 1, force_ocr = True, deskew = True, clean_final = True):

    ocrmypdf.ocr(
        input_file=inputFile,
        output_file=f"app/prozorro_functionality/temp_pdf/page_{num_of_page}_ocred.pdf",
        language=lang,
        tesseract_pagesegmode=pagesegmode,
        tesseract_oem=ocr_engine_mode,
        force_ocr=force_ocr,
        output_type="pdf",
        deskew=True,
        rotate_pages=True,
        pdf_renderer="hocr",
        #optimize=3,
        #clean_final=clean_final
    )
def get_table_from_pdf(path_to_pdf):
    splited_pdf = get_splited_pdf_by_pages(path_to_pdf)
    table_list = []
    first_skip = True
    for page_num in range(len(splited_pdf)-1, -1, -1):
        print(page_num)
        ocr_pdf(f"app/prozorro_functionality/temp_pdf/page_{page_num}.pdf", page_num)
        tables = camelot.read_pdf(f"app/prozorro_functionality/temp_pdf/page_{page_num}_ocred.pdf", pages="all", split_text=True, strip_text='\n',
                                  line_scale=15, flavor="lattice")
        if tables.n == 0 and first_skip == True:
            first_skip = False
            continue
        elif tables.n == 0 and first_skip == False:
            break

        for table in tables:
            table_list.append(table.df)

    if not table_list:
        raise Exception("There are no tables in document!")


    return table_list

def load_pdf(url):
    response = requests.get(url)
    with open('app/prozorro_functionality/temp_pdf/temp_pdf.pdf', 'wb') as file:
        file.write(response.content)

def find_col_idx(df):
    last_col = df.columns[-1]
    df[last_col] = df[last_col].str.replace('|', '').str.replace(' ', '').str.replace(',', '.')
    df[last_col] = pd.to_numeric(df[last_col], errors='coerce')
    indices = {'total_price': df.columns.get_loc(last_col)}
    for col in df.columns[-2::-1]:
        if df[col].str.contains('%').any():
            continue
        df[col] = df[col].str.replace('|', '').str.replace(' ', '').str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
        indices['unit_price'] = df.columns.get_loc(col)
        break

    df[indices['unit_price']-1] = df[indices['unit_price']-1].str.replace('|', '').str.replace(' ', '').str.replace(',', '.')
    df[indices['unit_price']-1] = pd.to_numeric(df[indices['unit_price']-1], errors='coerce')
    indices['quantity'] = (indices['unit_price']-1)


    df[indices['quantity']-1] = df[indices['quantity']-1].str.replace('|', '').astype(str)
    indices['unit_name'] = (indices['quantity']-1)


    for col in df.columns[1:]:
        if df[col].str.contains(r'^\d{8}-\d$', na=False).any() or df[col].str.contains(r'^\d{7}$', na=False).any():
            continue
        indices['name'] = df.columns.get_loc(col)
        break

    print("Total_price: ", indices['total_price'])
    print("Name: ", indices['name'])
    print("Unit_name: ", indices['unit_name'])
    print("Unit_price: ", indices['unit_price'])
    print("Quantity: ", indices['quantity'])


    return df, indices


def parse_pdf(documents_url):
    clear_folder("app/prozorro_functionality/temp_pdf")

    items = []
    for doc in documents_url:
        load_pdf(doc)
        table_list = get_table_from_pdf("app/prozorro_functionality/temp_pdf/temp_pdf.pdf")
        concat_table = pd.concat(table_list, ignore_index=True)
        res, indices = find_col_idx(concat_table)

        for index, row in res.iterrows():
            data = {}

            if index == 0:
                continue

            if str(row[1]).isdigit():
                continue

            data['name'] = row[indices['name']]
            data['quantity'] = row[indices['quantity']]
            data['unit_name'] = row[indices['unit_name']]
            data['unit_price'] = row[indices['unit_price']]
            data['total_price'] = row[indices['total_price']]

            if data['quantity'] == None or data['unit_price'] == None or data['unit_name'] == '':
                break

            items.append(data)
    return items

def validate_name(name, max_elements = 2):
    items = name.split(",")

    if len(items) > max_elements:
        return False

    return True

def get_contract_info(contract_id):
    contract = get_contract(contract_id)
    print(contract)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found!")

    if 'items' in contract:
        items = []
        for item in contract['items']:
            name = item.get('description', ' ')
            quantity = item.get('quantity', ' ')
            unit_name = item.get('unit', {}).get('name', 'од.')
            unit_price = item.get('unit', {}).get('value', {}).get('amount', ' ')
            data = {'name': name, 'quantity': quantity, 'unit_name': unit_name, 'unit_price': unit_price}

            # if the last one price for unit is not defined, then it tries to calculate it automatically, if there is only one item,
            # otherwise it will parse the documents to find all information there
            if unit_price == ' ':
                # here i am validating name in response for better filtration, because if there are a lot of commas this name is incorrect, it might have a lot of element names in it,
                # for example without this filter response can be: [{'name': 'Господарські товари( грунт,стрічка малярна,пінопласт,ніж канцелярський, клей Перфлікс)',
                # 'quantity': 15.0, 'unit_name': 'штука', 'unit_price': 63.733333333333334, 'total_price': 956.0}], its bad response for selenium price parsing,
                # because it has not clear name
                if len(contract['items']) == 1 and validate_name(name):
                    total_price = contract.get("value", {}).get("amount", " ")
                    if not total_price == " ":
                        data['total_price'] = total_price
                        data["unit_price"] = float(total_price) / float(quantity)
                    items.append(data)
                    return items
                else:
                    break


    # if price is not placed for the first element or if it cannot be calculated then program will parse the pdf to search the needed infomation
    documents = contract.get('documents', None)
    if documents:
        url = get_pdf_url(documents)
        items = parse_pdf(url)
        if len(items) == 0:
            raise HTTPException(status_code=404, detail="Could not find items in specification!")
    else:
        raise HTTPException(status_code=404, detail="Information about tender could not be found!")

    return items

#print(get_contract_info("33f405c1a83b4e3b9835e546cb8db51f"))