# main.py
from repository import DatabaseRepository
from gather import GatherAnimeInfo


def main():
    # Создаём объект работы с базой
    db_repo = DatabaseRepository("anime.db")
    db_repo.create_anime_table()  # создаём таблицу, если ещё нет

    # Создаём объект парсера
    gather_anime_info = GatherAnimeInfo()

    # -------------------------------
    # 1️⃣ Сбор базовых карточек
    print("Начало сбора карточек...")
    cards = gather_anime_info.get_all_cards()[:10]
    print(f"Собрано {len(cards)} карточек")

    # 2️⃣ Получение информации из карточек (title, link, image, episode, views)
    print("Сбор информации из карточек...")
    lst = gather_anime_info.get_info_from_all_cards(cards)
    print("Информация из карточек собрана")

    # 3️⃣ Вставка данных в базу (новые записи)
    print("Вставка базовых данных в базу...")
    db_repo.insert_data_to_anime_table(lst, batch_size=100)
    print("Базовые данные вставлены")

    # -------------------------------
    # 4️⃣ Получение ссылок без полной информации (year, genres, tags)
    print("Получение ссылок без дополнительной информации...")
    links_without_add_info = db_repo.get_all_links_without_additional_info()
    print(f"Найдено {len(links_without_add_info)} ссылок без доп. информации")

    # 5️⃣ Сбор информации с карточек аниме (year, genres, tags)
    print("Сбор дополнительной информации с карточек аниме...")
    lst_add_info = gather_anime_info.get_info_from_card_pages(links_without_add_info)
    print("Дополнительная информация собрана")

    # 6️⃣ Обновление базы данными (year, genres, tags)
    print("Обновление базы данных...")
    db_repo.insert_add_data_to_anime_table(lst_add_info, batch_size=100)
    print("База данных обновлена ✅")

if __name__ == '__main__':
    main()