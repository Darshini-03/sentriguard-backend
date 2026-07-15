import csv
import os
import json

from .url_analyzer import analyze_url


def validate_dataset():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    csv_path = os.path.join(
        BASE_DIR,
        "dataset",
        "website_dataset.csv"
    )


    total = 0
    correct = 0
    wrong = 0
    results = []


    with open(csv_path, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)


        for row in reader:

            website = row["website"]
            actual = row["actual_label"]


            analysis = analyze_url(website)

            predicted = analysis["verdict"]


            # Convert verdict into dataset label
            if predicted == "Likely Genuine Website":

                predicted_label = "Genuine"

            else:

                predicted_label = "Fraud"



            status = (
                "Correct"
                if predicted_label == actual
                else "Wrong"
            )


            total += 1


            if status == "Correct":

                correct += 1

            else:

                wrong += 1



            results.append({

                "website": website,

                "actual": actual,

                "predicted": predicted_label,

                "status": status

            })



    # Accuracy calculation

    accuracy = round(
        (correct / total) * 100,
        2
    ) if total else 0



    # Final validation output

    output = {

        "total": total,

        "correct": correct,

        "wrong": wrong,

        "accuracy": accuracy,

        "results": results

    }



    # Save result into JSON file

    json_path = os.path.join(
    BASE_DIR,
    "validation_result.json"
)
    


    print("Saving validation result at:", json_path)

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as f:
        
        json.dump(
            output,
            f,
            indent=4
        )



    return output


