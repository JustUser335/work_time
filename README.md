# work_time
Предоставляет инструменты извлечения данных о времени работы из фото или консольно, 
вычисление итоговой оплаты.

## Точки входа:  
`read_images_and_check_result()` - автоматическая обработка папки с изображениями.  
`cli()`- ручной ввод данных через консольный интерфейс (default).

Для `read_images_and_check_result`  
&nbsp;&nbsp;&nbsp;&nbsp;Особенности изображения:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user: name  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;labor date: dd/mm/yyyy  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clock in dd/mm/yyyy hh:mm  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clock out dd/mm/yyyy hh:mm  
&nbsp;&nbsp;&nbsp;&nbsp;При изменении формата полей необходимо редактировать `text_analysis`.

## Главный файл:
- time_tmp.py

## Обновлено:
- Добавлено док, annotations для payment_calc
- payment_calc улучшен расчет монетки one_hp_in_minutes 
- изменено описание валюты, более нейтрально
- добавлен фасад входа для изображений
- описание модуля
- удалены все комменты
- общие улучшения структуры

## Требования к фото  
- Желательно перпендикулярно экрану
- Чистый экран ( мешает распознованию )
- Особенности изображения:  
    user: name  
    labor date: dd/mm/yyyy  
    clock in dd/mm/yyyy hh:mm  
    clock out dd/mm/yyyy hh:mm  

## 
__!!! Ветка main закрыта__