def thread_read_token(data):
    fixed_token_val = "SioskKioskFixedTokenVerifyingTokenData"
    if data == fixed_token_val:
        return True
    elif data != fixed_token_val:
        return False
    else:
        return "ERROR"