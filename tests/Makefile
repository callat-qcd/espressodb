.PHONY: test
test: espressodb_tests migration_tests test_project_creation

.PHONY: espressodb_tests
espressodb_tests:
	make -C espressodb_tests test

.PHONY: migration_tests
migration_tests:
	make -C migration_tests test

.PHONY: test_project_creation
test_project_creation:
	$(RM) -r espressodb_new_test/
	# Create project
	espressodb startproject espressodb_new_test
	# Run first text for empty project
	cd espressodb_new_test/ && python manage.py test
	# Create new app
	cd espressodb_new_test/ && python manage.py startapp new_app
	# Create simple model
	echo "" >> espressodb_new_test/espressodb_new_test/new_app/models.py
	echo "class MyTable(Base):" >> espressodb_new_test/espressodb_new_test/new_app/models.py
	echo "    name=models.TextField()" >> espressodb_new_test/espressodb_new_test/new_app/models.py
	# And add to app list
	sed -i -e "s/PROJECT_APPS: \[\]/PROJECT_APPS: \[espressodb_new_test.new_app\]/g"  espressodb_new_test/settings.yaml
	cd espressodb_new_test/ && python manage.py makemigrations
	# Test
	cd espressodb_new_test/ && python manage.py test
	$(RM) -r espressodb_new_test/
