# Install the project
The example project lives in the repository root `example/my_project` directory.
In order to use it, you have to clone the repository
```bash
git clone https://github.com/callat-qcd/espressodb.git
```
Install the dependencies
```bash
cd example/my_project
pip install [--user] -r requirements.txt
```
And create the project tables
```
python manage.py migrate
```
Finally you can launch a local server
```
python manage.py runserver
```
and visit the project dashboard at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (this is the default port).
