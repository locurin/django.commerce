# Django.Commerce - a simple auctions web app project

Django.Commerce's execution example available at http://djangocommerce.pythonanywhere.com/ 

## Table of contents

*[General info](#general-info)

*[implementation](#implementation)

*[Technologies](#technologies)

*[functionalities](#functionalities)

*[version](#version)

*[credits](#credits)


## General info

It's a basic web app for creating auctions and bid on them. Users are able to simulate those transactions using fake currency that is given at the moment of create an account. Its data is stored in a database, so new users created will be saved in the database so they can log in whenever they wish. It was created as a personal project to learn to manage Django Framework's features regarding databases, models and migrations.

This version presents a basic and simple user interface and currently is not responsive not support phonescreen view. Being a personal not proffesional project, these features probably won't never be added. For an optimal view of the site, plese use a computer or tablet.



## Implementation 
Django.Commerce is an open source project, so everyone interesed can download all its features from Github [here](https://github.com/locurin/django.commerce). The same way, users are invited to improve its features or fully customize its look with HTML/CSS to fit their needs for implementation. 

*To learn how to deploy your costume version of the app into the web visit [Django Docs regarding the issue](https://docs.djangoproject.com/en/3.1/howto/deployment/).


## Technologies

*[Bootstrap](https://getbootstrap.com/) v.5-0.0-beta2

*[Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) 

*[Django](https://www.djangoproject.com/) v.3.1.7

*[Python](https://www.python.org/) v.3.8.5

*[SQLite3](https://www.sqlite.org/) v.3.35.2

## Scope of Functionalities

* Django.Commerce allows users to create a new user with an username, a password and a (can be fake) email. Once signed up, users can access as many time as they wish. Every new user starts with an amount of $4000 on his fake currency account.
* Users can create new auctions and bid on those already open if possible. If user is the highest bidder at the moment of the listing being close by its author, he/she will be considered winner. 
* Users can also comment on the auctions, and reply those comments if he/she is the author of said article. There is also a watchlist, where listings can be added/removed at will as many time as user please.
* There is a category submenu, where users can search available auctions of the requested category.
* User profile can be visited, and same aspects of it (password and username) can be updated in the same profile view. 

##  Version

This is version 1 of Django.Commerce, uploaded to Github in march 2021. Future versions should focus on improve UI and front-end aspects of the site. If ever intended to transit into a proffesional project, measures about data security are the main back-end issues to take care.

## Credits

This project was built by [locurin](https://github.com/locurin) for Github as a personal project. You can also contact me at **matiasfefernandez95@gmail.com**. 


