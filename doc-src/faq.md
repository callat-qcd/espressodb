# FAQ

- [Why (or when) should I use EspressoDB?](#q-why-or-when-should-i-use-espressodb)
- [How do I interact with EspressoDB projects?](#q-how-do-i-interact-with-espressodb-projects)
- [What should I know to get started with EspressoDB?](#q-what-should-i-know-to-get-started-with-espressodb)
- [What are possible deployment scenarios?](#q-what-are-possible-deployment-scenarios)
- [Who can access the data which is stored using EspressoDB?](#q-who-can-access-the-data-which-is-stored-using-espressodb)
- [How does EspressoDB help ensuring data integrity?](#q-how-does-espressodb-help-ensuring-data-integrity)

#### Q: Why (or when) should I use EspressoDB?

If you feel that having a dynamic, systematic but also flexible interface to data saves your time, EspressoDB might be able to help out.
EspressoDB provides a programmatic interface to relational databases (you can search nested tables with one line of Python) which is

* easy to use *(no prior knowledge of SQL required)*
* easy to set up *(coding up tables equates to writing classes)*
* flexible *(possible to change tables which contain data)*
* scalable *(fast searches and concurrent access from remote locations)*

This is realized by extending the [Django web framework](https://www.djangoproject.com) to streamline the process of creating the database interface while hiding details behind the scenes.


#### Q: How do I interact with EspressoDB projects?

The interaction with EspressoDB projects happens on three layers:

1. **Project development** *(admin like)*
    <br/>You create and develop your EspressoDB project by designing tables and interfaces

2. **Data interaction** *(user like)*
    <br/>You import your project to query and push data

3. **Data presentation** *(visitor like)*
    <br/>You access (pre-defined) web pages which visualize data

#### Q: What should I know to get started with EspressoDB?

Once the project has been set up, users have standardized and documented access to data.
Querying and pushing data requires minimal knowledge of object-oriented programming in Python.
This interface is realized through intuitive methods like `obj = queryset.filter(n=1)` or `obj.save()`.

The project development layer requires more technical expertise.
For simple EspressoDB projects, experience with object-oriented programming in Python and minimal command-line knowledge is helpful.
Even without prior knowledge of Django is possible to [set up projects in a few minutes](usage.md#tl-dr).
Because tables correspond to classes, you do not have to write any SQL to interface with the database.
EspressoDB provides default web views and you can start a local server within one command.

For more collaborative approaches, knowledge about how to set up databases--*"what are good table layouts and how to connect to the database?"*--simplify setting up projects.
Knowledge about Django is helpful if you want to create more sophisticated project layouts or custom-tailored frontend access.


#### Q: What are possible deployment scenarios?

In the scenario where updates of data happen less frequently and you just want to provide easy access to the data, a file-based [SQLite](https://www.sqlite.org/index.html) database backend might do the job. Once the tables are ready and the database is populated, you can share your project and (a copy of) this file.
You also can launch a web server interfacing with this file.

In a more dynamic scenario where collaborative access is important, we recommend using a [MySQL](https://www.mysql.com), [PostgresSQL](https://www.postgresql.org) or other relational database management systems.


#### Q: Who can access the data which is stored using EspressoDB?

This depends on the deployment scenario.
In general, all data is stored in the database you specify in your settings.
Every entity which has access to the database, whether it is direct access or indirect access through your EspressoDB project, can potentially interact with the data.

For example, if data is stored in an SQLite file, everyone who has read (and write) access to this file can interface it.
If you host a database accessible through a remote connection, everyone with the required credentials has access to this database.
Both of these statements are true independent of EspressoDB.

If you launch a web server that accesses your database, everyone who can visit the web page can access the data by the means you have specified in your project.
For example, it is possible to only allow the server to have read-only access to certain tables.
For a more sophisticated discussion about web-access security see also [the Django docs](https://docs.djangoproject.com/en/dev/topics/security/).


#### Q: How does EspressoDB help to ensure data integrity?

To reduce potential integrity violations, cross-checks are implemented on several layers:

1. Python side integrity checks
    </br> EspressoDB provides automated (optional) [consistency checks](features/consistency-checks.md) on tables and columns as well as [integrity checks](features/init-checks.md)  against the database to prohibit unwanted insertions.  Table checks should be provided by the project developers.
2. Database side integrity checks
    </br>This includes type checks (do not insert `strings` in `int` columns) and relation integrity checks (if you delete this entry, the related entry is updated).
3. Database access checks (depending on the backend)
    </br> Depending on the backend you can give different access rights to different users to allow, e.g., only read-only access to certain tables.

Data integrity goes hand-in-hand with access levels.
The more access you allow, the more things could potentially go wrong.
This statement is independent of EspressoDB.
For this reason, we recommend to always have backups of your database.
