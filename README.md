Данный проект представляет из себя платформу для публикации контента.

Стуктура проекта:
<li>Пользователи не зарегистрированные в системе 
могут выкладывать посты, но только после того как они пройдут проверку
модератора или администратора платформы<br>
<li>Чтобы пользователь мог свободно выкладывать посты ему нужно 
зарегистрироваться в системе, пройти верификацию по почте и
преобрести подписку, вход в систему осуществляется 
по номеру телефона<br>
<li>В функционал подписки входит: свободная публикация контента,
возможность поставить лайк посту, оставить комментарий, 
отображать только свои посты и осуществлять 
над ними манипуляцию(изменение, удаление)
просмотреть статистику о колличестве постов, самым популярным 
постам по просмотрам и лайкам<br>
<li>Любой пользователь может зайти на платформу и посмотреть контент
от других пользователей или найти интересующий 
его пост в строке поиска<br>
<br>
Проверка покрытия тестами и просмот отчёта<br>

**coverage run --source='.' manage.py test**<br>
**coverage report**

<br>Сборка докера<br>

**docker-compose build**<br>
**docker-compose up -d**

