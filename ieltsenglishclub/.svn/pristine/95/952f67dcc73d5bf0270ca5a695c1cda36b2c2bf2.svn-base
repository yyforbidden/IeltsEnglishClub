def generate_token():
    from string import printable
    import random

    letters = printable[:62]
    token = []
    for _ in range(32):
        index = random.randint(0, 61)
        token.append(letters[index])
    return "".join(token)
    
APP_TOKEN = "ZxJyqjvFiCaLllk6T2dFdc1u69fBkitS"

if __name__ == '__main__':
    print generate_token()