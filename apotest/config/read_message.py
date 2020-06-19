from config import gr_detect_module_config_pb2
import sys

def ListPeople(address_book):
    for person in address_book.people:
        print("Person ID:", person.id)

        for phone_number in person.phones:
            if phone_number.type == gr_detect_module_config_pb2.Person.MOBILE:
                print(" Mobile phone #:",)


if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
    sys.exit(-1)

address_book = gr_detect_module_config_pb2.AddressBook()

# Read the existing address book
f = open(sys.argv[1], "rb")
address_book.ParseFromString(f.read())
f.close()

ListPeople(address_book)
 