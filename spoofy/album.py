from datetime import datetime

from .object import Object
from .mixins import ExternalURLMixin, TrackMixin, ImageMixin, ArtistMixin, ExternalIDMixin


class Album(Object, ExternalURLMixin, TrackMixin, ImageMixin, ArtistMixin):
	'''
	Represents an Album object.
	
	id: str
		Spotify ID of the album.
	name: str
		Name of the album.
	tracks: List[:class:`Track`]
		List of tracks on the album.
	artists: List[:class:`Artist`]
		List of artists that appear on the album.
	images: List[:class:`Image`]
		List of associated images, such as album cover in different sizes.
	uri: str
		Spotify URI of the album.
	link: str
		Spotify URL of the album.
	type: str
		Plaintext string of object type: ``album``.
	album_type:
		Type of album, e.g. ``album``, ``single`` or ``compilation``.
	available_markets: List[str] or None
		Markets where the album is available: `ISO_3166-1 <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_.
	external_urls: dict
		Dictionary that maps type to url.
	release_date: `datetime <https://docs.python.org/3/library/datetime.html#module-datetime>`_
		Date (and maybe time) of album release.
	release_date_precision: str
		Precision of ``release_date``. Can be ``year``, ``month``, or ``day``.
	album_group: str or None
		Type of album, e.g. ``album``, ``single``, ``compilation`` or ``appears_on``.
	'''

	_type = 'album'
	__date_fmt = dict(year='%Y', month='%Y-%m', day='%Y-%m-%d')

	def __init__(self, client, data):
		super().__init__(client, data)

		self._tracks = {}

		self.album_group = data.pop('album_group', None)  # can be None, though this is not specified in the API docs
		self.album_type = data.pop('album_type')
		self.available_markets = data.pop('available_markets', None)

		self.release_date_precision = data.pop('release_date_precision')

		if self.release_date_precision is None:
			self.release_date = None
		else:
			try:
				self.release_date = datetime.strptime(
					data.pop('release_date'),
					self.__date_fmt[self.release_date_precision]
				)
			except ValueError:
				self.release_date = None

		self._fill_external_urls(data.pop('external_urls'))
		self._fill_artists(data.pop('artists'))
		self._fill_images(data.pop('images'))


class SimpleAlbum(Album):
	'''
	Alias of :class:`Album`
	'''

	pass


class FullAlbum(Album, ExternalIDMixin):
	'''
	Represents a complete Album object.
	
	This type has some additional attributes not existent in :class:`Album` or :class:`SimpleAlbum`.
	
	genres: List[str]
		List of genres associated with the album.
	label: str
		The label for the album.
	popularity: int
		An indicator of the popularity of the album, 0 being least popular and 100 being the most.
	copyrights: dict
		List of copyright objects.
	external_ids: dict
		Dictionary of external IDs.
	'''

	def __init__(self, client, data):
		super().__init__(client, data)

		self.genres = data.get('genres')
		self.label = data.get('label')
		self.popularity = data.get('popularity')
		self.copyrights = data.get('copyrights')

		self._fill_external_ids(data.get('external_ids'))
