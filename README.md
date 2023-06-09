#  **_wiki-ai_**
**"wiki-ai"** is a project that uses AI to provide a chatbot interface for retrieving information from Wikipedia.
It completely runs locally on your cpu after you have downloaded the dependencies..

## How to Run
### Prerequisites
Before running the "wiki-ai" project, please ensure that you have the following:

Python installed on your system (version 3.10 or higher).
Git installed on your system.
Latest C++ compiler [MinGW](https://sourceforge.net/projects/mingw/)
Internet connectivity to download dependencies and models.

Please follow the steps below to set up and run the "wiki-ai" project:

### 1.  Clone the Repository:
`git clone https://github.com/brijesh24bs/wiki-ai.git`

### 2. Change into the project's directory:

`cd wiki-ai`

Create a virtual environment:
`python3 -m venv venv`

Activate the virtual environment:

For Windows:
`venv\Scripts\activate`

For macOS and Linux:
`source venv/bin/activate`

### 3. Install Dependencies:

Run the following command to install the project's dependencies:

`pip install -r requirements.txt`
This will install all the necessary packages for running the "wiki-ai" project.


### 4. Run the Utils Script:

In your terminal, run the following command to execute the utils.py script:

`python3 utils.py`

This script sets up the necessary directories (_data/_, _models/_ , _db/_).

### 5.  Download the Model:

Download the pre-trained model [gpt4all](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin) and save it in the _models/_ directory of the project. Make sure to place the model file in the correct location.

### 6.  Start the Ingestion Process:

Also rename the _example.env_ file to _.env_

To retrieve Wikipedia data for the chosen topic, run the ingest.py script using the following command:
`python3 ingest.py`
You will be prompted to enter the topic name. Copy and paste the desired topic from Wikipedia into the terminal.

For another topic delete embeddings ("db/" - folder) and run utils.py file another time. (for ambiguity)

### 7.  Run the "wiki-ai" Script:
Once the ingestion process is complete, you can start using the "wiki-ai" chatbot. Run the wiki-ai.py script with the following command:

`python3 wiki-ai.py`

You can now interact with the chatbot by entering queries. To exit the session, simply type "exit" in the query and press Enter.