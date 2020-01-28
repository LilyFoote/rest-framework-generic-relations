pkg_resources = __import__('pkg_resources')
distribution = pkg_resources.get_distribution('rest-framework-generic-relations')

__version__ = distribution.version
