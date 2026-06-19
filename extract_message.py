import secret_data


def extract_secret_message(counts, receiver_key):

    encoded_message = secret_data.encoded_message

    recovered_message = ''.join(
        str(
            int(encoded_message[i]) ^
            int(receiver_key[i])
        )
        for i in range(4)
    )

    print("\nENCODED MESSAGE:")
    print(encoded_message)

    print("\nRECOVERED MESSAGE:")
    print(recovered_message)

    return recovered_message
