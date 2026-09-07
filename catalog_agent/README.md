requires codex-exec
requires the file-dfs from the ../explorer/generate_dfs_2.py
run in /catalog_agent

login to codex using the api key:
export OPENAI_API_KEY="your-api-key-here"
printenv OPENAI_API_KEY | codex login --with-api-key


upon running cataloger.py inside /catalog_agent, a chackpoint.txt  file is created. It allows to resume computation if it stops prematurely, or if you need to pause it.
