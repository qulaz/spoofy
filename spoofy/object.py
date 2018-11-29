
class Object:
	
	_type = None
	
	def __init__(self, client, data):
		self._client = client
		self.id = data.pop('id', None)
		self.name = data.pop('name', None)
		self.href = data.pop('href', None)
		self.uri = data.pop('uri', None)
	
	@property
	def type(self):
		return self._type
	
	def __repr__(self):
		repr_str = f'{self.__class__.__name__}'
		if self.id:
			repr_str += f' id=\'{self.id}\''
		if self.name:
			repr_str += f' name=\'{self.name}\''
		return f'<{repr_str}>'
	
	def __str__(self):
		return self.name or self.__repr__()