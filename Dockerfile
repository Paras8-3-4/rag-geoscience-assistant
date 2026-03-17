FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/.streamlit

RUN echo '[server]\n\
headless = true\n\
port = 7860\n\
address = "0.0.0.0"\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
maxUploadSize = 200\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "0.0.0.0"\n\
serverPort = 7860\n\
' > /app/.streamlit/config.toml

EXPOSE 7860

ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

CMD ["streamlit", "run", "app.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]