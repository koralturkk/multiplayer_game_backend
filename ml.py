import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()
doc = nlp("It's no surprise that it caught the eye of tech giant Apple Inc., who acquired HopStops for an estimated $1 billion.")



