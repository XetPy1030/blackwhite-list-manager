def tryies_decorator(num_of_tryies=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num_of_tryies):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                    print('Try again...')
                    continue
            raise Exception('Too many tryies')

        return wrapper

    return decorator
