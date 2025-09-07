local testing on windows

-use powershell
-navigate to /ai classifier challenge

docker build -t ai-challenge .
docker run -p 8000:8000 ai challenge