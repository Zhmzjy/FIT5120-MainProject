local testing on windows

-use powershell
-navigate to /australian wildle

docker build -t wildle .
docker run -p 8000:8000 wildle

test with browser:
http://127.0.0.1:8000/docs

