def compose(*functions):
    def composed_function(data):
        for function in reversed(functions):
            data = function(data)
        return data
    return composed_function
