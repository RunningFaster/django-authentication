from django.test import TestCase

# Create your tests here.

a = "INSERT INTO `DjangoAuthAdmin`.`users_menu_api`(`id`, `menu_id`, `api_id`) VALUES (1, 1, 1);"

for i in range(1, 28):
    b = a.replace("(1, 1, 1)", "({0}, 1, {0})".format(i))
    print(b)