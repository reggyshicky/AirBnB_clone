AirBnB_clone - The console

This respository contains the initial stage of a student project to build a clone of the Airbnb website. This stage implements a backendinterface, or console, to manage program data. Console commands allow the user to create, update, and destroy objects, and manage file storage. Using a system of JSON serialization/deserialization, storage is persistent between sessions.

First step: Write a command interpreter to manage your AirBnB objects.
This is the first step towards building your first full web application: the AirBnB clone. This first step is very important because you will use what you build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration…

Each task is linked and will help you to:

put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of your future instances
create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
create all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel
create the first abstracted storage engine of the project: File storage.
create all unittests to validate all our classes and storage engine

Execution
Your shell should work like this in interactive mode:

$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb)
(hbnb)
(hbnb) quit
$
But also in non-interactive mode: (like the Shell project in C)

$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$

Examples
Primary Command Syntax

Example 0: Create an object

Usage: class <class_name>


  (hbnb) create BaseModel


  (hbnb) create BaseModel
  3aa5babc-efb6-4041-bfe9-3cc9727588f8
  (hbnb)


Example 1: Show an object

Usage: show <class_name> <_id>


  (hbnb) show BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
  [BaseModel] (3aa5babc-efb6-4041-bfe9-3cc9727588f8) {'id': '3aa5babc-efb6-4041-bfe9-3cc9727588f8', 'created_at': datetime.datetime(2023  , 7, 14, 21, 12, 21, 96956), 'update_at': datetime.datetime(2023, 7, 14, 21, 12, 21, 96971)}
  (hbnb)

Example 2: Destroy an object

Usage: destroy <class_name> <_id>

  (hbnb) destroy BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
  (hbnb) show BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
  ** no instance found **
  (hbnb)
