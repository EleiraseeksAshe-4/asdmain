import json

def map_scores_to_values(scores, mapping):
    result = []
    for key, score in scores.items():
        str_score = str(score)
        if str_score == 'None':
            str_score = '-1'
        value = mapping[str_score]
        result.append(value)
#    return [mapping[str(score)] for score in scores]
    return result

def get_descriptive_label(value, mapping):
    return mapping.get(str(value), "Unknown")

def get_raw_score_description(raw_score, descriptions):
    current_description = ""
    for desc, text in descriptions.items():
        if raw_score >= float(desc):
            current_description = text
    return current_description

def calculate_scores(value_scores, questions):
    # Map parental scores to values using the score mapping
    raw_scores = []
    scaled_scores = []

    for question in questions:
        qid = question['questionid']
        qpc_items = question['qpc_items']

        raw_score = sum(value_scores[pq - 1] * w for pq, w in qpc_items)
        #raw_score = sum(value_scores[pq - 1] * w for pq, w in zip(parental_qs, weights))
        sum_weights = total_weight = sum(item[1] for item in qpc_items)
        scaled_score = raw_score / sum_weights if sum_weights != 0 else 0

        raw_scores.append(raw_score)
        scaled_scores.append(scaled_score)

    return raw_scores, scaled_scores


def get_age_range(age):
    if 2 <= age <= 12:
        return "Ages 2-12"
    elif age >= 13:
        return "Ages 13 and older"
    else:
        return "All ages"


def find_t_score_and_percentile(carscontext, age, score):
    age_range = get_age_range(age)
    scores_data = carscontext["Scores"][age_range]

    for item in scores_data:
        if isinstance(item["score"], str) and item["score"].startswith(">"):
            if score > float(item["score"][1:]):
                return item["t_score"], item["percentile"]
        elif isinstance(item["score"], str) and item["score"].startswith("<"):
            if score < float(item["score"][1:]):
                return item["t_score"], item["percentile"]
        elif isinstance(item["score"], str) and "–" in item["score"]:
            min_score, max_score = map(float, item["score"].split("–"))
            if min_score <= score <= max_score:
                return item["t_score"], item["percentile"]
        else:
            if float(item["score"]) == score:
                return item["t_score"], item["percentile"]

    return None, None


def get_scores(index, cars2context):
    questions = cars2context['questions'][index]
    weights = cars2context['weights'][index]
    sum_of_weights = sum(weights)
    answers = cars2context['answers']
    total_score = 0.0
    for idx, question_index in enumerate(questions):
        value = answers[question_index]
        weight = weights[idx]
        scaled_score = value * weight
        total_score += scaled_score

    scaled_total_score = total_score / sum_of_weights
    rounded = round(scaled_total_score, 0.5)
    return rounded

def get_level(age, scaled_score, severity_ranges):
    required_range = severity_ranges[0]
    for agerange in severity_ranges:
        if agerange['age_max'] <= age and agerange['age_min'] >= age:
            required_range = agerange
            break

    levels = agerange['levels']
    severitylevel = None
    severitydescription = "Not found"
    for level in levels:
        if scaled_score >= level['min'] and scaled_score <= level['max']:
            severitylevel = level['level']
            severitydescription = level['name']
            break

    return severitylevel, severitydescription

def get_jsondata(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data

def fetch_cars2_data(context):
    # Load JSON data from file
    fileroot = context['fileroot']
    cars_scales = get_jsondata(f"{fileroot}staticdata/cars2_scales.json")
    # Load context data from JSON file
    carscontext = get_jsondata(f"{fileroot}staticdata/carsdata_context.json")

    active_path = context['active_path']
    clientref = context['clientref']
    parental_scores = get_jsondata(f"{active_path}/word/{clientref}_cars2.json")['0']

    cars2 = {}

    severity_ranges = carscontext['severity_ranges']
    descriptive_mapping = carscontext['descriptive_mapping']
    # Extract score mapping and CARS2 questions from context
    score_mapping = carscontext['score_mapping']
    parental_values = map_scores_to_values(parental_scores, score_mapping)

    cars2_questions = carscontext['CARS2']
    #cars2_questions = carscontext['CARS2']['questions']
    # Calculate raw and scaled scores
    raw_scores, scaled_scores = calculate_scores(parental_values, cars2_questions)
    total_scaled_score = 0.0
    for index, scaled_score in enumerate(scaled_scores):
        total_scaled_score += scaled_score
        cars2[f"raw_{index}"] = scaled_score
        cars2[f"interpret_raw_{index}"] = get_raw_score_description(scaled_score, descriptive_mapping)



    # Output the results
    for i, (raw, scaled) in enumerate(zip(raw_scores, scaled_scores), start=1):
        print(f"CARS2 Question {i}: Raw Score = {raw:.2f}, Scaled Score = {scaled:.2f}")

    # # Example output format as a list of dictionaries
    # results = [{"question_id": i + 1, "raw_score": raw, "scaled_score": scaled}
    #            for i, (raw, scaled) in enumerate(zip(raw_scores, scaled_scores))]

    age = context['ageyears']
    t_score, percentile = find_t_score_and_percentile(cars_scales, age, total_scaled_score)

    level, level_description = get_level(age, total_scaled_score, severity_ranges)
    cars2['score']= total_scaled_score
    cars2['tscore']= t_score
    cars2['percent']= percentile
    cars2['level']= level
    cars2['interpret_level']= level_description
    ratingscales = context['rs']
    ratingscales['cars2'] = cars2

    return cars2
