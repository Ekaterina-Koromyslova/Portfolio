import json

def main():
    try:
        with open("input.txt", "r") as file:
            data = json.load(file)
    except:
        print("Incorrect input")
        return

    if "list1" not in data or "list2" not in data:
        print("Incorrect input")
        return

    list1 = data["list1"]
    list2 = data["list2"]

    if not isinstance(list1, list) or not isinstance(list2, list):
        print("Incorrect input")
        return

    if not validate_list(list1) or not validate_list(list2):
        print("Incorrect input")
        return

    result = merge_lists(list1, list2)

    print(json.dumps({"list0": result}, indent=2, ensure_ascii=False))


def validate_list(lst):
    for movie in lst:
        if not isinstance(movie, dict):
            return False
        if "title" not in movie or "year" not in movie:
            return False
        if not isinstance(movie["title"], str):
            return False
        if not isinstance(movie["year"], int):
            return False
    return True


def merge_lists(list1, list2):
    i = j = 0
    result = []

    while i < len(list1) and j < len(list2):
        if list1[i]["year"] <= list2[j]["year"]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    while i < len(list1):
        result.append(list1[i])
        i += 1

    while j < len(list2):
        result.append(list2[j])
        j += 1

    return result


if __name__ == "__main__":
    main()
