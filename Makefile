include .env
export $(shell sed 's/=.*//' .env)

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

train: 
	python train.py

update-branch: 
	git commit -am "Update with new results"
	git push --force origin HEAD:update

hf_login: 
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HUGGINGFACE_HUB) --add-to-git-credential

push_hub:
#	huggingface-cli upload ChaimaGharbi/Drug-Classification ./Model --repo-type=model --commit-message="new model proposition" --revision new_model --create-pr
	huggingface-cli upload ChaimaGharbi/Drug-Classification ./App /App --repo-type=model --commit-message="Sync Model" --revision main --create-pr --commit-description="$$(cat report.md)"
#	huggingface-cli upload ChaimaGharbi/Drug-Classification ./Results /Metrics --repo-type=space --commit-message="Sync Model"

deploy:
	make hf_login
	make push_hub

experiment_pipeline:
	make train
	python compare_metrics.py

generate_report:
	python compare_metrics.py
	python generate_report.py

all: generate_report update

update:
	gh pr create --title "trying git cli" --body "$$(cat report.md)" --base update --head main