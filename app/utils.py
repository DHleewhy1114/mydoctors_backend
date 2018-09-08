from graphene.relay.node import from_global_id


def input_to_dictionary(input):
    """Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    #print (input)
    for key in input:
        print(key)
        # Convert GraphQL global id to database id
        if key[-2:] == 'id':
            input[key] = from_global_id(input[key])[1]
            print (input[key])
        dictionary[key] = input[key]
    #print (dictionary)
    return dictionary