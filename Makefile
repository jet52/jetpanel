SKILL_NAME := jetpanel
VERSION := $(shell cat VERSION)
ZIP_NAME := $(SKILL_NAME)-skill-v$(VERSION).zip

.PHONY: package clean install test

package: clean
	mkdir -p $(SKILL_NAME)-skill
	cp -r skill/ install.py README.md VERSION $(SKILL_NAME)-skill/
	find $(SKILL_NAME)-skill -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	zip -r $(ZIP_NAME) $(SKILL_NAME)-skill/
	rm -rf $(SKILL_NAME)-skill

clean:
	rm -f $(SKILL_NAME)-skill*.zip

install:
	python3 install.py

test:
	@echo "Validating skill structure..."
	@test -f skill/SKILL.md || (echo "FAIL: skill/SKILL.md missing" && exit 1)
	@test -d skill/references || (echo "FAIL: skill/references/ missing" && exit 1)
	@test -f skill/references/panel-roster.md || (echo "FAIL: skill/references/panel-roster.md missing" && exit 1)
	@test -f install.py || (echo "FAIL: install.py missing" && exit 1)
	@test -f README.md || (echo "FAIL: README.md missing" && exit 1)
	@test -f VERSION || (echo "FAIL: VERSION missing" && exit 1)
	@echo "All checks passed."
