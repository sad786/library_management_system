""""
Here is the details about this Library Mangement System App

Authentication Feature and other flask feature, I have taken help from internet as I was less aware I have learned about them 
All the code I have written by myself 

1. All the database creation functionality is in models.py
    1. Database name is library 
    2. There are 4 Tables in library database
    3. a. Users table include columns id which autoincrement means it will be set up by database itself when user
            entry is created 
        email of the user, password and role mean either he is user or admin

    4. Second table is books having coulumns id which is autoincrement in nature
        title, isbn which is unique id of the book, authro of the book and available status 
    
    5. Third table is borrow_reqest which having the details about who borrwed the book and their start date and end date
    6. Fourth table is borrow_history which will have details of the book taken by each user


1. a There are two html file named index.html and user.html for homepage and user page

2. Main File is app.py 
    from this file app will start and user will have an option to enter their login details
    then detabase will check if the user is admin or simple user with details must be correct
    then corresponding feature will appear for admin or user

3. Admin will have the functionality to 
    1. Add a book into the library
    2. approve or deny request
    3. View User borrow history
    4. Adding New User to the library

4. User file users.py have the following functinality
    1. View Available Books
    2. Request a book
    3. view borrow history

5. Authorization related funcationlity is in the file auth.py
6. All the configuration related statments are written in config.py
7. Admin.py file is responsible to generate Admin related funcationlity and it routes admin_routes.py for other queries
8. User.py file is responsible to generate User related funcationality and it routes user_routes.py for user quieries
9. All the python framework requirement is written in requirement.txt file

"""
