from sentiment import SentimentDetection
import pandas as pd

text1 = """
rt @mohamad_pazouki: از شما انقلابی‌ها که یک روز از زاکانی بت میسازید و روز دیگر بخاطر یک تصمیم اشتباه ان را از دایره انقلاب خارج میکنید می‌…
"""
text2 = """
 کلیپ مهم و ترسناکی که محسن رضایی منتشر کرد رضایی : بعثی‌ها رفتند ؛ اما امروز ، تفکر بعثی می‌خواهد معیشت مردم را محاصره کند .
"""
text3 = """
جالبه سوالای فسادی به رییسی میوفته سوالای برنامه دار به جلیلی
"""
data = pd.DataFrame({'id': [1, 2, 3], 'text': [text1, text2, text3]})

# Set this true for using gpu in process
GPU = False

def test_infer():
    sentiment = SentimentDetection(GPU)

    result = sentiment.infer(data)
    assert list(result['label']) == ['منفی', 'مثبت', 'منفی']
