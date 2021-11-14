import bcrypt

class Password:

    def encript(password):
        return bcrypt.hashpw( password.encode('utf8'), bcrypt.gensalt() ).decode('utf8')

    def validate(password, hashed):
        return bcrypt.checkpw( password.encode('utf8'), hashed.encode('utf8') )
