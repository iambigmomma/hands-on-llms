# === Install ===

install:
	@echo "Installing financial bot..."
	
	poetry env use $(shell which python3.10) && \
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install && \
	poetry run pip install torch==2.0.1

install_dev: install
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install --only dev

install_only_dev:
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install --only dev

add:
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry add $(package)

add_dev:
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry add --group dev $(package)


# === Run ===

run:
	@echo "Running financial_bot..."

	poetry run python -m tools.bot \
		--about_me "I am a student and I have some money that I want to invest." \
		--question "Should I consider investing in stocks from the Tech Sector?" \
		--history "[[\"What is your opinion on investing in startup companies?\", \"Startup investments can be very lucrative, but they also come with a high degree of risk. It is important to do your due diligence and research the company thoroughly before investing.\"]]" \
		--debug False

run_dev:
	@echo "Running financial_bot [Dev Mode]..."

	poetry run python -m tools.bot \
		--about_me "I am a student and I have some money that I want to invest." \
		--question "Should I consider investing in stocks from the Tech Sector?" \
		--history "[[\"What is your opinion on investing in startup companies?\", \"Startup investments can be very lucrative, but they also come with a high degree of risk. It is important to do your due diligence and research the company thoroughly before investing.\"]]" \
		--debug True

run_ui:
	@echo "Running financial_bot UI..."

	poetry run python -m tools.ui

run_ui_dev:
	@echo "Running financial_bot UI [Dev Mode]..."

	poetry run gradio tools/ui.py --debug

run_ui_api:
	@echo "Running financial_bot UI and called REST API from Beam..."

	poetry run python -m tools.ui_api


# === Beam ===

export_requirements:
	@echo "Exporting requirements..."

	if [ -f requirements.txt ]; then rm requirements.txt; fi
	poetry export -f requirements.txt --output requirements.txt --without-hashes

deploy_beam: export_requirements
	@echo "Deploying financial_bot on Beam..."

	BEAM_IGNORE_IMPORTS_OFF=true beam deploy ./tools/bot.py:run

deploy_beam_dev: export_requirements
	@echo "Deploying financial_bot on Beam [Dev Mode]..."

	BEAM_IGNORE_IMPORTS_OFF=true beam deploy ./tools/bot.py:run_dev

call_restful_api:
	curl -X POST  \
	--compressed 'https://${BEAM_DEPLOYMENT_ID}.apps.beam.cloud' \
	-H 'Accept: */*' \
	-H 'Accept-Encoding: gzip, deflate' \
	-H 'Authorization: Basic ${BEAM_AUTH_TOKEN}' \
	-H 'Connection: keep-alive' \
	-H 'Content-Type: application/json' \
	-d '{"about_me": "I am a student and I have some money that I want to invest.", "question": "Should I consider investing in stocks from the Tech Sector?", "history": [["What is your opinion on investing in startup companies?", "Startup investments can be very lucrative, but they also come with a high degree of risk. It is important to do your due diligence and research the company thoroughly before investing."]]}'

# === Formatting & Linting ===
# Be sure to install the dev dependencies first #

lint_check:
	@echo "Checking for linting issues..."

	poetry run ruff check .

lint_fix:
	@echo "Fixing linting issues..."

	poetry run ruff check --fix .

format_check:
	@echo "Checking for formatting issues..."

	poetry run black --check .

format_fix:
	@echo "Formatting code..."

	poetry run black .
