# Electronic Invoicing using Image Processing 

This solution tackles the cumbersome process of manual electronic invoicing by introducing Image Processing. 

## **OCR**

Given the unique nature of the documents under consideration for electronic invoicing, the use of a regular OCR for image to text translation became restrictive and inaccurate. Electronic invoices have a combination of text, form-like data as well as tabulated information. Traditional OCRs provided by libraries and free services have a one dimensional technique of translating characters along the same line.
This is not serviceable for the type of information we need to extract. Along with character recognition, it is also important to understand the structure of the document provided (recognizing tables, forms, etc). Building a model that needs to be trained to identify such manually created information storage structures is extremely cumbersome and requires a large dataset and very high processing power. Even with these requirements, the accuracy of a model so built can be compromised by the quality of the document or differently structured documents with multiple pages. To devise the most optimum solution that considers processing without compromising on accuracy, the tool we used for OCR and data extraction was Amazon textract.

The Amazon Textract Text Detection API can detect text in a variety of documents including financial reports, medical records, and tax forms. For documents with structured data, the Amazon Textract Document Analysis API can be easily used to extract text, forms and tables. The only prerequisite for utilizing their API is the requirement of an AWS account. However, this seemed a minor requirement considering their unparalleled accuracy and speed with other open source solutions. 

**To use the AWS API, the user must:-**
Create an AWS account
Create an IAM User
Set up AWS CLI and SDK

Amazon Textract can detect and analyze text in single-page documents that are provided as images in JPEG, PNG or PDF format. The operations are synchronous and return results in near real time. 
Calling Amazon textract operations [Refer load.txt]

Amazon Textract operations process document images that are stored on a local file system, or document images stored in an Amazon S3 bucket. The file location is specified by using the Document input parameter. 

## **The Amazon S3 bucket**

Has the code to call an Amazon Textract operation using an image/file stored in an Amazon S3 bucket. A JSON response is now obtained from the API. 

## **Detecting Text: [Refer detect.py]**

To detect text in a document, the DetectDocumentText operation is used. This returns a JSON structure that contains lines and words of detected text, the location of the text in the document, and the relationships between detected text. In this procedure, the file is  uploaded to the S3 bucket.

## **Analyzing Text: [Refer Analyze.py]**

To analyze text in a document, the AnalyzeDocument operation is used. It returns a JSON structure that contains the analyzed text. This will display the document and boxes around detected items.

This is further classified into Raw text, tables and forms.

