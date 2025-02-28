class Cart():
    def __init__(self, request):

        self.session = request.session
        self.request = request

        # get existing session key. Otherwise, create one
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart