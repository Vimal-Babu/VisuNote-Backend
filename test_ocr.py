
from paddleocr import PaddleOCR

image_path = r"C:\Users\acer\Desktop\test.jpeg"  # Change this to your image path

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

result = ocr.predict(image_path)

for page in result:
    print(page["rec_texts"])