## **Information Extraction: [Refer extract.py]**
Invoices from different suppliers are never identical in format. They are always formatted to cater to the needs of the company. Therefore, invoices may have different keywords, forms, tables and structure. Training image classifiers using bounding boxes to detect specific fields over a number of invoices may seem like an option, but given the variety and lack of uniformity, the results of this technique are largely underwhelming.
The need arose to build a more flexible solution without exhausting too many resources. The key observation we decided to use to our advantage was the nature of the fields. Each field to be extracted had a specific type of data it required. 
For example :- PO Number is always a single string with a combination of letters and numbers, the discount rates are always expressed in percentages and dates always have a Date format. Using this information, we were able to devise a systematic scheme to extract the necessary information:-
**Key-Value pairings**: Search for fields within key-value pairs: (many fields can be found conveniently annotated as key-value pairings as extracted by AWS Textract. (Example:- Invoice number, PO Number)
**Data-Type Check**: If fields are not available as key-value pairs, short list candidates by matching the type of data that is expected for the field (Example:- the date format or Address)
**Distance calculation**: Using the candidates shortlisted from step 2, scan the text for the name of the identifier (Example: -The invoice GST is often referred to in invoices using abbreviations like GSTIN, GST No. etc) and find the candidate which bears the least distance with this identifier. This technique is certain to narrow down on the correct field.
**Table scanning**: For some tabulated data, the same technique as above may work, but the more reliable method is to scan the column names for the appropriate identifier, and to reinforce the same by validating that the data-type of the column matches the type of the field we wish to extract. 
**Special constraints**: May depend on certain types of data that display some anomalies that leads to ambiguity. (Example: There are two separate fields called “Invoice Date” and “Due date” that are often mentioned together. Making a data-type check alone does not solve the problem. Special care has to be taken not to pick up the wrong date and so must be given additional constraint to make sure that the date more closely associated with the word “due” is not the “invoice date” and vice versa. )
**Calculated fields**: Some fields are not obviously presented as information in the invoice and need to be computed. For example, the round off charges, which is the decimal amount entered by the WH operator. This charge is rounded off to the nearest rupee and then displayed as the total invoice. This information isn’t provided as a separate field on any of the invoice and must be computed separately. 

## **The output:**

Following the information extraction process, all the fields are extracted and documented. This file (.csv) is readily made available for download to the user, with each field and its values mapped out to present the information uniformly.

## **The application:**

The application was built using Django and includes functionalities to support file uploads, end-to-end processing from API calls and information extraction to finally giving the condensed information of extracted fields as the key deliverable, available for download. 

The application is easily integratable with any supporting software using Django REST framework. It can be hosted onto a software service or an internal dashboard belonging to the service. The intermediary service layer for the product is a defined API layer. Using the API, documents of invoices may be sent as requests to the tool, evaluated, and duly received as JSON/xlsx files of the appropriate format. Previously processed invoices that are stored in the application database can also be accessed through the service layer.

## **Advantages and Limitations:**

Another important inclusion we made was the spelling check. While AWS Textract is very robust and precise in its detection, the quality of its predictions is also dependent on the quality of the invoice and could be marred in performance by pixelated and blurry images. To ensure that the extraction process is as accurate as possible, we reinforce the extraction system by performing basic spell checks as often as possible using the python library symspell. Besides this, our product also displays commendable accuracy for handwritten drafts too. 
Integration with Textract is the most challenging part of the application. Given that AWS is constantly developing and rebuilding, Textract and its features are being continually updated and serviced. To be able to utilize the API, valid credentials are necessary.

## **Installation Guide:**

For UBUNTU:

1. Check if Python 3 is installed by executing the following command on the command line.
a. python3 --version
b. If not install using the following command
i. sudo apt-get install python3.6


2. Test if pip is installed by executing
a. pip list
b. If not install using the following command
i. sudo apt-get install python3-pip

3. Create a new directory using the following command
a. mkdir flipkart

4. Create a virtual environment using the following command
a. python3 -m venv myvenv
b. If the above statement fails, then install virtual environment using the following command:
i. sudo apt-get install python3-venv

5. Navigate to your newly created virtual environment folder using the following command
a. cd myvenv

6. Navigate to the bin folder in your myenv folder and execute the following command 
a. source activate

7. Make sure that you get a prefix of (myvenv) in your command line prompt, after step 6.

8. Navigate to the parent folder (myvenv) using the command cd..

9. Install few libraries/dependencies by using the following commands:
a. pip3 install os
b. pip3 install csv
c. pip3 install pandas
d. pip3 install regex
e. pip3 install requests
f. pip3 install Django
g. pip3 install djangorestframework django-cors-headers
h. pip3 install boto3
i. pip3 install psutil
j. Pip3 install pillow

10. Create a new project called ‘backend’
a. django-admin startproject backend

11. Navigate to your project folder
a. cd backend

12. Create a new django app using the following command
a. python3 manage.py startapp eInvoice

13. Now replace the content/copy the following files from the provided code to their respective locations
a. settings.py (path - flipkart/myvenv/backend/backend/)
b. admin.py, analyze.py, app.py, detect.py, extract.py, load.txt, models.py, texts.py, urls.py, views.py (path -  flipkart/myvenv/backend/eInvoice/)
c. Copy the folders static, templates to flipkart/myvenv/backend/eInvoice/)

14. Now execute the following commands, before running the browser
a. python3 manage.py makemigrations eInvoice
b. python3 manage.py migrate

15. Run server using the following command
a. python3 manage.py runserver
b. Now, go to your browser and type http://localhost:8000/ to use the app.
