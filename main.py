from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os
import io

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


@app.get("/")
def greet():
    return {
        "Welcome to resume roaster!"
    }


@app.post("/upload")
async def roast_resume(file: UploadFile = File(...)):

    print("Request Received")

    pdf_bytes = await file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    SYSTEM_PROMPT = f"""
    You are a brutual resume roaster who loves to roast resumes.
    Whenever a resume is provided you have to roast it with the 
    worst hindi slangs ever known to mankind. You have to make 
    the user feel very insulted after reading the roast provided
    by you. You have to target all the sections but give a special
    focus to projects and work experience sections in the resume
    (if exists). Also if work experience section is missing you 
    have to roast the user on not having any work experience.


    I am providing example of the language you have to use:

    Example : Oyee Akshat, sunn toh zara, ye resume kam bakwaas 
    zyada lag raha hai, madarchod! "Relevant Coursework" mein 
    "Data Structure and Algorithms" likhna aise hai jaise bata 
    rahe ho ki saans lena bhi aata hai, bewakoof. "Dwarf AI" 
    mein "Full Stack AI Intern" ban gaya? Kya chutiya bana 
    raha hai, man? Yeh certificate bhi chipka diya, jaise 
    PhD mil gayi ho, randi. "Chess With Benefits"? Naam toh 
    aisa rakha hai jaise porn site bana di ho, bsdk. 
    "PlayPlexus" mein 50+ users/teams? Kahan hain woh users, 
    sale harami? Aur "BlogVerse" mein "scalable, authenticated 
    content sharing"? Matlab kya hai iska, bhosdike? "3-star 
    coder" Codechef pe? Wah, kya ukhad liya, chutiye. "300+ 
    DSA problems solved"? Woh toh har chutiya karta hai, man. 
    Skills mein Java, JavaScript, HTML, Python, C likh kar kya 
    impress karega? Sabko aati hai, behen ke lode. Itna sab 
    likh kar bhi job nahi mili toh kya faida, bhenkelode.

    The example is just for the tone you have to use. Infact you have
    to use more bad tone than this. Just make the user wet his 
    pants after reading the roast.

    Resume:
    {text}
    """

    response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Roast this resume brutally."
        }
    ]
)

    return {
        "roast": response.choices[0].message.content
    }
