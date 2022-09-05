from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    # Модель, содержащая объекты всех авторов.
    # Имеет следующие поля:
    # cвязь «один к одному» с встроенной моделью пользователей User;

    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    def update_rating(self):
        # обновляет рейтинг пользователя, переданный в аргумент этого метода.
        # Он состоит из следующего:
        # суммарный рейтинг каждой статьи автора умножается на 3;
        # суммарный рейтинг всех комментариев автора;
        # суммарный рейтинг всех комментариев к статьям автора.

        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    # Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    # Имеет единственное поле: название категории.
    # Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    # Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    # Каждый объект может иметь одну или несколько категорий.
    # Соответственно, модель должна включать следующие поля:
    # связь «один ко многим» с моделью Author;
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # поле с выбором — «статья» или «новость»;
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)

    # автоматически добавляемая дата и время создания;
    dateCreation = models.DateTimeField(auto_now_add=True)

    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    postCategory = models.ManyToManyField(Category, through='postCategory')

    # заголовок статьи/новости;
    title = models.CharField(max_length=128)

    # текст статьи/новости;
    text = models.TextField()

    # рейтинг статьи/новости.
    rating = models.SmallIntegerField(default=0)

    def preview(self):
        # возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
        return f'{self.text[0:124]} ...'

    def like(self):
        # увеличивают/уменьшают рейтинг на единицу
        self.rating += 1
        self.save()

    def dislike(self):
        # увеличивают/уменьшают рейтинг на единицу
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    #     Промежуточная модель для связи «многие ко многим»:
    # связь «один ко многим» с моделью Post;
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)

    # связь «один ко многим» с моделью Category.
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    # Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    # Модель будет иметь следующие поля:
    # связь «один ко многим» с моделью Post;
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)

    # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    # текст комментария;
    text = models.TextField()

    # дата и время создания комментария;
    dateCreation = models.DateTimeField(auto_now_add=True)

    # рейтинг комментария.
    rating = models.SmallIntegerField(default=0)

    def like(self):
        # увеличивают/уменьшают рейтинг на единицу
        self.rating += 1
        self.save()

    def dislike(self):
        # увеличивают/уменьшают рейтинг на единицу
        self.rating -= 1
        self.save()