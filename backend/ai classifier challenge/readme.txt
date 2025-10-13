local testing on windows

-use powershell
-navigate to /ai classifier challenge

docker build -t ai-challenge .
docker run -p 8000:8000 ai-challenge

test with browser:
http://127.0.0.1:8000/docs


To Add New fields/questions:
-add relevant columns/entries to animal_details_top_animals.csv
-add append field and question to be asked to dictionary_questions_bool.csv

side_note - 'ibra_xxxx' field related questions are disabled as of 18th September 2025