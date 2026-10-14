# Work_time
Предоставляет инструменты извлечения данных о времени работы из фото или консольно, 
вычисление итоговой оплаты.  

## Точки входа:  
`read_images_and_check_result()` - автоматическая обработка папки с изображениями.  
`cli()`- ручной ввод данных через консольный интерфейс (default).

Для `read_images_and_check_result`  
&nbsp;&nbsp;&nbsp;&nbsp;Создать папку img в корне проекта, все изображения туда.  
&nbsp;&nbsp;&nbsp;&nbsp;Особенности изображения:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user: name  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;labor date: dd/mm/yyyy  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clock in dd/mm/yyyy hh:mm  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clock out dd/mm/yyyy hh:mm  
&nbsp;&nbsp;&nbsp;&nbsp;При изменении формата полей необходимо редактировать `text_analysis`, заменить `build_pattern` на свой.  


## Главный файл:
- time_tmp.py

## Обновлено:
- добавлен build_pattern ( легче управлять шаблоном )
- проверка операционной системы ( На Linux не тестирован )  
&nbsp;&nbsp;&nbsp;&nbsp;Обработчик на 158 строке

## Требования к фото  
- Желательно перпендикулярно экрану
- Чистый экран ( Грязь на экране создаёт помехи на фото это создаёт ошибки распознавания ) 
- Особенности изображения:  
    user: name  
    labor date: dd/mm/yyyy  
    clock in dd/mm/yyyy hh:mm  
    clock out dd/mm/yyyy hh:mm  

Лучшим вариантом будет скриншот

## 
__!!! Ветка main закрыта__