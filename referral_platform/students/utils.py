

def generate_id(
            first_name,
            father_name,
            last_name,
            mother_full_name,
            gender,
            birthday_day,
            birthday_month,
            birthday_year
        ):
    """
    Unique Number Proposal:
    full name total char number
    mother full name total char number
    Concatenate hash number for: first name, father name and last name
    Concatenate hash number for: mother first name and mother last name
    Concatenate hash number for birthday: day, month, year
    Gender type first letter

    :return:
    """
    import hashlib

    try:
        # concatenate name to form full name with no spaces
        full_name = u'{}{}{}'.format(first_name, father_name, last_name)

        # take the count of full name and zero pad to two digits
        full_name_char_count = '{0:0>2}'.format(len(full_name))

        # take the count of mother name and zero pad to two digits
        mother_name_char_count = '{0:0>2}'.format(len(mother_full_name))

        # take the hash of fullname and convert to integer, zero padding to 4 digits
        full_name_hash = '{0:0>4}'.format(int(hashlib.sha1(full_name.encode('UTF-8')).hexdigest(), 16) % 10000)

        # take the hash of mother name and convert to integer, zero padding to 4 digits
        mother_name_hash = '{0:0>3}'.format(int(hashlib.sha1(mother_full_name.encode('UTF-8')).hexdigest(), 16) % 1000)

        # take the first character of the gender to denote sex
        gender_first_char = gender[:1]

        # concatenate day, month and year to form birthday without space or special characters
        birthday = u'{}{}{}'.format(birthday_day, birthday_month, birthday_year)

        # take the hash of birthday and convert to integer, zero padding to 3 digits
        birthday_hash = '{0:0>3}'.format(int(hashlib.sha1(birthday.encode()).hexdigest(), 16) % 1000)

        # arrange in order
        result = '{fullname_char}{mothername_char}{fullname_hash}{mothername_hash}{birthday}{gender_char}'.format(
            fullname_char=full_name_char_count,
            mothername_char=mother_name_char_count,
            fullname_hash=full_name_hash,
            mothername_hash=mother_name_hash,
            birthday=birthday_hash,
            gender_char=gender_first_char
        )
        return result

    except Exception as exp:
        print(exp.message)  #TODO: use logging instead
        return ''
