import cProfile
from prompt_extraction import TimeExtractor
from settings import PROMPT_FILE, OPENAI_API_KEY

def test_time_extractor():
    api_key = OPENAI_API_KEY
    prompt_filename = PROMPT_FILE
    time_extractor = TimeExtractor(api_key, prompt_filename)
    query = "what is the price of Conflux in the past two weeks?"
    result = time_extractor.extract_time_interval(query)
    print(result)

if __name__ == "__main__":
    cProfile.run("test_time_extractor()", sort="tottime")