FROM freqtradeorg/freqtrade:stable

# Install dependencies
COPY requirements.txt /freqtrade/

RUN pip install -r requirements.txt --user --no-cache-dir
