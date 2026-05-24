# Medical-chatbot
For human like conversation regarding health. Like talking with a   Virtual doctor.

# ⚙️ How To Run

## STEP 01- Clone the repository

```bash
git clone https://github.com/monisharani1/Medical-chatbot
```

---

## STEP 02- Create Virtual Environment

```bash
python -m venv venv
```

---

## STEP 03- Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## STEP 04- Install Requirements

```bash
pip install -r requirements.txt
```

---

## STEP 05- Install Project

```bash
pip install -e .
```

---

## STEP 06- Create `.env` file

Add your API keys inside `.env`

```ini
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

---

## STEP 07- Run the Application

```bash
python app.py
```
## TEST UPDATE