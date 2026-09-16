from PIL import Image
import pytesseract

# Укажите путь к tesseract.exe (актуально для Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Откройте изображение
image = Image.open('./img/photo_2026-09-14_23-29-14.jpg')

# Распознайте текст (укажите нужный язык, например, 'rus' или 'eng')
text = pytesseract.image_to_string(image, lang='rus+eng')

print('Распознанный текст:')
print(text)