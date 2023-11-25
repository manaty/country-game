# Making of

The list countries and their capitals, currency, languages, population, food and drinks and landmarks has been obtained by [chatGPT](./createCountryList.python).

The images have been obtained by crawling wikipedia.





## Setting up the environment

Create a file `keys.json` in a `./private` directory. This file will be containing your [openAI secret key](https://gptforwork.com/help/gpt-for-docs/setup/create-openai-api-key)

```json
{
    "OPENAI_SECRET_KEY":"sk-0lA*****************************aEXbhVrrlO2JdIQ"
}
```

Run the `setup_environment` bash script in this directory

```bash
bash setup_environment.sh
```

The script does the following:

* Creates a Python virtual environment named after your project with -venv suffix.
* Activates the virtual environment.
* Reads the keys.json file and sets each key-value pair as an environment variable.

Note:

* This script assumes that Python, pip and venv are already installed on your system.
* Be cautious with environment variables, as they contain sensitive information. Make sure environment variables are not exposed or logged in an insecure manner.