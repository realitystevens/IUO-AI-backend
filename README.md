## IUO AI Backend

Backend application (built as an API) for IUO AI project. Built using `FastAPI` Python Framework

### Instructions

- Install python packages for the application recursively using the command
```sh
pip install -r requirements.txt
```

- Add `GOOGLE_API_KEY` to the `.env` file. Access `GOOGLE_API_KEY` [here](https://aistudio.google.com/app/apikey)


- Summarize document `IUO_prospectus_2016-202.pdf` (from which AI get answer) by running the command
```sh
python prototype/summarizePDF.py
```

- Start application by using the command
```sh
uvicorn app:app --reload
```

Project built by [Google Developer Student Club, Igbinedion University Okada](https://linktr.ee/gdsciuo)
