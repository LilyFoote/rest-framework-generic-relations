# Rest Framework Generic Relations Changelog

## v2.1.0

General dependency update

* Minimum Python version is now 3.6
* Minimum DRF version is now 3.11
* Supported Django versions are now [2.2, 3.1, 3.2]

## v2.0.0

* Add Python 3.8, Django 3.0 and DRF 3.11 support
* Drop Python 2
* Drop DRF 3.7

Minimum supported dependencies are now:
* Python 3.4
* Django 1.11
* DRF 3.8

## v1.2.1
* Add error handling for reusing a `Serializer` instance in a `GenericRelatedField`.

## v1.2.0

* Add Django 2.0 support (need Python min 3.4, Django min. 1.11).

## v1.1.0

* Add `GenericModelSerializer` as a counterpart to `GenericRelatedField`.
* Dynamically determine the best serializer to use to serialize a model instance.
* Rename `determine_serializer_for_data` to `get_deserializer_for_data`
* Rename `determine_deserializer_for_data` to `get_serializer_for_instance`

## v1.0.0

* Add support for Django 1.8 and 1.9
* Add support for Django Rest Framework 3
* Drop support for earlier versions of Django and DRF

## v0.1.0

* Initial release
