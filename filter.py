import json

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)


def load_seen(path="seen_jobs.json"):
    with open(path) as f:
        return set(json.load(f))


def save_seen(seen, path="seen_jobs.json"):
    with open(path, "w") as f:
        json.dump(list(seen), f)


def matches_filters(text, filters):
    text = text.lower()
    if filters["keywords"]:
        if not any(k.lower() in text for k in filters["keywords"]):
            return False
    if filters["locations"]:
        if not any(loc.lower() in text for loc in filters["locations"]):
            return False
    if filters["job_types"]:
        if not any(jt.lower() in text for jt in filters["job_types"]):
            return False
    return True
