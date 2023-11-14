from __future__ import annotations  # для аннотации собственным классом
from pprint import pprint  # для красивого вывода
import click  # для CLI
import random  # для генерации случайных значений


class Pizza:
    '''
    Базовый класс для всех видов пицц.

    Атрибуты класса
    =======
    l_size : int
        размер L
    xl_size : int
        размер XL

    Атрибуты экземпляра
    =======
    recipe : dict
        рецепт пиццы

    Методы класса
    =======
    avalible_size():
        Печатает доступные размеры пиццы для заказа.

    Методы экземпляра
    =======
    avalible_dict():
        Печатает рецепт пиццы.
    '''

    # Доступный размер ЛЮБОЙ пиццы в см
    # поэтому и вынес в атрибуты класса
    l_size = 30
    xl_size = 40

    def __init__(self):
        '''Конструктор'''
        self.recipe = {}

    def __eq__(self, other: Pizza) -> None:  # сравнение пицц
        '''Магический метод для сравнения пицц'''
        if not isinstance(other, Pizza):
            print('Вы пытайтесь сравнить пиццу не с пиццой!')
            return
        if self.__class__.__name__ == other.__class__.__name__:
            print('Это один и тот же вид пиццы :)')
            return

        my_len = len(self.recipe)  # длина рецепта левой пиццы
        other_len = len(other.recipe)  # длина рецепта правой пиццы
        if my_len > other_len:
            print('В левой пицце больше ингридиентов')
        elif my_len < other_len:
            print('В левой пицце меньше ингридиентов')
        else:
            print('В пиццах одинаковое кол-во ингридиентов')

    @classmethod
    def avalible_size(cls: Pizza | Margherita | Pepperoni | Hawaiian) -> None:
        '''Выводит доступные размеры для любой пиццы'''

        print('У Вас есть два варианта размера пиццы:')
        print(f'размер L -> {cls.l_size} см')
        print(f'размер XL -> {cls.l_size} см')

    def dict(self) -> None:
        '''Выводит рецепт конкретной пиццы'''

        print(f'Рецепт пиццы {self.__class__.__name__}:')
        # смотрим, что хранится в атрибуте-рецепте каждого класса пиццы
        pprint(self.__getattribute__('recipe'))


class Margherita(Pizza):
    '''
    Класс пиццы Маргариты.
    Содержит единственный атрибут -> рецепт.
    '''

    def __init__(self):
        # можно и без следующей строки, добавил, чтобы линтер не ругался ;)
        super().__init__()
        self.recipe = {'Пшеничная мука': '1.5 стол. ложки',
                       'Сухие дрожжи': '1 чай. ложка',
                       'Оливковое масло': '2 стак.',
                       'Томатная паста': '3 стол. ложки',
                       'Моцарелла': '200 гр.',
                       'Помидоры черри': '8 шт.',
                       'Чеснок': '1 зубч.'}


class Pepperoni(Pizza):
    '''
    Класс пиццы Пепперони.
    Содержит единственный атрибут -> рецепт.
    '''

    def __init__(self):
        super().__init__()
        self.recipe = {'Пшеничная мука': '1.5 стол. ложки',
                       'Сухие дрожжи': '1 чай. ложка',
                       'Оливковое масло': '3 стак.',
                       'Томатная паста': '5 стол. ложек',
                       'Смесь секретных трав': '100 гр.',
                       'Сырокопченая колбаса': '150 гр.',
                       'Паприка': '1 щепотка',
                       'Моцарелла': '200 гр.',
                       'Помидоры черри': '6 шт.'}


class Hawaiian(Pizza):
    '''
    Класс Гавайской пиццы.
    Содержит единственный атрибут -> рецепт.
    '''

    def __init__(self):
        super().__init__()  # рецепт с самого известного сайта о пиццах
        self.recipe = {'Мука пшеничная': '450 Грамм',
                       'Вода': '180 Грамм',
                       'Масло растительное': '1.5 Ст. ложки',
                       'Сахар': '0.5 Чайных ложки',
                       'Соль': '0.5 Чайных ложки',
                       'Дрожжи': '5 Грамм',
                       'Куриное филе': '180 Грамм',
                       'Сыр': '50 Грамм',
                       'Ананасы': '150 Грамм',
                       'Кетчуп': '2 Ст. ложки',
                       'Майонез': '1 Ст. ложка'}


def log(func):
    '''
    Декоратор, который выводит случайное время выполнения
    в дополнение к выводу функции
    '''

    def wrapper(pizza):
        original_result = func(pizza)  # результат ф-ции до декорирования
        return f'{original_result} - {random.randint(1, 10)}с!'
    return wrapper


@log
def bake(pizza):
    return 'bake'  # просто возвращает строку с названием


@click.group()  # для группировки всех декорируемых функций
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    '''Готовит и доставляет пиццу'''

    if pizza.strip().lower() not in ('pepperoni', 'hawaiian', 'margherita'):
        print('У нас нет такой пиццы, перезвоните позже.')
    else:
        print(f'👨‍🍳 Приготовили за {random.randint(1, 10)}с!')
        if delivery:
            print(f'🛵 Доставили за {random.randint(1, 10)}с!')


@cli.command()
def menu():
    '''Выводит меню'''

    for classs in (Margherita, Pepperoni, Hawaiian):
        emoji = random.choice(['🍕', '🧀'])  # пусть эможи генерится случайно ;)
        print(f'- {classs.__name__} {emoji}:')
        classs().dict()
        print('=' * 30)  # разделитель вывода


@cli.command()
def test():  # unit-тесты
    '''Выводит тесты'''

    # вывод результата декорируемой функции
    print(bake(Margherita()))

    # создаём экземпляры классов
    margo = Margherita()
    peperoni = Pepperoni()
    hawaii = Hawaiian()

    # выводит доступные размеры пиццы
    margo.avalible_size()
    print('=' * 30)

    # посмотрим рецепт каждого вида пиццы
    for instance in [margo, peperoni, hawaii]:
        instance.dict()
        print('=' * 30)

    # сравнение двух различных видов пицц
    margo == peperoni

    # сравнение двух одинаковых видов пицц
    margo == margo
    # сравнение пиццы с другим типом данных
    margo == 123


if __name__ == '__main__':
    cli()
