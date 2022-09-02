# Install

`PROJECT_DIR` is project root

```bash
mkdir ${PROJECT_DIR}
cd ${PROJECT_DIR}

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update -y
sudo apt install -y python3.6 python3.6-venv git

git clone http://185.208.77.246/inference/sentiment.git .
# git checkout develop

python3 -m venv venv
source venv/bin/activate
pip install -U pip wheel setuptools pytest
pip install -r requirements.txt
```

# Test

```bash
bin/test.sh

# or

source venv/bin/activate
pytest
```

# Install package in other projects

```bash
pip install git+http://185.208.77.246/inference/sentiment.git
```

# User manual

```python
from sentiment import SentimentDetection
import pandas as pd

text = "آقای حسن روحانی به دیدار رییس جمهور روسیه در تهران رفت"

data = pd.DataFrame({'id': [1], 'text': [text]})

gpu = False #if you want to use gpu, set this true

sentiment_detection = SentimentDetection(gpu)
result = sentiment_detection.infer(data) #return result as Pandas DataFrame
print(result)
```
