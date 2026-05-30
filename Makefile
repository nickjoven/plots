.PHONY: build preview

# Regenerate the static site under docs/ from the source files.
build:
	python3 scripts/build_site.py

# Serve the built site locally on port 8000. Opening docs/index.html directly
# also works; this is closer to how GitHub Pages serves it.
preview: build
	@echo "serving docs/ at http://localhost:8000/ (ctrl-c to stop)"
	python3 -m http.server 8000 --directory docs
