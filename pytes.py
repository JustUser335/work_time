# from PIL import Image
# import pytesseract

# # Укажите путь к tesseract.exe (актуально для Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Откройте изображение
# image = Image.open('./img/photo_2026-09-14_23-29-14.jpg')

# # Распознайте текст (укажите нужный язык, например, 'rus' или 'eng')
# text = pytesseract.image_to_string(image, lang='rus+eng')

# print('Распознанный текст:')
# print(text)

#########################################
# # Тест 2 с обработкой фото
#########################################
# import cv2
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # 1. Загружаем изображение
# image_path = './img/photo_2026-09-18_23-19-52.jpg'
# image = cv2.imread(image_path)

# # 2. Переводим в оттенки серого (убираем лишний цвет)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # --- СОХРАНЯЕМ СЕРОЕ ИЗОБРАЖЕНИЕ ---
# # Файл появится в той же папке, где запускается скрипт
# cv2.imwrite('step1_gray.png', gray) 

# # 3. Повышаем контрастность (бинаризация / адаптивный порог)
# # Этот метод делает текст четко черным, а фон — белым
# processed_img = cv2.adaptiveThreshold(
#     gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
# )

# # --- СОХРАНЯЕМ КОНТРАСТНОЕ ИЗОБРАЖЕНИЕ ---
# cv2.imwrite('step2_contrast.png', processed_img)

# # 4. (Опционально) Убираем мелкие шумы/размытие, если текст смазан
# processed_img = cv2.medianBlur(processed_img, 5)

# # Сохраняем результат для проверки (можно открыть и посмотреть)
# cv2.imwrite('processed_preview.png', processed_img)

# # 5. Передаем обработанное изображение в Tesseract
# custom_config = r'--oem 3 --psm 6' # настройки движка для улучшения точности
# text = pytesseract.image_to_string(processed_img, lang='rus+eng', config=custom_config)

# print("Распознанный текст:")
# print(text)
