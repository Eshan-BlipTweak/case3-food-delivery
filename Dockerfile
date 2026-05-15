FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "numpy>=1.24,<2.0"
RUN pip install --no-cache-dir streamlit==1.36.0 pandas==2.2.2 plotly==5.22.0 prophet==1.1.5 scikit-learn==1.5.0

COPY . .

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]