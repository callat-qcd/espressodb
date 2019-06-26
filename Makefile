
clean-migrations:
	$(RM) base/migrations/0*.py
	$(RM) gaugeconfigs/migrations/0*.py
	$(RM) propagators/migrations/0*.py

clean-sqlite:
	$(RM) *.sqlite3

clean-all: clean-migrations clean-sqlite


.PHONY: clean-migrations clean-sqlite
