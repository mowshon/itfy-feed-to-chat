import dialogflow_v2
from dialogflow_v2.types import Intent

def add_tp(id, pid, message):
    client = dialogflow_v2.IntentsClient()
    name = client.intent_path(pid, id)
    intent = client.get_intent(name, intent_view='INTENT_VIEW_FULL')
    tp = intent.training_phrases
    part = Intent.TrainingPhrase.Part(text=message)
    new_tp = Intent.TrainingPhrase(parts=[part])
    tp.MergeFrom([new_tp])
    client.update_intent(intent)
