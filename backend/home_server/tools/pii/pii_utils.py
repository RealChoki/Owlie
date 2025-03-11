import yaml
from langdetect import detect, LangDetectException
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from pathlib import Path

# Define the path to the languages configuration file
LANGUAGES_CONFIG_FILE = Path(__file__).resolve().parent / "languages-config.yml"

# Load the configuration data from the YAML file
with open(LANGUAGES_CONFIG_FILE, "r") as file:
    language_config_data = yaml.safe_load(file)

# Create NLP engine based on configuration
provider = NlpEngineProvider(conf_file=LANGUAGES_CONFIG_FILE)
nlp_engine_with_german = provider.create_engine()

# Initialize the analyzer
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine_with_german, 
    supported_languages=["en", "de"],
    default_score_threshold=0.62
)

# Initialize the anonymizer
anonymizer = PresidioReversibleAnonymizer(
    languages_config=language_config_data,
    add_default_faker_operators=True
)

# Detects the language of the text
def detect_language(text: str) -> str:
    try:
        if detect(text) == "en":
            return "en"
        else:
            return "de"
    except LangDetectException:
        return "de"

# A function to check if the message contains PII
def contains_pii(text):
    results = analyzer.analyze(text=text, language=detect_language(text))
    print("PII results:", results)
    return results

# A function to anonymize the users message
def presidio_anonymize(user_message):
    results = list(set(contains_pii(user_message)))
    if results:
        allowed_types = [r.entity_type for r in results]
        print("Allowed types:", allowed_types)
        anonymized_user_message = anonymizer.anonymize(
            text=user_message,
            language=detect_language(user_message),
            allow_list=allowed_types
        )
        return anonymized_user_message
    return user_message

# A function to de-anonymize the assistants response s
def presidio_deanonymize(anonymized_response):
    if anonymizer.deanonymizer_mapping:
        de_anonymized_response = anonymizer.deanonymize(text_to_deanonymize=anonymized_response)
        return de_anonymized_response
    return anonymized_response