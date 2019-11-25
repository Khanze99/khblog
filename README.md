[Computer Science Blog](http://www.khanze.com)
=====================

About project
=====================
A project has been implemented so that people share knowledge and learn something new. The user can create a post that can be commented on and rated.

The project has an:
+ authentication and authorization system
+ post model
+ comment model
+ likes
+ dislikes
+ profile model
+ search
+ reply comment
+ reset password

Add new function:
+ When post to a blog, the data is transferred to VK api and post to the group [CSB | Computer Science Blog](https://vk.com/computerscienceblog)

Celery + redis tasks:
+ send_mail registration
+ reset_password
+ change_password
+ Post to vk


Access to the API through the token generated in the application. When registering, a notification comes from the application to the mail that you wrote when filling in the data. Search for posts by title and context of the post has been implemented.