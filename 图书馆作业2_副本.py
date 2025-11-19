# --------------------------------------------

# Программа моделирования работы библиотеки

# 使用继承、封装、对象关系的图书馆系统

# Лабораторная работа: библиотека (Python)

# --------------------------------------------

# ====== Класс Book (Базовый класс) / 图书基类 ======

class Book:
def **init**(self, title, author, year):
# Инкапсулированные поля / 封装属性
self.__title = title
self.__author = author
self.__year = year
self.__available = True  # доступна ли книга / 是否可借

```
# --- Геттеры / 获取方法 ---
def get_title(self):
    return self.__title

def get_author(self):
    return self.__author

def get_year(self):
    return self.__year

# --- Проверка доступности / 检查可借状态 ---
def is_available(self):
    return self.__available

# --- Отметить как взятую / 标记为已借出 ---
def mark_as_taken(self):
    self.__available = False

# --- Отметить как возвращённую / 标记为已归还 ---
def mark_as_returned(self):
    self.__available = True

# --- Строковое представление / 打印输出 ---
def __str__(self):
    status = "доступна" if self.__available else "недоступна"
    return f"《{self.__title}》 — {self.__author}, {self.__year} год ({status})"
```

# ====== Подкласс PrintedBook / 纸质书类 ======

class PrintedBook(Book):
def **init**(self, title, author, year, pages, condition):
super().**init**(title, author, year)
self.pages = pages
self.condition = condition  # состояние: новая / хорошая / плохая

```
# Метод ремонта / 修复书籍
def repair(self):
    if self.condition == "плохая":
        self.condition = "хорошая"
        print(f"Книга 《{self.get_title()}》 отремонтирована до состояния 'хорошая'. / 修复完成，状态为“好”。")
    elif self.condition == "хорошая":
        self.condition = "новая"
        print(f"Книга 《{self.get_title()}》 улучшена до состояния 'новая'. / 状态提升为“新”。")
    else:
        print(f"Книга 《{self.get_title()}》 уже новая. / 书籍已是“新”的。")

def __str__(self):
    base = super().__str__()
    return f"{base}, {self.pages} стр., состояние: {self.condition}"
```

# ====== Подкласс EBook / 电子书类 ======

class EBook(Book):
def **init**(self, title, author, year, file_size, format_):
super().**init**(title, author, year)
self.file_size = file_size
self.format = format_

```
# Метод загрузки / 下载方法
def download(self):
    print(f"Книга 《{self.get_title()}》 загружается... / 正在下载《{self.get_title()}》...")

def __str__(self):
    base = super().__str__()
    return f"{base}, {self.file_size} МБ, формат: {self.format}"
```

# ====== Класс User / 用户类 ======

class User:
def **init**(self, name):
self.name = name
self.__borrowed_books = []  # инкапсулированный список / 封装借阅列表

```
# Взять книгу / 借书
def borrow(self, book):
    if book.is_available():
        book.mark_as_taken()
        self.__borrowed_books.append(book)
        print(f"{self.name} взял(а) 《{book.get_title()}》 / {self.name} 借了《{book.get_title()}》")
    else:
        print(f"Книга 《{book.get_title()}》 недоступна. / 《{book.get_title()}》不可借。")

# Вернуть книгу / 还书
def return_book(self, book):
    if book in self.__borrowed_books:
        book.mark_as_returned()
        self.__borrowed_books.remove(book)
        print(f"{self.name} вернул(а) 《{book.get_title()}》 / {self.name} 已归还《{book.get_title()}》")
    else:
        print(f"{self.name} не имеет этой книги. / {self.name} 没有这本书。")

# Показать список своих книг / 显示借书清单
def show_books(self):
    if self.__borrowed_books:
        print(f"Книги у {self.name}: / {self.name} 借阅的书籍：")
        for b in self.__borrowed_books:
            print(" -", b.get_title())
    else:
        print(f"{self.name} не имеет книг. / {self.name} 当前没有借书。")

# Получить копию списка / 获取只读列表
def get_borrowed_books(self):
    return tuple(self.__borrowed_books)
```

# ====== Класс Librarian (наследник User) / 图书管理员类 ======

class Librarian(User):
def **init**(self, name):
super().**init**(name)  # 调用父类构造函数初始化 name

```
# Добавить книгу / 添加书籍
def add_book(self, library, book):
    library.add_book(book)
    print(f"Библиотекарь {self.name} добавил(а) 《{book.get_title()}》 / 管理员 {self.name} 已添加《{book.get_title()}》")

# Удалить книгу / 删除书籍
def remove_book(self, library, title):
    library.remove_book(title)
    print(f"Библиотекарь {self.name} удалил(а) 《{title}》 / 管理员 {self.name} 已删除《{title}》")

# Зарегистрировать пользователя / 注册用户
def register_user(self, library, user):
    library.add_user(user)
    print(f"Пользователь {user.name} зарегистрирован / 用户 {user.name} 已注册")
```

# ====== Класс Library / 图书馆类 ======

class Library:
def **init**(self):
self.__books = []
self.__users = []

```
# Добавить книгу / 添加书籍
def add_book(self, book):
    self.__books.append(book)

# Удалить книгу по названию / 按标题删除书籍
def remove_book(self, title):
    for b in self.__books:
        if b.get_title() == title:
            self.__books.remove(b)
            return
    print(f"Книга 《{title}》 не найдена / 未找到《{title}》")

# Добавить пользователя / 添加用户
def add_user(self, user):
    self.__users.append(user)

# Найти книгу / 查找书籍
def find_book(self, title):
    for b in self.__books:
        if b.get_title() == title:
            return b
    return None

# Показать все книги / 显示所有书籍
def show_all_books(self):
    print("Все книги в библиотеке / 图书馆所有书籍：")
    for b in self.__books:
        print("-", b)

# Показать доступные книги / 显示可借书籍
def show_available_books(self):
    print("Доступные книги / 可借书籍：")
    for b in self.__books:
        if b.is_available():
            print("-", b)

# Выдать книгу пользователю / 借出书籍
def lend_book(self, title, user_name):
    book = self.find_book(title)
    user = next((u for u in self.__users if u.name == user_name), None)
    if book and user:
        user.borrow(book)
    else:
        print("Ошибка: книга или пользователь не найдены / 错误：未找到书籍或用户。")

# Принять возврат / 接收归还
def return_book(self, title, user_name):
    book = self.find_book(title)
    user = next((u for u in self.__users if u.name == user_name), None)
    if book and user:
        user.return_book(book)
    else:
        print("Ошибка возврата / 归还出错。")
```

# ====== Пример использования / 示例运行 ======

if **name** == "**main**":
lib = Library()

```
# Создание книг / 创建书籍
b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

# Создание пользователей / 创建用户
user1 = User("Анна")
librarian = Librarian("Мария")

# Добавление книг / 管理员添加书籍
librarian.add_book(lib, b1)
librarian.add_book(lib, b2)
librarian.add_book(lib, b3)

# Регистрация пользователя / 注册用户
librarian.register_user(lib, user1)

# Пользователь берёт книгу / 借书
lib.lend_book("Война и мир", "Анна")

# Просмотр книг / 查看借书列表
user1.show_books()

# Возврат книги / 还书
lib.return_book("Война и мир", "Анна")

# Электронная книга / 下载电子书
b2.download()

# Ремонт книги / 修复纸质书
b3.repair()
print(b3)

