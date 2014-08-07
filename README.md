About
======

A Lightweight Blog System. Powered by Tornado Web Framework. Easy to read and write.

Installation
======

Requirements:

    1.Tornado
    2.Mistune
    3.pygments

How to Build:

* `git clone https://github.com/JmPotato/Pomash.git`
* `cd Pomash`
* `pip install -r requirements.txt`
* Edit the `settings.py`
* `python init_db.py` to creat database.
* `python run.py` to run your blog.
* Your blog is ready for you!

Note: The default admin username is `admin` and the password is 'admin', too. You can change them with `settings.py` and admin panel.

Usgae
=====

Support Markdown

    #Hello World

    ```python
    print('Hello, World!')
    ```

    Hello, World!

    * Hello
    * World

Theme
=====

Pomash's theme named Potheme. Here is a Potheme list:

* [Potheme-Clean](https://github.com/JmPotato/Potheme-Clean)

License
=====

Please read the MIT-LICENSE
