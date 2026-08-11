LOCAL RAG SUPPORT AGENT — RAG-Support-Agent/README.md
Local RAG Support Agent

A local technical-support prototype that uses retrieval-augmented generation to surface relevant information from historical support records.

The project explores local inference, semantic retrieval, metadata filtering, sensitive-data masking, feedback-informed ranking, and automated evaluation without requiring a hosted LLM API for normal use.

What It Does

A user submits a technical support question through a CLI.

The system:

Searches indexed support information for relevant historical context
Applies metadata filtering where appropriate
Extracts targeted context for the current issue
Masks configured sensitive-data patterns before model processing
Sends the retrieved context to a locally running language model
Produces a proposed support response
Allows the result to be checked against expected behavior through an evaluation workflow

The project is intended as a prototype for experimenting with support-oriented retrieval, not as a production support platform.

Key Features
Filtered Semantic Retrieval

Support records are embedded and stored in ChromaDB.

Queries use semantic similarity together with available metadata to narrow the context provided to the model.

Targeted Context Extraction

Rather than placing large amounts of retrieved text into the model prompt, the workflow attempts to identify the parts of historical records most relevant to the current issue.

This is intended to reduce irrelevant context and make generated support responses easier to evaluate.

Sensitive-Data Masking

Configured patterns such as:

Email addresses
Client identifiers
ISIN-like identifiers

can be masked before retrieved text is provided to the model.

This is a prototype privacy control and should not be interpreted as providing regulatory compliance on its own.

Local Inference

Normal model inference is performed through Ollama.

This makes it possible to experiment with the support workflow without sending support records to a hosted LLM provider.

Feedback-Weighted Retrieval

The prototype includes a mechanism for verified resolutions to influence how historical fixes are prioritized during later retrieval.

This is an experiment in incorporating human feedback into retrieval rather than retraining the underlying model.

Evaluation

The repository includes a small automated evaluation set covering support scenarios such as:

Calculation-related issues
API failures
UI/crash reports

On the included fixtures, the current implementation extracts the expected technical parameters for the test cases.

This evaluation is intended as a regression check for the prototype rather than a production benchmark or general accuracy claim.

Tech Stack
Python
Ollama
Qwen2.5
ChromaDB
Sentence Transformers
all-MiniLM-L6-v2
Local embeddings
Rich CLI
Running the Project

Install dependencies:

pip install -r requirements.txt

Make sure Ollama is installed and the configured model is available.

Then run:

python chat.py

Run the evaluation workflow with:

python evaluator.py
Privacy Model

The support workflow is designed to run locally after setup.

Model inference uses Ollama and embeddings are generated locally, so normal support queries do not require a hosted LLM API.

Local execution alone is not a complete security model. A production deployment would still require appropriate access controls, storage security, auditability, data-retention policies, and review of any external integrations.

What I Was Exploring

The main question behind this project was not simply whether an LLM could answer support questions.

I wanted to experiment with the surrounding system:

How much context should be retrieved?
How can irrelevant historical information be filtered out?
How can sensitive values be removed before inference?
How can human-approved resolutions influence future retrieval?
How can the output be tested instead of judged only by whether it sounds plausible?

Those questions are the parts of applied AI systems I find most interesting.
