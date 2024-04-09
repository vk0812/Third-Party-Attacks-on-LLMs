def delete_elements(response, elements_to_delete):
    for element in elements_to_delete:
        if element in response:
            del response[element]
        else:
            print(element)

    return response
