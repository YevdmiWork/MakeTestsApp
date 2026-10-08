class TestMessages:
    NOT_FOUND = 'Тест не найден'
    ACCESS_DENIED = 'Доступ отклонен'
    NOT_AUTHOR = 'Вы не являетесь владельцем теста'
    ALREADY_PUBLISHED = 'Тест уже опубликован'
    TEST_LIMIT = 'Лимит тестов'
    REQUIRED_TAG = 'Для публикации необходимо добавить хотя бы один тег'


class QuestionMessages:
    EMPTY_TEXT = 'Текст не может быть пустым'
    TYPE_NOT_FOUND = 'Тип вопроса не найден'
    WRONG_TYPE = 'Некорректный тип вопроса'
    QUESTION_LIMIT = 'Лимит вопросов'
    WRONG_IMAGE_FORMAT = 'Некорректный формат изображения'
    IMAGE_TOO_LARGE = 'Изображение имеет слишком большой размер'


class TagMessages:
    TAG_LIMIT = 'Лимит тегов'
    ALREADY_ADDED = 'Тег уже добавлен'
    NOT_FOUND = 'Тег не найден'


class AnswerMessages:
    ALREADY_EXISTS = 'Новый ответ дублируется'
    ANSWER_LIMIT = 'Лимит ответов'
    EMPTY_TEXT = 'Пустой ответ'


class UserMessages:
    NOT_AUTH = 'Ошибка авторизации'
