.PHONY: feature

feature: ## Usage: make feature path/to/feature_dir
	@echo "Usage: make feature <dir>"
	@exit 1

feature-%:
	@echo "Creating placeholder files for feature development in $*..."
	@mkdir -p "src/features/$*"
	@touch "src/features/$*/schemas.py" \
	       "src/features/$*/controller.py" \
	       "src/features/$*/component.py" \
	       "src/features/$*/operation.py" \
	       "src/features/$*/exception.py" \
	       "src/features/$*/__init__.py"
	@echo "Placeholder files created in $*."
